"""B02 native PH09/PH10 subtopic route integrity and honest author status.

This suite is static, not scientific/QRT or browser acceptance. HTTP Chromium
is exercised by the companion workflow.
"""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]/"nsejs"/"physics"/"curriculum"/"topics"
def test_29_dedicated_native_candidate_routes_and_no_stale_unautored_labels():
    units={"PH09":12,"PH10":17}
    for unit,count in units.items():
        base=ROOT/unit/"subtopics"
        idx=(base/"index.html").read_text(encoding="utf-8")
        assert "NATIVE_SUBTOPIC_NOT_AUTHORED" not in idx,unit
        pairs=re.findall(r'href="('+unit+r'-\d{2})/core1a\.html"',idx)
        assert len(pairs)==count and len(set(pairs))==count,(unit,pairs)
        for ident in pairs:
            path=base/ident
            a=path/"core1a.html"
            b=path/"core1b.html"
            pkg=path/"core1b-candidate.v1.json"
            assert a.is_file() and b.is_file() and pkg.is_file(),ident
            assert "Core1B" in b.read_text(encoding="utf-8")
            assert "ACADEMIC HOLD" in b.read_text(encoding="utf-8")
            assert "core1b-runtime.js" in b.read_text(encoding="utf-8")
