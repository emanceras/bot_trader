"""Version preserved scientific text; do not reinterpret evidence as validation."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from pydantic import JsonValue

from bot_trader.core.contracts import Principal
from bot_trader.core.errors import Conflict
from bot_trader.core.security import Policy
from bot_trader.persistence import DocumentRecord, Repository


class HypothesisService:
    def __init__(self, repo: Repository, policy: Policy) -> None:
        self.repo = repo
        self.policy = policy

    def import_file(self, path: Path, principal: Principal) -> list[DocumentRecord]:
        self.policy.require(principal, "sessions.manage")
        raw = path.read_bytes()
        if len(raw) > 1_000_000:
            raise Conflict("Hypothesis source exceeds the import bound.")
        source = raw.decode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        sections: list[tuple[str, str]] = []
        for heading in re.finditer(r"(?m)^## (.+)\n", source):
            start = heading.start()
            following = re.search(r"(?m)^## ", source[heading.end() :])
            end = heading.end() + following.start() if following else len(source)
            sections.append((heading.group(1), source[start:end]))
        found: dict[str, dict[str, JsonValue]] = {}
        for section_title, section in sections:
            for line in section.splitlines():
                match = re.match(r"\| (H-\d{2})(?:\s+\||;)", line)
                null_match = re.match(r"\*\*(H-00):\*\*", line)
                selected = match if match is not None else null_match
                if selected is None:
                    continue
                cells = [cell.strip() for cell in line.split("|")[1:-1]] if match else []
                # Bibliographic follow-up tables repeat IDs but are not definitions.
                if match is not None and len(cells) != 5:
                    continue
                identifier = selected[1]
                if identifier in found:
                    raise Conflict("Duplicate scientific hypothesis definition.")
                found[identifier] = {
                    "id": identifier,
                    "language": "es",
                    "status": "proposed_not_validated",
                    "source_path": "HYPOTHESES.md",
                    "source_sha256": digest,
                    "source_section": section_title,
                    "source_excerpt": section,
                    "verbatim": line,
                    "statement": cells[1] if len(cells) > 1 else line,
                    "null_and_comparator": cells[2] if len(cells) > 2 else None,
                    "refutation": cells[3] if len(cells) > 3 else None,
                    "required_data": cells[4] if len(cells) > 4 else None,
                    "financial_validation": False,
                }
        if set(found) != {f"H-{number:02d}" for number in range(25)}:
            raise Conflict("Import requires exactly the original H-00 through H-24 definitions.")
        records = [self.repo.put("hypothesis", key, found[key]) for key in sorted(found)]
        self.repo.append_audit(
            principal.id,
            "hypotheses.import",
            "HYPOTHESES.md",
            "succeeded",
            {"source_sha256": digest, "count": len(records)},
        )
        return records

    def list(self, principal: Principal) -> list[DocumentRecord]:
        self.policy.require(principal, "hypotheses.read")
        return self.repo.list("hypothesis")

    def get(self, id: str, principal: Principal, version: int | None = None) -> DocumentRecord:
        self.policy.require(principal, "hypotheses.read")
        return self.repo.get("hypothesis", id, version)
