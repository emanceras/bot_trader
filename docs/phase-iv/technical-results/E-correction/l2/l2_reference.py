"""Causal reference quote from one unchanged L2 snapshot; no extra depth."""
from decimal import Decimal
import hashlib
import json


def derive(snapshot):
    if snapshot["kind"] != "book_snapshot":
        raise ValueError("Only original complete snapshots are supported")
    for field in ("event_ns", "available_ns"):
        if type(snapshot[field]) is not int or snapshot[field] < 0:
            raise ValueError("Timestamp must be an exact nonnegative integer")
    bids, asks = snapshot["bids"], snapshot["asks"]
    if not bids or not asks:
        raise ValueError("Both sides required; no synthetic fallback price")
    for side in (bids, asks):
        if len({Decimal(p) for p, _ in side}) != len(side):
            raise ValueError("Duplicate snapshot levels are not normalized here")
        if any(not Decimal(v).is_finite() or Decimal(v) <= 0 for level in side for v in level):
            raise ValueError("Nonpositive/nonfinite source level")
    bid, bid_size = max(bids, key=lambda v: Decimal(v[0]))
    ask, ask_size = min(asks, key=lambda v: Decimal(v[0]))
    if Decimal(bid) >= Decimal(ask):
        raise ValueError("Crossed source book is not silently repaired")
    return {
        "event_id": snapshot["event_id"] + ":derived-reference",
        "source_event_id": snapshot["event_id"],
        "source_sha256": hashlib.sha256(json.dumps(snapshot, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "event_ns": snapshot["event_ns"], "available_ns": snapshot["available_ns"],
        "receive_ordinal": snapshot["receive_ordinal"],
        "bid": bid, "ask": ask, "bid_size": bid_size, "ask_size": ask_size,
        "origin": "supervisor derives top-of-book from the same original snapshot; not an independent liquidity refresh",
    }
