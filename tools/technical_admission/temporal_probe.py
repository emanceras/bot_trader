"""Bounded, offline R prototype; invented observations, never trading decisions.

The fixture file contains hand-authored expected states. The transition below does
not construct the oracle. Batch/replay/injector paths share this causal function.
"""
from __future__ import annotations

import argparse
import copy
from collections import deque
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import sys
import time
from zoneinfo import ZoneInfo

TZ_HASH = "e9ed07d7bee0c76a9d442d091ef1f01668fee7c4f26014c0a868b19fe6c18a95"
PATHS = ("batch_1", "batch_7", "batch_64", "replay", "injector")


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def decimal_text(value: Decimal) -> str:
    return format(value.normalize(), "f")


def aggregate(rows: list[dict]) -> dict:
    if not rows:
        raise ValueError("empty_aggregation")
    prices = [Decimal(row["price"]) for row in rows]
    quantities = [Decimal(row["quantity"]) for row in rows]
    return {
        "open": decimal_text(prices[0]), "high": decimal_text(max(prices)),
        "low": decimal_text(min(prices)), "close": decimal_text(prices[-1]),
        "quantity": decimal_text(sum(quantities, Decimal(0))),
        "amount": decimal_text(sum((p*q for p, q in zip(prices, quantities)), Decimal(0))),
        "count": len(rows),
    }


class Transition:
    """Small causal state machine for synthetic observation eligibility only."""

    def __init__(self, zone: ZoneInfo | None):
        self.zone = zone
        self.state = {
            "eligible_ids": [], "values": {}, "latest_complete_bar": None,
            "valid": True, "last_sequence": None,
        }
        self.identities: dict[str, str] = {}
        self.trades: dict[str, dict] = {}
        self.bars: dict[str, dict] = {}
        self.fx: dict | None = None
        self.last_receive = -1
        self.last_ordinal = -1

    def snapshot(self) -> dict:
        return copy.deepcopy({"state": self.state, "identities": self.identities,
                              "trades": self.trades, "bars": self.bars,
                              "fx": self.fx, "last_receive": self.last_receive, "last_ordinal": self.last_ordinal})

    def restore(self, value: dict) -> None:
        for key, item in value.items():
            setattr(self, key, copy.deepcopy(item))

    def apply(self, event: dict, *, restore_checkpoint: bool = True) -> dict:
        receive = event["receive_ns"]
        if receive < self.last_receive:
            raise ValueError("fixture receive order regressed")
        if event["receive_ordinal"] <= self.last_ordinal:
            raise ValueError("fixture receive ordinal did not increase")
        self.last_receive = receive
        self.last_ordinal = event["receive_ordinal"]
        unit = event.get("time_unit", "ns")
        multipliers = {"ns": 1, "us": 1000, "ms": 1_000_000}
        raw_tick = event.get("event_tick", event["event_ns"])
        event_ns = raw_tick * multipliers[unit] if unit in multipliers and type(raw_tick) is int else None
        reason = "accepted"
        accepted = False
        if unit not in multipliers or type(raw_tick) is not int:
            reason = "unsupported_time_unit"
        elif event_ns != event["event_ns"]:
            reason = "time_unit_mismatch"
        elif event["available_ns"] is None:
            reason = "unknown_availability"
        elif event["available_ns"] > receive:
            reason = "not_yet_available"
        else:
            identity = "|".join((event["source_id"], event["instrument_id"], event["id"]))
            body = {k: v for k, v in event.items() if k not in {"receive_ns", "receive_ordinal", "expected"}}
            fingerprint = digest(body)
            if identity in self.identities:
                reason = "duplicate" if fingerprint == self.identities[identity] else "conflicting_duplicate"
            else:
                reason, accepted = self._operation(event, event_ns, restore_checkpoint)
                if accepted:
                    self.identities[identity] = fingerprint
                    self.state["eligible_ids"].append(event["id"])
        action = "OBSERVE" if reason in {"accepted", "duplicate", "checkpoint", "joined", "warm"} else "BLOCK"
        if not self.state["valid"]:
            action = "BLOCK"
        public = copy.deepcopy(self.state)
        return {"event_id": event["id"], "source_id": event["source_id"],
                "instrument_id": event["instrument_id"], "event_ns": event_ns,
                "cutoff_ns": receive, "decision": action, "reason": reason,
                "state": public, "state_digest": digest(public)}

    def _operation(self, event: dict, ns: int, restore_checkpoint: bool) -> tuple[str, bool]:
        op = event["op"]
        data = event.get("data", {})
        values = self.state["values"]
        if op == "set":
            values[data["key"]] = data["value"]
        elif op == "clock":
            values[data["key"]] = ns
        elif op == "trade":
            self.trades[event["id"]] = {"event_ns": ns, "price": data["price"], "quantity": data["quantity"]}
            start = ns // data["width_ns"] * data["width_ns"]
            rows = sorted((v for v in self.trades.values() if start <= v["event_ns"] < start+data["width_ns"]), key=lambda r: r["event_ns"])
            values[f"bin:{start}"] = aggregate(rows)
        elif op == "open_bar":
            values["provisional_bar"] = data["bar_id"]
        elif op in {"close_bar", "correct_bar"}:
            if op == "correct_bar":
                self.trades[data["trade_id"]]["price"] = data["price"]
            rows = sorted((v for v in self.trades.values() if data["start_ns"] <= v["event_ns"] < data["end_ns"]), key=lambda r: r["event_ns"])
            bar = aggregate(rows)
            if op == "correct_bar":
                values[f"bin:{data['start_ns']}"] = copy.deepcopy(bar)
            self.bars[data["bar_id"]] = {"start_ns": data["start_ns"], "end_ns": data["end_ns"], "bar": bar}
            values[f"bar:{data['bar_id']}"] = bar
            self.state["latest_complete_bar"] = data["bar_id"]
            values.pop("provisional_bar", None)
        elif op == "coarse":
            bars = [self.bars[x] for x in data["parents"]]
            if (data["start_ns"] != data["anchor_ns"] or
                bars[0]["start_ns"] != data["start_ns"] or bars[-1]["end_ns"] != data["end_ns"] or
                any(a["end_ns"] != b["start_ns"] for a, b in zip(bars, bars[1:]))):
                return "misaligned_aggregation", False
            rows = sorted((v for v in self.trades.values() if data["start_ns"] <= v["event_ns"] < data["end_ns"]), key=lambda r: r["event_ns"])
            direct = aggregate(rows)
            fine = {"open": bars[0]["bar"]["open"], "high": decimal_text(max(Decimal(b["bar"]["high"]) for b in bars)),
                    "low": decimal_text(min(Decimal(b["bar"]["low"]) for b in bars)), "close": bars[-1]["bar"]["close"],
                    "quantity": decimal_text(sum((Decimal(b["bar"]["quantity"]) for b in bars), Decimal(0))),
                    "amount": decimal_text(sum((Decimal(b["bar"]["amount"]) for b in bars), Decimal(0))),
                    "count": sum(b["bar"]["count"] for b in bars)}
            if direct != fine:
                return "aggregation_disagreement", False
            values[f"coarse:{data['bar_id']}"] = {"direct": direct, "from_fine": fine}
        elif op in {"book", "snapshot"}:
            sequence = data["sequence"]
            previous = self.state["last_sequence"]
            if op == "book" and previous is not None and sequence != previous+1:
                if sequence <= previous:
                    return "stale_sequence", False
                self.state["valid"] = False
                return "sequence_gap", False
            if op == "book" and not self.state["valid"]:
                return "invalid_book", False
            self.state["valid"] = True
            self.state["last_sequence"] = sequence
            values["book"] = data["value"]
        elif op == "calendar":
            if self.zone is None:
                return "timezone_unavailable", False
            local = datetime.fromisoformat(data["local"])
            choices = []
            for fold in (0, 1):
                aware = local.replace(tzinfo=self.zone, fold=fold)
                utc = aware.astimezone(timezone.utc)
                if utc.astimezone(self.zone).replace(tzinfo=None) == local:
                    choices.append((fold, utc))
            if not choices:
                return "nonexistent_local_time", False
            unique = {utc for _, utc in choices}
            if len(unique) > 1 and "fold" not in data:
                return "ambiguous_local_time", False
            utc = next((utc for fold, utc in choices if fold == data.get("fold", 0)), None)
            if utc is None:
                return "invalid_fold", False
            if "open_local" in data:
                opened = datetime.fromisoformat(data["open_local"])
                closed = datetime.fromisoformat(data["close_local"])
                if not opened <= local < closed:
                    return "session_closed", False
                values["trading_date"] = data["trading_date"]
            values[data["key"]] = utc.isoformat()
        elif op == "fx":
            self.fx = {"rate": data["rate"], "available_ns": event["available_ns"]}
            values["USDT_USD"] = data["rate"]
        elif op == "join":
            if self.fx is None:
                return "conversion_missing", False
            if event["receive_ns"]-self.fx["available_ns"] > data["max_age_ns"]:
                return "stale_conversion", False
            values["B_USD"] = decimal_text(Decimal(values["B_USDT"])*Decimal(self.fx["rate"]))
            return "joined", False
        elif op == "warmup":
            if sum(k.startswith("p:") for k in values) < data["minimum"]:
                return "insufficient_warmup", False
            return "warm", False
        elif op == "checkpoint":
            before = self.snapshot()
            restored = json.loads(canonical(before))
            if restore_checkpoint:
                fresh = Transition(self.zone)
                fresh.restore(restored)
                self.restore(fresh.snapshot())
            if self.snapshot() != before:
                raise AssertionError("checkpoint state differs from uninterrupted state")
            return "checkpoint", False
        elif op == "native_side":
            side = data["side"]
            role = data["role"]
            if role not in {"maker", "taker"} or side not in {"buy", "sell"}:
                return "unsupported_side", False
            values[data["key"]] = side if role == "taker" else {"buy": "sell", "sell": "buy"}[side]
        else:
            raise ValueError(f"unsupported fixture operation: {op}")
        return "accepted", True


def run_journal(events: list[dict], path: str, zone: ZoneInfo | None) -> list[dict]:
    machine = Transition(zone)
    outputs = []
    if path.startswith("batch_"):
        size = int(path.split("_")[1])
        batches = [events[i:i+size] for i in range(0, len(events), size)]
        for batch in batches:
            for event in batch:
                outputs.append(machine.apply(event))
    elif path == "replay":
        for event in events:
            outputs.append(machine.apply(event, restore_checkpoint=False))
    elif path == "injector":
        queue = deque(events)
        while queue:
            outputs.append(machine.apply(queue.popleft()))
    else:
        raise ValueError(path)
    return outputs


def expected_journal(case: dict, limit: int) -> list[dict]:
    """Format hand-authored assertions; does not call Transition or aggregation."""
    outputs = []
    for event, expected in zip(case["events"][:limit], case["expected"][:limit]):
        state = expected["state"]
        outputs.append({"event_id": event["id"], "source_id": event["source_id"],
                        "instrument_id": event["instrument_id"], "event_ns": expected["event_ns"],
                        "cutoff_ns": event["receive_ns"], "decision": expected["decision"],
                        "reason": expected["reason"], "state": state, "state_digest": digest(state)})
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--zone-source", type=Path, default=Path("/usr/share/zoneinfo/America/New_York"))
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("output exists: preserve prior attempt; choose a new path")
    args.output.mkdir(parents=True)
    start = time.monotonic()
    before_cpu = time.process_time()
    if sys.version_info[:3] != (3, 12, 14):
        raise SystemExit("the authorized interpreter is Python 3.12.14")
    bundle = json.loads(args.fixtures.read_text())
    assert bundle["synthetic"] is True and len(bundle["journals"]) == 8
    source_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    fixture_hash = hashlib.sha256(args.fixtures.read_bytes()).hexdigest()
    zone = None
    tz_actual = None
    if args.zone_source.is_file():
        tz_actual = hashlib.sha256(args.zone_source.read_bytes()).hexdigest()
        if tz_actual == TZ_HASH:
            target = args.output/"America_New_York.TZif"
            shutil.copyfile(args.zone_source, target)
            target.chmod(0o444)
            with target.open("rb") as stream:
                zone = ZoneInfo.from_file(stream, key="America/New_York")
    manifest = {"scope_commit": "fa435a4f3ff2c15360b5fa0b5da4e2cf2259d14f",
                "source_sha256": source_hash, "fixture_sha256": fixture_hash,
                "expected_oracle": "hand-authored per-event states in fixture file; no transition-generated expectations",
                "python": sys.version, "timezone_expected": TZ_HASH, "timezone_actual": tz_actual,
                "paths": PATHS, "planned_initial_runs": 160, "random_seed": None,
                "financial_experiments": 0, "market_data_rows": 0, "network_required": False}
    (args.output/"frozen-manifest.json").write_bytes(canonical(manifest)+b"\n")
    results = []
    with (args.output/"runs.jsonl").open("w") as handle:
        for case in bundle["journals"]:
            events = case["events"]
            assert 4 <= len(events) <= 256 and len(events) == len(case["expected"])
            limits = (len(events), 1, len(events)//2, len(events)-1)
            for path in PATHS:
                full = None
                for limit in limits:
                    row = {"case": case["id"], "path": path, "event_count": limit,
                           "role": "full" if limit == len(events) else "prefix"}
                    if case["id"] == "R5" and zone is None:
                        row.update(status="blocked", reason="pinned_timezone_unavailable")
                    else:
                        try:
                            actual = run_journal(events[:limit], path, zone)
                            expected = expected_journal(case, limit)
                            assert len(actual) == len(expected), "missing or extra decision outputs"
                            differences = [i for i, (a, e) in enumerate(zip(actual, expected)) if a != e]
                            prefix_equal = full is None or actual == full[:limit]
                            row.update(status="passed" if not differences and prefix_equal else "failed",
                                       differing_indices=differences, prefix_equal=prefix_equal,
                                       actual_digest=digest(actual), expected_digest=digest(expected))
                            if differences:
                                i = differences[0]
                                row["first_difference"] = {"actual": actual[i], "expected": expected[i]}
                            if limit == len(events):
                                full = actual
                                (args.output/f"{case['id']}-{path}.json").write_bytes(canonical(actual)+b"\n")
                        except Exception as error:
                            row.update(status="failed", error=f"{type(error).__name__}: {error}")
                    results.append(row)
                    handle.write(json.dumps(row, sort_keys=True)+"\n")
                    handle.flush()
    summary = {"package": "R", "synthetic_only": True, "manifest": manifest,
               "runs": len(results), "passed": sum(x["status"] == "passed" for x in results),
               "failed": sum(x["status"] == "failed" for x in results),
               "blocked": sum(x["status"] == "blocked" for x in results),
               "elapsed_seconds": time.monotonic()-start, "cpu_seconds": time.process_time()-before_cpu,
               "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
               "artifact_bytes": sum(p.stat().st_size for p in args.output.rglob("*") if p.is_file()),
               "software_download_bytes": 0, "runtime_network_calls": 0,
               "limits": ["standalone synthetic prototype; no production implementation", "no real feed, strategy or fill equivalence demonstrated", "checkpoint reconstruction is in-memory for transformation state, not engine crash recovery"]}
    (args.output/"summary.json").write_text(json.dumps(summary, indent=2)+"\n")
    print(json.dumps({k: v for k, v in summary.items() if k != "manifest"}, indent=2))
    return 0 if summary["passed"] == 160 else 1


if __name__ == "__main__":
    raise SystemExit(main())
