"""PH01 author-exposed pilot verification; mechanical checks never confer QRT or science approval."""
from __future__ import annotations

import importlib.util
import json
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "nsejs/physics/curriculum/contracts"
PKG_PATH = ROOT / "nsejs/physics/curriculum/agent1/PH01/physics-topic-package.v1.json"
INVENTORY_PATH = ROOT / "nsejs/physics/curriculum/agent1/ph01-ph06-syllabus-inventory.v1.json"
CHAPTER_PATH = ROOT / "nsejs/physics/textbook/PH01/index.html"
V = CONTRACTS / "tools/validate_physics_contracts.py"
spec = importlib.util.spec_from_file_location("physics_ph01_contract_validator", V)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class VisibleReading(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ignore = 0
        self.parts = []
        self.ids = set()
        self.h2 = 0
        self.svg = 0
        self.image_titles = 0
        self.details = 0
        self.ranges = 0
        self.bad_svg = 0
        self.h1 = 0
    def handle_starttag(self, name, attrs):
        attrs = dict(attrs)
        if name in ("script", "style"):
            self.ignore += 1
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if name == "h2":
            self.h2 += 1
        if name == "h1":
            self.h1 += 1
        if name == "svg":
            self.svg += 1
            if attrs.get("role") != "img" or "aria-labelledby" not in attrs:
                self.bad_svg += 1
        if name == "details":
            self.details += 1
        if name == "input" and attrs.get("type") == "range":
            self.ranges += 1
    def handle_endtag(self, name):
        if name in ("script", "style"):
            self.ignore -= 1
    def handle_data(self, text):
        if not self.ignore:
            self.parts.append(text)


def package():
    return json.loads(PKG_PATH.read_text(encoding="utf-8"))


def test_ph01_package_contract_is_mechanically_valid_and_unqualified():
    receipt = mod.inspect_package(PKG_PATH)
    assert receipt["issues"] == []
    assert receipt["mechanical_status"] == "PASS"
    assert receipt["academic_status"] == "HOLD"
    assert receipt["release_status"] == "HOLD"


def test_ph01_source_integrity_and_no_exam_imposture():
    p = package()
    assert p["core2_sources"] == []
    assert all(q["source_role"] == "AUTHORED_TRANSFER" and q["qrt_status"] == "PROPOSED"
               for sub in p["subtopics"] for q in sub["qrt_targets"])
    assert p["acceptance"]["release"] == "HOLD"
    assert all(x["status"] == "HOLD" for x in p["acceptance"]["b1_b7"].values())


def test_qrt_operations_and_bands_are_distinct():
    targets = package()["subtopics"][0]["qrt_targets"]
    assert {q["primary_operation"] for q in targets} == {"MODEL", "REPRESENT", "SYNTHESIZE"}
    assert {q["blueprint_cell"] for q in targets} == {"D3.4", "D3.5", "D3.6"}
    assert all(sum(x["score"] for x in q["factor_evidence"].values()) in (6, 7)
               for q in targets)


def test_protected_core1b_cycles_are_separate_and_unrun():
    cycles = package()["core1b"]
    assert len(cycles) == 6
    for c in cycles:
        assert c["runtime_verification"] == "NOT_RUN"
        assert c["attempt_policy"]["save_first_answer_before_hint"]
        assert c["attempt_policy"]["track_help_exposure"]
        assert c["attempt_policy"]["preserve_original_revision"]
        assert c["attempt_policy"]["fail_closed_on_storage_error"]
        assert len(c["stages"]["reconstruct"]) > 75


def test_inventory_covers_first_six_topics_without_false_claim_of_completion():
    x = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    assert x["counts"]["assigned_topics"] == 6
    assert x["counts"]["subtopics"] == 49
    assert [c["topic_id"] for c in x["chapters"]] == [f"PH{i:02d}" for i in range(1, 7)]
    assert all(c["status"] in ("TEXTBOOK_PILOT_IN_PROGRESS", "INVENTORIED_NOT_AUTHORED")
               for c in x["chapters"])
    assert all(sub["qrt_status"] == "HOLD" for c in x["chapters"] for sub in c["subtopics"])


def test_textbook_is_sustained_exposition_not_short_key():
    html = CHAPTER_PATH.read_text(encoding="utf-8")
    parser = VisibleReading()
    parser.feed(html)
    reading_words = len(" ".join(parser.parts).split())
    assert reading_words > 2400, reading_words
    assert parser.h1 == 1
    assert parser.h2 >= 10
    assert parser.svg >= 2 and parser.bad_svg == 0
    assert parser.details >= 5
    assert parser.ranges == 1
    assert "Academic HOLD" in html


def test_reading_navigation_and_interactive_model_are_bound():
    html = CHAPTER_PATH.read_text(encoding="utf-8")
    parser = VisibleReading()
    parser.feed(html)
    assert all(section in parser.ids for section in (
        "observe", "distance", "speed", "accel", "graphs",
        "derive", "relative", "stages", "circular", "transfer", "next"
    ))
    assert {"observer", "a-output", "rel-output", "lab-meaning"} <= parser.ids
    assert "slider.addEventListener('input', update);" in html
    assert "aria-live" in html
    assert 'href="../../index.html"' in html


def test_reading_worked_graph_and_average_math():
    displacement = 3 * 4 + (-1) * 3
    distance = abs(3 * 4) + abs((-1) * 3)
    assert (displacement, distance) == (9, 15)
    assert (80 + 30) / 20 == 5.5
    assert (80 - 30) / 20 == 2.5
    assert "Net displacement is +9 m" in CHAPTER_PATH.read_text(encoding="utf-8")


def test_ph01_main_train_reversal_reconstruction_is_correct():
    # First-stage candidate 36/(6+4)=3.6 s is invalid after A reverses at t=3.
    first = 36 / 10
    assert first > 3
    t = 6
    assert 18 - 2 * (t - 3) == 36 - 4 * t == 12


def test_ph01_instance_delayed_departure_is_correct():
    t = 36 / 7
    assert t > 2
    assert abs(4 * t - (30 - 3 * (t - 2))) < 1e-12


def test_chapter_does_not_embed_third_party_papers():
    html = CHAPTER_PATH.read_text(encoding="utf-8")
    assert "This page is reading material and contains no authenticated examination answer key." in html
    assert "<iframe" not in html


def test_standalone_adapter_matches_authoring_package_exactly():
    adapter_path = PKG_PATH.parent / "topic-adapter.PH01.v0.1.0.json"
    adapter = json.loads(adapter_path.read_text(encoding="utf-8"))
    assert adapter == package()["topic_adapter"]
    assert adapter["status"] == "CANDIDATE_ONLY"


def test_contract_gap_c06_main_join_is_open_and_release_holds():
    gap = json.loads((PKG_PATH.parent / "contract-gap-C06-MAIN-join.v1.json").read_text(encoding="utf-8"))
    assert gap["oracle_decision"] == "PENDING"
    assert gap["status"] == "OPEN_AUTHOR_EXPOSED__NOT_APPROVED"
    assert package()["acceptance"]["b1_b7"]["B4"]["status"] == "HOLD"
    assert package()["acceptance"]["b1_b7"]["B6"]["status"] == "HOLD"
