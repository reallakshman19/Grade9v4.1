"""B01 subtopic-isolated candidates. Structural checks are not academic approval."""
from __future__ import annotations

import json
import runpy
from pathlib import Path
from html.parser import HTMLParser

import pytest

ROOT = Path(__file__).resolve().parents[1]
CURRICULUM = ROOT / "nsejs" / "physics" / "curriculum"
VALIDATOR = runpy.run_path(str(CURRICULUM / "contracts/tools/validate_physics_contracts.py"))["inspect_package"]
SLICES = ("PH07-01", "PH08-04")


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []
        self.iframes = 0

    def handle_starttag(self, tag, attrs):
        self.iframes += tag == "iframe"
        for key, val in attrs:
            if key in ("href", "src", "data-package") and val and not val.startswith(("http:", "https:", "#")):
                self.paths.append(val.split("#")[0])


@pytest.mark.parametrize("sid", SLICES)
def test_subtopic_contract_and_dedicated_pair(sid):
    folder = CURRICULUM / "topics" / sid.split("-")[0] / "b01" / sid
    package = folder / "physics-topic-package.v1.json"
    data = json.loads(package.read_text(encoding="utf-8"))
    result = VALIDATOR(package, ROOT)
    assert result["mechanical_status"] == "PASS", result["issues"]
    assert result["academic_status"] == result["release_status"] == "HOLD"
    assert [s["id"] for s in data["subtopics"]] == [sid]
    assert len(data["core1a"]) == 1
    targets = data["subtopics"][0]["qrt_targets"]
    assert len({q["primary_operation"] for q in targets}) == 3
    assert all(q["source_role"] == "AUTHORED_TRANSFER" for q in targets)
    assert not data["core2_sources"]
    assert len(data["core1b"]) == 6
    assert len({c["fresh_task"] for c in data["core1b"]}) == 6
    for c in data["core1b"]:
        assert c["stages"]["attempt"] == c["fresh_task"]
        assert c["protected_work"] not in c["stages"]["predict"]
        assert c["runtime_verification"] == "NOT_RUN"
        assert c["subtopic_id"] == sid
    for name in ("core1a.html", "core1b.html"):
        html = (folder / name).read_text(encoding="utf-8")
        assert sid in html and "ACADEMIC_HOLD" in html.replace("ACADEMIC HOLD", "ACADEMIC_HOLD")
        parser = Links()
        parser.feed(html)
        assert parser.iframes == 0
        for path in parser.paths:
            assert (folder / path).is_file(), (sid, name, path)
    assert '<svg' in (folder / "core1a.html").read_text(encoding="utf-8")


def test_author_arithmetic_regression():
    assert 100 * (56 - 8) / 80 == 60
    assert 100 * (35 - 20) / 50 == 30
    assert 100 * (6 + 10) / 40 == 40
    assert 100 * (18 - 3) / 50 == 30
    assert (5.16 - 0.40) / 4 / ((29.2 - 1.2) / 8 / 1000) == pytest.approx(340)
    assert 1.02 / 0.003 == pytest.approx(340)
    assert (4.36 - 0.40) / 6 / ((19 - 5) / 7 / 1000) == pytest.approx(330)
