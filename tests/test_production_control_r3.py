"""Real Git and OpenSSL adversarial fixtures; never real reviewer receipts."""
from __future__ import annotations
import base64, copy, importlib.util, json, subprocess, sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
CONTROL=ROOT/"docs/agent-entry/production-control-r3"
sys.path.insert(0,str(CONTROL))
import control as C
import release as R

def git(root,*args):return subprocess.check_output(["git","-C",str(root),*args],stderr=subprocess.PIPE).decode().strip()
def write(root,path,data):
    p=root/path;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes(data if isinstance(data,bytes) else data.encode() if isinstance(data,str) else C.canonical(data))
def save(root,message="fixture"):
    git(root,"add","-A");git(root,"commit","-m",message);return git(root,"rev-parse","HEAD")
def fresh(tmp):
    root=tmp/"repo";root.mkdir();git(root,"init");git(root,"config","user.email","fixture@example.invalid");git(root,"config","user.name","Fixture Only")
    write(root,"index.html","<html><body>Technical preview HOLD</body></html>")
    write(root,"nsejs/physics/ph05/units.v1.json",{"legacy":True})
    write(root,"nsejs/physics/textbook/PH06/U08/index.html","Old unadmitted candidate")
    write(root,"nsejs/physics/ph06/reader.js","// baseline")
    write(root,"nsejs/data/learner-search-index.v1.json",[{"url":"index.html","category":"page"}])
    write(root,"review/private-source.pdf",b"private example bytes")
    legacy=save(root,"pre-control preview")
    policy=json.loads((CONTROL/"policy.v1.json").read_text());policy["legacy_preview_baseline"]=legacy
    write(root,C.POLICY,policy)
    base=save(root,"trusted control");return root,base,policy
def make_key(tmp,key_id="owner",principal="trusted-owner",roles=("OWNER",)):
    priv=tmp/(key_id+".pem");pub=tmp/(key_id+".pub")
    subprocess.run(["openssl","genpkey","-algorithm","ED25519","-out",str(priv)],check=True,capture_output=True)
    subprocess.run(["openssl","pkey","-in",str(priv),"-pubout","-out",str(pub)],check=True,capture_output=True)
    return priv,{"id":key_id,"principal":principal,"roles":list(roles),"public_key_pem":pub.read_text()}
def make_receipt(tmp,priv,key,purpose,binding,subject,decision,details=None):
    rec={"schema":"g9-r3-receipt/v1","key_id":key["id"],"purpose":purpose,"binding":binding,"subject":subject,"decision":decision,"issued_at":"2020-01-01T00:00:00Z","details":details or {}}
    path=tmp/"record";sig=tmp/"signature";path.write_bytes(C.canonical(rec))
    subprocess.run(["openssl","pkeyutl","-sign","-inkey",str(priv),"-rawin","-in",str(path),"-out",str(sig)],check=True,capture_output=True)
    return {"record":rec,"signature":base64.b64encode(sig.read_bytes()).decode()}
def trust(*keys):return {"schema":"g9-r3-trust/v1","keys":list(keys)}
def reason(result,part):
    assert result["status"]=="BLOCKED",result
    assert part in result["reason"],result

@pytest.mark.parametrize("path",[
    "nsejs/physics/ph03/source-led-r2/reader.js",
    "nsejs/physics/ph05/source-led-r2/figures/solution.svg",
    "nsejs/physics/ph06/reader.js",
    "nsejs/physics/core1/PH04/W01/index.html",
    "nsejs/physics/textbook/PH06/U09/index.html",
    "nsejs/data/physics-core2-candidates.v1.json",
    "nsejs/chemistry/textbook/index.html",
    "nsejs/biology/index.html",
    "data/learner-search-index.v1.json",
    "js/site-search.js",
    "new-unclassified-chapter.html",
    ".github/workflows/unknown-bypass.yml"
])
def test_freeze_covers_known_and_unknown_content(tmp_path,path):
    root,base,_=fresh(tmp_path);write(root,path,"new content");head=save(root)
    reason(C.gate(root,base,head,trust()),"NEW_LEARNER_CONTENT_FROZEN")

def test_delete_rename_and_policy_self_bypass(tmp_path):
    root,base,policy=fresh(tmp_path)
    git(root,"mv","nsejs/physics/ph06/reader.js","reader-hidden.js")
    policy["governance_prefixes"].append("nsejs/");write(root,C.POLICY,policy);head=save(root)
    assert "nsejs/physics/ph06/reader.js" in C.changed(root,base,head)
    reason(C.gate(root,base,head,trust()),"NEW_LEARNER_CONTENT_FROZEN")
def test_receipt_namespace_cannot_hide_executable_content(tmp_path):
    root,base,_=fresh(tmp_path);write(root,C.EVID+"conftest.py","raise RuntimeError()");head=save(root)
    reason(C.gate(root,base,head,trust()),"NON_EVIDENCE_FILE")
def test_unsigned_governance_change_blocked(tmp_path):
    root,base,_=fresh(tmp_path);write(root,"AGENTS.md","Try to bypass")
    head=save(root);reason(C.gate(root,base,head,trust()),"MISSING_FILE")
def test_real_owner_signature_governance_only(tmp_path):
    root,base,_=fresh(tmp_path);priv,key=make_key(tmp_path)
    write(root,"AGENTS.md","New control explanation");h=save(root)
    fp=C.fingerprint(C.tree(root,h))
    receipt=make_receipt(tmp_path,priv,key,"GOVERNANCE",fp,base,"AUTHORIZED")
    write(root,C.EVID+"governance-receipt.json",receipt);head=save(root)
    assert C.fingerprint(C.tree(root,head))==fp
    assert C.gate(root,base,head,trust(key))["status"]=="CONTROL_OR_EVIDENCE_ONLY"
    write(root,"AGENTS.md","Changed after review");head=save(root)
    reason(C.gate(root,base,head,trust(key)),"RECEIPT_SCOPE_OR_REVISION_MISMATCH")
def test_forged_and_wrong_role_receipt(tmp_path):
    priv,key=make_key(tmp_path);other,otherkey=make_key(tmp_path,"other","author",("R00",))
    receipt=make_receipt(tmp_path,other,otherkey,"GOVERNANCE","a"*64,"b"*40,"AUTHORIZED")
    with pytest.raises(C.Block,match="UNTRUSTED_SIGNER"):C.signed(receipt,trust(key,otherkey),"GOVERNANCE","a"*64,"b"*40,"AUTHORIZED","OWNER")
    receipt["record"]["key_id"]=key["id"]
    with pytest.raises(C.Block,match="INVALID_RECEIPT_SIGNATURE"):C.signed(receipt,trust(key),"GOVERNANCE","a"*64,"b"*40,"AUTHORIZED","OWNER")
    r=make_receipt(tmp_path,other,otherkey,"R00","a"*64,"task","ACCEPTED")
    with pytest.raises(C.Block,match="AUTHOR_SELF_APPROVAL"):C.signed(r,trust(otherkey),"R00","a"*64,"task","ACCEPTED","R00",["author"])
def test_signed_policy_cannot_activate_without_separate_golden_adoption(tmp_path):
    root,base,p=fresh(tmp_path);priv,key=make_key(tmp_path)
    p.update(phase="ACTIVE_AFTER_OWNER_GOLDEN",production_enabled=True);write(root,C.POLICY,p);h=save(root)
    fp=C.fingerprint(C.tree(root,h));write(root,C.EVID+"governance-receipt.json",make_receipt(tmp_path,priv,key,"GOVERNANCE",fp,base,"AUTHORIZED"));head=save(root)
    reason(C.gate(root,base,head,trust(key)),"ACTIVATION_REQUIRES_SEPARATE_ADOPTION_WORKPACK")
def test_stale_base_rejected(tmp_path):
    root,base,_=fresh(tmp_path);write(root,C.EVID+"note.md","author note");head=save(root)
    git(root,"checkout","--detach",base);write(root,C.EVID+"different.md","new main");newbase=save(root)
    reason(C.gate(root,newbase,head,trust()),"STALE_BRANCH_REBASE_REQUIRED")
def test_unsigned_golden_submission_cannot_bypass_freeze(tmp_path):
    root,base,_=fresh(tmp_path);write(root,"nsejs/physics/ph06/reader.js","new candidate")
    write(root,C.EVID+"submissions/golden.json",{"workpack_path":C.EVID+"workpacks/golden.json","design_commit":base,"packet_paths":{}})
    head=save(root);reason(C.gate(root,base,head,trust()),"MISSING_FILE")

def design_fixture(root,base):
    pins=[]
    for n,role in enumerate(sorted(C.PIN_ROLES)):
        p="physics/wpe/actual-reference.md" if role=="WPE_COMPARATOR" else f"authority/pin-{n}.md"
        data=f"Distinct synthetic pinned authority input for {role}.".encode();write(root,p,data)
        pins.append({"role":role,"path":p,"sha256":C.sha(data)})
    h=save(root)
    w={"schema":"g9-r3-design/v1","id":"PH06-design","subject":"Physics","topic_id":"PH06","authors":["fixture-author"],"route":"CURRICULUM_FIRST","delivery_kind":"GOLDEN_SAMPLE","pins":pins,"items":[{"uid":"fixture-task","subtopic_id":"PH06-U08","core2_identity":"fixture-source","source_role":"AUTHORED_TRANSFER","direct_exam_credit":0,"sources":[],"cell":"D3.4","paths":["nsejs/physics/ph06/reader.js"],"construction":{k:"A different precise synthetic teaching construction for "+k for k in ("X","Y","Z","W","anchor_W","fresh_W","wrong_model","boundary","figure_job","diagnosis_rule","wpe_comparison")}}]}
    w["items"][0]["construction"].update(prerequisites=["Density and geometry"],teaching_obligations=["Compute actual displacement at boundary A.","Reject invalid continued geometry at boundary B.","Verify the pressure balance independently."])
    return h,w
def test_design_needs_distinct_pinned_authority_and_no_credit_inflation(tmp_path):
    root,base,_=fresh(tmp_path);h,w=design_fixture(root,base)
    C.workpack_design(root,h,w,C.tree(root,h))
    bad=copy.deepcopy(w);bad["items"][0]["direct_exam_credit"]=1
    with pytest.raises(C.Block,match="AUTHORED_TRANSFER_FALSE_EXAM_CREDIT"):C.workpack_design(root,h,bad,C.tree(root,h))
    bad=copy.deepcopy(w);bad["items"][0]["construction"]["fresh_W"]=bad["items"][0]["construction"]["anchor_W"]
    with pytest.raises(C.Block,match="IDENTICAL_DECISIVE_W"):C.workpack_design(root,h,bad,C.tree(root,h))
    bad=copy.deepcopy(w);bad["items"][0]["cell"]="D3.1"
    with pytest.raises(C.Block,match="D31_PAUSED"):C.workpack_design(root,h,bad,C.tree(root,h))
    bad=copy.deepcopy(w);bad["pins"][0]["sha256"]="0"*64
    with pytest.raises(C.Block,match="PIN_HASH_MISMATCH"):C.workpack_design(root,h,bad,C.tree(root,h))
    bad=copy.deepcopy(w);bad["items"][0]["source_role"]="DIRECT_EXAM_EVIDENCE"
    with pytest.raises(C.Block,match="DIRECT_EXAM_WITHOUT_SOURCE"):C.workpack_design(root,h,bad,C.tree(root,h))
def test_direct_source_missing_figure_or_key_rejected(tmp_path):
    root,base,_=fresh(tmp_path);h,w=design_fixture(root,base)
    w["items"][0]["sources"]=[{"identity":"fixture-Q38","role":"DIRECT_EXAM_EVIDENCE","paper_sha256":"a"*64,"key_sha256":None,"figure_need":"REQUIRED","figure_sha256":None,"rights":"VERIFIED_BY_CUSTODIAN"}]
    with pytest.raises(C.Block,match="DIRECT_SOURCE_CUSTODY_HOLD"):C.workpack_design(root,h,w,C.tree(root,h))
    w["items"][0]["sources"][0]["key_sha256"]="b"*64
    with pytest.raises(C.Block,match="DIRECT_SOURCE_FIGURE_MISSING"):C.workpack_design(root,h,w,C.tree(root,h))
def test_signed_preview_stages_only_exact_manifest(tmp_path):
    root,base,_=fresh(tmp_path);priv,key=make_key(tmp_path)
    items=C.tree(root,base);fp=C.fingerprint(items)
    m={"schema":"g9-r3-publication/v1","kind":"TECHNICAL_PREVIEW_ONLY","content_fingerprint":fp,"files":[{"path":"index.html","sha256":C.sha(C.blob(root,base,"index.html",items))}]}
    mp=C.EVID+"publication-manifest.json";raw=C.canonical(m);write(root,mp,raw)
    write(root,C.EVID+"release-receipt.json",make_receipt(tmp_path,priv,key,"PREVIEW_RELEASE",C.sha(raw),fp,"AUTHORIZED"));head=save(root)
    out=tmp_path/"public";r=R.stage(root,head,mp,out,trust(key),base)
    assert r["status"]=="AUTHORIZED_TECHNICAL_PREVIEW_STAGED" and r["academic_status"]=="HOLD"
    assert [p.name for p in out.iterdir()]==["index.html"]
    assert (out/"index.html").read_bytes()==C.blob(root,base,"index.html")
    with pytest.raises(C.Block,match="UNTRUSTED_SIGNER"):R.stage(root,head,mp,tmp_path/"unsigned",trust(),base)
    # A signed manifest cannot include private originals.
    m["files"].append({"path":"review/private-source.pdf","sha256":C.sha(C.blob(root,base,"review/private-source.pdf"))})
    raw=C.canonical(m);write(root,mp,raw);write(root,C.EVID+"release-receipt.json",make_receipt(tmp_path,priv,key,"PREVIEW_RELEASE",C.sha(raw),fp,"AUTHORIZED"));head=save(root)
    with pytest.raises(C.Block,match="NONPUBLIC_RELEASE_PATH"):R.stage(root,head,mp,tmp_path/"private",trust(key),base)
    # A signed manifest cannot release an unapproved new chapter.
    write(root,"nsejs/physics/ph06/new.html","new chapter");head=save(root)
    with pytest.raises(C.Block,match="FROZEN_CONTENT_IN_RELEASE_TREE"):R.stage(root,head,mp,tmp_path/"new",trust(key),base)
def test_release_rejects_search_to_unpublished_path(tmp_path):
    root,base,_=fresh(tmp_path);priv,key=make_key(tmp_path)
    items=C.tree(root,base);fp=C.fingerprint(items);path="nsejs/data/learner-search-index.v1.json"
    # The search row is valid but its target is deliberately omitted; use alternate
    # root entrypoint under the baseline to demonstrate explicit closure.
    # index.html is mandatory, so mutate baseline fixture through a new control baseline.
    write(root,path,[{"url":"nsejs/physics/textbook/PH06/U08/index.html","category":"tablet"}]);legacy=save(root)
    p=C.load_policy(root,legacy);p["legacy_preview_baseline"]=legacy;write(root,C.POLICY,p);base=save(root)
    items=C.tree(root,base);fp=C.fingerprint(items)
    m={"schema":"g9-r3-publication/v1","kind":"TECHNICAL_PREVIEW_ONLY","content_fingerprint":fp,"files":[{"path":n,"sha256":C.sha(C.blob(root,base,n,items))} for n in ("index.html",path)]}
    raw=C.canonical(m);mp=C.EVID+"publication-manifest.json";write(root,mp,raw);write(root,C.EVID+"release-receipt.json",make_receipt(tmp_path,priv,key,"PREVIEW_RELEASE",C.sha(raw),fp,"AUTHORIZED"));head=save(root)
    with pytest.raises(C.Block,match="SEARCH_TARGET_NOT_PUBLISHED"):R.stage(root,head,mp,tmp_path/"public",trust(key),base)
@pytest.mark.parametrize("path",["nsejs/physics/curriculum/agent1/private.json","nsejs/physics/review/evidence.html","physics/wpe/official-answer-key.pdf","workspace/file.json","review/secret.json","nsejs/../private.html"])
def test_public_path_denial(path):
    try: assert not R.public_path(path)
    except C.Block: assert ".." in path

def test_forged_receipt_cannot_be_merged_as_evidence_only(tmp_path):
    root,base,_=fresh(tmp_path);priv,key=make_key(tmp_path)
    path=C.EVID+"receipts/fixture/R00-task.json"
    write(root,path,make_receipt(tmp_path,priv,key,"R00","a"*64,"task","ACCEPTED"))
    head=save(root)
    reason(C.gate(root,base,head,trust(key)),"UNTRUSTED_SIGNER")
def test_duplicate_public_key_cannot_impersonate_independent_roles(tmp_path):
    priv,key=make_key(tmp_path);other=dict(key,id="different",principal="another",roles=["R00"])
    with pytest.raises(C.Block,match="REUSED_TRUST_PUBLIC_KEY"):C.trust_keys(trust(key,other))

def test_generated_preview_requires_exact_signed_final_bytes(tmp_path):
    root,base,p=fresh(tmp_path);priv,key=make_key(tmp_path)
    # Synthetic pinned builder only: actual repository builder is replayed in dedicated CI.
    write(root,"tools/build_search_index.py","from pathlib import Path\np=Path(__file__).resolve().parents[1]/'index.html'\np.write_text('<html>Generated HOLD</html>')\n")
    write(root,"tools/search_learner_pages.py","# frozen helper\n")
    legacy=save(root);p["legacy_preview_baseline"]=legacy;write(root,C.POLICY,p);base=save(root)
    items=C.tree(root,base);fp=C.fingerprint(items)
    mp=C.EVID+"publication-manifest.json"
    m={"schema":"g9-r3-publication/v1","kind":"TECHNICAL_PREVIEW_ONLY","content_fingerprint":fp,"build_mode":"FROZEN_SEARCH_R1","files":[{"path":"index.html","sha256":C.sha(b"<html>Generated HOLD</html>")}]}
    raw=C.canonical(m);write(root,mp,raw);write(root,C.EVID+"release-receipt.json",make_receipt(tmp_path,priv,key,"PREVIEW_RELEASE",C.sha(raw),fp,"AUTHORIZED"));head=save(root)
    assert R.stage(root,head,mp,tmp_path/"public",trust(key),base)["status"]=="AUTHORIZED_TECHNICAL_PREVIEW_STAGED"
    assert (tmp_path/"public/index.html").read_text()=="<html>Generated HOLD</html>"
    m["files"][0]["sha256"]="0"*64;raw=C.canonical(m);write(root,mp,raw);write(root,C.EVID+"release-receipt.json",make_receipt(tmp_path,priv,key,"PREVIEW_RELEASE",C.sha(raw),fp,"AUTHORIZED"));head=save(root)
    with pytest.raises(C.Block,match="RELEASE_BYTE_MISMATCH"):R.stage(root,head,mp,tmp_path/"bad",trust(key),base)


def _r3_pages_preflight_script():
    """Extract the deployed preflight, not a parallel test-only implementation."""
    import textwrap
    data=(ROOT/".github/workflows/deploy.yaml").read_text(encoding="utf-8")
    start=data.index("      - name: Check externally authorized release prerequisites (fail closed)")
    start=data.index("        run: |\n",start)+len("        run: |\n")
    end=data.index("      - name: Checkout externally pinned control code",start)
    return textwrap.dedent(data[start:end])


@pytest.mark.parametrize("content_changed", [False, True])
def test_pages_r3_frozen_content_preflight_exact_git_gate(tmp_path, content_changed):
    """Governance and receipt-only reach the trusted verifier; frozen content never does."""
    import os
    repo,control_rev,policy=fresh(tmp_path)
    write(repo,C.EVID+"publication-manifest.json","{}\n")
    write(repo,C.EVID+"release-receipt.json","{}\n")
    if content_changed:
        write(repo,"nsejs/physics/ph06/reader.js","// unauthorized new content\n")
    head=save(repo,"pages release candidate")
    (tmp_path/"repo").rename(tmp_path/"candidate")
    output=tmp_path/"output"
    env=dict(os.environ,CONTROL_SHA=control_rev,
             TRUST_JSON='{"schema":"g9-r3-trust/v1","keys":[]}',
             REF="refs/heads/main",GITHUB_SHA=head,GITHUB_OUTPUT=str(output))
    result=subprocess.run(["bash","-e","-c",_r3_pages_preflight_script()],
                          cwd=tmp_path,env=env,capture_output=True,text=True)
    if content_changed:
        assert result.returncode!=0,(result.stdout,result.stderr)
        assert "FROZEN_CONTENT_IN_RELEASE_TREE" in result.stdout
        assert "nsejs/physics/ph06/reader.js" in result.stdout
        assert not output.exists()
    else:
        assert result.returncode==0,(result.stdout,result.stderr)
        assert output.read_text().strip()=="sha="+control_rev
        # This preflight does NOT check signatures; the real stage still invokes
        # the externally pinned trusted implementation, which rejects these
        # deliberately unsigned fixture receipts.
        workflow=(ROOT/".github/workflows/deploy.yaml").read_text()
        assert "python trusted/docs/agent-entry/production-control-r3/release.py" in workflow


def test_r3_frozen_search_diagnostic_not_a_routine_pr_gate():
    """Frozen-search builder drift must be visible manually, never silently authorized."""
    workflow=(ROOT/".github/workflows/production-control-r3-ci.yml").read_text()
    step=workflow.split("      - name: Frozen unified-search diagnostic (manual only, never published)",1)
    assert len(step)==2, "Keep an explicit manual frozen-search diagnostic"
    assert step[1].split("      - ",1)[0].find("if: github.event_name == 'workflow_dispatch'")>=0
    assert "preview_build.py" in step[1].split("      - uses:",1)[0]
    trusted=(ROOT/".github/workflows/production-control-r3-trusted.yml").read_text()
    assert "pull_request_target:" in trusted
    assert "g9/r3-production-decision" in trusted
    release=(ROOT/".github/workflows/deploy.yaml").read_text()
    assert "python trusted/docs/agent-entry/production-control-r3/release.py" in release


def test_owner_preview_publication_exception_explicit_and_restricted():
    """No preview pass may masquerade as signed R3/academic acceptance."""
    preview=(ROOT/".github/workflows/owner-technical-preview-pages.yml").read_text()
    assert "workflow_dispatch:" in preview
    assert "push:" in preview and "branches: [main]" in preview
    assert "paths:\n      - .github/workflows/owner-technical-preview-pages.yml" in preview
    assert "pull_request:" not in preview and "pull_request_target:" not in preview
    assert '"review", "tests", "tools", "src"' in preview
    assert '"workspace"' in preview
    assert '"academic_status": "HOLD"' in preview
    assert '"r3_signed_production_release": False' in preview
    assert "actions/upload-pages-artifact@v4" in preview
    assert "actions/deploy-pages@v4" in preview
    signed=(ROOT/".github/workflows/deploy.yaml").read_text()
    assert "python trusted/docs/agent-entry/production-control-r3/release.py" in signed
    assert "G9_R3_TRUST_JSON" in signed
    assert "github-pages" in signed
