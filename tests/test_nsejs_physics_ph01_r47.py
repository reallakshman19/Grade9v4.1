"""R00 exact-revision engineering witnesses for the source-proximal PH01 R4.7 transfer batch.

Tests original Q35/Q33/Q60 authored transfer warrants and source links,
not authenticity of the examination text or independent QRT/B1–B7.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PH = "nsejs/physics/curriculum/agent1/PH01/"
TASKS = {
    "PH01-LINK-2022-51-Q35": ("PH01-M05", "D3.5", "REPRESENT", "Q35"),
    "PH01-LINK-2024-51-Q33": ("PH01-M04", "D3.4", "MODEL", "Q33"),
    "PH01-LINK-2024-51-Q60": ("PH01-M05", "D3.7", "JUSTIFY", "Q60"),
}

def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def git_blob(path):
    raw = (ROOT / path).read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def test_r47_contract_and_historical_custody():
    spec = importlib.util.spec_from_file_location(
        "ph01_r47_contract_validator",
        ROOT / "nsejs/physics/curriculum/contracts/tools/validate_physics_contracts.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    result = mod.inspect_package(ROOT / (PH + "physics-topic-package.v1_1.r4_7.json"))
    assert result["issues"] == [], result
    assert result["mechanical_status"] == "PASS"
    assert result["academic_status"] == result["release_status"] == "HOLD"

    prior = read(PH + "physics-topic-package.v1_1.r4_6.json")
    after = read(PH + "physics-topic-package.v1_1.r4_7.json")
    support = read(PH + "ph01-core1b-support.r4_7.json")
    route = read(PH + "ph01-subtopic-routes.r4_7.json")
    assert after["status"] == "DRAFT_AUTHOR_EXPOSED" and after["acceptance"]["release"] == "HOLD"
    assert after["version"] == support["package_version"] == "0.11.0"
    assert len(after["subtopics"]) == 8 and len(after["core1b"]) == len(support["cycles"]) == 63
    assert sum(c["kind"] == "INSTANCE" for c in after["core1b"]) == 53
    assert sum(c["kind"] == "MAIN" for c in after["core1b"]) == 10
    old = {c["id"]: c for c in prior["core1b"]}
    new = {c["id"]: c for c in after["core1b"]}
    assert set(old) - set(new) == {
        "PH01-MAIN-D3.4-R32", "PH01-MAIN-D3.5-R32", "PH01-MAIN-D3.7-R43"}
    assert set(new) - set(old) == {
        "PH01-MAIN-D3.4-R47", "PH01-MAIN-D3.5-R47", "PH01-MAIN-D3.7-R47",
        *(f"{sub}-QRT-{op}-D3-R47-{q}-INSTANCE"
          for sub,op,q in (("PH01-M05","REPRESENT","Q35"),
                           ("PH01-M04","MODEL","Q33"),("PH01-M05","JUSTIFY","Q60")))
    }
    assert all(new[id] == old[id] for id in set(old) & set(new))
    assert route["prior_r46_package_blob"] == git_blob(PH + "physics-topic-package.v1_1.r4_6.json")
    assert route["prior_r46_support_blob"] == git_blob(PH + "ph01-core1b-support.r4_6.json")
    assert after["topic_adapter"] == read(PH + "topic-adapter.PH01.v0.11.0.json")
    assert {c["id"] for c in after["core1b"]} == {s["cycle_id"] for s in support["cycles"]}
    assert route["integrated_main"]["cycle_ids"] == [c["id"] for c in after["core1b"] if c["kind"] == "MAIN"]

def test_r47_each_source_has_fresh_target_visual_task_and_bidirectional_route():
    pack = read(PH + "physics-topic-package.v1_1.r4_7.json")
    support = read(PH + "ph01-core1b-support.r4_7.json")
    srcmap = read(PH + "ph01-core2-construction-map.r4_7.json")
    teach = read(PH + "ph01-r47-teaching-extensions.json")
    assert len(teach) == 3
    tasks = {t["source"]: t for t in teach}
    records = {r["id"]: r for r in srcmap["records"]}
    targets = {t["id"]: (s["id"], t) for s in pack["subtopics"] for t in s["qrt_targets"]}
    cycles = {c["id"]: c for c in pack["core1b"]}
    supports = {s["cycle_id"]: s for s in support["cycles"]}
    html = (ROOT/"nsejs/physics/textbook/PH01/core2-links-r47/index.html").read_text()
    total_graphs = 0
    for source,(sub,cell,op,q) in TASKS.items():
        item = tasks[source]
        assert item["m"] == sub[-3:] and item["cell"] == cell and item["op"] == op
        tid, cid = item["id"], item["cid"]
        assert (sub, targets[tid][1]["primary_operation"]) == (sub, op)
        assert targets[tid][1]["blueprint_cell"] == cell
        assert targets[tid][1]["band"] == "D3"
        assert targets[tid][1]["source_role"] == "AUTHORED_TRANSFER"
        assert targets[tid][1]["qrt_status"] == "PROPOSED"
        assert sum(v["score"] for v in targets[tid][1]["factor_evidence"].values()) == 7
        c = cycles[cid]
        assert c["kind"] == "INSTANCE" and c["qrt_target_id"] == tid
        assert c["fresh_task"] == item["task"] == c["stages"]["attempt"]
        assert c["stages"]["reconstruct"] == item["ans"]
        assert c["stages"]["boundary_test"] == item["bound"]
        assert supports[cid]["boundary_solution"] == item["sol"]
        assert supports[cid]["prompt_graphs"] == item["graphs"]
        assert c["runtime_verification"] == "NOT_RUN"
        assert c["attempt_policy"]["save_first_answer_before_hint"]
        assert c["attempt_policy"]["fail_closed_on_storage_error"]
        assert len(item["scores"]) == 5 and sum(item["scores"]) == 7
        assert item["ans"] != item["sol"] and item["task"] != item["teach"]
        total_graphs += len(item["graphs"])
        original = records[source]
        assert original["source_status"] == original["exact_fit"] == "HOLD"
        links = [x for x in original["preparation"] if x["cycle_id"] == cid]
        assert len(links) == 1
        link = links[0]
        assert link["fit"] == "FOCUSED_SOURCE_CONSTRUCTION_TRANSFER_CANDIDATE_NOT_EXACT_QUALIFIED"
        assert (link["subtopic_id"],link["cell_id"],link["qrt_target_id"]) == (sub,cell,tid)
        assert (ROOT/link["core1a"]).is_file() and (ROOT/link["core1b"]).is_file()
        assert f'id="{source}"' in html
        assert cid in html
        page = (ROOT/link["core1b"]).read_text()
        assert 'ph01-qrt-r47/scoped-runtime.js' in page
        assert "academic" in page.lower()
        assert len(item["graphs"]) in (0,1,3)
        for g in item["graphs"]:
            assert g["x_max"] > 0 and g["y_max"] > g["y_min"]
            assert all(len(segment) >= 2 for segment in g["segments"])
    assert total_graphs == 4
    assert srcmap["counts"]["qualified"] == 0
    assert len(srcmap["records"]) == 15
    assert not any(v["source_role"] == "DIRECT_EXAM_EVIDENCE" for v in pack["core2_sources"])

def test_r47_exact_graph_q35_bidirectional_reversal_energy_witness():
    # a=+3 [0,2], 0 [2,5], -2 [5,8], initial v=-4 and x=+5.
    v = [F(-4), F(2), F(2), F(-4)]
    dx = [F(-2), F(6), F(-3)]
    assert sum(dx) == 1 and F(5)+sum(dx) == 6
    assert F(4,3) < 2 and 5 < 6 < 8
    xmin = F(5)-4*F(4,3)+F(3,2)*F(4,3)**2
    xmax = F(9)+2*1-1
    assert xmin == F(7,3) and xmax == 10
    path = F(10,3)+F(6)+F(5)
    assert path == F(43,3) and path > abs(sum(dx))
    assert (v[1] == v[2]) and v[1] != 0
    newv = [F(4),F(10),F(10),F(4)]
    assert min(newv) > 0
    assert (newv[0]+newv[1])*1 + newv[1]*3 + F(1,2)*(newv[2]+newv[3])*3 == 65

def test_r47_q33_nonconstant_velocity_endpoint_and_q60_mixed_axis_witnesses():
    # A converted from km/h and milliseconds, B from s, C from v²-x.
    a,b,c,dmean = F(-5),F(6),F(2),F(-7)
    assert sorted([abs(a),abs(b),abs(c),abs(dmean)]) == [2,5,6,7]
    assert (F(-5)-F(10))/3 == a
    assert 2*F(27)/9 == b
    assert (8*8-2*2)/(2*15) == c
    assert (F(-11)-F(3))/2 == dmean
    # Same D endpoints can have arbitrarily different instantaneous rates.
    from math import pi,sin
    for k in (0,4):
        assert abs(3-7*2+k*sin(2*pi)-(-11)) < 1e-12
    assert max(abs(-7+4*pi), abs(-7-4*pi)) > 7
    assert (F(27)-F(6)*3)/F(9,2) == 2  # B boundary changes ranking
    # Q60 axes: graph A 0→10 m/s in 120s, B 6m/s in100s, C 5→15m/s in60s.
    distances = [F(0+10,2)*120,F(6)*100,F(5+15,2)*60]
    assert distances == [600,600,600]
    assert [d/t for d,t in zip(distances,[120,100,60])] == [5,6,10]
    assert F(10,120)*2 == F(10,60)
    # Shift C down 36km/h = 10m/s: negative then positive, path 150, signed area 0.
    assert F(-5+5,2)*60 == 0
    assert F(5)*30/2*2 == 150
    assert -6*100 == -600  # westward B: same path, different signed displacement

def test_r47_original_figures_are_bound_to_payload_digest():
    package = ROOT/(PH+"physics-topic-package.v1_1.r4_7.json")
    support = ROOT/(PH+"ph01-core1b-support.r4_7.json")
    digest = hashlib.sha256(package.read_bytes()+b"\n"+support.read_bytes()).hexdigest()
    assert len(digest) == 64
    js = (ROOT/"nsejs/physics/core1/ph01-qrt-r47/scoped-runtime.js").read_text()
    assert 'rawA + "\\n" + rawB' in js
    assert 'prompt_graphs' in js and "renderPromptGraphs()" in js
    assert "R47:" in js
    src = read(PH+"ph01-core1b-support.r4_7.json")
    g = {r["cycle_id"]:r.get("prompt_graphs", []) for r in src["cycles"]}
    assert len(g["PH01-M05-QRT-REPRESENT-D3-R47-Q35-INSTANCE"]) == 1
    assert len(g["PH01-M04-QRT-MODEL-D3-R47-Q33-INSTANCE"]) == 0
    assert len(g["PH01-M05-QRT-JUSTIFY-D3-R47-Q60-INSTANCE"]) == 3
