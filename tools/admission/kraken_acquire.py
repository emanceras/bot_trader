"""Acquire only the two D-040-authorized QA objects after a recorded rights check.

No credentials, market API, strategy calculation, extraction or application import.
Large bodies and transport logs must remain outside the repository.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import time
from datetime import datetime, timezone
from urllib.request import Request, urlopen


OBJECTS = (
    ("Kraken_OHLCVT_2026Q3.zip", 576348633, '"caa4a859d2f1c2b3740006d3dadf80ea-69"'),
    ("Kraken_Trades_2026Q3.zip", 1596570274, '"a6f2034bf0c0ee9f5adc580e35ec460e-191"'),
)
BASE_URL = "https://assets.kraken.com/marketing/institutions/"
CHUNK = 1024 * 1024
HTTP_HEADERS = {"User-Agent": "Mozilla/5.0", "Accept-Encoding": "identity"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def append(path: Path, item: dict) -> None:
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(item, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def checked_headers(response, url: str, size: int, etag: str) -> dict:
    headers = {key: response.headers.get(key) for key in (
        "Content-Type", "Content-Length", "Last-Modified", "ETag", "Content-Encoding"
    )}
    if response.status != 200 or response.url != url:
        raise ValueError("Unexpected HTTP status or redirect; no additional source admitted")
    if int(headers["Content-Length"] or -1) != size:
        raise ValueError("Object size changed from the approved manifest")
    if headers["ETag"] != etag:
        raise ValueError("Object identity changed from the reviewed manifest")
    if headers["Content-Type"] not in ("application/zip", "application/octet-stream"):
        raise ValueError("Unexpected object media type")
    if headers["Content-Encoding"] not in (None, "identity"):
        raise ValueError("Unexpected HTTP content encoding")
    return headers


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--rights-record", type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    output = args.output.resolve()
    if output == repo or repo in output.parents:
        raise ValueError("Archive storage must be outside the repository")
    rights = json.loads(args.rights_record.read_text())
    if rights.get("disposition") != "proceed_narrow_private_qa" or rights.get("authority") != "D-040":
        raise ValueError("A documented scoped rights/authority assessment is required")
    output.mkdir(parents=True, exist_ok=True)
    journal = output / "acquisition.jsonl"
    start, cpu = time.monotonic(), time.process_time()
    append(journal, {"event": "start", "at": now(), "authority": "D-040",
                     "rights_sha256": hashlib.sha256(args.rights_record.read_bytes()).hexdigest(),
                     "request_headers": HTTP_HEADERS,
                     "compressed_byte_ceiling": sum(x[1] for x in OBJECTS),
                     "free_bytes_before": shutil.disk_usage(output).free})
    # Neither filename nor URL can be supplied by a remote source or command argument.
    try:
        for name, size, etag in OBJECTS:
            url = BASE_URL + name
            dest, partial = output / name, output / (name + ".part")
            if dest.exists() or partial.exists():
                raise ValueError("Existing artifact: inspect provenance before an explicit retry")
            with urlopen(Request(url, headers=HTTP_HEADERS, method="HEAD"), timeout=30) as response:
                headers = checked_headers(response, url, size, etag)
            append(journal, {"event": "preflight", "at": now(), "url": url,
                             "headers": headers, "body_bytes_read": 0})
            if shutil.disk_usage(output).free <= size:
                raise ValueError("Insufficient free local storage for the approved object")
            digest, count = hashlib.sha256(), 0
            obj_start = time.monotonic()
            with urlopen(Request(url, headers=HTTP_HEADERS), timeout=60) as response:
                checked_headers(response, url, size, etag)
                with partial.open("xb") as stream:
                    while block := response.read(min(CHUNK, size - count + 1)):
                        count += len(block)
                        if count > size:
                            raise ValueError("Response exceeds approved size; stopped")
                        if count == len(block) and not block.startswith(b"PK\x03\x04"):
                            raise ValueError("Response is not the expected ZIP signature")
                        stream.write(block)
                        digest.update(block)
                    stream.flush()
                    os.fsync(stream.fileno())
            if count != size:
                raise ValueError("Incomplete body; partial artifact retained for diagnosis")
            partial.rename(dest)
            result = {"event": "acquired", "at": now(), "url": url, "path": str(dest),
                      "bytes": count, "sha256": digest.hexdigest(), "headers": headers,
                      "wall_seconds": time.monotonic() - obj_start,
                      "hash_limit": "Local content identity, not independent provider checksum"}
            append(journal, result)
            print(json.dumps(result), flush=True)
    except Exception as error:
        append(journal, {"event": "failure", "at": now(), "type": type(error).__name__,
                         "message": str(error), "wall_seconds": time.monotonic() - start})
        raise
    append(journal, {"event": "complete", "at": now(), "wall_seconds": time.monotonic() - start,
                     "cpu_seconds": time.process_time() - cpu,
                     "peak_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                     "free_bytes_after": shutil.disk_usage(output).free})


if __name__ == "__main__":
    main()
