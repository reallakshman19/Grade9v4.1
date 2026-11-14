"""PH01 R4.x historical source-custody adapter.

Never rewrite a current source bank to match an older review pin. Current and
historical source revisions coexist; the historical public-candidate snapshot
is exclusively for reproducible older PH01 review evidence. No academic
admission is inferred.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

HISTORICAL_BLOBS = {
    "nsejs/data/physics-core2-candidates.v1.json": (
        "81628a45bfa20133fc0d219db138602fa45dd083",
        "review/physics/ph01-historical-source/physics-core2-candidates-r41.json",
    ),
    "nsejs/data/physics-core2-integrity.v1.json": (
        "5e40fba433c0d31491688f0af4e4464ccabf2316",
        "review/physics/ph01-historical-source/physics-core2-integrity-r41.json",
    ),
}

def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def pinned_bytes(root: Path, pin: dict) -> bytes:
    path = pin["path"]
    sha = pin.get("git_blob_sha", pin.get("blob"))
    if not isinstance(sha, str) or len(sha) != 40:
        raise AssertionError("invalid source pin")
    current = (root / path).read_bytes()
    if blob_sha(current) == sha:
        return current
    old = HISTORICAL_BLOBS.get(path)
    if old is None or old[0] != sha:
        raise AssertionError(f"unexplained current source drift: {path}")
    historic = (root / old[1]).read_bytes()
    if blob_sha(historic) != sha:
        raise AssertionError(f"historical source custody drift: {old[1]}")
    return historic

def pinned_blob_sha(root: Path, pin: dict) -> str:
    return blob_sha(pinned_bytes(root, pin))

def pinned_json(root: Path, pin: dict):
    return json.loads(pinned_bytes(root, pin).decode("utf-8"))
