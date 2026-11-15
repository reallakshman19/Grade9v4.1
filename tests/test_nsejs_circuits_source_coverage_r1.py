"""Source-safe intake regression for circuits worksheet levels 1 and 2.

No test here grants exam authenticity, academic admission or redistribution rights.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "nsejs" / "data"
ASSETS = (ROOT / "nsejs" / "assets", ROOT / "nsejs" / "physics" / "assets")
SHA = "1d7f16219d4353bf74e6dd29ebd9c3e9b770ad3d2b402d46aed81165bb4e3c4e"
KEY1 = "B A A ABC B C C C A D AB BCD C C D B B B D A C AC B D A A B D D C D ACD A C B C".split()
KEY2 = "A B C B C B C B C D C D A D B A A D A CD".split()
FIG1 = {3, 10, 11, 13, 16, 18, 19, 21, 22, 33, 35}
FIG2 = {1,2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18}

def load(file):
    return json.loads((DATA / file).read_text(encoding="utf-8"))

def test_intake_inventory_and_two_level_numbering():
    l1 = load("circuits-level1-core2-candidates.v1.json")
    l2 = load("circuits-level2-core2-candidates.v1.json")
    assert l1["total_questions"] == len(l1["questions"]) == 36
    assert l2["total_questions"] == len(l2["questions"]) == 20
    assert l1["source_pdf_sha256"] == l2["source_pdf_sha256"] == SHA
    for level, bank in [(1,l1),(2,l2)]:
        ids = [q["id"] for q in bank["questions"]]
        assert ids == [f"NSEJS-CIRC-L{level}-Q{i:02d}" for i in range(1,len(bank["questions"])+1)]
        assert len(ids) == len(set(ids))

def test_supplied_worksheet_key_and_question_fields():
    for level, keys, file in [
      (1,KEY1,"circuits-level1-core2-candidates.v1.json"),
      (2,KEY2,"circuits-level2-core2-candidates.v1.json"),
    ]:
        bank=load(file)
        for i,q in enumerate(bank["questions"],1):
            assert len(q["options"]) == 4
            assert [x[:2] for x in q["options"]] == ["A:","B:","C:","D:"]
            actual = q["answer"].split(":",1)[0].replace(",","").replace(" ","")
            assert actual == keys[i-1], (level,i,actual,keys[i-1])
            assert q["stem"].strip()
            assert len(q["hints"]) == 3
            assert len(q["steps"]) == 3
            assert q["review_state"] == "NOT_ADMITTED"
            assert q["academic_admission"] == "HOLD"
            assert q["science_review"] == q["qrt_adjudication"] == "HOLD"
            assert q["source_pdf_sha256"] == SHA

def test_level1_explicit_multicorrect():
    bank=load("circuits-level1-core2-candidates.v1.json")
    multi={4,11,12,22,32}
    for i,q in enumerate(bank["questions"],1):
        assert (q["question_type"]=="multiple_correct_mcq") == (i in multi)

def test_all_diagram_dependencies_exist_and_dual_paths_match():
    for level, expected in [(1,FIG1),(2,FIG2)]:
        bank=load(f"circuits-level{level}-core2-candidates.v1.json")
        seen=set()
        for i,q in enumerate(bank["questions"],1):
            names=q["source_figures"]
            assert bool(names) == (i in expected or (level==2 and i==9))
            for name in names:
                if level==2 and i==9:
                    assert name == "fig_nsejs_circ_l2_q08.svg"
                if name in seen: continue
                seen.add(name)
                bytecopies=[(p/name).read_bytes() for p in ASSETS]
                assert bytecopies[0] == bytecopies[1]
                root=ET.fromstring(bytecopies[0])
                assert root.tag.endswith("svg")
                assert root.attrib.get("viewBox")
                texts=" ".join((e.text or "") for e in root.iter() if e.tag.endswith("text"))
                assert not re.search(r"(?:⇒|R_AB\s*=|R_edge\s*=|R_face_diagonal\s*=|S Open:)",texts,re.I), name
        assert len(seen)==len(expected)

def test_level1_authored_reader_integration_and_hold():
    q=load("circuits-level1-core2-candidates.v1.json")["questions"]
    a=load("physics-authored-practice-r1.json")
    by_id={x["id"]:x for x in a["questions"]}
    assert len(by_id)==len(a["questions"])
    for item in q:
        other=by_id[item["id"]]
        assert other["stem"]==item["stem"]
        assert other["options"]==item["options"]
        assert other["source_figures"]==item["source_figures"]
        assert other["answer"]==item["answer"]
        assert item["source_rights"]=="HOLD"
        assert item["construction_fit"]=="TOPIC_ONLY_RELATED"

def test_technical_reader_never_claims_approved_exam_key():
    js=(ROOT/"nsejs/js/core2-physics-reader.js").read_text(encoding="utf-8")
    assert "perfectly matches the official verified key" not in js
    assert "Candidate derivation & reported key" in js
    assert "MATCHES CANDIDATE KEY" in js

def test_reader_attempt_revision_storage_and_hint_locks():
    js=(ROOT/"nsejs/js/core2-physics-reader.js").read_text(encoding="utf-8")
    assert 'candidate-attempt","v2"' in js
    assert 'const contentRevision = await revision(q);' in js
    assert 'const k = attemptKey(q, contentRevision);' in js
    assert 'if (!saveAttempt(k, attempt))' in js
    assert 'candidate answer and solution remain locked' in js
    assert 'hints.slice(0, count)' in js
    assert 'const count = worksheet ? hintDepth' in js
    assert 'localStorage.setItem(hintKey, String(hintDepth + 1))' in js
    assert 'hints_revealed: hintDepth, assisted: hintDepth > 0' in js
    assert 'hint-exposure:v1' in js
    assert 'localStorage.removeItem(k)' not in js

def test_circuit_figure_bytes_and_hints_are_revision_bound():
    js=(ROOT/"nsejs/js/core2-physics-reader.js").read_text(encoding="utf-8")
    assert 'figure_bytes_sha256: await circuitFigureHashes(q)' in js
    assert 'hints: q.hints || []' in js
    assert 'candidate-attempt","v2"' in js
    assert 'content_revision_sha256: contentRevision' in js
    assert 'if (!getAttempt(k)) return false;' in js
    assert 'function revealAnswerAfterCommit()' in js
    assert 'answerBox.replaceChildren(' in js
    assert 'if (!response.ok) throw new Error("Circuit prompt figure unavailable:' in js
