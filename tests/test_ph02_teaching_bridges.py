"""PH02 additional Core1A constructions: teaching presence, not cognitive approval."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
BRIDGES=ROOT/"nsejs/physics/ph02/teaching-bridges.v1.json"
QRT=ROOT/"nsejs/physics/ph02/qrt-candidates.v1.json"


def test_all_ph02_extra_operations_have_distinct_original_teaching():
    data=json.loads(BRIDGES.read_text(encoding="utf-8"))
    qrt=json.loads(QRT.read_text(encoding="utf-8"))
    assert data["status"]=="AUTHOR_EXPOSED_CANDIDATE__ACADEMIC_HOLD"
    assert set(data["bridges"])=={f"PH02-F{i:02d}" for i in range(1,9)}
    for unit, items in data["bridges"].items():
        assert len(items)==2
        expected={x["op"] for x in qrt["tasks"] if x["unit"]==unit}
        assert len(expected)==2==len({x["op"] for x in items})
        assert {x["op"] for x in items}==expected
        for item in items:
            for name in ("title","teaching","worked","check"):
                assert len(item[name])>45
            assert item["worked"]!=next(x["prompt"] for x in qrt["tasks"]
                                        if x["unit"]==unit and x["op"]==item["op"])


def test_core1a_renderer_requires_two_bridges_before_success():
    js=(ROOT/"nsejs/physics/ph02/lesson.js").read_text(encoding="utf-8")
    assert 'bridgeData.bridges?.[uid]' in js
    assert 'bridges.length!==2' in js
    assert 'additional-constructions' in js
    assert 'throw Error("Missing or invalid Core1A operation bridge; HOLD")' in js
