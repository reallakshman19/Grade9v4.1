"""Ensure source-unqualified Circuit worksheet questions are discoverable without false approval claims."""
from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("search_builder",ROOT/"tools/build_search_index.py")
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_circuit_worksheet_index_has_all_56_and_valid_reader_links():
    docs=module.build_question_documents(ROOT,module.DEFAULT_SYNONYMS)
    by_id={d["original_id"]:d for d in docs}
    circuit=[d for d in docs if d["original_id"].startswith("NSEJS-CIRC-L")]
    assert len(circuit)==56
    ids=[d["original_id"] for d in circuit]
    assert ids==[f"NSEJS-CIRC-L1-Q{i:02d}" for i in range(1,37)]+[
               f"NSEJS-CIRC-L2-Q{i:02d}" for i in range(1,21)]
    for d in circuit:
        assert d["badge"]=="SOURCE WORKSHEET · ACADEMIC HOLD"
        assert "HOLD" in d["breadcrumb"]
        assert d["url"]=="nsejs/physics/index.html?topic=circuits#"+d["original_id"]
        assert "worksheet" in d["search_text"]
        assert "Reviewed" not in d["badge"]
        assert d["hints"] == []
        assert d["is_nsejs"] is True and d["subject"]=="Physics"
        assert d["category"]=="question"
    assert len(set(d["id"] for d in docs))==len(docs)


def test_committed_search_manifest_covers_every_worksheet_candidate():
    import hashlib
    import json
    from urllib.parse import urlparse,parse_qs
    a=(ROOT/"data/learner-search-index.v1.json").read_bytes()
    b=(ROOT/"nsejs/data/learner-search-index.v1.json").read_bytes()
    assert a==b
    manifest=json.loads((ROOT/"data/learner-search-manifest.v1.json").read_text())
    assert (ROOT/"nsejs/data/learner-search-manifest.v1.json").read_bytes()==(
      ROOT/"data/learner-search-manifest.v1.json").read_bytes()
    assert hashlib.sha256(a).hexdigest()==manifest["sha256"]
    docs=json.loads(a)
    assert manifest["total_documents"]==len(docs) and len(docs)>402
    assert manifest["by_category"]["question"]==sum(d["category"]=="question" for d in docs) >=347
    circuit=[d for d in docs if d["original_id"].startswith("NSEJS-CIRC-L")]
    assert len(circuit)==56
    assert len(set(x["id"] for x in docs))==len(docs)
    for q in circuit:
        assert q["badge"]=="SOURCE WORKSHEET · ACADEMIC HOLD"
        assert q["hints"] == []
        link=urlparse(q["url"])
        assert (ROOT/link.path).is_file()
        assert parse_qs(link.query).get("topic")==["circuits"]
        assert link.fragment==q["original_id"]
        assert not q["url"].startswith("nsejs/physics/authored-practice")
