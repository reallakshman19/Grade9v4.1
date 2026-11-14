"""B01 subtopic-isolated candidates. Structural checks are not academic approval."""
from __future__ import annotations

import json
import hashlib
from urllib.parse import urlsplit, parse_qs
import runpy
from pathlib import Path
from tools.ph01_source_pin_custody import pinned_json, HISTORICAL_BLOBS
from html.parser import HTMLParser

import pytest

ROOT = Path(__file__).resolve().parents[1]
CURRICULUM = ROOT / "nsejs" / "physics" / "curriculum"
VALIDATOR = runpy.run_path(str(CURRICULUM / "contracts/tools/validate_physics_contracts.py"))["inspect_package"]
SLICES = ("PH07-01", "PH07-02", "PH07-03", "PH07-04", "PH07-05", "PH07-06", "PH07-07", "PH07-08", "PH07-09", "PH07-10", "PH07-11", "PH07-12", "PH08-01", "PH08-02", "PH08-03", "PH08-04", "PH08-05", "PH08-06", "PH08-07", "PH08-08", "PH08-09", "PH08-10", "PH08-11", "PH08-12", "PH08-13")


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []
        self.iframes = 0

    def handle_starttag(self, tag, attrs):
        self.iframes += tag == "iframe"
        for key, val in attrs:
            if key in ("href", "src", "data-package") and val and not val.startswith(("http:", "https:", "#")):
                self.paths.append(urlsplit(val).path)


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
    expected = {sid: [] if sid in {"PH07-01", "PH07-03", "PH07-07", "PH07-08", "PH07-09", "PH07-10", "PH07-11", "PH07-12", "PH08-01", "PH08-02", "PH08-03", "PH08-08", "PH08-09", "PH08-10", "PH08-11", "PH08-12", "PH08-13"} else ["NSEJS-FND-CIRC-04"] if sid.startswith("PH07") else ["NSEJS-24-MECH-07"] for sid in SLICES}
    assert [q["item_id"] for q in data["core2_sources"]] == expected[sid]
    assert all(q["source_role"] == "PREREQUISITE_BRIDGE" and q["academic_status"] == "HOLD" for q in data["core2_sources"])
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


@pytest.mark.parametrize("sid", ("PH07-02", "PH08-07"))
def test_exact_existing_core2_candidate_binding(sid):
    folder = CURRICULUM / "topics" / sid[:4] / "b01" / sid
    meta = json.loads((folder / "core2-link.v1.json").read_text(encoding="utf-8"))
    candidate = meta["candidate"]
    bank = pinned_json(ROOT, candidate)
    ledger = pinned_json(ROOT, {"path":"nsejs/data/physics-core2-integrity.v1.json",
        "git_blob_sha":HISTORICAL_BLOBS["nsejs/data/physics-core2-integrity.v1.json"][0]})
    question, = [q for q in bank["questions"] if q["source_id"] == candidate["source_id"]]
    record, = [q for q in ledger["items"] if q["source_id"] == candidate["source_id"]]
    assert question["id"] == candidate["id"]
    assert question["band"] == candidate["producer_band"] == "D2"
    assert record["observed_question_revision_sha256"] == candidate["observed_question_revision_sha256"]
    assert hashlib.sha256(question["stem"].replace("\r\n", "\n").encode()).hexdigest() == candidate["observed_stem_sha256"]
    assert record["figure_dependency_missing"] == candidate["figure_dependency_missing"]
    # A later source bank may correct figure/producer metadata; preserve the
    # historical source pin, but independently guard the live stem and ID.
    live = json.loads((ROOT / candidate["path"]).read_text(encoding="utf-8"))
    live_question, = [q for q in live["questions"] if q["source_id"] == candidate["source_id"]]
    assert live_question["id"] == candidate["id"]
    assert hashlib.sha256(live_question["stem"].replace("\r\n", "\n").encode()).hexdigest() == candidate["observed_stem_sha256"]
    assert meta["academic_status"] == "HOLD"
    route = urlsplit(meta["core2_return"])
    assert (ROOT / route.path).is_file()
    assert parse_qs(route.query)["q"] == [candidate["source_id"]]
    assert route.fragment == candidate["source_id"]
    for name in ("core1a.html", "core1b.html"):
        assert candidate["source_id"] in (folder / name).read_text(encoding="utf-8")


def test_25_subtopic_crosswalk_is_not_exam_admission():
    p = CURRICULUM / "topics/PH07/b01/B01_CORE2_COVERAGE.v1.json"
    m = json.loads(p.read_text(encoding="utf-8"))
    assert len(m["rows"]) == len({r["subtopic_id"] for r in m["rows"]}) == 25
    assert sum(r["relation"] == "PRIMARY_RELATED_CANDIDATE_HOLD" for r in m["rows"]) == 2
    assert sum(r["native_candidate"] == "B01_DEDICATED_PAIR" for r in m["rows"]) == 25
    assert m["audit"]["qualified_direct_exam_items"] == m["audit"]["qualified_d3_d4_exam_items"] == 0
    for row in m["rows"]:
        assert row["direct_exam_admission"] == "HOLD"
        if row["core1a"]:
            assert (ROOT / row["core1a"]).is_file() and (ROOT / row["core1b"]).is_file()


def test_inverse_wave_model_and_thermal_power_checks():
    candidates = [(0.20 + 0.80*n)/0.005 for n in range(-10,11)]
    candidates = [u for u in candidates if 100 <= abs(u) <= 500]
    assert sorted(candidates) == pytest.approx([-440,-280,-120,200,360])
    survivors = [u for u in candidates if abs((u*0.0015)%0.80 - 0.54) < 1e-9]
    assert survivors == pytest.approx([360])
    assert 4 ** 1.5 == 8
    assert 9 ** 1.5 == 27
    assert (2 * 2 ** 3) ** 0.5 == 4


@pytest.mark.parametrize("sid,op", (("PH07-05","MODEL"), ("PH08-05","SYNTHESIZE"), ("PH08-06","JUSTIFY")))
def test_increment3_d4_proposals_remain_authored(sid, op):
    p = CURRICULUM / "topics" / sid[:4] / "b01" / sid / "physics-topic-package.v1.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    target, = [t for t in d["subtopics"][0]["qrt_targets"] if t["primary_operation"] == op]
    assert target["band"] == "D4"
    assert 8 <= sum(v["score"] for v in target["factor_evidence"].values()) <= 10
    assert target["source_role"] == "AUTHORED_TRANSFER"
    assert target["qrt_status"] == "PROPOSED"
    assert d["acceptance"]["release"] == "HOLD"


def test_increment3_author_model_arithmetic():
    # Layered propagation: fixed-delay reference and independent check.
    delay = 0.0056 - 2/500
    x = (0.0072 - delay - 2/500)/(1/300 - 1/500)
    assert delay == pytest.approx(0.0016)
    assert x == pytest.approx(1.2)
    assert 1/300 + delay == pytest.approx(0.0049333333333)
    # Pressure comparison under different impedances.
    assert 2**2 / 8 == 0.5
    # Radiative absorption and loss fitted to two short-interval slopes.
    alpha = 300*(0.16-0.08)/(150-90)
    loss = 90*alpha-300*0.08
    assert alpha == pytest.approx(0.4)
    assert loss == pytest.approx(12)
    assert (120*alpha-loss)/300 == pytest.approx(0.12)
    assert (120*alpha-loss)/300 != pytest.approx(0.10)


@pytest.mark.parametrize("sid,op", (("PH07-07","MODEL"), ("PH08-12","SYNTHESIZE"), ("PH08-12","JUSTIFY")))
def test_increment4_d4_and_no_direct_exam_claim(sid, op):
    d = json.loads((CURRICULUM / "topics" / sid[:4] / "b01" / sid / "physics-topic-package.v1.json").read_text(encoding="utf-8"))
    target, = [t for t in d["subtopics"][0]["qrt_targets"] if t["primary_operation"] == op]
    assert target["band"] == "D4"
    assert 8 <= sum(v["score"] for v in target["factor_evidence"].values()) <= 10
    assert target["source_role"] == "AUTHORED_TRANSFER"
    assert target["qrt_status"] == "PROPOSED"
    assert not d["core2_sources"]
    assert d["acceptance"]["release"] == "HOLD"
    for c in d["core1b"]:
        assert c["fresh_task"] not in target["decisive_route"]


def test_increment4_phase_evaporation_and_echo_arithmetic():
    assert (30-6)*100 == (30-14)*150 == 2400
    assert 12 - 0.004*2400 == pytest.approx(2.4)
    assert (20-6)/2500 == pytest.approx(0.0056)
    from math import sqrt
    assert (sqrt(12**2+9**2)-sqrt(4**2+9**2))/300 > 0.015
    assert (sqrt(12**2+6**2)-10)/340 < 0.012
    v=250
    width=v*0.056/2
    one=v*0.016/2
    other=width-one
    assert (one,other) == pytest.approx((2,5))
    assert sorted([2*(one+1)/v,2*(other-1)/v]) == pytest.approx([0.024,0.032])
    assert sorted([2*(other+1)/v,2*(one-1)/v]) == pytest.approx([0.008,0.048])
    assert [0.056+2*x/v for x in (one,other)] == pytest.approx([0.072,0.096])
