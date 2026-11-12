"""Private bounded QA of existing archives. Public output contains hashes/counts only."""

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
import traceback

from bot_trader.core.events import BarData, canonical_bytes, content_hash, datetime_to_ns
from bot_trader.market_data.archive import LocalArchive, SourceSpec
from bot_trader.market_data.kraken_history import (
    BAR_SCHEMA,
    TRADE_SCHEMA,
    HistoricalAvailability,
    KrakenHistoricalNormalizer,
    select_prefix,
    verify_archive,
)
from bot_trader.market_data.normalization import store_normalized
from bot_trader.market_data.replay import MarketReplay
from bot_trader.market_data.storage import LocalArtifactStore

REPO = Path(__file__).resolve().parents[2]
SELECTIONS = (
    ("Kraken_Trades_2026Q3.zip", "XBTUSD.csv", TRADE_SCHEMA, None),
    ("Kraken_OHLCVT_2026Q3.zip", "XBTUSD_1.csv", BAR_SCHEMA, 60),
)


def main():
    private = Path(os.environ["SLICE_EVIDENCE_DIR"])
    private.mkdir(parents=True, exist_ok=False)
    stage = "rights"
    try:
        assessment_path = REPO / "docs/phase-iv/admission/kraken-rights-assessment.json"
        assessment = json.loads(assessment_path.read_text())
        current = json.loads((REPO / "docs/integration/kraken/sources.json").read_text())
        assert assessment["disposition"] == "proceed_narrow_private_qa"
        assert "no redistribution" in current["rights_disposition"]["existing_archives"]
        rights_hash = hashlib.sha256(assessment_path.read_bytes()).hexdigest()
        receipts = [
            json.loads(line) for line in
            (REPO / "docs/phase-iv/admission/kraken-acquisition.jsonl").read_text().splitlines()
        ]
        replay = MarketReplay()
        public = []
        first_events = []
        for filename, member, schema, interval in SELECTIONS:
            stage = "existing_archive_identity"
            acquired = next(r for r in receipts if r.get("event") == "acquired" and Path(r["path"]).name == filename)
            path = Path(acquired["path"])
            if not path.is_file():
                public.append({"archive": filename, "status": "original_unavailable_no_download"})
                continue
            proof = verify_archive(path, expected_sha256=acquired["sha256"], expected_size=acquired["bytes"])
            stage = "bounded_selection"
            args = dict(member=member, source_schema=schema, instrument="XBTUSD",
                        base_currency="XBT", quote_currency="USD", interval_seconds=interval,
                        max_rows=64)
            raw, selection = select_prefix(path, proof, **args)
            repeated, selected_again = select_prefix(path, proof, **args)
            assert raw == repeated and selection == selected_again
            raw_path = private / (schema + ".csv")
            raw_path.write_bytes(raw)
            source = SourceSpec(
                source_id="kraken-historical-qa", source_version="2026Q3",
                source_schema=schema, locator=f"{acquired['url']}#{member};first-64-data-rows-v1",
                rights="Private technical QA only; no redistribution. Assessment SHA256:" + rights_hash,
                acquired_ns=datetime_to_ns(datetime.fromisoformat(acquired["at"])),
                raw_sha256=selection.raw_sha256, size_bytes=len(raw),
                data_class="exposed_structural_only",
            )
            stage = "immutable_archive_and_resume"
            store = LocalArtifactStore(private / (schema + "-artifacts"))
            importer = LocalArchive(store, max_bytes=2*1024*1024, chunk_size=256)
            progress = importer.import_step(raw_path, source, max_chunks=1)
            assert not progress.complete, "Fixture selection should exercise actual partial import."
            importer = LocalArchive(LocalArtifactStore(private / (schema + "-artifacts")),
                                    max_bytes=2*1024*1024, chunk_size=256)
            while not progress.complete:
                progress = importer.import_step(raw_path, source, checkpoint_hash=progress.checkpoint_hash, max_chunks=1)
            repeated_import = importer.import_step(raw_path, source, max_chunks=1000)
            assert repeated_import.archive_hash == progress.archive_hash
            archived, restored_source, restored = importer.read(progress.archive_hash)
            assert restored == raw and restored_source == source
            stage = "exact_normalization"
            adapter = KrakenHistoricalNormalizer(selection, HistoricalAvailability(delay_ns=0))
            normalized = adapter.normalize_with_provenance(restored, restored_source, archived.source_manifest_hash)
            normalized_hash = store_normalized(normalized.batch, store)
            sidecar_hash = store.put(canonical_bytes(normalized.model_dump(mode="json")), "json")
            assert adapter.normalize(restored, restored_source, archived.source_manifest_hash) == normalized.batch
            events = normalized.batch.events
            assert all(event.received_ns is None and event.engine_ts_init_ns is None for event in events)
            stage = "data_only_replay"
            result = replay.inspect_history(events, data_class=source.data_class)
            again = replay.inspect_history(events, data_class=source.data_class)
            assert result == again and not hasattr(result, "signals")
            duplicate = replay.inspect_history((*events, events[0]), data_class=source.data_class)
            assert duplicate.events == result.events and duplicate.checkpoint == result.checkpoint
            first = replay.inspect_history(events, data_class=source.data_class, until_ns=events[0].effective_ns)
            resumed = replay.inspect_history(events, data_class=source.data_class, checkpoint=first.checkpoint)
            assert resumed.events == result.events and resumed.checkpoint == result.checkpoint
            canary = None
            if isinstance(events[0].data, BarData):
                stage = "closed_bar_canary"
                before = replay.inspect_history(events, data_class=source.data_class, until_ns=events[0].data.end_ns-1)
                assert not before.events
                assert all(e.available_ns == e.data.end_ns for e in events)
                canary = {"before_first_close_count": 0, "at_first_close_count": len(first.events),
                          "all_available_at_close_under_zero_delay_assumption": True}
            first_events.append(events[0])
            store.put(canonical_bytes(result.model_dump(mode="json")), "json")
            diagnostics = {}
            for item in normalized.batch.diagnostics:
                category = item.split(":", 1)[0]
                diagnostics[category] = diagnostics.get(category, 0) + 1
            public.append({
                "archive": filename, "archive_sha256": proof.sha256,
                "archive_bytes_verified": proof.size_bytes, "member": member,
                "readme_sha256": selection.readme_sha256,
                "selection": "first-64-data-rows-v1", "selected_rows": selection.rows,
                "selected_bytes": len(raw), "selection_hash": content_hash(selection.model_dump(mode="json")),
                "raw_sha256": selection.raw_sha256, "archive_record_hash": progress.archive_hash,
                "normalized_hash": normalized_hash, "private_sidecar_hash": sidecar_hash,
                "unique_replayed_events": len(result.events), "diagnostic_counts": diagnostics,
                "availability": normalized.availability.model_dump(mode="json"),
                "source_reception_observed": False, "bar_canary": canary,
                "selection_repeat_identical": True, "import_resume_idempotent": True,
                "normalizer_repeat_identical": True, "replay_repeat_and_resume_identical": True,
                "duplicate_does_not_double_effect": True, "whole_member_crc_retested": False,
                "status": "technical_qa_passed_not_financial_admission",
            })
        aligned = None
        if len(first_events) == 2:
            trade, bar = first_events
            aligned = bar.data.start_ns <= trade.event_ns < bar.data.end_ns
            assert aligned, "First trade and first opening-labelled interval do not align."
        report = {
            "status": "completed" if len(first_events) == 2 else "partial_originals_unavailable",
            "rights_assessment_sha256": rights_hash, "cases": public,
            "first_trade_in_first_opening_labelled_interval": aligned,
            "data_class": "exposed_structural_only", "signals_generated": 0,
            "engine_invoked": False, "financial_metrics_computed": False,
            "limitations": ["Two fixed prefixes, no quarter-wide completeness inference",
                           "No observed reception, quotes, order book or financial admission",
                           "Gaps in native IDs/sparse bars do not prove missing market events"],
        }
        (private / "public-summary.json").write_bytes(canonical_bytes(report))
        print(json.dumps(report, indent=2))
    except Exception as error:
        (private / "error.txt").write_text(traceback.format_exc())
        # Never serialize exception text/inputs into a public technical log.
        print(json.dumps({"status": "blocked", "stage": stage, "error_type": type(error).__name__,
                          "details": "Private error retained; no market payload exported"}))
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
