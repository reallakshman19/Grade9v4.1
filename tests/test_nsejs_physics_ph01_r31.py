"""A01 R3.1 mechanical checks, not academic qualification."""
import json
import importlib.util
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PH = ROOT / "nsejs/physics/curriculum/agent1/PH01/"
def read(name):
    return json.loads((PH / name).read_text(encoding="utf-8"))
def test_r31_contract_and_preserved_history():
    path = ROOT / "nsejs/physics/curriculum/contracts/tools/validate_physics_contracts.py"
    spec = importlib.util.spec_from_file_location("ph01_r31_validator", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    result = mod.inspect_package(PH / "physics-topic-package.v1_1.r3_1.json")
    assert result["issues"] == [], result
    assert result["mechanical_status"] == "PASS"
    assert result["academic_status"] == result["release_status"] == "HOLD"
    old = read("physics-topic-package.v1_1.json")
    new = read("physics-topic-package.v1_1.r3_1.json")
    assert len(old["subtopics"]) == 3
    old_instances = {c["id"]: c for c in old["core1b"] if c["kind"] == "INSTANCE"}
    new_instances = {c["id"]: c for c in new["core1b"] if c["kind"] == "INSTANCE"}
    assert all(new_instances[k] == v for k, v in old_instances.items())
    assert len(new_instances) == 15
def test_r31_coverage_and_binding():
    p = read("physics-topic-package.v1_1.r3_1.json")
    assert p["topic_adapter"] == read("topic-adapter.PH01.v0.3.0.json")
    assert {s["id"] for s in p["subtopics"]} == {"PH01-M01","PH01-M02","PH01-M03","PH01-M05","PH01-M07"}
    assert len(p["core1b"]) == 18
    assert not p["core2_sources"]
    assert p["acceptance"]["release"] == "HOLD"
    for c in p["topic_adapter"]["cells"]:
        main = [m for m in p["core1b"] if m["kind"] == "MAIN" and m["cell_id"] == c["cell_id"]]
        assert len(main) == 1 and len(c["instance_ids"]) == 5
        assert set(main[0]["instance_qrt_ids"]) == set(c["instance_ids"])
    support = read("ph01-core1b-support.r3_1.json")
    assert support["package_version"] == p["version"]
    assert len(support["cycles"]) == len({s["cycle_id"] for s in support["cycles"]}) == 18
    assert {s["cycle_id"] for s in support["cycles"]} == {c["id"] for c in p["core1b"]}
    ledger = read("ph01-subtopic-qrt-coverage.r3_1.json")["summary"]
    assert (ledger["total_subtopics"], ledger["subtopics_with_3_distinct_proposed_qrt_operations"], ledger["qualified_qrt_targets"]) == (8,5,0)
def test_r31_exact_math():
    from fractions import Fraction as F
    assert 22-2*5 == 12 and 22-2*10 == 2
    assert [4+2*r for r in [-1,3,3,0]] == [2,10,10,4]
    assert F(-4+6,3) == F(2,3) and (14+4)/2 == 9
    assert sum(abs(b-a) for a,b in zip([-4,8,5],[8,5,1])) == 19
    assert [3,3-8,3-8,3-8+11,3-8+11-6] == [3,-5,-5,6,0]
    P = F(23-6,2)
    assert P>1 and (P+2)+(P-1)+5 == 23
    t = F(17,2)
    assert 15-t == -2+t == F(13,2)
    assert [-2,0,2] == [F(1-7,3),F(1-1,2),F(9-1,4)]
    assert -6+8 == 2 and 6+8 == 14
    assert F(22,6)>3 and (26-2*7)-(22-2*7) == 4
def test_r31_runtime_links_and_revision_namespace():
    page = (ROOT / "nsejs/physics/core1/ph01-qrt-r31/index.html").read_text(encoding="utf-8")
    assert page.count("data-textbook-help") == 3
    assert "G9V41:PH01:R31:" in page and "cycles.length !== 18" in page
    assert "physics-topic-package.v1_1.r3_1.json" in page and "ph01-core1b-support.r3_1.json" in page
    assert 'crypto.subtle.digest("SHA-256", bytes)' in page
    assert "TEXTBOOK_BEFORE_FIRST" in page and "TEXTBOOK_AFTER_FIRST" in page
