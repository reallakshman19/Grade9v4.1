"""Synthetic real-Git tests of platform authority, not academic qualification."""
from __future__ import annotations
import copy,hashlib,json,subprocess,sys
from pathlib import Path
import pytest
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent));sys.path.insert(0,str(HERE))
import control as C
import platform_contract as P
from entry import render_entry
from fixture_builder import build
from audit_stacks import audit
def git(root,*a):return subprocess.check_output(["git","-C",str(root),*a],stderr=subprocess.PIPE).decode().strip()
def write(root,path,data):
    p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data if isinstance(data,bytes) else C.canonical(data))
def save(root):
    git(root,"add","-A");git(root,"commit","-m","synthetic fixture");return git(root,"rev-parse","HEAD")
@pytest.fixture
def bundle(tmp_path):
    root=tmp_path/"repo";root.mkdir();git(root,"init");git(root,"config","user.email","fixture@example.invalid");git(root,"config","user.name","Fixture")
    dest=root/"nsejs/physics/synthetic";build(tmp_path/"generated")
    for file in (tmp_path/"generated/physics").iterdir():
        if file.name!="index.html":write(root,"nsejs/physics/synthetic/"+file.name,file.read_bytes())
    ep="js/assessment/engine.mjs";rp="js/assessment/reader.mjs"
    for path,name in [(ep,"engine.mjs"),(rp,"reader.mjs")]:write(root,path,(HERE/name).read_bytes())
    entry="nsejs/physics/synthetic/index.html";manifest="nsejs/physics/synthetic/manifest.json";raw=(root/manifest).read_bytes()
    write(root,entry,render_entry(entry,manifest,C.sha(raw),rp))
    intake=C.EVID+"intakes/opaque.json";prompt=json.loads((dest/"challenge.json").read_bytes())["payload"]["stem"]
    write(root,intake,{"schema":"g9-cold-intake/v1","opaque_id":"a"*32,"stem":prompt,"conditions":["Synthetic only"],"figures":[]})
    item={"uid":"synthetic-physics","cell":"D3.3","paths":[entry,manifest,ep,rp]+[str(x.relative_to(root)) for x in dest.iterdir() if x.name not in ("index.html","manifest.json")],"platform":{"entry":entry,"manifest":manifest,"intake":intake,"engine":ep,"reader":rp,"engine_sha256":C.sha((root/ep).read_bytes()),"reader_sha256":C.sha((root/rp).read_bytes())},"construction":{"task_stem":prompt,"primary_operation":"APPLY","prerequisite_graph":[{"id":"direction","description":"Synthetic directional prerequisite description","requires":[],"worked_witness":"Synthetic worked prerequisite representation"}],"worked_transitions":[{"prerequisite":"direction","anchor":"Synthetic anchor","transition":"Synthetic transition"}],"shortest_route":[{"id":"step","operation":"APPLY","reason":"Synthetic fixture step","requires":["direction"]}],"competing_operations":[{"operation":"MODEL","why_not":"Synthetic competing operation"}],"response_map":[{"field":"model"},{"field":"value"}]}}
    head=save(root);return root,head,item
def candidate(root,head,item):return P.check_candidate(root,head,item,C.tree(root,head),C.blob,C.parse,C.sha,C.require,C.validate_schema,C.path_ok)
def test_exact_shared_entry_and_assets(bundle):
    root,head,item=bundle
    result=candidate(root,head,item);assert result["opaque_id"]=="a"*32
    write(root,item["platform"]["engine"],b"// another chapter engine");head=save(root)
    with pytest.raises(C.Block,match="PLATFORM_ENGINE_BYTES_MISMATCH"):candidate(root,head,item)
def test_entry_with_extra_script_denied(bundle):
    root,head,item=bundle;p=root/item["platform"]["entry"];p.write_bytes(p.read_bytes()+b"<script>bad()</script>");head=save(root)
    with pytest.raises(C.Block,match="PLATFORM_ENTRY_NOT_SHARED_TEMPLATE"):candidate(root,head,item)
def test_tampered_model_and_intake_anchoring_denied(bundle):
    root,head,item=bundle
    p=root/item["platform"]["intake"];intake=json.loads(p.read_bytes());intake["proposed_cell"]="D3.4";write(root,item["platform"]["intake"],intake);head=save(root)
    with pytest.raises(C.Block,match="SCHEMA:reviewer-intake"):candidate(root,head,item)
    git(root,"checkout","HEAD~1");write(root,"nsejs/physics/synthetic/feedback.json",b"{}");head=save(root)
    with pytest.raises(C.Block,match="PLATFORM_ASSET_HASH"):candidate(root,head,item)
def test_graph_cycle_unworked_and_operation_mismatch(bundle):
    _,_,item=bundle;w={"items":[item]};P.validate_design(w,C.require)
    bad=copy.deepcopy(w);bad["items"][0]["construction"]["prerequisite_graph"][0]["requires"]=["direction"]
    with pytest.raises(C.Block,match="CYCLIC_PREREQUISITE"):P.validate_design(bad,C.require)
    bad=copy.deepcopy(w);bad["items"][0]["construction"]["worked_transitions"]=[]
    with pytest.raises(C.Block,match="MISSING_WORKED_TRANSITION"):P.validate_design(bad,C.require)
    bad=copy.deepcopy(w);bad["items"][0]["cell"]="D3.4"
    with pytest.raises(C.Block,match="OPERATION_CELL_MISMATCH"):P.validate_design(bad,C.require)
def test_stacked_cumulative_diff_is_not_parent_only(tmp_path):
    root=tmp_path/"stack";root.mkdir();git(root,"init");git(root,"config","user.email","fixture@example.invalid");git(root,"config","user.name","Fixture")
    write(root,C.POLICY,json.loads((HERE.parent/"policy.v1.json").read_bytes()));main=save(root)
    write(root,"nsejs/physics/ph06/reader.js",b"parent frozen runtime");parent=save(root)
    write(root,C.EVID+"note.md",b"child only evidence");head=save(root)
    r=audit(root,main,head,"parent");assert r["status"]=="STACKED_DIAGNOSTIC_ONLY" and r["content_paths"]==["nsejs/physics/ph06/reader.js"]
    assert r["counts"]["EVIDENCE"]==1 and r["academic_status"]=="HOLD"
