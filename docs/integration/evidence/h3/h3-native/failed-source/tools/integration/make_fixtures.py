"""Author tiny deterministic synthetic integration sources, never market data."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "tests/fixtures/integration"
T0 = 1_700_000_000_000_000_000
SECOND = 1_000_000_000


def write_case(name, size):
    rows = []

    def emit(identifier, event, available, data):
        rows.append(dict(schema_version=2, event_id=identifier, source_id="slice-fixture",
                         source_version="1", stream_id="market", sequence=len(rows)+1,
                         instrument="SYNTH-USD", original_tick=event, original_unit="ns",
                         event_ns=event, available_ns=available, received_ns=available+10,
                         data=data))

    def bar(n, status, available):
        start, end = T0+(n-1)*SECOND, T0+n*SECOND
        price = 99+n
        emit(f"bar-{n}-{status}", start if status == "open" else end, available,
             dict(kind="bar", bar_id=f"bar-{n}", start_ns=start, end_ns=end, status=status,
                  label="open" if status == "open" else "close", open=str(price),
                  high=str(price if status == "open" else price+2), low=str(price),
                  close=str(price if status == "open" else price+2),
                  volume="0" if status == "open" else "2"))

    for n in (1, 2, 3):
        start = T0+(n-1)*SECOND
        offset = 300 if n == 3 else 30
        bar(n, "open", start+offset)
        for index, price in enumerate((99+n, 101+n), 1):
            at = start+offset+index*100
            emit(f"trade-{n}-{index}", at, at+10,
                 dict(kind="trade", price=str(price), quantity="1"))
        bar(n, "closed", start+SECOND+10)
        if n in (2, 3):
            event = start+SECOND+100
            bid, ask = ("104.95", "105.05") if n == 2 else ("106.95", "107.05")
            emit("quote-buy" if n == 2 else "quote-sell", event, event+10,
                 dict(kind="quote", origin="synthetic_explicit",
                      bids=[dict(price=bid, quantity="2")],
                      asks=[dict(price=ask, quantity=size)]))
            if n == 2:
                emit("quote-cancel", event+100, event+110,
                     dict(kind="quote", origin="synthetic_explicit",
                          bids=[dict(price="104.96", quantity="2")],
                          asks=[dict(price="105.06", quantity="2")]))
    raw = b"\n".join(json.dumps(row, sort_keys=True, separators=(",", ":")).encode()
                     for row in rows)+b"\n"
    raw_path = ROOT / f"{name}.jsonl"
    raw_path.write_bytes(raw)
    source = dict(schema_version=2, source_id="slice-fixture", source_version="1",
                  source_schema="fixture-jsonl-v2", locator=f"internal:integration/{name}",
                  rights="Internally authored synthetic fixture; project technical use permitted.",
                  permitted_use="technical_validation_only", acquired_ns=raw_path.stat().st_mtime_ns,
                  raw_sha256=hashlib.sha256(raw).hexdigest(), size_bytes=len(raw),
                  data_class="synthetic", partition="development")
    (ROOT / f"{name}.source.json").write_text(json.dumps(source, indent=2)+"\n")


if __name__ == "__main__":
    ROOT.mkdir(parents=True, exist_ok=True)
    write_case("roundtrip", "2")
    write_case("partial", "1")
