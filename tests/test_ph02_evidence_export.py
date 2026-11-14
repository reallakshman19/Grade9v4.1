"""The 30 PH02 task author-prepackets must be actually generated and hash-grounded."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "review-artifacts/physics-ph02/task-evidence-prep"


def test_ph02_30_task_evidence_export_all_hashes_and_lines():
    result = subprocess.run(
        [sys.executable, "tools/physics_ph02_task_evidence_prep.py"],
        cwd=ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    report = json.loads(result.stdout)
    assert report["prepared_task_packets"] == 30
    assert report["disposition"] == "PREP_ONLY_ACADEMIC_HOLD"
    index = json.loads((OUT / "INDEX.json").read_text(encoding="utf-8"))
    assert index["count"] == 30
    assert len(index["items"]) == 30
    assert len({x["uid"] for x in index["items"]}) == 30
    for item in index["items"]:
        packet = json.loads((OUT / (item["uid"] + ".prepacket.json")).read_text(encoding="utf-8"))
        assert packet["academic_status"] == "HOLD"
        assert packet["owner_golden_sha"] is None
        assert packet["r01_receipt"] is None
        assert len(packet["evidence"]) >= 7
        for witness in packet["evidence"]:
            source = ROOT / witness["path"]
            assert source.is_file()
            assert hashlib.sha256(source.read_bytes()).hexdigest() == witness["sha256"]
            lines = source.read_text(encoding="utf-8").splitlines()
            assert witness["excerpt"] == lines[witness["start_line"] - 1].strip()
