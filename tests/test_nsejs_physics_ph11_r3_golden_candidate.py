"""PH11-07 R3 exposed adversarial review; not a blind science/QRT acceptance receipt.

This regression checks arithmetic, representation/binding, novelty and remaining
academic HOLD boundaries. It does not assign QRT bands or establish learner mastery.
"""
import json
from fractions import Fraction
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
CUR = ROOT / "nsejs/physics/curriculum/topics/PH11"
CASE = ROOT / "review/physics/ph09-ph12-wpe-parity-r1/FOUR_WPE_PARITY_REFERENCE_CANDIDATES_R1.json"
OLD = CUR / "topic-adapter.PH11.wpe-parity-r2.v1.json"
NEW = CUR / "topic-adapter.PH11.wpe-parity-r3.v1.json"
CORE1A = CUR / "subtopics/PH11-07/core1a.html"
CORE1B = CUR / "subtopics/PH11-07/core1b.html"
PREVIEW = ROOT / "review/physics/ph09-ph12-wpe-parity-r1/preview.js"
AUDIT = ROOT / "review/physics/ph11-07-r3/PH11_07_R3_ADVERSARIAL_EVIDENCE.json"
VALID_OPS = {"RETRIEVE": 1, "EXPLAIN": 2, "APPLY": 3, "MODEL": 4,
             "REPRESENT": 5, "SYNTHESIZE": 6, "JUSTIFY": 7}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def ph11():
    return next(c for c in load(CASE)["cases"] if c["chapter"] == "PH11")


def parallel(a, b):
    return Fraction(1, Fraction(1, a) + Fraction(1, b))


def test_source_and_two_anchors_have_independent_conservation_witnesses():
    # Authored source checkpoint: 9 V; upstream 3Ω; parallel 6Ω and 6Ω.
    rp = parallel(6, 6)
    assert rp == 3
    source_i = Fraction(9, 3 + rp)
    source_v = source_i * rp
    assert source_i == Fraction(3, 2)
    assert source_v == Fraction(9, 2)
    assert source_v / 6 + source_v / 6 == source_i
    # Direct-parallel Core1A anchor: supply 12 V, 6Ω || 3Ω.
    assert parallel(6, 3) == 2
    assert Fraction(12, 6) + Fraction(12, 3) == 6
    # Connected Core1A bridge: 10 V, 2Ω series, 4Ω || 4Ω.
    rp_bridge = parallel(4, 4)
    total_i = Fraction(10, 2 + rp_bridge)
    v_branch = total_i * rp_bridge
    assert (rp_bridge, total_i, v_branch) == (2, Fraction(5, 2), 5)
    assert v_branch / 4 + v_branch / 4 == total_i
    assert total_i * 2 + v_branch == 10
    obj = ph11()
    assert "12 V" in obj["core1a"]["worked_a"]
    assert "10 V" in obj["core1a"]["connected_bridge"]["question"]
    assert len(obj["core1a"]["connected_bridge"]["steps"]) == 4
    assert "9 V" in load(NEW)["source"]["stem"]


def test_inverse_transfer_has_unique_positive_solution_and_a_genuine_boundary():
    # New challenge: measure 4 A upstream at 18 V, 3Ω series, 6Ω || R.
    total_equiv = Fraction(18, 4)
    downstream = total_equiv - 3
    voltage_ab = downstream * 4
    known_i = voltage_ab / 6
    unknown_i = Fraction(4) - known_i
    unknown_r = voltage_ab / unknown_i
    assert (total_equiv, downstream, voltage_ab, known_i, unknown_i, unknown_r) == (
        Fraction(9, 2), Fraction(3, 2), 6, 1, 3, 2
    )
    assert parallel(6, unknown_r) == downstream
    assert (voltage_ab + Fraction(4) * 3) == 18
    assert Fraction(18, 3 + parallel(6, unknown_r)) == 4
    # For any positive passive downstream equivalent, I_total < 18 / 3=6 A.
    assert Fraction(18, 3) == 6
    assert not (Fraction(7) < Fraction(18, 3))
    obj = ph11()
    assert "unknown positive resistor R" in obj["core1b"]["original_b"]
    assert "ammeter" in obj["core1b"]["original_b"]
    assert "7 A" in obj["core1b"]["boundary"]
    assert all(str(n) in " ".join(obj["core1b"]["reconstruction"])
               for n in ["4.5", "1.5", "6", "3", "2"])


def test_original_case_is_not_a_number_swap_of_the_worked_example():
    obj = ph11()
    worked = obj["core1a"]["worked_a"]
    bridge = obj["core1a"]["connected_bridge"]["question"]
    transfer = obj["core1b"]["original_b"]
    assert "unknown" not in worked.lower() and "unknown" not in bridge.lower()
    assert "measured" not in worked.lower() and "ammeter" not in bridge.lower()
    assert "unknown" in transfer.lower() and "ammeter" in transfer.lower()
    assert "18 V" in transfer and "12 V" in worked and "10 V" in bridge
    assert "infer" in obj["core1b"]["protected_work"].lower()
    assert "If the saved reasoning" not in obj["core1b"]["diagnose"]
    assert "Do not diagnose" in obj["core1b"]["diagnose"]


def test_r3_adapter_rejects_prior_inflated_d4_without_claiming_independence():
    old, new = load(OLD), load(NEW)
    assert old["task"]["proposed_cell"] == "D4.4" and old["task"]["proposed_total"] == 8
    assert new["version"] == "0.5.0"
    assert new["task"]["id"].endswith("-R3-MAIN-01")
    assert new["schema"] == "g9v41-physics-wpe-parity-topic-adapter-r3/v1"
    assert new["task"]["proposed_primary_operation"] == "MODEL"
    assert new["task"]["proposed_cell"] == "D3.4"
    assert new["task"]["proposed_total"] == 7
    assert new["task"]["qrt_independent"] == "NOT_RUN"
    assert VALID_OPS[new["task"]["proposed_primary_operation"]] == int(
        new["task"]["proposed_cell"].split(".")[1]
    )
    factors = new["task"]["factor_evidence"]
    assert list(factors) == [
        "concept_model_selection", "representation_translation",
        "reasoning_chain_length", "algebra_computational_load",
        "trap_exception_sensitivity"
    ]
    assert len(factors) == 5
    assert all(type(f["score"]) is int and 0 <= f["score"] <= 2 and len(f["evidence"]) >= 35
               for f in factors.values())
    assert sum(f["score"] for f in factors.values()) == 7
    assert factors["representation_translation"]["score"] == 1
    assert "INDEPENDENT_QRT_HOLD" in new["academic_status"]
    assert new["review_disposition"]["reviewer_exposure"].startswith("AUTHOR_READ_PREVIOUS")
    assert new["adoption"] == "SIDE_CAR__DO_NOT_REPLACE_NATIVE_PACKAGE_OR_BLUEPRINT"
    assert new["blueprint"]["pin_reconciliation"].startswith("HOLD")
    assert new["source"]["exam_source_uid"] is None
    assert new["source"]["not_an_official_exam"]
    assert all(new["review_disposition"][f"B{i}"] == "HOLD" for i in range(1, 8))
    assert all(new["assertions"][x] == "HOLD" for x in
               ["source_authenticity", "science", "b1_b7", "owner_release"])


class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.illustrations = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and a.get("rel") == "stylesheet":
            self.links.append(a.get("href"))
        if tag == "svg":
            self.illustrations.append(a.get("aria-label", ""))


def test_native_pages_link_the_correct_adapter_and_the_repaired_figures():
    a, b = CORE1A.read_text(encoding="utf-8"), CORE1B.read_text(encoding="utf-8")
    doc = Tags()
    doc.feed(a)
    assert len(doc.illustrations) == 2
    assert "12 volt source connected directly" in doc.illustrations[0]
    assert "ten volt source, series two ohm" in doc.illustrations[1]
    assert "10 V" in a and "12 V" in a
    assert "An ideal 18 V source" not in a  # avoid copying the new challenge stem into teaching
    for page in [CORE1A, CORE1B]:
        source = page.read_text(encoding="utf-8")
        parsed = Tags()
        parsed.feed(source)
        assert parsed.links
        for href in parsed.links:
            resolved = (page.parent / href).resolve()
            assert resolved.is_file(), (str(page.relative_to(ROOT)), href, str(resolved))
        assert "topic-adapter.PH11.wpe-parity-r3.v1.json" in source
        assert "ACADEMIC HOLD" in source
        assert "<iframe" not in source.lower()
    assert "source-first" in b.lower()
    assert "D3.4" in b and "D4.4 proposal is explicitly disputed" in b


def test_runtime_uses_r3_adapter_and_does_not_show_source_or_decisive_work_early():
    code = PREVIEW.read_text(encoding="utf-8")
    assert 'topic === "PH11" ? "wpe-parity-r3.v1.json"' in code
    assert "g9v41-physics-wpe-parity-topic-adapter-r3/v1" in code
    assert "adapters[x.chapter].task.protected_decisive_work !== x.core1b.protected_work" in code
    assert "versionMaterial" in code and 'crypto.subtle.digest("SHA-256"' in code
    assert '    $("connected-bridge").hidden = true;' in code
    assert '    $("reviewer-adapter-evidence").hidden = true;' in code
    assert '    $("journey").hidden = true;' in code
    assert "function renderTeaching()" in code
    # The rendered source-first gate must NOT prepopulate the lesson or the transfer.
    choose = code.split("  function choose(id) {", 1)[1].split("  function exposed(type)", 1)[0]
    assert 'say("teaching-model", current.core1a.model)' not in choose
    assert 'say("fresh-task", current.core1b.original_b)' not in choose
    assert "renderTeaching();" in code.split("  function openTeaching() {", 1)[1].split(
        "  function choose(id)", 1
    )[0]


def test_r3_evidence_packet_retains_noncompensatory_hold():
    audit = load(AUDIT)
    assert audit["mode"] == "AUTHOR_EXPOSED_ADVERSARIAL_R3_NOT_BLIND"
    assert audit["subtopic_id"] == "PH11-07"
    assert all(audit["b1_b7"][f"B{i}"]["academic_disposition"] == "HOLD"
               for i in range(1, 8))
    assert audit["real_exam_question_admitted"] == 0
    assert audit["independent_qrt"] == "NOT_RUN"
    assert audit["owner_release"] == "HOLD"
    assert any("D4.4" in issue["finding"] for issue in audit["rca"])
