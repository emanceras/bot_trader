"""Finite synthetic M storage checks; execution requires the approved external guard.

No market inputs or network access. Commands preserve frozen expectations and old
outputs. The caller owns isolated interpreters, source exports and resource caps.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import traceback


PACKS = ("v1", "boundary", "precision")
EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode()


def create(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def modules(source: Path):
    sys.path.insert(0, str(source / "src"))
    import pyarrow as pa
    import pyarrow.parquet as pq
    import duckdb
    return pa, pq, duckdb


def versions(pa, duckdb) -> dict:
    return {"python": sys.version, "pyarrow": pa.__version__, "duckdb": duckdb.__version__}


def require_versions(role: str, pa, duckdb) -> None:
    expected = "23.0.1" if role == "control" else "26.0.0"
    if pa.__version__ != expected or duckdb.__version__ != "1.5.6":
        raise RuntimeError(f"Pinned versions differ: {versions(pa, duckdb)}")
    if sys.version_info[:3] != (3, 12, 14):
        raise RuntimeError("M requires Python 3.12.14")


def instant_us(value: datetime) -> int:
    delta = value - EPOCH
    return (delta.days * 86400 + delta.seconds) * 1_000_000 + delta.microseconds


def scalar_json(value):
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, datetime):
        return instant_us(value)
    return value


def normalize_table(table, pa) -> dict:
    """Normalize exact typed values without routing nanoseconds through datetime."""
    result = {}
    for field in table.schema:
        column = table[field.name]
        if pa.types.is_timestamp(field.type):
            values = column.cast(pa.int64()).to_pylist()
        else:
            values = [scalar_json(v) for v in column.to_pylist()]
        result[field.name] = values
    return result


def schema_description(schema) -> dict:
    return {
        "fields": [{"name": f.name, "type": str(f.type), "nullable": f.nullable} for f in schema],
        "metadata": {k.decode(): v.decode() for k, v in (schema.metadata or {}).items()},
    }


def fixture_tables(pa, pq):
    from bot_trader.core.contracts import DatasetSpec
    from bot_trader.market_data.service import _generate, _serialize

    spec = DatasetSpec(seed=42, rows=120)
    bars = _generate(spec)
    payload = _serialize(bars)
    v1 = pq.read_table(BytesIO(payload))
    # Actual control generator values are the declared old-format reference;
    # boundary/precision goldens below are independent declarative arithmetic.
    expected_v1 = {name: [] for name in v1.column_names}
    for bar in bars:
        raw = bar.model_dump()
        for name in expected_v1:
            value = raw[name]
            if isinstance(value, Decimal):
                value = value.quantize(Decimal("0.00000001"))
            expected_v1[name].append(scalar_json(value))

    amount_cycle = [None, "0.00000000", "0.00000001", "-0.00000001",
                    "9999999999999999.99999999", "-9999999999999999.99999999",
                    "123456789.12345678", "-12.34000000"]
    amounts = [None if amount_cycle[i % 8] is None else Decimal(amount_cycle[i % 8]) for i in range(32)]
    units = ["USD" if i % 2 == 0 else "USDT" for i in range(32)]
    schema = pa.schema([
        pa.field("event_id", pa.string(), nullable=False),
        pa.field("amount", pa.decimal128(24, 8)),
        pa.field("unit", pa.dictionary(pa.int8(), pa.string())),
        pa.field("available_us", pa.int64(), nullable=False),
        pa.field("nullable_label", pa.string()),
    ], metadata={b"fixture": b"M-boundary/1", b"availability_unit": b"us", b"synthetic": b"true"})
    boundary_values = {
        "event_id": [f"B-{i:02d}" for i in range(32)], "amount": amounts, "unit": units,
        "available_us": [1_600_000_000_000_000 + i for i in range(32)],
        "nullable_label": [None if i % 3 == 0 else "" if i % 3 == 1 else "present" for i in range(32)],
    }
    boundary = pa.Table.from_pydict(boundary_values, schema=schema)
    expected_boundary = {k: [scalar_json(v) for v in values] for k, values in boundary_values.items()}

    ticks = [1_600_000_000_000_000_001 + i * 101 for i in range(32)]
    precision_schema = pa.schema([
        pa.field("event_id", pa.string(), nullable=False),
        pa.field("event_ns", pa.int64(), nullable=False),
        pa.field("available_ns", pa.int64(), nullable=False),
        pa.field("display_utc", pa.timestamp("ns", tz="UTC")),
        pa.field("display_us", pa.timestamp("us", tz="UTC")),
    ], metadata={b"fixture": b"M-precision/1", b"canonical_clock": b"integer epoch nanoseconds", b"display_only": b"true"})
    precision_values = {
        "event_id": [f"P-{i:02d}" for i in range(32)],
        "event_ns": ticks, "available_ns": [v + 1003 for v in ticks],
        "display_utc": ticks, "display_us": [v // 1000 for v in ticks],
    }
    precision = pa.Table.from_arrays([
        pa.array(precision_values["event_id"]), pa.array(ticks, type=pa.int64()),
        pa.array(precision_values["available_ns"], type=pa.int64()),
        pa.array(ticks, type=pa.timestamp("ns", tz="UTC")),
        pa.array(precision_values["display_us"], type=pa.timestamp("us", tz="UTC")),
    ], schema=precision_schema)
    return {
        "v1": (v1, expected_v1), "boundary": (boundary, expected_boundary),
        "precision": (precision, precision_values),
    }, spec.model_dump(mode="json")


def freeze(args, pa, pq, duckdb) -> dict:
    require_versions("control", pa, duckdb)
    packs, spec = fixture_tables(pa, pq)
    expected = {
        "id": "M-frozen-expectations/1", "synthetic": True, "spec": spec,
        "versions": versions(pa, duckdb), "harness_sha256": digest(Path(__file__).read_bytes()),
        "packs": {name: {"rows": table.num_rows, "schema": schema_description(table.schema),
                          "values": values} for name, (table, values) in packs.items()},
        "oracle_scope": "v1 control generator reference; independent Decimal/null/integer-time declarative values; no candidate outputs consulted",
    }
    data = json_bytes(expected)
    create(args.workspace / "frozen.json", data)
    create(args.workspace / "frozen.sha256", (digest(data) + "\n").encode())
    return {"status": "prepared", "expectations_sha256": digest(data), "packs": list(packs)}


def load_frozen(workspace: Path) -> dict:
    data = (workspace / "frozen.json").read_bytes()
    assert digest(data) == (workspace / "frozen.sha256").read_text().strip()
    return json.loads(data)


def write_packs(args, pa, pq, duckdb) -> dict:
    require_versions(args.role, pa, duckdb)
    frozen = load_frozen(args.workspace)
    packs, _ = fixture_tables(pa, pq)
    files = []
    for name, (table, _) in packs.items():
        assert normalize_table(table, pa) == frozen["packs"][name]["values"]
        assert schema_description(table.schema) == frozen["packs"][name]["schema"]
        parquet = BytesIO()
        if name == "v1":
            from bot_trader.core.contracts import DatasetSpec
            from bot_trader.market_data.service import _generate, _serialize
            parquet.write(_serialize(_generate(DatasetSpec.model_validate(frozen["spec"]))))
        else:
            pq.write_table(table, parquet, compression="zstd", version="2.6")
        ipc = pa.BufferOutputStream()
        with pa.ipc.new_file(ipc, table.schema) as writer:
            writer.write_table(table)
        for suffix, data in (("parquet", parquet.getvalue()), ("arrow", ipc.getvalue().to_pybytes())):
            path = args.workspace / "packs" / args.role / f"{name}.{suffix}"
            create(path, data)
            files.append({"path": str(path), "bytes": len(data), "sha256": digest(data)})
    record = {"status": "prepared", "writer": args.role, "versions": versions(pa, duckdb), "files": files}
    create(args.workspace / f"writer-{args.role}.json", json_bytes(record))
    return record


def check_equal(actual, expected, label: str):
    if actual != expected:
        raise AssertionError(f"{label}: actual and frozen expected values differ")


def read_packs(args, pa, pq, duckdb) -> dict:
    require_versions(args.role, pa, duckdb)
    frozen = load_frozen(args.workspace)
    cases = []
    for writer_role in ("control", "candidate"):
        manifest = json.loads((args.workspace / f"writer-{writer_role}.json").read_text())
        for name in PACKS:
            record = {"case": f"M2-{name}-{writer_role}-to-{args.role}", "writer": writer_role, "reader": args.role}
            try:
                expected = frozen["packs"][name]
                tables = []
                for suffix in ("parquet", "arrow"):
                    path = args.workspace / "packs" / writer_role / f"{name}.{suffix}"
                    entry = next(x for x in manifest["files"] if x["path"] == str(path))
                    check_equal(digest(path.read_bytes()), entry["sha256"], "immutable writer bytes")
                    table = pq.read_table(path) if suffix == "parquet" else pa.ipc.open_file(path).read_all()
                    check_equal(normalize_table(table, pa), expected["values"], suffix + " values")
                    check_equal(schema_description(table.schema), expected["schema"], suffix + " schema")
                    tables.append(table)
                db = duckdb.connect(":memory:", config={"threads": "1"})
                try:
                    db.register("pack", tables[0])
                    if name == "v1":
                        rows = db.execute("SELECT instrument, epoch_us(event_time), epoch_us(received_at), close, volume, quote_currency FROM pack").fetchall()
                        wanted = list(zip(expected["values"]["instrument"], expected["values"]["event_time"], expected["values"]["received_at"], expected["values"]["close"], expected["values"]["volume"], expected["values"]["quote_currency"]))
                        check_equal([[scalar_json(x) for x in row] for row in rows], [list(x) for x in wanted], "DuckDB v1 exact projection")
                    elif name == "boundary":
                        rows = db.execute("SELECT event_id, amount, unit, available_us, nullable_label FROM pack").fetchall()
                        wanted = list(zip(*(expected["values"][k] for k in ("event_id", "amount", "unit", "available_us", "nullable_label"))))
                        check_equal([[scalar_json(x) for x in row] for row in rows], [list(x) for x in wanted], "DuckDB boundary exact projection")
                    else:
                        rows = db.execute("SELECT event_id, event_ns, available_ns FROM pack").fetchall()
                        wanted = list(zip(*(expected["values"][k] for k in ("event_id", "event_ns", "available_ns"))))
                        check_equal([list(x) for x in rows], [list(x) for x in wanted], "canonical ticks preserved")
                        lossy = [r[0] for r in db.execute("SELECT epoch_ns(display_utc) FROM pack").fetchall()]
                        check_equal(lossy, [v // 1000 * 1000 for v in expected["values"]["event_ns"]], "known lossy native conversion negative control")
                        assert lossy != expected["values"]["event_ns"]
                        record["negative_control"] = {"native_zoned_ns_loss_observed": True, "admitted_sort_key": "event_ns integer", "unsafe_view_not_used_as_canonical": True}
                finally:
                    db.close()
                record["status"] = "passed"
            except Exception as error:
                record.update(status="failed", error=f"{type(error).__name__}: {error}")
            cases.append(record)
    return {"versions": versions(pa, duckdb), "cases": cases, "all_passed": all(c["status"] == "passed" for c in cases)}


def guards(args, pa, pq, duckdb) -> dict:
    require_versions(args.role, pa, duckdb)
    from bot_trader.core.contracts import DatasetSpec, Principal
    from bot_trader.core.errors import AccessDenied, PlatformError
    from bot_trader.core.security import Policy
    from bot_trader.core.settings import Settings
    from bot_trader.market_data import DatasetService, LocalArtifactStore
    from bot_trader.persistence import Database, Repository, migrate

    class NoReadStore:
        calls = 0
        def get(self, *a):
            self.calls += 1
            raise AssertionError("Forbidden payload fetched before denial")

    root = args.workspace / f"guards-{args.role}"
    root.mkdir(parents=True, exist_ok=False)
    settings = Settings(repository_root=args.source, data_dir=root)
    database = Database(settings)
    migrate(database)
    store = LocalArtifactStore(root / "artifacts")
    repo = Repository(database)
    service = DatasetService(repo, store, Policy(), settings)
    admin = Principal(id="technical-check", role="admin")
    original = service.create(DatasetSpec(rows=4), admin)
    cases = []
    for kind in ("corrupt", "reserved", "real-label"):
        record = {"case": f"M3-{kind}-{args.role}"}
        try:
            if kind == "corrupt":
                artifact = original.body["artifact"]
                path = store.root / f"{artifact['digest']}.parquet"
                old_bytes = path.read_bytes()
                path.write_bytes(b"deliberately corrupt synthetic artifact")
                try:
                    service.bars(original.id, admin)
                    raise AssertionError("Corrupt payload accepted")
                except PlatformError as error:
                    assert "checksum" in str(error)
                finally:
                    path.write_bytes(old_bytes)
                assert digest(path.read_bytes()) == artifact["digest"]
            else:
                body = deepcopy(original.body)
                if kind == "reserved":
                    body["partition"] = "final"
                    body["spec"]["partition"] = "final"
                else:
                    body["synthetic"] = False
                document = repo.put("dataset", f"guard-{kind}", body)
                denied_store = NoReadStore()
                guarded = DatasetService(repo, denied_store, Policy(), settings)
                try:
                    guarded.bars(document.id, admin)
                    raise AssertionError("Unauthorized payload accepted")
                except (AccessDenied, PlatformError) as error:
                    if kind == "reserved":
                        assert isinstance(error, AccessDenied)
                    else:
                        assert "synthetic" in str(error)
                assert denied_store.calls == 0
            record["status"] = "passed"
        except Exception as error:
            record.update(status="failed", error=f"{type(error).__name__}: {error}")
        cases.append(record)
    return {"versions": versions(pa, duckdb), "cases": cases, "all_passed": all(c["status"] == "passed" for c in cases)}


def interrupted_child(args):
    from bot_trader.market_data.storage import LocalArtifactStore
    store = LocalArtifactStore(args.workspace)
    original_link = os.link
    def stop_before_link(*a, **kw):
        create(args.workspace / "ready.json", json_bytes({"pid": os.getpid(), "cut": "after_file_fsync_before_link"}))
        os.kill(os.getpid(), signal.SIGSTOP)
        return original_link(*a, **kw)
    os.link = stop_before_link
    store.put(b"new synthetic version pending publication", "json")
    raise AssertionError("Child resumed unexpectedly")


def crash(args, pa, pq, duckdb) -> dict:
    require_versions(args.role, pa, duckdb)
    from bot_trader.core.errors import NotFound
    from bot_trader.market_data.storage import LocalArtifactStore
    root = args.workspace / f"crash-{args.role}"
    root.mkdir(parents=True, exist_ok=False)
    store = LocalArtifactStore(root)
    original = b"old admitted synthetic artifact"
    old_digest = store.put(original, "json")
    manifest = {"artifact_digest": old_digest, "version": 1}
    create(root / "original-manifest.json", json_bytes(manifest))
    manifest_hash = digest((root / "original-manifest.json").read_bytes())
    cmd = [sys.executable, str(Path(__file__).resolve()), "_interrupt", "--source", str(args.source), "--workspace", str(root), "--role", args.role]
    process = subprocess.Popen(cmd)
    record = {"case": f"M4-interrupted-publication-{args.role}", "cut": "after_file_fsync_before_atomic_link"}
    try:
        deadline = time.monotonic() + 20
        while not (root / "ready.json").exists() and time.monotonic() < deadline:
            if process.poll() is not None:
                raise AssertionError(f"Writer exited before cut: {process.returncode}")
            time.sleep(0.01)
        assert (root / "ready.json").exists(), "Writer did not reach cut"
        os.kill(process.pid, signal.SIGKILL)
        assert process.wait(timeout=5) == -signal.SIGKILL
        assert digest((root / "original-manifest.json").read_bytes()) == manifest_hash
        assert store.get(old_digest, "json") == original
        new_digest = digest(b"new synthetic version pending publication")
        try:
            store.get(new_digest, "json")
            raise AssertionError("Interrupted artifact became published")
        except NotFound:
            pass
        pending = list(root.glob(".pending-*"))
        assert len(pending) == 1
        assert digest(pending[0].read_bytes()) == new_digest
        # Restore means an independent new store reads the same old manifest;
        # pending bytes remain preserved, never treated as an admitted result.
        restored = LocalArtifactStore(root)
        assert restored.get(manifest["artifact_digest"], "json") == original
        record.update(status="passed", pending_preserved=True, original_manifest_sha256=manifest_hash,
                      killed_returncode=process.returncode)
    except Exception as error:
        record.update(status="failed", error=f"{type(error).__name__}: {error}")
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=5)
    return {"versions": versions(pa, duckdb), "cases": [record], "all_passed": record["status"] == "passed"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("freeze", "write", "read", "guards", "crash", "_interrupt"))
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--role", choices=("control", "candidate"), default="control")
    parser.add_argument("--result", type=Path)
    args = parser.parse_args()
    args.source = args.source.resolve()
    args.workspace = args.workspace.resolve()
    if args.result is not None and args.result.exists():
        raise SystemExit("Result path exists; preserve prior attempts")
    pa, pq, duckdb = modules(args.source)
    if args.command == "_interrupt":
        interrupted_child(args)
        return 1
    started = time.monotonic()
    try:
        result = {"freeze": freeze, "write": write_packs, "read": read_packs,
                  "guards": guards, "crash": crash}[args.command](args, pa, pq, duckdb)
    except Exception as error:
        result = {"status": "failed", "all_passed": False,
                  "error": f"{type(error).__name__}: {error}", "traceback": traceback.format_exc()}
    result.update(command=args.command, role=args.role, synthetic=True, financial_experiments=0,
                  harness_sha256=digest(Path(__file__).read_bytes()), elapsed_seconds=time.monotonic()-started)
    if args.result:
        create(args.result, json_bytes(result))
    print(json.dumps(result, sort_keys=True))
    return 0 if result.get("all_passed", result.get("status") == "prepared") else 1


if __name__ == "__main__":
    raise SystemExit(main())
