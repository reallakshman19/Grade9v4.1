"""PH01 subtopic delivery routes; no academic qualification."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PH = ROOT / "nsejs/physics/curriculum/agent1/PH01/"
def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
def test_m01_m02_independent_routes_and_unchanged_content():
    routes = json.loads((PH / "ph01-subtopic-routes.r3_1.json").read_text(encoding="utf-8"))
    assert routes["release"] == "HOLD"
    for key in ("package", "support"):
        assert blob(ROOT / routes[key]["path"]) == routes[key]["git_blob_sha"]
    pack = json.loads((ROOT / routes["package"]["path"]).read_text(encoding="utf-8"))
    assert [u["subtopic_id"] for u in routes["units"]] == ["PH01-M01", "PH01-M02"]
    for u in routes["units"]:
        a, b = ROOT / u["core1a"], ROOT / u["core1b"]
        assert a.is_file() and b.is_file()
        a_html, b_html = a.read_text(encoding="utf-8"), b.read_text(encoding="utf-8")
        assert f'data-scope="{u["subtopic_id"]}"' in b_html
        assert "scoped-runtime.js" in b_html and "<iframe" not in b_html
        assert u["subtopic_id"] in a_html and "Academic HOLD" in a_html
        assert len(u["instance_ids"]) == 3 and u["qualified"] == 0
        assert set(u["instance_ids"]) == {c["id"] for c in pack["core1b"] if c["kind"]=="INSTANCE" and c["subtopic_id"]==u["subtopic_id"]}
        assert any(x["id"]==u["lesson_id"] and x["subtopic_id"]==u["subtopic_id"] for x in pack["core1a"])
        assert b.parent.name in a_html
        assert f'PH01/{a.parent.name}/index.html' in b_html
    main = routes["integrated_main"]
    assert set(main["cycle_ids"]) == {c["id"] for c in pack["core1b"] if c["kind"]=="MAIN"}
    assert 'data-scope="MAIN"' in (ROOT / main["path"]).read_text(encoding="utf-8")
    assert len(main["cycle_ids"]) == 3
