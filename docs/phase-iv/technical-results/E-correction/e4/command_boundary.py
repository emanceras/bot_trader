"""Minimal offline command/fill identity boundary; no native fill injection."""
from copy import deepcopy
import hashlib
import json


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


class CommandBoundary:
    def __init__(self, account_id, persist=None):
        self.account_id = account_id
        self.entries = {}
        self.events = []
        self.persist = persist

    def _save(self, cid, action):
        event = {"sequence": len(self.events)+1, "account_id": self.account_id,
                 "command_id": cid, "action": action, "entry": deepcopy(self.entries[cid])}
        if self.persist:
            self.persist(event)  # Durable pending identity precedes native submission.
        self.events.append(event)

    def begin(self, command):
        cid = command["command_id"]
        signature = digest(command)
        if cid in self.entries:
            if self.entries[cid]["signature"] != signature:
                raise ValueError("Same command identity with conflicting payload; block")
            self._save(cid, "duplicate_suppressed")
            return False, deepcopy(self.entries[cid])
        self.entries[cid] = {"signature": signature, "command": deepcopy(command),
            "dispatch_state": "PENDING", "native_order": None, "native_events": []}
        self._save(cid, "admitted_pending")
        return True, deepcopy(self.entries[cid])

    def dispatched(self, cid, error=None):
        self.entries[cid]["dispatch_state"] = "DISPATCH_ERROR_UNKNOWN" if error else "DISPATCHED"
        if error:
            self.entries[cid]["dispatch_error"] = error
        self._save(cid, "dispatch_error" if error else "dispatched")

    def native_event(self, row):
        cid = row.get("client_order_id")
        if cid in self.entries:
            self.entries[cid]["native_events"].append(deepcopy(row))
            self._save(cid, "native_event_observed")

    def observe(self, orders):
        by_id = {o["id"]: o for o in orders}
        for cid, entry in self.entries.items():
            target = entry["command"].get("target", cid)
            if target in by_id:
                entry["native_order"] = deepcopy(by_id[target])
                self._save(cid, "native_cache_observed")

    @classmethod
    def reconstruct(cls, events):
        if not events:
            raise ValueError("Empty journal has no account identity")
        result = cls(events[0]["account_id"])
        for expected, event in enumerate(events, 1):
            if event["sequence"] != expected or event["account_id"] != result.account_id:
                raise ValueError("Journal continuity/account mismatch")
            entry, cid = event["entry"], event["command_id"]
            if entry["signature"] != digest(entry["command"]) or entry["command"]["command_id"] != cid:
                raise ValueError("Corrupt identity or payload")
            if cid in result.entries and result.entries[cid]["signature"] != entry["signature"]:
                raise ValueError("Historical command payload changed")
            result.entries[cid] = deepcopy(entry)
            result.events.append(deepcopy(event))
        return result


class FillBoundary:
    def __init__(self):
        self.fills = {}

    def accept(self, fill):
        identity = (fill["venue"], fill["fill_id"])
        if identity in self.fills:
            if self.fills[identity] != fill:
                raise ValueError("Conflicting content for known native fill identity")
            return False
        self.fills[identity] = deepcopy(fill)
        return True
