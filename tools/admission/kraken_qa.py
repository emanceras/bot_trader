"""Offline Package A structural audit; no strategy or application imports.

Two authorized immutable ZIPs only. All bytes are streamed for CRC/hash/row
counts; numerical checks sample the first/last 64 rows of every CSV. A separate
declared trade/bar sample tests exact aggregation. Raw rows never enter reports.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import resource
import stat
import time
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal, Inexact, InvalidOperation, getcontext
from pathlib import Path, PurePosixPath
from zipfile import ZIP_DEFLATED, ZipFile

START = int(datetime(2026, 7, 1, tzinfo=timezone.utc).timestamp())
END = int(datetime(2026, 10, 1, tzinfo=timezone.utc).timestamp())
MINUTES = (1, 5, 15, 60, 240, 720, 1440)
EDGE_ROWS = 64
BUFFER = 65536
CHUNK = 1024 * 1024
EXPECTED = {
    "ohlcvt": ("Kraken_OHLCVT_2026Q3.zip", 576348633,
               "35d1f89eac2b22560756a839130c40533653c12e3e74651a5b9f515e8653ae54"),
    "trades": ("Kraken_Trades_2026Q3.zip", 1596570274,
               "b802c78e05351b485c4ce2c8619e473a0e8c110883569f55ffe29baf59d7496f"),
}
ARCHIVE_SHA256 = {
    "ohlcvt": "96daae63c7b3acb522892e1f602f9c564d1a3fb659089d9b0699282f30d41226",
    "trades": "67aa726be17a0f3ed14e4737030c777e1aa522e568090e72aa950415d66bce25",
}
TRADE_COLUMNS = ["timestamp", "price", "volume", "type", "order_type", "misc", "trade_id"]
BAR_COLUMNS = ["timestamp", "open", "high", "low", "close", "volume", "trades"]
getcontext().prec = 80
getcontext().traps[Inexact] = True  # Fail instead of silently rounding an exact notional.


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(CHUNK):
            digest.update(chunk)
    return digest.hexdigest()


def verify_inventory_identity(kind: str, result: dict) -> None:
    """Bind the computed local body identity to the acquisition receipt."""
    if result["sha256"] != ARCHIVE_SHA256[kind]:
        raise ValueError("Archive body differs from its acquisition receipt")


def stream_member(archive: ZipFile, name: str) -> tuple[dict, bytes, bytes]:
    """zipfile verifies the CRC on EOF; retain bounded edges, never whole CSVs."""
    digest = hashlib.sha256()
    size = newlines = 0
    first = last = b""
    with archive.open(name) as stream:
        while chunk := stream.read(CHUNK):
            digest.update(chunk)
            size += len(chunk)
            newlines += chunk.count(b"\n")
            first = (first + chunk[:BUFFER])[:BUFFER]
            last = (last + chunk)[-BUFFER:]
    lines = newlines + int(size > 0 and not last.endswith(b"\n"))
    return {"bytes_read": size, "physical_lines": lines,
            "sha256": digest.hexdigest(), "crc_verified": True}, first, last


def edge_records(first: bytes, last: bytes, size: int, rows: int,
                 has_header: bool) -> list[tuple[int, list[str]]]:
    """Select unique numbered first/last records; records cannot contain newlines."""
    initial = first.splitlines()
    if size > len(first) and not first.endswith(b"\n"):
        initial = initial[:-1]
    initial = initial[int(has_header):]
    ending = last.splitlines()
    if size > len(last):
        ending = ending[1:]  # buffer may start mid-record; drop it conservatively
    else:
        ending = ending[int(has_header):]
    selected = dict(enumerate(initial[:EDGE_ROWS]))
    tail = ending[-EDGE_ROWS:]
    selected.update((rows - len(tail) + i, line) for i, line in enumerate(tail))
    return [(number, next(csv.reader([line.decode("utf-8")])))
            for number, line in sorted(selected.items())]


def validate_records(records: list[tuple[int, list[str]]], kind: str,
                     interval: int | None) -> dict:
    errors: Counter = Counter()
    notes: Counter = Counter()
    first_time = last_time = None
    previous = previous_id = previous_values = None
    seen_ids: set[int] = set()
    max_precision = 0
    for _, row in records:
        if len(row) != 7:
            errors["column_count"] += 1
            continue
        try:
            numeric = row[:3] if kind == "trades" else row[:6]
            values = [Decimal(value) for value in numeric]
            if not all(value.is_finite() for value in values):
                errors["nonfinite"] += 1
                continue
            timestamp = values[0]
            first_time = timestamp if first_time is None else first_time
            last_time = timestamp
            max_precision = max(max_precision, max(0, -timestamp.as_tuple().exponent))
            if timestamp < START or timestamp >= END:
                errors["outside_named_quarter"] += 1
            if previous is not None and timestamp < previous:
                errors["timestamp_regression_in_sample"] += 1
            if kind == "ohlcvt":
                if timestamp != timestamp.to_integral_value() or timestamp % (interval * 60):
                    errors["unaligned_bar_start"] += 1
                _, opening, high, low, closing, volume = values
                trades = Decimal(row[6])
                if min(opening, high, low, closing) <= 0 or volume < 0:
                    errors["invalid_sign"] += 1
                if not (low <= min(opening, closing) <= max(opening, closing) <= high):
                    errors["ohlc_invariant"] += 1
                if not trades.is_finite() or trades <= 0 or trades != trades.to_integral_value():
                    errors["invalid_trade_count"] += 1
                if previous == timestamp:
                    errors["duplicate_bar_start_in_sample"] += 1
                if previous is not None and timestamp - previous > interval * 60:
                    notes["sparse_or_unsampled_gap"] += 1
            else:
                _, price, volume = values
                if price <= 0 or volume <= 0:
                    errors["invalid_sign"] += 1
                if row[3] not in ("b", "s", "") or row[4] not in ("l", "m", ""):
                    errors["invalid_side_or_order_type"] += 1
                if all(value == "" for value in row[3:]):
                    notes["metadata_and_trade_id_absent"] += 1
                if row[6]:
                    trade_id = int(row[6])
                    if trade_id in seen_ids:
                        errors["duplicate_trade_id_in_sample"] += 1
                    if previous_id is not None and trade_id < previous_id:
                        errors["trade_id_regression_in_sample"] += 1
                    seen_ids.add(trade_id)
                    previous_id = trade_id
                else:
                    notes["trade_id_absent"] += 1
                if previous_values == tuple(values):
                    notes["repeated_time_price_quantity_candidate"] += 1
                previous_values = tuple(values)
            previous = timestamp
        except (InvalidOperation, ValueError, OverflowError):
            errors["invalid_numeric"] += 1
    return {"rows_checked": len(records), "errors": dict(errors), "notes": dict(notes),
            "first_sample_timestamp": str(first_time), "last_sample_timestamp": str(last_time),
            "max_sample_timestamp_decimal_places": max_precision}


def inventory(path: Path, kind: str, output: Path) -> dict:
    expected_name, expected_size, reviewed_notice_hash = EXPECTED[kind]
    if path.name != expected_name or path.stat().st_size != expected_size:
        raise ValueError("Archive name or size differs from the authorized object")
    start, cpu = time.monotonic(), time.process_time()
    errors: Counter = Counter()
    notes: Counter = Counter()
    sampled_rows = total_rows = crc_bytes = 0
    per_field: dict[str, list[str]] = {}
    metadata_absent: list[str] = []
    with ZipFile(path) as archive:
        infos = archive.infolist()
        names = [item.filename for item in infos]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate ZIP member names")
        for item in infos:
            parts = PurePosixPath(item.filename)
            if (parts.is_absolute() or ".." in parts.parts or "\\" in item.filename
                    or stat.S_ISLNK(item.external_attr >> 16) or item.flag_bits & 1
                    or item.compress_type != ZIP_DEFLATED):
                raise ValueError("Unsafe or unsupported ZIP entry")
        total_unpacked = sum(item.file_size for item in infos)
        if total_unpacked > 7_000_000_000:
            raise ValueError("Changed directory exceeds observed per-object streaming budget")
        if set(name for name in names if not name.endswith(".csv")) != {"README.md", "MANIFEST.json"}:
            raise ValueError("New archive notices need review before processing")
        notice = archive.read("README.md")
        if hashlib.sha256(notice).hexdigest() != reviewed_notice_hash:
            raise ValueError("Archive notice differs from the privately reviewed version")
        manifest = json.loads(archive.read("MANIFEST.json"))
        expected_columns = BAR_COLUMNS if kind == "ohlcvt" else TRADE_COLUMNS
        if (manifest["product"] != kind or manifest["columns"] != expected_columns
                or manifest["has_header"] != (kind == "trades")):
            raise ValueError("Unadmitted schema")
        if b"SHA256SUMS.txt" in notice and "SHA256SUMS.txt" not in names:
            notes["referenced_provider_checksum_file_absent"] = 1
        pairs: set[str] = set()
        intervals: Counter = Counter()
        csv_files = 0
        with (output / f"{kind}-inventory.jsonl").open("x") as ledger:
            for item in infos:
                facts, first, last = stream_member(archive, item.filename)
                crc_bytes += facts["bytes_read"]
                entry = {"name": item.filename, "advertised_size": item.file_size,
                         "compressed_size": item.compress_size, "crc32": f"{item.CRC:08x}",
                         **facts}
                if item.filename.endswith(".csv"):
                    csv_files += 1
                    match = re.fullmatch(r"([A-Z0-9]+)_(1|5|15|60|240|720|1440)\.csv", item.filename) if kind == "ohlcvt" else re.fullmatch(r"([A-Z0-9]+)\.csv", item.filename)
                    if not match:
                        raise ValueError(f"Unknown filename convention: {item.filename}")
                    pair = match[1]
                    interval = int(match[2]) if kind == "ohlcvt" else None
                    pairs.add(pair)
                    intervals[str(interval)] += 1
                    if kind == "trades" and first.splitlines()[0].decode().split(",") != TRADE_COLUMNS:
                        raise ValueError(f"Trade header differs: {item.filename}")
                    rows = facts["physical_lines"] - int(kind == "trades")
                    records = edge_records(first, last, item.file_size, rows, kind == "trades")
                    checks = validate_records(records, kind, interval)
                    entry.update({"rows": rows, "sample": checks})
                    total_rows += rows
                    sampled_rows += checks["rows_checked"]
                    errors.update(checks["errors"])
                    notes.update(checks["notes"])
                    for field in checks["errors"]:
                        per_field.setdefault(field, []).append(item.filename)
                    if checks["notes"].get("metadata_and_trade_id_absent"):
                        metadata_absent.append(pair)
                ledger.write(json.dumps(entry, sort_keys=True) + "\n")
        for field, actual in (("rows", total_rows), ("files", csv_files), ("pairs", len(pairs))):
            if manifest[field] != actual:
                errors[f"manifest_{field}_mismatch"] += 1
        result = {
            "object": path.name, "sha256": digest_file(path), "archive_bytes": path.stat().st_size,
            "members": len(infos), "csv_files": csv_files, "pairs": len(pairs),
            "uncompressed_bytes": total_unpacked, "crc_verified_members": len(infos),
            "crc_bytes_read": crc_bytes, "all_member_line_count_rows": total_rows,
            "sampled_rows": sampled_rows, "sample_policy": "First and last 64 data rows per CSV, overlap removed",
            "errors": dict(errors), "notes": dict(notes), "members_with_errors": per_field,
            "metadata_absent_pairs_in_sample": metadata_absent,
            "interval_member_counts_minutes": dict(intervals), "manifest": manifest,
            "inventory_sha256": digest_file(output / f"{kind}-inventory.jsonl"),
            "wall_seconds": time.monotonic() - start, "cpu_seconds": time.process_time() - cpu,
        }
        verify_inventory_identity(kind, result)
        return result


def aggregate_trade(bucket: dict, timestamp: Decimal, price: Decimal, volume: Decimal) -> None:
    if not bucket:
        bucket.update(open=price, high=price, low=price, close=price,
                      volume=Decimal(0), trades=0, exact_quote_notional=Decimal(0),
                      diagnostic_float_volume=0.0)
    bucket["high"] = max(bucket["high"], price)
    bucket["low"] = min(bucket["low"], price)
    bucket["close"] = price
    bucket["volume"] += volume
    bucket["trades"] += 1
    bucket["exact_quote_notional"] += price * volume
    bucket["diagnostic_float_volume"] += float(volume)


def reconcile(trade_path: Path, bar_path: Path, pairs: list[str],
              volume_diagnostics: bool = False) -> dict:
    """Fixed calendar windows, no price-dependent selection or tolerance tuning."""
    # Technical coverage windows are not strategy horizons or research partitions.
    days = [int(datetime(2026, month, day, tzinfo=timezone.utc).timestamp())
            for month, day in ((7, 2), (8, 15), (9, 29))]
    findings = []
    start, cpu = time.monotonic(), time.process_time()
    with ZipFile(trade_path) as trades, ZipFile(bar_path) as bars:
        for pair in pairs:
            buckets: dict[tuple[int, int], dict] = {}
            scanned = selected = 0
            regressions = 0
            previous = None
            with trades.open(f"{pair}.csv") as raw:
                rows = csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8", newline=""))
                for row in rows:
                    scanned += 1
                    timestamp = Decimal(row["timestamp"])
                    if previous is not None and timestamp < previous:
                        regressions += 1
                    previous = timestamp
                    if not any(day <= timestamp < day + 86400 for day in days):
                        continue
                    selected += 1
                    price, volume = Decimal(row["price"]), Decimal(row["volume"])
                    for interval in MINUTES:
                        beginning = int(timestamp // (interval * 60)) * interval * 60
                        bucket = buckets.setdefault((interval, beginning), {})
                        aggregate_trade(bucket, timestamp, price, volume)
            counters: Counter = Counter()
            per_interval = {}
            for interval in MINUTES:
                counts: Counter = Counter()
                max_volume_difference = Decimal(0)
                volume_places: Counter = Counter()
                seen = set()
                with bars.open(f"{pair}_{interval}.csv") as raw:
                    for row in csv.reader(io.TextIOWrapper(raw, encoding="utf-8", newline="")):
                        timestamp = int(row[0])
                        if not any(day <= timestamp and timestamp + interval * 60 <= day + 86400 for day in days):
                            continue
                        counts["bars_compared"] += 1
                        key = (interval, timestamp)
                        if key in seen:
                            counts["duplicate_bar"] += 1
                        seen.add(key)
                        bucket = buckets.get(key)
                        if bucket is None:
                            counts["bar_without_trades"] += 1
                            continue
                        mismatch = False
                        for field, value in zip(("open", "high", "low", "close", "volume", "trades"), row[1:], strict=True):
                            if Decimal(value) != bucket[field]:
                                counts[f"exact_{field}_mismatch"] += 1
                                mismatch = True
                        counts["bars_exactly_matching"] += int(not mismatch)
                        if bucket["close"] * bucket["volume"] != bucket["exact_quote_notional"]:
                            counts["close_times_volume_differs_from_exact_notional"] += 1
                        if volume_diagnostics:
                            observed_volume = Decimal(row[5])
                            max_volume_difference = max(max_volume_difference,
                                                        abs(observed_volume - bucket["volume"]))
                            volume_places[str(-observed_volume.as_tuple().exponent)] += 1
                            if observed_volume == Decimal(str(bucket["diagnostic_float_volume"])):
                                counts["volume_reproduced_by_ordered_float_sum"] += 1
                counts["trade_bins_without_bar"] = sum(1 for key in buckets if key[0] == interval and key not in seen)
                per_interval[str(interval)] = dict(counts)
                if volume_diagnostics:
                    per_interval[str(interval)]["max_absolute_volume_difference_base_units"] = str(max_volume_difference)
                    per_interval[str(interval)]["bar_volume_decimal_places_counts"] = dict(volume_places)
                counters.update(counts)
            findings.append({"pair_label_unverified_identity": pair, "trade_rows_scanned": scanned,
                             "trade_rows_in_windows": selected,
                             "full_selected_member_timestamp_regressions": regressions,
                             "by_interval_minutes": per_interval, "totals": dict(counters)})
    return {"windows_utc": [datetime.fromtimestamp(day, timezone.utc).isoformat() for day in days],
            "window_seconds": 86400, "bin_convention": "[start, end), UTC epoch-aligned; exact Decimal comparison; no tolerance fitted",
            "selection": "XBTUSD and ETHUSD named structural anchors; lexicographically first pair with sampled absent metadata, if any (deduplicated)",
            "volume_diagnostics": "Sequential Python binary-float volume sum is a diagnostic reconstruction, not an admitted rounding tolerance or source certification" if volume_diagnostics else None,
            "pairs": findings, "wall_seconds": time.monotonic() - start,
            "cpu_seconds": time.process_time() - cpu}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archives", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    if any(path.resolve() == repo or repo in path.resolve().parents for path in (args.archives, args.output)):
        raise ValueError("Raw archives and detailed inventories must remain outside the repository")
    args.output.mkdir(parents=True, exist_ok=True)
    if args.result.exists():
        raise ValueError("Preserve prior results; choose a new result path for another audit")
    started, wall, cpu = stamp(), time.monotonic(), time.process_time()
    results = {}
    for kind, (name, _, _) in EXPECTED.items():
        results[kind] = inventory(args.archives / name, kind, args.output)
        (args.output / f"{kind}-summary.json").write_text(json.dumps(results[kind], indent=2) + "\n")
        print(json.dumps({"completed_inventory": kind, "rows": results[kind]["all_member_line_count_rows"],
                          "sampled_rows": results[kind]["sampled_rows"], "errors": results[kind]["errors"]}), flush=True)
    pairs = ["XBTUSD", "ETHUSD"]
    if results["trades"]["metadata_absent_pairs_in_sample"]:
        pairs.append(sorted(results["trades"]["metadata_absent_pairs_in_sample"])[0])
    reconciliation = reconcile(args.archives / EXPECTED["trades"][0],
                               args.archives / EXPECTED["ohlcvt"][0], list(dict.fromkeys(pairs)))
    record = {"schema_version": 1, "authority": "D-040", "started_at": started, "finished_at": stamp(),
              "scope": "Real Q3 data, structural QA only; no strategy, return, P&L or financial experiment",
              "script_sha256": digest_file(Path(__file__)), "inventories": results,
              "reconciliation": reconciliation,
              "resources": {"wall_seconds": time.monotonic() - wall,
                            "cpu_seconds": time.process_time() - cpu,
                            "peak_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                            "archive_disk_bytes": sum(value["archive_bytes"] for value in results.values()),
                            "private_output_bytes": sum(path.stat().st_size for path in args.output.iterdir() if path.is_file()),
                            "whole_archive_extraction": False},
              "limits": ["Full byte integrity and line counts are not full numerical validation",
                         "Only sampled rows checked for numeric, metadata and ID quality; no global duplicate claim",
                         "Quote labels do not certify currency identity or USD conversion",
                         "Absent intervals may have no trades; no original receipt timestamps, quotes or depth",
                         "Quarter and venue do not constrain future research history; this material is exposed QA",
                         "First/last observations are not listing/delisting records; missing metadata is not proof of delisting",
                         "Manifest/CRC/local hashes do not certify independent source correctness"]}
    args.result.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"audit_complete": True, "result": str(args.result), "resources": record["resources"]}), flush=True)


if __name__ == "__main__":
    main()
