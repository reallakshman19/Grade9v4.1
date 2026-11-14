"""No silent source rewriting or arbitrary-hash pin fallback for PH01 R4.x."""
import hashlib
import json
import pytest
from pathlib import Path
from tools.ph01_source_pin_custody import HISTORICAL_BLOBS,blob_sha,pinned_bytes,pinned_json

ROOT=Path(__file__).resolve().parents[1]
def test_historical_source_archives_preserve_original_git_blobs_and_current_data():
    for live,(old_sha,archive) in HISTORICAL_BLOBS.items():
        old=(ROOT/archive).read_bytes()
        current=(ROOT/live).read_bytes()
        assert blob_sha(old)==old_sha
        assert blob_sha(current)!=old_sha
        assert pinned_bytes(ROOT,{"path":live,"git_blob_sha":old_sha})==old
        assert pinned_bytes(ROOT,{"path":live,"git_blob_sha":blob_sha(current)})==current
        with pytest.raises(AssertionError):
            pinned_bytes(ROOT,{"path":live,"git_blob_sha":"0"*40})
    integrity=json.loads((ROOT/"nsejs/data/physics-core2-integrity.v1.json").read_text())
    assert integrity["academic_admission"]=="HOLD"
    historic=pinned_json(ROOT,{"path":"nsejs/data/physics-core2-integrity.v1.json","git_blob_sha":HISTORICAL_BLOBS["nsejs/data/physics-core2-integrity.v1.json"][0]})
    assert len(historic["items"])==len(integrity["items"])==50
