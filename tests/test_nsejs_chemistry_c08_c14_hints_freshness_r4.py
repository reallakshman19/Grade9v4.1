"""Author-exposed negative controls for Chemistry R4 hints and B4 leakage; NOT blind academic acceptance."""
import json, re
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
CURR=ROOT/"curriculum"/"chemistry"/"agent-b"
AUD=ROOT/"docs"/"audits"/"chemistry-c08-c14"

def read(path): return json.loads(path.read_text(encoding="utf-8"))

def target_tasks():
    delta=read(AUD/"CHEMISTRY_C08_C14_REMEDIATION_DELTA_R3.json")
    for unit in sorted({x["unit_id"] for x in delta["changes"]}):
        practice=read(CURR/"core1b"/f"{unit}.core1b.v0.1.0.json")
        book=read(CURR/"learner"/f"{unit}.reader.v0.1.0.json")
        for item in delta["changes"]:
            if item["unit_id"]==unit:
                task=next(x for x in practice["cycles"] if x["cycle_id"]==item["cycle_id"])
                section=next(x for x in book["sections"] if x["id"]==item["subtopic_id"])
                yield task,section,book

def _hints(t): return [h["text"] for h in t["attempt"]["hints"]]
def _contains_all(s,*words): return all(w.casefold() in s.casefold() for w in words)

def test_17_distinct_exact_domain_hints_and_no_post_commit_reveal():
    tasks=list(target_tasks())
    assert len(tasks)==17
    h2,h3=[],[]
    for t,_,_ in tasks:
        hints=t["attempt"]["hints"]
        assert [h["id"] for h in hints]==["H1","H2","H3"]
        assert [h["verb"] for h in hints]==["CLARIFY","CORRELATE","OPEN_THE_WAY"]
        assert all(len(h["text"])>=95 for h in hints)
        h2.append(hints[1]["text"]);h3.append(hints[2]["text"])
        assert hints[1]["text"]!=hints[2]["text"]
        assert t["attempt"]["post_commit_closure"]["model_response"] not in "\n".join(_hints(t))
        assert all(v=="UNREVIEWED" for v in t["reviews"].values())
        assert t["source_exam_question_id"] is None
    assert len(set(h2))==len(set(h3))==17

def _check_critical(task_id,h2,h3):
    h2=h2.casefold();h3=h3.casefold()
    if task_id=="CORE1B-C12-01-1":
        return ("piston" in h2 and "stop" in h2 and "300" in h2 and
                "p/v/t" in h3 and "pressure ratio" in h3 and
                all(x not in h2+" "+h3 for x in ("reaction", "cooling", "gas species", "species ledger")))
    if task_id=="CORE1B-C09-01-1":
        return ("hcl" in h2 and "ch₃cooh" in h2 and
                "ionisation" in h2 and "conductivity" in h3 and "ph" in h3 and
                "hydrate" not in h2+" "+h3)
    if task_id in ("CORE1B-C08-04-1","CORE1B-C08-04-2"):
        return ("ion" in h2 and "solid" in h3 and
                all(x not in h2+" "+h3 for x in ("electron", "redox", "oxidation", "reduction")))
    if task_id=="CORE1B-C14-02-1":
        return ("nitrate" in h2 and "micro" in h2 and
                "treatment" in h3 and "potability" in h3 and
                all(x not in h2+" "+h3 for x in ("atmospheric", "emission", "air pollution", "rival causal")))
    raise ValueError("Unknown critical task "+task_id)

def test_all_four_science_mismatch_families_and_synthetic_bad_hints():
    practice={t["cycle_id"]:t for t,_,_ in target_tasks()}
    critical=("CORE1B-C12-01-1","CORE1B-C09-01-1",
              "CORE1B-C08-04-1","CORE1B-C08-04-2","CORE1B-C14-02-1")
    for tid in critical:
        h=_hints(practice[tid])
        assert _check_critical(tid,h[1],h[2]),tid
    assert not _check_critical("CORE1B-C12-01-1",
        "Separate initial, reaction, cooling and measurement stages; declare constraints and list every gas species present.",
        "Write a stage-by-stage species ledger with unknown cells")
    assert not _check_critical("CORE1B-C09-01-1",
        "Distinguish measured property and formula assumptions",
        "Write a candidate ion or hydrate ledger")
    assert not _check_critical("CORE1B-C08-04-1",
        "Write an electron ledger", "Make two model columns")
    assert not _check_critical("CORE1B-C14-02-1",
        "Make an atmospheric-emission causal table","Describe two rival causal accounts")

def words(s): return re.findall(r"[^\W_]+", s.casefold(), flags=re.UNICODE)

def shingles(s,n=6):
    tokens=words(s)
    return set(tuple(tokens[i:i+n]) for i in range(max(0,len(tokens)-n+1)))

def test_native_core1a_and_figures_have_no_exact_or_6_word_surface_replay():
    # IMPORTANT: lexical scan cannot certify semantic novelty. This is a negative control only.
    checks=0
    for task,section,book in target_tasks():
        text="\n".join([section.get("hook",""),section.get("worked",""),
            section.get("misconception",""),section.get("boundary",""),
            *section.get("teaching",[])])
        question=task["attempt"]["prompt"]
        assert question not in text, task["cycle_id"]
        assert not (shingles(question)&shingles(text)),task["cycle_id"]
        # All figures in the chapter can be visited before practice. Inspect their actual SVG text.
        for s in book["sections"]:
            for rel in s.get("figures",[]):
                figure=(ROOT/"nsejs/chemistry/textbook"/rel).resolve()
                assert figure.is_relative_to(ROOT.resolve()) and figure.is_file()
                root=ET.fromstring(figure.read_text(encoding="utf-8"))
                caption=" ".join(root.itertext())
                assert question not in caption,task["cycle_id"]
                assert not (shingles(question)&shingles(caption)),task["cycle_id"]
        checks+=1
    assert checks==17

def test_author_semantic_witnesses_remain_holds_and_reader_hides_model():
    doc=read(AUD/"CHEMISTRY_C08_C14_B4_SEMANTIC_REVIEW_R4.json")
    assert len(doc["comparisons"])==17 and doc["independent_signoff"] is False
    assert all(x["blind_qrt_b4"]=="NOT_RUN" and x["academic_status"]=="HOLD" for x in doc["comparisons"])
    assert next(x for x in doc["comparisons"] if x["cycle_id"]=="CORE1B-C12-05-1")["semantic_clone_risk"].startswith("HEIGHTENED")
    js=(ROOT/"nsejs/chemistry/textbook/reader.js").read_text(encoding="utf-8")
    precommit=js[js.index("if(!saved){"):js.index("prediction.value=saved.prediction;")]
    assert "task.attempt.post_commit_closure.model_response" not in precommit
    assert "task.reconstruct.asks" not in precommit
    assert "visualStages(task,renderEpoch)" not in precommit
    assert "return;\n    }\n    prediction.value=saved.prediction;" in js
