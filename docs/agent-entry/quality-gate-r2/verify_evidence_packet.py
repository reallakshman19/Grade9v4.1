#!/usr/bin/env python3
"""Structural evidence gate: never confuses a mechanical witness with academic truth.

Usage:
  python docs/agent-entry/quality-gate-r2/verify_evidence_packet.py PACKET.json
  python docs/agent-entry/quality-gate-r2/verify_evidence_packet.py --repo-root . PACKET.json
Return 0: evidence physically grounded, no detected HOLD or breach, still REVIEW_REQUIRED.
Return 2: missing/contradictory/held evidence; candidate cannot be promoted.
No author-written packet can return ACADEMIC_APPROVED.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMA_FILE = Path(__file__).with_name("evidence-packet.schema.json")

REF_ROLES = {
    ("science","primary_derivation_ref"):"SCIENCE_PRIMARY_DERIVATION",
    ("science","independent_check_ref"):"SCIENCE_INDEPENDENT_CHECK",
    ("science","units_signs_ref"):"SCIENCE_UNITS_AND_SIGNS",
    ("science","assumptions_limit_ref"):"SCIENCE_ASSUMPTIONS_AND_LIMIT",
    ("science","counterexample_ref"):"SCIENCE_COUNTEREXAMPLE",
    ("core1a","phenomenon_ref"):"CORE1A_PHENOMENON",
    ("core1a","prerequisite_ref"):"CORE1A_PREREQUISITE",
    ("core1a","causal_explanation_ref"):"CORE1A_CAUSAL_EXPLANATION",
    ("core1a","diagram_ref"):"CORE1A_DIAGRAM",
    ("core1a","foundation_ref"):"CORE1A_WORKED_FOUNDATION",
    ("core1a","connected_ref"):"CORE1A_WORKED_CONNECTED",
    ("core1a","advanced_ref"):"CORE1A_WORKED_ADVANCED",
    ("core1a","misconception_ref"):"CORE1A_MISCONCEPTION_REPAIR",
    ("core1a","synthesis_ref"):"CORE1A_SYNTHESIS",
    ("core1b","fresh_task_ref"):"CORE1B_FRESH_TASK",
    ("core1b","model_route_ref"):"CORE1B_MODEL_ROUTE",
    ("core1b","boundary_ref"):"CORE1B_BOUNDARY_TRANSFER",
    ("core1b","hint_nonleak_ref"):"CORE1B_HINT_NONLEAK",
    ("core1b","first_save_ref"):"CORE1B_FIRST_SAVE",
    ("core1b","revision_return_ref"):"CORE1B_REVISION_RETURN",
    ("core2","stem_figure_ref"):"CORE2_STEM_AND_FIGURE",
    ("core2","derivation_key_ref"):"CORE2_REASONING_KEY",
    ("browser","portrait_receipt_ref"):"QA_BROWSER_RECEIPT",
    ("browser","landscape_receipt_ref"):"QA_BROWSER_RECEIPT",
}
GOLDEN_NEGATIVE = {
    "WRONG_DIMENSION","WRONG_SIGN_OR_LIMIT","NUMERIC_CLONE","HINT_LEAK",
    "BAD_SOURCE_FIGURE","SAVE_FAILURE","STALE_REVISION","FALSE_REVIEW_BADGE",
}
BATCH_NEGATIVE = {"WRONG_DIMENSION","NUMERIC_CLONE","HINT_LEAK"}

BAD_CLAIMS = (
    "{Reviewed}", "Peer-Audited Module", "B1–B7 peer review verified",
    "Disciplinary Peer-Review Audit Completed",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized_problem(text: str) -> str:
    """Catch obvious numerical substitution; *not* a proof of real task novelty."""
    text = text.lower()
    text = re.sub(r"(?<![a-z])[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[-+]?\d+)?", "#", text)
    text = re.sub(r"\s+", " ", re.sub(r"[^a-z#]+", " ", text)).strip()
    return text


def validate(packet: dict, root: Path) -> dict:
    findings = []
    schema = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    failures = sorted(Draft202012Validator(schema).iter_errors(packet), key=str)
    for err in failures:
        findings.append("SCHEMA:" + "/".join(map(str, err.absolute_path)) + ":" + err.message[:220])
    if failures:
        return {"mechanical_status":"BLOCKED","academic_status":"HOLD","findings":findings}

    root = root.resolve()
    refs = {}
    files = set()
    used_excerpt = set()
    for e in packet["evidence"]:
        evid = e["id"]
        if evid in refs:
            findings.append("DUPLICATE_EVIDENCE_ID:"+evid)
            continue
        refs[evid] = e
        raw_path = e["path"]
        candidate = (root / raw_path).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            findings.append("PATH_ESCAPES_ROOT:"+evid)
            continue
        if candidate.suffix in {".json"} and candidate.name.endswith("packet.json"):
            findings.append("SELF_REFERENTIAL_PACKET:"+evid)
            continue
        if not candidate.is_file():
            findings.append("MISSING_EVIDENCE_FILE:"+evid)
            continue
        files.add(raw_path)
        blob = candidate.read_bytes()
        if sha256_bytes(blob) != e["sha256"]:
            findings.append("BYTE_HASH_MISMATCH:"+evid)
        try:
            lines = blob.decode("utf-8").splitlines()
        except UnicodeDecodeError:
            findings.append("NON_UTF8_EVIDENCE:"+evid)
            continue
        a,b = e["start_line"],e["end_line"]
        if b < a or b > len(lines):
            findings.append("BAD_LINE_RANGE:"+evid)
            continue
        text = "\n".join(lines[a-1:b])
        if e["excerpt"] not in text:
            findings.append("EXCERPT_NOT_AT_GIVEN_LINES:"+evid)
        exact = (raw_path,a,b,e["excerpt"])
        if exact in used_excerpt:
            findings.append("REUSED_IDENTICAL_PROOF:"+evid)
        used_excerpt.add(exact)
    if len(files) < 3:
        findings.append("INSUFFICIENT_DISTINCT_SOURCE_FILES:minimum_three")

    for (group, field), role in REF_ROLES.items():
        ref = packet[group][field]
        obj = refs.get(ref)
        if obj is None:
            findings.append("UNKNOWN_EVIDENCE_REF:"+group+":"+field+":"+ref)
        elif obj["role"] != role:
            findings.append("EVIDENCE_ROLE_MISMATCH:"+group+":"+field+":"+role)

    if packet["core1a"]["student_ready_path"] not in files:
        findings.append("CORE1A_PAGE_NOT_EVIDENCED")
    if packet["core1b"]["student_ready_path"] not in files:
        findings.append("CORE1B_PAGE_NOT_EVIDENCED")
    if packet["task"]["head_sha"] != packet["browser"]["head_sha"]:
        findings.append("BROWSER_HEAD_NOT_BOUND_TO_SOURCE_HEAD")

    if normalized_problem(packet["core1b"]["anchor_problem"]) == normalized_problem(packet["core1b"]["new_problem"]):
        findings.append("NUMERIC_REPARAMETERIZATION_DETECTED")
    if normalized_problem(packet["core1b"]["anchor_crux"]) == normalized_problem(packet["core1b"]["new_crux"]):
        findings.append("DECISIVE_W_IDENTICAL")
    if not packet["core1b"]["hints"]["blocked_until_first_save"]:
        findings.append("HINTS_UNLOCKED_BEFORE_FIRST_SAVE")

    main = packet["core1b"]["multiple_subtopic_main"]
    if main["contract_applies"]:
        if len(set(main["instance_ids"])) < 2 or len(set(main["subtopic_ids"])) < 2:
            findings.append("MAIN_NOT_MULTI_INSTANCE_MULTI_SUBTOPIC")
    elif packet["task"]["contract_version"].startswith("1.1"):
        findings.append("C06_V11_MULTI_SUBTOPIC_FLAG_MISSING")

    if packet["core2"]["figure_need"] == "REQUIRED" and packet["core2"]["figure_status"] != "PRESENT_AND_INSPECTED":
        findings.append("REQUIRED_FIGURE_MISSING")
    if packet["core2"]["figure_need"] == "NOT_REQUIRED" and packet["core2"]["figure_status"] != "NO_FIGURE_NEEDED":
        findings.append("FIGURE_NEED_STATUS_CONTRADICTION")

    requested_negative = GOLDEN_NEGATIVE if packet["task"]["delivery_kind"] == "GOLDEN_SAMPLE" else BATCH_NEGATIVE
    reported = [x["case"] for x in packet["negative_tests"]]
    if len(reported) != len(set(reported)):
        findings.append("DUPLICATE_NEGATIVE_CASE")
    for missing in sorted(requested_negative - set(reported)):
        findings.append("MISSING_ADVERSARIAL_TEST:"+missing)
    for test in packet["negative_tests"]:
        e=refs.get(test["log_ref"])
        if not e or e["role"] != "QA_NEGATIVE_LOG":
            findings.append("NEGATIVE_TEST_LOG_NOT_EVIDENCED:"+test["case"])
        elif test["observed_failure"] not in e["excerpt"]:
            findings.append("NEGATIVE_FAILURE_NOT_IN_LOG:"+test["case"])
        if not re.search(r"\b(REJECTED|BLOCKED|FAIL_CLOSED)\b", test["observed_failure"], re.I):
            findings.append("NEGATIVE_TEST_HAS_NO_REJECTION:"+test["case"])

    for name,needle in [("portrait_receipt_ref","1000x1600"),("landscape_receipt_ref","1600x1000")]:
        x=refs.get(packet["browser"][name])
        if x and needle not in x["excerpt"].replace(" ",""):
            findings.append("WRONG_BROWSER_VIEWPORT:"+name)
    for name in ["keyboard_and_touch","storage_failure","stale_revision","pre_first_help","figure_render"]:
        if packet["browser"][name] != "PASS":
            findings.append("BROWSER_GATE_HOLD:"+name)

    for page_name in ["core1a","core1b"]:
        raw_path = packet[page_name]["student_ready_path"]
        path = (root/raw_path).resolve()
        if path.is_file() and path.suffix.lower() in {".html",".htm",".js"}:
            source = path.read_text(encoding="utf-8")
            for bad in BAD_CLAIMS:
                if bad in source:
                    findings.append("UNSUPPORTED_REVIEW_BADGE:"+page_name+":"+bad)
            if "<iframe" in source.lower():
                findings.append("FORBIDDEN_IFRAME:"+page_name)
    if packet["self_audit"]["known_defects"]:
        findings.append("OPEN_DEFECTS_NOT_CLOSED:"+str(len(packet["self_audit"]["known_defects"])))
    if packet["self_audit"]["evidence_completeness"] != "AUTHOR_ASSERTED_COMPLETE":
        findings.append("AUTHOR_REPORTED_INCOMPLETE")
    return {
        "mechanical_status":"BLOCKED" if findings else "EVIDENCE_STRUCTURALLY_GROUNDED",
        "academic_status":"HOLD",
        "review_required":True,
        "owner_per_question_approval_required":False,
        "findings":sorted(set(findings)),
        "evidence_items":len(refs),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("packets",nargs="+",type=Path)
    ap.add_argument("--repo-root",type=Path,default=Path(__file__).resolve().parents[3])
    args = ap.parse_args(argv)
    result = []
    for file in args.packets:
        try:
            result.append({"packet":str(file),"result":validate(json.loads(file.read_text(encoding="utf-8")),args.repo_root)})
        except (ValueError,OSError,TypeError,KeyError) as e:
            result.append({"packet":str(file),"result":{"mechanical_status":"BLOCKED","academic_status":"HOLD","findings":[type(e).__name__+":"+str(e)[:200]]}})
    print(json.dumps({"quality_gate":"AUTHOR_PACKET_ONLY","results":result},indent=2,ensure_ascii=False))
    return 2 if any(r["result"]["mechanical_status"]=="BLOCKED" for r in result) else 0


if __name__=="__main__":
    sys.exit(main())
