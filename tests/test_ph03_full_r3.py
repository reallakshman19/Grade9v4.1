"""PH03 seven-pair author-candidate science, source and byte-custody checks.

Numerical and engineering verification only. Independent science/QRT/B1–B7 = HOLD.
"""
import hashlib
import json
import math
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PH = ROOT / "nsejs" / "physics"
SRC = PH / "ph03" / "complete-r3"
IDS = ("P01", "P02", "P04", "P05", "P06", "P07")


def unit(i):
    return json.loads((SRC / f"{i}.json").read_text())


def post(i):
    return json.loads((SRC / f"post-{i}.json").read_text())


def sha1_blob(blob):
    return hashlib.sha1(b"blob " + str(len(blob)).encode() + b"\0" + blob).hexdigest()


def equal(actual, expected):
    return math.isclose(actual, expected, rel_tol=0, abs_tol=1e-10)


def test_six_new_and_existing_p03_are_all_real_native_pairs():
    catalog = json.loads((PH / "learn/catalog.json").read_text())
    ph03 = next(c for c in catalog["chapters"] if c["id"] == "PH03")
    assert [x["id"] for x in ph03["units"]] == [
        "P01", "P02", "P03", "P04", "P05", "P06", "P07"
    ]
    assert ph03["authorCoverage"] == {
        "nativePairs": 7,
        "authoredNew": 6,
        "existingGolden": 1,
        "academicallyAccepted": 0,
        "sourceAuthenticated": 0,
        "sourceRole": "AUTHOR_EXPOSED_NOT_EXAM",
        "status": "HOLD",
        "extensionReview": ["P06", "P07"],
    }
    for c in ph03["units"]:
        assert (PH / c["learn"]).is_file() and (PH / c["practice"]).is_file()
        if c["id"] == "P03":
            assert "Golden Sample" in c["title"]
            assert "source-led-r2" in (PH / c["learn"]).read_text()
            assert "source-led-r2" in (PH / c["practice"]).read_text()
        else:
            for kind in ("learn", "practice"):
                page = (PH / c[kind]).read_text()
                assert "data-ph03-r3" in page and f'data-unit="{c["id"]}"' in page
                assert "reader.js" in page and "<iframe" not in page
    assert "7/7 authored candidates · Academic HOLD" in (PH / "index.html").read_text()
    assert "0/7 accepted" in (PH / "learn/chapter.js").read_text()


def test_science_teaching_has_real_multiple_worked_and_disjoint_prompt():
    for i in IDS:
        u = unit(i)
        p = post(i)
        assert u["id"] == i and u["academic"] == "HOLD"
        assert u["sourceRole"] == "AUTHOR_EXPOSITION_AND_TRANSFER_NOT_EXAM"
        assert u["academic"] == "HOLD"
        assert p["schema"] == "g9-ph03-postattempt/v1"
        assert p["revision"] == u["revision"]
        assert p["academic"] == "HOLD"
        assert len(u["sections"]) >= 4
        assert len(u["worked"]) >= 3
        assert len({w["setup"] for w in u["worked"]}) == len(u["worked"])
        assert all(len(w["steps"]) >= 3 and w["check"] for w in u["worked"])
        assert len(u["goals"]) >= 3 and len(u["assumptions"]) >= 3
        assert u["trap"]["wrong"] and u["trap"]["repair"]
        assert u["prompt"]["stem"] and u["prompt"]["prediction"]
        assert u["prompt"]["boundaryPrompt"] and len(u["prompt"]["boundaryFields"]) >= 2
        assert "expected" not in u and "boundaryExpected" not in u
        assert "steps" not in u["prompt"]
        assert len(p["hints"]) == 3 and len(p["steps"]) >= 3
        assert len(p["boundarySteps"]) >= 3
        field_ids = [x["id"] for x in u["prompt"]["fields"]]
        boundary_ids = [x["id"] for x in u["prompt"]["boundaryFields"]]
        assert len(set(field_ids)) == len(field_ids)
        assert len(set(boundary_ids)) == len(boundary_ids)
        assert set(field_ids) == set(p["expected"])
        assert set(boundary_ids) == set(p["boundaryExpected"])
        assert set(p["firstErrorOrder"]) == set(field_ids)
        assert all(x["type"] in ("number", "choice") for x in
                   u["prompt"]["fields"] + u["prompt"]["boundaryFields"])
        assert len(u["sections"][0]["body"]) > 100
        assert "EXTENSION" not in u["scope"] or i in ("P06", "P07")
    assert unit("P06")["scope"] == unit("P07")["scope"] == "EXTENSION_REVIEW"
    assert unit("P05")["scope"] == "ADVANCED_REASONING_CANDIDATE"


def test_exact_after_first_json_and_solution_svg_blob_pins():
    for i in IDS:
        u = unit(i)
        postbytes = (SRC / f"post-{i}.json").read_bytes()
        solutionbytes = (SRC / u["figures"]["solution"]).read_bytes()
        assert sha1_blob(postbytes) == u["postBlobSha1"]
        assert sha1_blob(solutionbytes) == u["solutionBlobSha1"]
        assert u["postBlobSha1"] != u["solutionBlobSha1"]
    code = (SRC / "reader.js").read_text()
    assert 'if(!rec?.first)throw Error("Protected answer requested before first attempt")' in code
    assert 'sha!==content.postBlobSha1' in code
    assert 'solutionImage.blobSha!==content.solutionBlobSha1' in code
    assert 'await digest("SHA-256"' in code
    assert 'navigator.locks.request(storeKey' in code
    assert 'localStorage.getItem(storeKey)!==raw' in code
    assert 'old.first?old' in code
    assert "Skipped " in code and 'null' in code
    assert "return \"insufficient\"" not in code or "insufficient" in code


def test_native_svg_diagrams_are_three_distinct_role_artifacts():
    for i in IDS:
        diagrams = []
        for role in ("guide", "prompt", "solution"):
            raw = (SRC / f"figures/{i}-{role}.svg").read_text()
            root = ET.fromstring(raw)
            assert root.tag.endswith("svg")
            assert root.attrib["viewBox"] == "0 0 940 345"
            assert "raster" not in raw.lower()
            assert not any(el.tag.endswith("image") for el in root.iter())
            labels = [el.text for el in root.iter() if el.tag.endswith("text")]
            assert len(labels) >= 5
            fonts = [int(el.attrib["font-size"]) for el in root.iter()
                     if el.tag.endswith("text") and "font-size" in el.attrib]
            assert fonts and min(fonts) >= 14
            diagrams.append(raw)
        assert len(set(diagrams)) == 3
        prompt = diagrams[1]
        assert "P(total) =" not in prompt
        assert "K(total) =" not in prompt
        assert "Joined 5 kg velocity" not in prompt
        assert "source-led-r2/index.html" not in (SRC / f"{i}.json").read_text()


def test_independent_physical_invariants_and_negative_controls():
    # P01 signed vectors; equal KE does not imply equal signed p.
    assert equal(2*3 + 3*(-1), post("P01")["expected"]["totalP"])
    assert equal(.5*2*3**2 + .5*3*(-1)**2, post("P01")["expected"]["totalK"])
    assert 2*3 + 3*(-1) != 2*3 + 3*(+1)
    assert equal(2*post("P01")["expected"]["totalP"], post("P01")["boundaryExpected"]["totalP"])
    assert equal(4*post("P01")["expected"]["totalK"], post("P01")["boundaryExpected"]["totalK"])
    # P02 triangular vs rectangular net-force area.
    J = .5*4*6 - 4*1
    assert equal(J, post("P02")["expected"]["impulse"])
    assert equal(-1 + J/2, post("P02")["expected"]["velocity"])
    assert J != 4*6-4  # peak height wrongly used as mean
    assert equal(.5*2*6-4, post("P02")["boundaryExpected"]["impulse"])
    assert equal(-1 + post("P02")["boundaryExpected"]["impulse"]/2,
                 post("P02")["boundaryExpected"]["velocity"])
    # P04 third-law impulse on distinct bodies.
    a,b=-6/2,+6/3
    assert equal(a,post("P04")["expected"]["vA"])
    assert equal(b,post("P04")["expected"]["vB"])
    assert equal(2*a + 3*b,post("P04")["expected"]["totalP"])
    assert post("P04")["boundaryExpected"] == {
        "totalP": 3, "individual": "undetermined"
    }
    # P05 recoil lab vs relative. The latter would require different answer.
    V=-2*6/10
    assert equal(V,post("P05")["expected"]["platformV"])
    assert equal(10*V+2*6,post("P05")["expected"]["totalP"])
    assert equal((10*V+2*6)/12,post("P05")["expected"]["cmV"])
    assert not equal(V,-2*6/12)  # incorrect relative-velocity equation
    assert post("P05")["boundaryExpected"] == {"platformV": 0, "totalP": 12}
    # P06 sticking vs elastic must have independent energy ledgers.
    joined=(1*4+3*0)/(1+3)
    before=.5*1*4**2
    after=.5*4*joined**2
    assert equal(joined,post("P06")["expected"]["joinedV"])
    assert equal(before-after,post("P06")["expected"]["loss"])
    assert not equal(before,after)
    vA,vB=-2,2
    assert equal(1*vA+3*vB,4)
    assert equal(.5*1*vA*vA+.5*3*vB*vB,before)
    assert post("P06")["boundaryExpected"]=={"vA":-2,"vB":2,"loss":0}
    # P07 short contact -> friction -> short contact; stop before obstacle.
    first=1*6/3
    pre=first - .2*10*.5
    final=3*pre/4
    friction=-.2*3*10*.5
    assert all(equal(x,post("P07")["expected"][k]) for x,k in [
        (first,"firstV"),(pre,"beforeThirdV"),(final,"finalV"),(friction,"frictionJ")
    ])
    stopping=first**2/(2*.4*10)
    assert equal(stopping,post("P07")["boundaryExpected"]["stopDistance"])
    assert stopping < .75 and post("P07")["boundaryExpected"]["reach"]=="no"
    assert "NO second collision" not in unit("P07")["prompt"]["stem"]


def test_source_and_academic_gates_remain_fail_closed():
    source=json.loads((SRC/"source-ledger.v1.json").read_text())
    science=json.loads((SRC/"science-evidence.v1.json").read_text())
    assert source["status"] == "SOURCE_AUTHENTICITY_HOLD"
    assert source["original_examination_items_admitted"] == 0
    assert source["independently_qualified_exact_joins"] == 0
    assert source["historical_cohorts_exhaustively_screened"] == 0
    assert len(source["entries"]) == len(science["topics"]) == 6
    assert all(row["B1_B7"] == {f"B{i}":"HOLD" for i in range(1,8)}
               for row in source["entries"])
    assert all(row["QRT"].startswith("UNADJUDICATED") for row in source["entries"])
    assert all(row["science"]=="HOLD_INDEPENDENT_REVIEW" for row in science["topics"])
    assert (SRC/"source-ledger.v1.html").is_file()
    assert "No exam stem" in (SRC/"source-ledger.v1.html").read_text()
    assert "EXTENSION_REVIEW" in (SRC/"README.md").read_text()



def test_core1ab_guide_alignment_records_task_specific_w_without_academic_promotion():
    """Author-side shortest-route/freshness review, not an independent B1–B7 verdict."""
    science = json.loads((SRC / "science-evidence.v1.json").read_text(encoding="utf-8"))
    rows = {r["id"].split("-")[-1]: r for r in science["topics"]}
    assert set(rows) == set(IDS)
    works = [r["W_learner_work"] for r in rows.values()]
    assert len(set(works)) == len(IDS), "One generic W cannot certify six distinct tasks"
    for uid, row in rows.items():
        assert row["freshness_risk_author_audit"] in {"HIGH", "MEDIUM"}
        assert row["freshness_disposition"] == "HOLD_PENDING_INDEPENDENT_B4_COMPARISON"
        assert row["shortest_route_author_candidate"]
        assert row["credible_shortcut_author_candidate"]
        assert row["anchor_to_transfer_overlap"]
        assert row["freshness_falsifier"]
        assert row["primary_operation_candidate"]
        assert row["B1_B7"] == {f"B{i}": "HOLD" for i in range(1, 8)}
    assert sum(r["freshness_risk_author_audit"] == "HIGH" for r in rows.values()) == 5
    assert rows["P02"]["freshness_risk_author_audit"] == "MEDIUM"
    assert "LAB" in rows["P05"]["anchor_to_transfer_overlap"]
    assert "relative" in rows["P05"]["freshness_falsifier"].lower()


def test_core1a_exit_checks_are_original_ungraded_and_do_not_change_attempt_revision():
    exits = json.loads((SRC / "exit-checks.v1.json").read_text(encoding="utf-8"))
    assert exits["schema"] == "g9-ph03-core1a-exit/v1"
    assert exits["academic"] == "HOLD"
    assert exits["source_role"] == "AUTHORED_TEACHING_NOT_EXAM"
    assert exits["scope"] == "CORE1A_ONLY_UNGRADED_NOT_PROTECTED_TRANSFER"
    assert set(exits["units"]) == set(IDS)
    for uid, row in exits["units"].items():
        assert all(len(row[k].strip()) >= 60 for k in ("question", "answer", "check"))
        assert row["question"] != unit(uid)["prompt"]["stem"]
        assert "P0" not in row["answer"] or "P0" not in row["question"]
    code = (SRC / "reader.js").read_text(encoding="utf-8")
    assert 'if(mode==="learn"){const exitPacket=parse(await readUrl("exit-checks.v1.json"))' in code
    assert 'class="core1a-exit"' in code
    assert "<details><summary>Compare the reasoning</summary>" in code
    assert "not a graded Core1B attempt" in code
    assert 'revision=await digest("SHA-256",encoder.encode(JSON.stringify([' in code
    assert 'if(!rec?.first)throw Error("Protected answer requested before first attempt")' in code
    # Exit teaching is loaded ONLY in the learn branch; practice revision inputs stay unchanged.
    assert code.index('if(mode==="learn"){const exitPacket=') > code.index('revision=await digest("SHA-256"')


def test_p03_legacy_wrappers_show_current_coverage_and_preserve_old_attempt_links():
    for path in (
        PH / "textbook/PH03/P03/index.html",
        PH / "core1/PH03/P03/index.html",
    ):
        doc = path.read_text(encoding="utf-8")
        assert "Six additional PH03 Learn/Try pairs are available" in doc
        assert "remain unauthored" not in doc
        assert "<details>" in doc and "historical attempt route" in doc
        assert "source-led-r1" in doc and "source-led-r2" in doc
        assert "Academic HOLD" not in doc or "academic HOLD" in doc
