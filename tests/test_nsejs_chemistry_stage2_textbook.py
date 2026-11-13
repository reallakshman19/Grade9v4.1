"""Agent A Chemistry C01-C07 candidate textbook integration contracts.

Technical checks only. Neither passing these tests nor a browser session grants
scientific, 28-QRT, source fidelity, or student release approval.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CHEM = ROOT / "curriculum" / "chemistry"
UNITS = {f"C{i:02d}": n for i, n in zip(range(1, 8), (6, 7, 6, 6, 6, 6, 7))}
OPS = {"RETRIEVE", "EXPLAIN", "APPLY", "MODEL", "REPRESENT", "SYNTHESIZE", "JUSTIFY"}
STAGES = {"predict", "attempt", "reconstruct", "diagnose", "repair", "boundary", "model_response"}


def load(relative: str) -> dict:
    return json.loads((CHEM / relative).read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def materials() -> dict:
    books = {k: load(f"authored/{k}-core1ab-book.v0.1.0.json") for k in UNITS}
    adapters = {k: load(f"adapters/{k}.v1.json") for k in UNITS}
    return {
        "books": books,
        "adapters": adapters,
        "concepts": load("registry/agent-a-canonical-concepts.v0.1.0.json"),
        "syllabus": load("syllabus/chemistry-syllabus.v1.json"),
        "blueprint": load("blueprint/chemistry-qrt.D3-D4.v0.1.0.json"),
        "schema": load("contracts/chem-topic-adapter.schema.v0.1.0.json"),
    }


def test_authoring_scope_and_demand_count(materials):
    books = materials["books"]
    assert len(books) == 7
    assert {k: len(b["subtopics"]) for k, b in books.items()} == UNITS
    assert sum(len(b["subtopics"]) for b in books.values()) == 44
    assert sum(len(s["demands"]) for b in books.values() for s in b["subtopics"]) == 132


def test_every_subtopic_has_connected_science_and_worked_model(materials):
    for unit, book in materials["books"].items():
        assert book["schema"] == "g9v41-chem-core1ab-book/v1", unit
        assert "HOLD" in book["academic_status"]
        for sub in book["subtopics"]:
            assert sub["id"].startswith("CHEM-" + unit + ".")
            assert len(sub["core1a_paragraphs"]) >= 3, sub["id"]
            assert all(len(x) >= 90 for x in sub["core1a_paragraphs"]), sub["id"]
            assert len(sub["entry_question"]) >= 20
            assert len(sub["representation"]) >= 80
            assert len(sub["worked_example"]["steps"]) >= 3
            assert len(sub["worked_example"]["check"]) >= 20
            assert all(len(sub["misconception"][k]) > 30 for k in ("wrong", "why", "repair"))
            assert len(sub["demands"]) == 3


def test_subtopics_match_stage0_and_scope_flags(materials):
    for unit, book in materials["books"].items():
        ref = next(x for x in materials["syllabus"]["units"] if x["id"] == unit)
        assert ref["owner_agent"] == "A"
        for sub, initial in zip(book["subtopics"], ref["subtopics"], strict=True):
            assert sub["id"] == initial["id"]
            assert sub["scope"] == initial["scope"]
    assert materials["books"]["C07"]["subtopics"][-1]["scope"] == "ENRICHMENT"
    assert materials["books"]["C04"]["subtopics"][4]["scope"] == "EXTENSION"


def test_adapter_schema_and_qrt_bindings(materials):
    schema = materials["schema"]
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    qrtcells = materials["blueprint"]["cells"]
    for unit, adapter in materials["adapters"].items():
        validator.validate(adapter)
        assert adapter["unit_id"] == unit
        assert adapter["status"] == "CANDIDATE"
        assert adapter["canonical_truth_status"] == "DRAFT"
        for sub in adapter["subtopics"]:
            ops = [x["primary_operation"] for x in sub["qrt_instances"]]
            assert len(set(ops)) >= 3
            assert set(ops) <= OPS
            assert sub["canonical_truth_status"] == "DRAFT"
            assert sub["status"] == "ACADEMIC_HOLD"
            for q in sub["qrt_instances"]:
                assert q["template_ref"] == f"QRT-{q['primary_operation']}-{q['band']}"
                assert q["band"] in ("D3", "D4")
                idx = "RETRIEVE EXPLAIN APPLY MODEL REPRESENT SYNTHESIZE JUSTIFY".split().index(q["primary_operation"]) + 1
                assert qrtcells[f"{q['band']}.{idx}"]["template_ref"] == q["template_ref"]
                assert q["canonical_concept_refs"] == sub["canonical_concept_refs"]
                assert q["source_bindings"][0]["role"] == "AUTHORED_PRACTICE"
                assert q["source_bindings"][0]["review_status"] == "CANDIDATE"


def test_adapter_and_book_tasks_match_without_duplication(materials):
    all_instance_ids = []
    for unit in UNITS:
        b = materials["books"][unit]
        a = materials["adapters"][unit]
        for textbook_sub, adapter_sub in zip(b["subtopics"], a["subtopics"], strict=True):
            assert textbook_sub["id"] == adapter_sub["subtopic_id"]
            for d, q in zip(textbook_sub["demands"], adapter_sub["qrt_instances"], strict=True):
                all_instance_ids.append(d["instance_id"])
                assert d["template_ref"] == q["template_ref"]
                assert d["core1b"]["attempt"] == q["student_task"]
                assert d["independent_check"] == q["independent_check"]
                assert "W" in q["slots"] and len(q["slots"]["W"]) > 30
    assert len(set(all_instance_ids)) == len(all_instance_ids) == 132


def test_core1b_has_attempt_repair_boundary_and_nondecorative_hints(materials):
    for book in materials["books"].values():
        for sub in book["subtopics"]:
            for d in sub["demands"]:
                cycle = d["core1b"]
                assert set(cycle) == STAGES
                assert all(len(cycle[k]) >= 30 for k in STAGES)
                assert len(d["hints"]) == 3
                assert all(len(h) >= 25 for h in d["hints"])
                assert cycle["model_response"] not in "\n".join(d["hints"])
                assert len(d["worked_reasoning"]) >= 50


def test_44_canonical_draft_refs_resolve(materials):
    reg = materials["concepts"]
    entries = reg["concepts"]
    assert len(entries) == 44
    assert len({e["concept_id"] for e in entries}) == 44
    names = {e["concept_id"] for e in entries}
    for e in entries:
        assert e["concept_id"].endswith("-CORE1A")
        assert e["canonical_truth_status"] == "AUTHOR_DRAFT_ACADEMIC_HOLD"
        assert (ROOT / e["content_path"]).is_file()
        assert len(e["content_git_blob_sha"]) == 40
    for adapter in materials["adapters"].values():
        for s in adapter["subtopics"]:
            assert set(s["canonical_concept_refs"]) <= names
    for _, target in reg["aliases"].items():
        assert target in names


def test_qrt_band_distribution_and_original_question_protection(materials):
    bands = Counter(d["band"] for book in materials["books"].values() for sub in book["subtopics"] for d in sub["demands"])
    assert bands["D3"] > 0 and bands["D4"] > 0
    for b in materials["books"].values():
        assert "HOLD" in b["academic_status"]
        assert all("IAPT" not in d["instance_id"] and "NSEJS-20" not in d["instance_id"]
                   for s in b["subtopics"] for d in s["demands"])


def test_html_routes_and_local_assets(materials):
    preview = CHEM / "preview"
    assert (preview / "index.html").is_file()
    for unit in UNITS:
        html = (preview / f"{unit}.html").read_text(encoding="utf-8")
        assert f"../authored/{unit}-core1ab-book.v0.1.0.json" in html
        assert 'src="reader.js"' in html
        assert 'href="reader.css"' in html
    reader = (preview / "reader.js").read_text(encoding="utf-8")
    assert "localStorage.getItem" in reader
    assert "localStorage.setItem" in reader
    assert "field.disabled=true" in reader
    assert "post.hidden=true" in reader
    assert "Storage unavailable" in reader or "storage unavailable" in reader.lower()


def test_c07_figures_exist_and_have_accessible_metadata(materials):
    c07 = materials["books"]["C07"]
    figures = [s for s in c07["subtopics"] if "figure_ref" in s]
    assert len(figures) == 4
    for s in figures:
        path = CHEM / "preview" / s["figure_ref"]
        assert path.is_file(), path
        contents = path.read_text(encoding="utf-8")
        assert "<svg" in contents and "<title" in contents and "<desc" in contents
        assert len(s["figure_alt"]) > 35


def test_scope_hold_and_no_auto_approval(materials):
    assert materials["blueprint"]["status"] == "DRAFT_OWNER_ACADEMIC_REVIEW"
    assert all(b["academic_status"] == "ACADEMIC_HOLD_AUTHOR_DRAFT" for b in materials["books"].values())
    assert all(a["status"] == "CANDIDATE" for a in materials["adapters"].values())
