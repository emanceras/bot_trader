"""Export small E recovery evidence; omit binaries and signed redirect queries."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit, urlunsplit


def sha(data):
    return hashlib.sha256(data).hexdigest()


def clean(text):
    # Public software redirects can carry ephemeral bearer-like query tokens.
    # Preserve stable URL path; record original and exported hashes separately.
    def url(match):
        raw = match.group(0)
        parsed = urlsplit(raw)
        return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", "")) if parsed.query else raw
    return re.sub(r'https?://[^\s"<>]+', url, text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.scratch
    out = args.output
    out.mkdir(parents=True, exist_ok=False)
    manifest = []
    omitted = []

    def write(source, target, data=None):
        original = source.read_bytes() if data is None else data
        exported = clean(original.decode()).encode()
        dest = out / target
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("xb") as stream:
            stream.write(exported)
        manifest.append({"path": str(target), "source_sha256": sha(original),
                         "published_sha256": sha(exported), "bytes": len(exported),
                         "signed_or_other_URL_query_removed": original != exported})

    selected = [root / "setup-pin.json"]
    for directory in ("frozen", "corrected", "diagnostic", "observations", "evaluations", "research-restoration"):
        selected.extend(p for p in (root / directory).rglob("*") if p.is_file() and p.suffix in (".json", ".jsonl", ".py", ".log"))
    for source in sorted(selected):
        if source.name == "same-source-engine-cases.json":
            omitted.append({"path": str(source.relative_to(root)), "sha256": sha(source.read_bytes()),
                            "reason": "Exact original bundle includes unused E6 workload; reproduce from preserved engine_fixtures.py and temporal journal, not another large copy"})
            continue
        if source.stat().st_size > 2_000_000:
            raise ValueError("Unexpected large recovery evidence: " + str(source))
        write(source, source.relative_to(root))
    for source in sorted(root.parent.glob("recovery*.log")):
        write(source, Path("logs") / source.name)
    for name in ("runs.jsonl", "downloads.jsonl"):
        source = root.parent / name
        selected_rows = [line for line in source.read_text().splitlines() if "recovery" in line]
        write(source, Path(name), ("\n".join(selected_rows) + "\n").encode())
    result = {"scope": "D-048 recovery only; previous receipts remain untouched",
              "url_redaction": "Queries removed from public software redirect URLs; original scratch records preserved, not published with ephemeral signed parameters",
              "entries": manifest, "omitted_reconstructible_sources": omitted}
    (out / "publication-manifest.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"files": len(manifest), "bytes": sum(r["bytes"] for r in manifest),
                      "redacted_files": [r["path"] for r in manifest if r["signed_or_other_URL_query_removed"]]}))


if __name__ == "__main__":
    main()
