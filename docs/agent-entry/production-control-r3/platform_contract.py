"""Trusted R3.1 semantic design/asset/intake structural checks.
Only trusted platform validator executes; candidate bytes are parsed as data.
Signatures and semantic reviewer decisions are separate.
"""
from __future__ import annotations
import importlib.util,json,posixpath,re,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
PLAT=HERE/"platform"
REL="docs/agent-entry/production-control-r3/"
EVID="review/production-control-r3/"
PROFILE=REL+"subject-profiles.v1.json"
ENGINE=REL+"platform/engine.mjs"
READER=REL+"platform/reader.mjs"
def _load_entry():
    spec=importlib.util.spec_from_file_location("trusted_entry",PLAT/"entry.py")
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
def validate_design(w,require):
    for item in w["items"]:
        c=item["construction"];p=item["platform"]
        graph={n["id"]:n for n in c["prerequisite_graph"]}
        require(len(graph)==len(c["prerequisite_graph"]),"DUPLICATE_PREREQUISITE")
        visited=set();visiting=set()
        def visit(key):
            require(key in graph,"UNKNOWN_PREREQUISITE:"+key)
            require(key not in visiting,"CYCLIC_PREREQUISITE_GRAPH")
            if key in visited:return
            visiting.add(key)
            for dep in graph[key]["requires"]:visit(dep)
            visiting.remove(key);visited.add(key)
        for key in graph:visit(key)
        transitions=[x["prerequisite"] for x in c["worked_transitions"]]
        require(set(transitions)==set(graph) and len(transitions)==len(graph),"MISSING_WORKED_TRANSITION")
        route_ids=[x["id"] for x in c["shortest_route"]]
        require(len(route_ids)==len(set(route_ids)),"DUPLICATE_ROUTE_STEP")
        used={k for step in c["shortest_route"] for k in step["requires"]}
        require(used==set(graph),"SHORTEST_ROUTE_PREREQUISITE_COVERAGE")
        alternatives=[x["operation"] for x in c["competing_operations"]]
        require(c["primary_operation"] not in alternatives and len(alternatives)==len(set(alternatives)),"COMPETING_OPERATION_INVALID")
        ops=["RETRIEVE","EXPLAIN","APPLY","MODEL","REPRESENT","SYNTHESIZE","JUSTIFY"]
        require(item["cell"].endswith("."+str(ops.index(c["primary_operation"])+1)),"OPERATION_CELL_MISMATCH")
        fs=[x["field"] for x in c["response_map"]];require(len(fs)==len(set(fs)),"DUPLICATE_RESPONSE_FIELD")
        require(p["intake"].startswith(EVID+"intakes/") and p["intake"].endswith(".json"),"COLD_INTAKE_NAMESPACE")
        require(p["entry"].endswith(".html") and p["manifest"].endswith(".json") and posixpath.dirname(p["entry"])==posixpath.dirname(p["manifest"]),"ENTRY_MANIFEST_PATH")
        require({p["entry"],p["manifest"],p["engine"],p["reader"]}<=set(item["paths"]),"PLATFORM_PATHS_NOT_IN_SCOPE")
def check_profile(repo,rev,w,items,blob,sha,require):
    require(sha(blob(repo,rev,PROFILE,items))==w["subject_profile_sha256"],"SUBJECT_PROFILE_PIN_MISMATCH")
    require(sha((HERE/"subject-profiles.v1.json").read_bytes())==w["subject_profile_sha256"],"SUBJECT_PROFILE_NOT_TRUSTED")
    for item in w["items"]:
        p=item["platform"]
        require(p["engine_sha256"]==sha((PLAT/"engine.mjs").read_bytes()) and p["reader_sha256"]==sha((PLAT/"reader.mjs").read_bytes()),"DESIGN_ENGINE_PIN_NOT_TRUSTED")
def public_path(p):
    return p.startswith(("nsejs/","curriculum/","js/assessment/")) and not any(x.lower() in {"review","reviews","evidence","receipts","private","workspace","source-custody","sources","originals","answer-keys","tests","qa","agent1","contracts"} or x.startswith(".") for x in p.split("/"))
def check_candidate(repo,head,item,items,blob,parse,sha,require,validate_schema,path_ok):
    p=item["platform"];scope=set(item["paths"])
    for k in ("entry","manifest","engine","reader"):
        path_ok(p[k]);require(public_path(p[k]),"PLATFORM_NONPUBLIC_PATH:"+p[k])
    for key,ref in (("engine","engine.mjs"),("reader","reader.mjs")):
        data=blob(repo,head,p[key],items)
        require(data==(PLAT/ref).read_bytes() and sha(data)==p[key+"_sha256"],"PLATFORM_ENGINE_BYTES_MISMATCH:"+key)
    raw=blob(repo,head,p["manifest"],items);m=parse(raw)
    require(m.get("uid")==item["uid"],"PLATFORM_TASK_UID")
    root=posixpath.dirname(p["manifest"]);assets={};media={}
    for role,pin in m["assets"].items():
        # Before reading any candidate path, require a single safe filename.
        name=pin["path"];require(isinstance(name,str) and re.fullmatch(r"[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*\.json",name),"PLATFORM_ASSET_PATH")
        file=root+"/"+name;require(file in scope and public_path(file),"PLATFORM_ASSET_OUT_OF_SCOPE:"+file)
        data=blob(repo,head,file,items);require(sha(data)==pin["sha256"],"PLATFORM_ASSET_HASH:"+file);assets[role]=parse(data)
        for im in pin.get("media",[]):
            name=im["path"];require(isinstance(name,str) and re.fullmatch(r"[A-Za-z0-9_-]+\.(png|webp)",name),"PLATFORM_MEDIA_PATH")
            file=root+"/"+name;require(file in scope and public_path(file),"PLATFORM_MEDIA_OUT_OF_SCOPE:"+file)
            data=blob(repo,head,file,items);require(sha(data)==im["sha256"],"PLATFORM_MEDIA_HASH")
            require((name.endswith(".png") and data.startswith(b"\x89PNG\r\n\x1a\n")) or (name.endswith(".webp") and data[:4]==b"RIFF" and data[8:12]==b"WEBP"),"PLATFORM_MEDIA_FORMAT")
            media[file]=im["sha256"]
    result=subprocess.run(["node",str(PLAT/"validate_bundle.mjs")],input=json.dumps({"manifest":m,"assets":assets}),text=True,capture_output=True,timeout=30,cwd=PLAT)
    require(result.returncode==0,"PLATFORM_BUNDLE_INVALID:"+result.stderr[-1000:])
    validated=json.loads(result.stdout)
    require(set(validated["challenge_fields"])=={x["field"] for x in item["construction"]["response_map"]},"PLATFORM_RESPONSE_MAP_MISMATCH")
    require(validated["challenge_stem"]==item["construction"]["task_stem"],"PLATFORM_TASK_STEM_CHANGED")
    expected=_load_entry().render_entry(p["entry"],p["manifest"],sha(raw),p["reader"])
    require(blob(repo,head,p["entry"],items)==expected,"PLATFORM_ENTRY_NOT_SHARED_TEMPLATE")
    intake_raw=blob(repo,head,p["intake"],items);intake=parse(intake_raw);validate_schema(intake,"reviewer-intake.schema.json")
    require(intake["stem"]==validated["challenge_stem"],"INTAKE_STEM_MISMATCH")
    require(item["uid"] not in intake["opaque_id"] and item["uid"] not in intake["stem"],"INTAKE_ID_EXPOSED")
    challenge_media={root+"/"+x["path"]:x["sha256"] for x in m["assets"]["challenge"].get("media",[])}
    require({x["path"]:x["sha256"] for x in intake["figures"]}==challenge_media and len(intake["figures"])==len(challenge_media),"INTAKE_FIGURE_MISMATCH")
    for im in intake["figures"]:require(sha(blob(repo,head,im["path"],items))==im["sha256"],"INTAKE_FIGURE_HASH")
    return {"opaque_id":intake["opaque_id"],"sha256":sha(intake_raw),"manifest_sha256":sha(raw)}
