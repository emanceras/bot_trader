"""Verify published history byte prefixes; an amendment records, never grants, authority."""

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

PROTECTED = ("DECISIONS.md", "EXPERIMENTS.md")


def verify_published_prefix(
    repository: Path, baseline_commit: str, amendments: list[dict[str, str]] | None = None
) -> dict[str, object]:
    """The caller supplies the pinned latest published commit, not a mutable branch."""
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", baseline_commit):
        raise ValueError("Use a full immutable published commit ID, not a branch or abbreviation.")
    resolved = subprocess.check_output(
        ["git", "rev-parse", "--verify", baseline_commit + "^{commit}"],
        cwd=repository, text=True,
    ).strip()
    if resolved != baseline_commit:
        raise ValueError("Baseline must identify the commit itself.")
    exceptions = {}
    for amendment in amendments or []:
        required = {
            "file", "baseline_commit", "previous_sha256", "replacement_sha256",
            "amendment_id", "reason", "authority_reference",
        }
        if set(amendment) != required or any(
            not isinstance(value, str) or not value.strip() for value in amendment.values()
        ):
            raise ValueError("An amendment must explicitly bind both hashes and state its authority.")
        name = amendment["file"]
        if name not in PROTECTED or name in exceptions:
            raise ValueError("Amendment file is unprotected or repeated.")
        exceptions[name] = amendment
    results = []
    for name in PROTECTED:
        previous = subprocess.check_output(
            ["git", "show", f"{baseline_commit}:{name}"], cwd=repository,
        )
        path = repository / name
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"Protected history must be a regular file: {name}")
        current = path.read_bytes()
        old_hash = hashlib.sha256(previous).hexdigest()
        new_hash = hashlib.sha256(current).hexdigest()
        prefix = current.startswith(previous)
        amendment = exceptions.pop(name, None)
        if prefix and amendment:
            raise ValueError(f"Unused amendment for unchanged published prefix: {name}")
        if not prefix:
            if amendment is None:
                raise ValueError(f"Published history was replaced or truncated: {name}")
            if (
                amendment["baseline_commit"] != baseline_commit
                or amendment["previous_sha256"] != old_hash
                or amendment["replacement_sha256"] != new_hash
            ):
                raise ValueError(f"Amendment does not match the exact original and replacement: {name}")
        results.append({
            "file": name, "published_bytes": len(previous), "current_bytes": len(current),
            "previous_sha256": old_hash, "current_sha256": new_hash,
            "prefix_preserved": prefix, "explicit_amendment": amendment,
        })
    return {
        "baseline_commit": baseline_commit, "files": results, "accepted": True,
        "limit": "Checks content and declared amendment identity, not authenticity of authority.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--baseline-commit", required=True)
    parser.add_argument("--amendments", type=Path)
    args = parser.parse_args()
    amendments = json.loads(args.amendments.read_text()) if args.amendments else None
    if amendments is not None and not isinstance(amendments, list):
        raise ValueError("Amendment document must contain a JSON list.")
    print(json.dumps(verify_published_prefix(args.repository, args.baseline_commit, amendments)))


if __name__ == "__main__":
    main()
