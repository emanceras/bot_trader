"""Author the fixed invented R assertions without importing the tested transition.

The explicit expected deltas, reasons, UTC strings and arithmetic below are the
oracle. This preparation utility only expands them into full per-event states.
It neither runs the probe nor derives expectations from observed output.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path


class Journal:
    def __init__(self, identifier: str, purpose: str):
        self.value = {"id": identifier, "purpose": purpose, "events": [], "expected": []}
        self.state = {"eligible_ids": [], "values": {}, "latest_complete_bar": None,
                      "valid": True, "last_sequence": None}

    def add(self, identifier, op, event_ns, receive, data=None, *, available="event",
            reason="accepted", accepted=True, changes=None, delete=(), latest="keep",
            valid=None, sequence="keep", source="fixture", instrument="SYN-USD",
            tick=None, unit="ns", revision=None):
        event = {"id": identifier, "source_id": source, "instrument_id": instrument,
                 "event_ns": event_ns, "event_tick": event_ns if tick is None else tick,
                 "time_unit": unit, "available_ns": event_ns if available == "event" else available,
                 "receive_ns": receive, "receive_ordinal": len(self.value["events"]),
                 "op": op, "data": data or {}}
        if revision is not None:
            event["revision_of"] = revision
        self.value["events"].append(event)
        if accepted:
            self.state["eligible_ids"].append(identifier)
        self.state["values"].update(copy.deepcopy(changes or {}))
        for key in delete:
            self.state["values"].pop(key, None)
        if latest != "keep":
            self.state["latest_complete_bar"] = latest
        if valid is not None:
            self.state["valid"] = valid
        if sequence != "keep":
            self.state["last_sequence"] = sequence
        observable_reasons = {"accepted", "duplicate", "checkpoint", "joined", "warm"}
        decision = "OBSERVE" if reason in observable_reasons and self.state["valid"] else "BLOCK"
        self.value["expected"].append({"event_ns": event_ns, "decision": decision,
                                       "reason": reason, "state": copy.deepcopy(self.state)})


def build():
    r1 = Journal("R1", "Effective time is not availability; equality and unknown receipt are explicit.")
    r1.add("scheduled", "set", 1000, 10, {"key": "scheduled", "value": "announced"}, available=5, changes={"scheduled": "announced"})
    r1.add("delayed", "set", 2, 20, {"key": "release", "value": "initial"}, available=30, accepted=False, reason="not_yet_available")
    r1.add("unknown", "set", 3, 25, {"key": "unknown", "value": "must not enter"}, available=None, accepted=False, reason="unknown_availability")
    r1.add("delayed", "set", 2, 30, {"key": "release", "value": "initial"}, available=30, changes={"release": "initial"})
    r1.add("equal", "set", 30, 30, {"key": "equal_cutoff", "value": "eligible"}, changes={"equal_cutoff": "eligible"})
    r1.add("earlier_event", "set", 1, 40, {"key": "late", "value": "now only"}, available=35, changes={"late": "now only"})

    r2 = Journal("R2", "Submicrosecond order, declared units, true duplicates and namespaced identities.")
    r2.add("ns1", "clock", 1_000_000_001, 2_000_000_000, {"key": "fine1"}, changes={"fine1": 1_000_000_001})
    r2.add("ns2", "clock", 1_000_000_002, 2_000_000_001, {"key": "fine2"}, changes={"fine2": 1_000_000_002})
    r2.add("micro", "clock", 1_000_001_000, 2_000_000_002, {"key": "us"}, tick=1_000_001, unit="us", changes={"us": 1_000_001_000})
    r2.add("milli", "clock", 1_001_000_000, 2_000_000_003, {"key": "ms"}, tick=1001, unit="ms", changes={"ms": 1_001_000_000})
    r2.add("ns1", "clock", 1_000_000_001, 2_000_000_004, {"key": "fine1"}, reason="duplicate", accepted=False)
    r2.add("equal-value-new-id", "clock", 1_000_000_001, 2_000_000_005, {"key": "equal"}, changes={"equal": 1_000_000_001})
    r2.add("ns1", "clock", 1_000_000_001, 2_000_000_006, {"key": "other_source"}, source="other", changes={"other_source": 1_000_000_001})
    r2.add("mismatch", "clock", 1000, 2_000_000_007, {"key": "wrong"}, tick=1, unit="ms", reason="time_unit_mismatch", accepted=False)
    r2.value["expected"][-1]["event_ns"] = 1_000_000

    b10 = {"open":"10","high":"10","low":"10","close":"10","quantity":"1","amount":"10","count":1}
    b0 = {"open":"10","high":"12","low":"10","close":"12","quantity":"3","amount":"34","count":2}
    b19 = {"open":"9","high":"9","low":"9","close":"9","quantity":"3","amount":"27","count":1}
    b1 = {"open":"9","high":"11","low":"9","close":"11","quantity":"4","amount":"38","count":2}
    coarse = {"open":"10","high":"12","low":"9","close":"11","quantity":"7","amount":"72","count":4}
    corrected = {"open":"10","high":"10","low":"8","close":"8","quantity":"3","amount":"26","count":2}
    r3 = Journal("R3", "Open bars, half-open boundary, exact notional, compatible coarse aggregation and later correction.")
    r3.add("open0", "open_bar", 0, 1, {"bar_id":"b0-open"}, changes={"provisional_bar":"b0-open"})
    r3.add("t0", "trade", 10, 10, {"price":"10","quantity":"1","width_ns":100}, changes={"bin:0":b10})
    r3.add("t1", "trade", 60, 60, {"price":"12","quantity":"2","width_ns":100}, changes={"bin:0":b0})
    r3.add("open1", "open_bar", 70, 70, {"bar_id":"b0-open-v2"}, changes={"provisional_bar":"b0-open-v2"})
    r3.add("close0", "close_bar", 100, 105, {"bar_id":"b0","start_ns":0,"end_ns":100}, available=105, changes={"bar:b0":b0}, delete=("provisional_bar",), latest="b0")
    r3.add("t2", "trade", 100, 110, {"price":"9","quantity":"3","width_ns":100}, available=110, changes={"bin:100":b19})
    r3.add("t3", "trade", 160, 160, {"price":"11","quantity":"1","width_ns":100}, changes={"bin:100":b1})
    r3.add("close1", "close_bar", 200, 205, {"bar_id":"b1","start_ns":100,"end_ns":200}, available=205, changes={"bar:b1":b1}, latest="b1")
    r3.add("coarse", "coarse", 210, 210, {"bar_id":"c0","parents":["b0","b1"],"start_ns":0,"end_ns":200,"anchor_ns":0}, changes={"coarse:c0":{"direct":coarse,"from_fine":coarse}})
    r3.add("misaligned", "coarse", 220, 220, {"bar_id":"wrong","parents":["b0","b1"],"start_ns":0,"end_ns":200,"anchor_ns":50}, reason="misaligned_aggregation", accepted=False)
    r3.add("correct0", "correct_bar", 60, 240, {"trade_id":"t1","price":"8","bar_id":"b0-r1","start_ns":0,"end_ns":100}, available=240, revision="close0", changes={"bin:0":corrected,"bar:b0-r1":corrected}, latest="b0-r1")

    r4 = Journal("R4", "A sequence gap blocks decisions until a valid later snapshot; recovery never backdates.")
    r4.add("book1","book",10,10,{"sequence":1,"value":"A"},sequence=1,changes={"book":"A"})
    r4.add("book2","book",20,20,{"sequence":2,"value":"B"},sequence=2,changes={"book":"B"})
    r4.add("gap4","book",40,40,{"sequence":4,"value":"D"},accepted=False,reason="sequence_gap",valid=False)
    r4.add("book2","book",20,50,{"sequence":2,"value":"B"},accepted=False,reason="duplicate")
    r4.add("future_snapshot","snapshot",60,60,{"sequence":10,"value":"future"},available=200,accepted=False,reason="not_yet_available")
    r4.add("while_invalid","book",70,70,{"sequence":3,"value":"C"},accepted=False,reason="invalid_book")
    r4.add("snapshot10","snapshot",80,80,{"sequence":10,"value":"J"},sequence=10,valid=True,changes={"book":"J"})
    r4.add("book11","book",90,90,{"sequence":11,"value":"K"},sequence=11,changes={"book":"K"})
    r4.add("stale","book",80,100,{"sequence":10,"value":"old"},available=100,accepted=False,reason="stale_sequence")

    r5 = Journal("R5", "Pinned zone DST ambiguity/gap; invented early close and overnight trading date.")
    r5.add("ambiguous","calendar",1,1,{"local":"2024-11-03T01:30:00","key":"fold"},accepted=False,reason="ambiguous_local_time")
    r5.add("fold0","calendar",2,2,{"local":"2024-11-03T01:30:00","fold":0,"key":"fold0"},changes={"fold0":"2024-11-03T05:30:00+00:00"})
    r5.add("fold1","calendar",3,3,{"local":"2024-11-03T01:30:00","fold":1,"key":"fold1"},changes={"fold1":"2024-11-03T06:30:00+00:00"})
    r5.add("spring_gap","calendar",4,4,{"local":"2024-03-10T02:30:00","key":"gap"},accepted=False,reason="nonexistent_local_time")
    r5.add("post_gap","calendar",5,5,{"local":"2024-03-10T03:30:00","key":"post_gap"},changes={"post_gap":"2024-03-10T07:30:00+00:00"})
    r5.add("before_early_close","calendar",6,6,{"local":"2024-07-03T12:59:00","open_local":"2024-07-03T09:30:00","close_local":"2024-07-03T13:00:00","trading_date":"2024-07-03","key":"early"},changes={"trading_date":"2024-07-03","early":"2024-07-03T16:59:00+00:00"})
    r5.add("at_early_close","calendar",7,7,{"local":"2024-07-03T13:00:00","open_local":"2024-07-03T09:30:00","close_local":"2024-07-03T13:00:00","trading_date":"2024-07-03","key":"closed"},accepted=False,reason="session_closed")
    r5.add("overnight_open","calendar",8,8,{"local":"2024-01-02T18:30:00","open_local":"2024-01-02T18:00:00","close_local":"2024-01-03T17:00:00","trading_date":"2024-01-03","key":"overnight_open"},changes={"trading_date":"2024-01-03","overnight_open":"2024-01-02T23:30:00+00:00"})
    r5.add("overnight_after_midnight","calendar",9,9,{"local":"2024-01-03T00:30:00","open_local":"2024-01-02T18:00:00","close_local":"2024-01-03T17:00:00","trading_date":"2024-01-03","key":"overnight_after_midnight"},changes={"overnight_after_midnight":"2024-01-03T05:30:00+00:00"})

    r6 = Journal("R6", "Availability-as-of cross-instrument conversion; missing/stale USDT conversion cannot equal USD.")
    r6.add("a","set",10,10,{"key":"A_USD","value":"100"},instrument="A-USD",changes={"A_USD":"100"})
    r6.add("b","set",20,20,{"key":"B_USDT","value":"25"},instrument="B-USDT",changes={"B_USDT":"25"})
    r6.add("missing","join",30,30,{"max_age_ns":20},accepted=False,reason="conversion_missing")
    r6.add("fx1","fx",30,40,{"rate":"0.98"},available=70,accepted=False,reason="not_yet_available")
    r6.add("fx1","fx",30,70,{"rate":"0.98"},available=70,changes={"USDT_USD":"0.98"})
    r6.add("joined","join",75,75,{"max_age_ns":20},accepted=False,reason="joined",changes={"B_USD":"24.5"})
    r6.add("stale","join",95,95,{"max_age_ns":20},accepted=False,reason="stale_conversion")
    r6.add("fx2","fx",80,100,{"rate":"1.01"},available=100,revision="fx1",changes={"USDT_USD":"1.01"})
    r6.add("joined2","join",105,105,{"max_age_ns":20},accepted=False,reason="joined",changes={"B_USD":"25.25"})

    r7 = Journal("R7", "Warm-up, delayed external first release, revisions and explicitly labelled corrected-history view.")
    r7.add("cold","warmup",1,1,{"minimum":2},accepted=False,reason="insufficient_warmup")
    r7.add("p1","set",10,10,{"key":"p:1","value":"100"},changes={"p:1":"100"})
    r7.add("publication","set",5,20,{"key":"news","value":"first version"},available=40,accepted=False,reason="not_yet_available")
    r7.add("p2","set",30,30,{"key":"p:2","value":"110"},changes={"p:2":"110"})
    r7.add("warm","warmup",35,35,{"minimum":2},accepted=False,reason="warm")
    r7.add("publication","set",5,40,{"key":"news","value":"first version"},available=40,changes={"news":"first version"})
    r7.add("correction","set",10,50,{"key":"p:1","value":"90"},available=50,revision="p1",changes={"p:1":"90"})
    r7.add("backfill","set",2,70,{"key":"p:0","value":"95"},available=70,changes={"p:0":"95"})
    r7.add("revised_publication","set",5,80,{"key":"news","value":"revised version"},available=80,revision="publication",changes={"news":"revised version"})
    r7.add("label_corrected_view","set",90,90,{"key":"history_view","value":"corrected after receipt, not original decision history"},changes={"history_view":"corrected after receipt, not original decision history"})

    r8 = Journal("R8", "Transformation snapshot continuity, duplicate delivery and maker/taker native mapping.")
    r8.add("kraken1","native_side",10,10,{"side":"buy","role":"taker","key":"aggressor_K"},source="invented_kraken_semantics",changes={"aggressor_K":"buy"})
    r8.add("coinbase1","native_side",20,20,{"side":"buy","role":"maker","key":"aggressor_C"},source="invented_coinbase_semantics",changes={"aggressor_C":"sell"})
    r8.add("checkpoint","checkpoint",30,30,accepted=False,reason="checkpoint")
    r8.add("kraken1","native_side",10,40,{"side":"buy","role":"taker","key":"aggressor_K"},source="invented_kraken_semantics",accepted=False,reason="duplicate")
    r8.add("kraken2","native_side",50,50,{"side":"buy","role":"taker","key":"aggressor_K2"},source="invented_kraken_semantics",changes={"aggressor_K2":"buy"})
    r8.add("continued","set",60,60,{"key":"continuation","value":"same state"},changes={"continuation":"same state"})
    r8.add("unsupported","native_side",70,70,{"side":"unknown","role":"maker","key":"wrong"},accepted=False,reason="unsupported_side")
    return {"schema":"bot-trader.synthetic-temporal-journals.v1", "synthetic":True,
            "oracle_provenance":"Manually specified deltas, Decimal arithmetic and UTC strings; no probe imports or observed outputs used.",
            "journals":[x.value for x in (r1,r2,r3,r4,r5,r6,r7,r8)]}


if __name__ == "__main__":
    destination = Path(__file__).with_name("temporal_journals.json")
    if destination.exists():
        raise SystemExit("fixture already exists; do not overwrite frozen inputs")
    destination.write_text(json.dumps(build(), indent=2, ensure_ascii=False)+"\n")
