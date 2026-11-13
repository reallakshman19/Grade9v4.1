"""B01 author-side regression evidence for R00. Not independent QRT/academic approval."""
import hashlib
import json
from pathlib import Path
from fractions import Fraction as F
import pytest

ROOT = Path(__file__).resolve().parents[1]
TOPICS = ROOT / "nsejs/physics/curriculum/topics"
DIR = TOPICS / "PH07/b01"
REG = json.loads((DIR / "B01_ADAPTER_RECONCILIATION.v1.json").read_text(encoding="utf-8"))
HANDOFF = json.loads((DIR / "B01_R00_STAGE_HANDOFF.v1.json").read_text(encoding="utf-8"))

def read_package(pin):
    raw = (ROOT / pin["path"]).read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    assert blob == pin["blob"], pin["path"]
    p = json.loads(raw)
    assert p["version"] == pin["version"]
    assert p["topic_adapter"]["adapter_id"] == pin["adapter_id"]
    assert p["topic_adapter"]["version"] == pin["adapter_version"]
    return p

def test_additive_reconciliation_does_not_select_canonical_adapter():
    assert REG["status"] == "PROPOSAL_ONLY_INTEGRATION_BLOCKED"
    assert REG["selection"]["canonical_topic_adapter"] is None
    assert REG["selection"]["automatic_supersession"] is False
    assert REG["selection"]["cross_instance_compatibility"] == "NOT_QUALIFIED"
    pins = REG["legacy_packages"] + REG["isolated_slices"]
    ids, identities, cycle_ids, cell_bindings = set(), set(), set(), set()
    versions = set()
    for pin in pins:
        p = read_package(pin)
        if pin in REG["isolated_slices"]:
            assert p["version"] not in versions
            versions.add(p["version"])
        for s in p["subtopics"]:
            for t in s["qrt_targets"]:
                assert t["id"] not in ids
                assert t["task_identity"] not in identities
                ids.add(t["id"])
                identities.add(t["task_identity"])
                cell_bindings.add((p["topic_adapter"]["adapter_id"]+"/"+t["blueprint_cell"], t["id"], pin["blob"]))
        for c in p["core1b"]:
            assert c["id"] not in cycle_ids
            cycle_ids.add(c["id"])
    assert len(ids) == 72 and len(cycle_ids) == 144
    assert len(versions) == 20
    assert cell_bindings == {(k, t["target_id"], t["package_blob"]) for k,v in REG["cell_candidates"].items() for t in v}
    assert {r["subtopic_id"] for r in REG["overlapping_subtopics"]} == {"PH07-05","PH07-07","PH08-05","PH08-08"}
    r, = [r for r in REG["overlapping_subtopics"] if r["subtopic_id"]=="PH07-07"]
    m, = [r for r in r["relations"] if r["legacy_target"]=="PH07-07-D3-MODEL-02"]
    assert m["legacy_cell"] == "D3.4"
    assert m["proposed_same_operation"] == [{"target":"PH07-07-B01-D4-MODEL-01","cell":"D4.4","relation":"DISTINCT_TASK_NOT_EQUIVALENT_NOT_RECLASSIFICATION"}]

def test_all_120_prediction_revisions_are_task_specific_and_not_literal_w():
    prompts = set()
    for pin in REG["isolated_slices"]:
        p = read_package(pin)
        assert p["acceptance"]["b1_b7"]["B5"]["status"] == "HOLD"
        assert p["acceptance"]["release"] == "HOLD"
        for c in p["core1b"]:
            assert c["id"].endswith(("-R2","-R3"))
            assert c["stages"]["predict"] not in prompts
            prompts.add(c["stages"]["predict"])
            assert c["protected_work"] not in c["stages"]["predict"]
            assert c["stages"]["predict"] != c["fresh_task"]
            assert c["stages"]["attempt"] == c["fresh_task"]
            assert c["runtime_verification"] == "NOT_RUN"
    assert len(prompts) == 120

def test_stage_handoff_is_bound_to_increment4_5_and_6_not_runtime_approval():
    assert HANDOFF["stage_order"] == ["PREDICT","ATTEMPT","RECONSTRUCT","DIAGNOSE","REPAIR","BOUNDARY_TEST"]
    assert HANDOFF["status"] == "PROPOSED_PLATFORM_DEPENDENCY"
    assert len(HANDOFF["criteria"]) == 72
    packages = {p["subtopics"][0]["id"]:read_package(p) for p in REG["isolated_slices"]}
    seen = set()
    for row in HANDOFF["criteria"]:
        p = packages[row["subtopic_id"]]
        c, = [c for c in p["core1b"] if c["id"] == row["cycle_id"]]
        assert c["id"] not in seen
        seen.add(c["id"])
        assert row["package_version"] == p["version"]
        assert row["target_id"] == c["qrt_target_id"]
        assert row["boundary_prompt"] == c["stages"]["boundary_test"]
        assert set(row["stage_response_criteria"]) == set(HANDOFF["stage_order"])
        assert all(row["stage_response_criteria"].values())
        assert row["runtime_status"] == "NOT_IMPLEMENTED"
        assert row["academic_status"] == "AUTHOR_PROPOSED_NOT_INDEPENDENTLY_QUALIFIED"

def test_wave_alias_model_oracle():
    # Enumerate integer shifts using exact rational arithmetic, not the authored answer string.
    lam, t1, offset = F(4,5), F(5,1000), F(1,5)
    velocities = [(offset+n*lam)/t1 for n in range(-10,11)]
    valid = [u for u in velocities if 100<=abs(u)<=500]
    assert len(valid)==5
    assert [u for u in valid if (u*F(15,10000))%lam==F(54,100)] == [360]
    # A measurement at twice t1 is redundant for every admissible velocity.
    assert len({(u*2*t1)%lam for u in valid})==1

def test_absorption_model_counterexample_oracle():
    C=300
    fits=[(F(a,100), loss) for a in range(101) for loss in range(31)
          if 90*F(a,100)-loss==C*F(8,100) and 150*F(a,100)-loss==C*F(16,100)]
    assert fits==[(F(2,5),12)]
    assert all((120*a-loss)/C!=F(10,100) for a,loss in fits)
    # Same two slopes without C: scaling C, alpha, loss by 1/2 remains admissible.
    assert (90*F(1,5)-6)/150==F(8,100)

def test_layered_path_model_oracle():
    # Exhaustively recover admissible mixed length on 0.1m grid; all-B fixes delay.
    delay=F(56,10000)-F(2,500)
    candidates=[F(i,10) for i in range(21)]
    fit=[x for x in candidates if delay+x/300+(2-x)/500==F(72,10000)]
    assert fit==[F(6,5)]
    assert delay+F(1,300)==F(37,7500)
    # Same medium speed makes all fractions observationally equivalent.
    assert len({x/500+(2-x)/500 for x in candidates})==1

def test_intensity_countermodel_oracle():
    # Fixed pressure ratio 2, impedance ratio variable; intensity ordering can reverse.
    assert [4/F(z) for z in [2,4,8]]==[2,1,F(1,2)]
    # With displacement ratio 2 and frequency ratio 1/2, impedance alone controls ratio.
    assert [(F(2)*F(1,2))**2*Z for Z in [F(1,2),1,2]]==[F(1,2),1,2]

def test_evaporation_residual_and_uncertainty_oracle():
    dry,wet=(12,20),(18,32)
    observed=[w-d for w,d in zip(wet,dry)]
    predicted=[2400*r for r in [F(25,10000),F(40,10000)]]
    assert [o-p for o,p in zip(observed,predicted)]==[0,F(12,5)]
    assert abs(observed[1]-predicted[1])<=2400*F(1,1000)

def echo_orders(a,b,v):
    # Trace actual legs for both initial directions instead of using the closed-form result.
    out={}
    for direction,first,last in [("L",a,b),("R",b,a)]:
        for order in range(1,4):
            distance=first+(order-1)*(a+b)+(first if order%2 else last)
            out[direction+str(order)]=F(distance,v)
    return out

def test_echo_inverse_displaced_model_oracle():
    v=250
    # 56 ms common second arrival and 16 ms identified first arrival.
    candidates=[(a,7-a) for a in range(1,7) if F(16,1000) in [F(2*a,v),F(2*(7-a),v)]]
    assert candidates==[(2,5),(5,2)]
    fit=[(a,b) for a,b in candidates if sorted([F(2*(a+1),v),F(2*(b-1),v)])==[F(24,1000),F(32,1000)]]
    assert fit==[(2,5)]
    o=echo_orders(2,5,v)
    assert sorted([o["L3"],o["R3"]])==[F(72,1000),F(96,1000)]
    assert o["L2"]==o["R2"]==F(56,1000)

def test_echo_countermodel_oracle():
    centered=echo_orders(F(9,2),F(9,2),300)
    offset=echo_orders(3,6,300)
    assert centered["L2"]==offset["L2"]==F(60,1000)
    assert centered["L1"]==centered["R1"]==F(30,1000)
    assert sorted([offset["L1"],offset["R1"]])==[F(20,1000),F(40,1000)]
    assert set(centered.values())!=set(offset.values())


def test_increment5_conduction_model_oracle():
    # Fit each competing model to the first observation, then evaluate independent geometry.
    delta, nominal, initial = F(20), F(4), F(7)
    altered_R=delta/initial
    bypass=initial-delta/nominal
    assert delta/(2*altered_R)==F(7,2)
    assert delta/(2*nominal)+bypass==F(9,2)
    assert delta/(4*nominal)+bypass==F(13,4)
    assert delta/(4*nominal)+bypass != 4

def test_increment5_heating_curve_model_oracle():
    # Independently enumerate physically admissible capacities and common losses.
    pairs=[(c,l) for c in range(50,501) for l in range(0,46)
           if F(45-l,c)==F(1,10) and F(75-l,c)==F(22,100)]
    assert pairs==[(250,20)]
    assert F(60-20,250)==F(16,100)
    assert F(60-20,250)!=F(19,100)
    assert F(36-20,200)==F(8,100)

def test_increment5_longitudinal_spacing_inverse_oracle():
    equilibrium=[0,10,20,30,40]
    def gaps(displacements):
        actual=[x+d for x,d in zip(equilibrium,displacements)]
        return [b-a for a,b in zip(actual,actual[1:])]
    assert gaps([0,1,0,-2,0])==gaps([3,4,3,1,3])==[11,9,8,12]
    fits=[[offset,offset+1,offset,offset-2,offset] for offset in range(-5,6) if offset-2==1]
    assert fits==[[3,4,3,1,3]]
    pin,=[p for p in REG["isolated_slices"] if p["subtopics"][0]["id"]=="PH08-02"]
    target,=[t for t in read_package(pin)["subtopics"][0]["qrt_targets"] if t["primary_operation"]=="JUSTIFY"]
    assert target["band"]=="D3"
    assert sum(v["score"] for v in target["factor_evidence"].values())==7


def test_increment6_expansion_contact_oracle():
    # Use exact millimetre arithmetic; model stops at zero clearance.
    rate_a=F(2)*F(12,10**6)*1000
    rate_b=F(2)*F(18,10**6)*1000/2
    assert (rate_a,rate_b)==(F(24,1000),F(18,1000))
    gap=F(21,10)
    assert gap/(rate_a+rate_b)==50
    assert gap-30*(rate_a+rate_b)==F(84,100)
    assert gap-60*(rate_a+rate_b)<0  # free prediction invalid after contact
    rate=F(15,10)*F(16,10**6)*1000*2+F(8,10)*F(20,10**6)*1000
    assert F(18,10)/rate==F(225,8)

def test_increment6_alternative_medium_paths_oracle():
    route_a=F(12,10)/1200+F(6,10)/300
    route_b=F(24,10)/2400
    assert route_a==F(3,1000) and route_b==F(1,1000)
    assert F(102,100)/340==F(3,1000)
    assert F(4,2000)==F(2,1000)

def grouped_intervals(paths, duration, threshold, quiet_gap):
    groups=[]
    for start, amplitude in sorted(paths):
        if amplitude < threshold:
            continue
        end=start+duration
        if groups and start-groups[-1][1] < quiet_gap:
            groups[-1]=(groups[-1][0],max(groups[-1][1],end))
        else:
            groups.append((start,end))
    return groups

def test_increment6_reverberation_model_oracle():
    a=[(0,F(1)),(9,F(7,10)),(38,F(4,10))]
    b=a+[(21,F(2,10))]
    assert grouped_intervals(a,14,F(3,10),4)==grouped_intervals(b,14,F(3,10),4)==[(0,23),(38,52)]
    assert grouped_intervals(a,3,F(3,10),4)==grouped_intervals(b,3,F(3,10),4)
    assert grouped_intervals(b,3,F(1,10),4)==[(0,3),(9,12),(21,24),(38,41)]
    assert grouped_intervals(b,14,F(1,10),4)==[(0,52)]
    x=[(0,F(1)),(12,F(8,10)),(48,F(5,10))]
    y=x+[(28,F(1,4))]
    assert grouped_intervals(x,18,F(1,5),6)==[(0,30),(48,66)]
    assert grouped_intervals(y,18,F(1,5),6)==[(0,66)]
    assert grouped_intervals(y,4,F(1,5),10)==[(0,16),(28,32),(48,52)]

def test_increment6_sonar_calibration_and_locus_oracle():
    from math import sqrt
    delay=F(6,1000)-F(6,1500)
    assert delay==F(2,1000)
    radius=F(1500,2)*(F(10,1000)-delay)
    assert radius==6
    x=F(8,2)
    y=sqrt(radius**2-x**2)
    predicted=[float(delay)+2*sqrt(x*x+(sign*y-6)**2)/1500 for sign in (1,-1)]
    assert predicted[0]*1000==pytest.approx(7.709,abs=.001)
    assert predicted[1]*1000>16
    assert all(abs(t*1000-7.508)>.001 for t in predicted)
    # A third off-axis observation may reject both mirror candidates.
    assert abs(predicted[0]*1000-7.709)<.001
    assert abs(predicted[1]*1000-7.709)>.001
    d=F(12,1000)-F(10,1000)
    ra=500*(F(12,1000)-d)
    rb=500*(F(20,1000)-d)
    x=(ra*ra-rb*rb+100)/20
    assert x==F(11,5)
    assert ra*ra-x*x==F(504,25)

def test_increment6_paused_retrieve_not_silently_activated():
    pin,=[p for p in REG["isolated_slices"] if p["subtopics"][0]["id"]=="PH08-03"]
    p=read_package(pin)
    assert {t["primary_operation"] for t in p["subtopics"][0]["qrt_targets"]}=={"EXPLAIN","REPRESENT","MODEL"}
    assert "D3.1 is paused" in p["acceptance"]["acceptance_note"]
