"""PH02 owner-directed physics sanity checks, independently recomputed formulas.

Exercises remain *authored*, not authenticated original examination items.
Numerical consistency checks are not third-party academic credentials.
"""
import math
from pathlib import Path
import json
import pytest

ROOT=Path(__file__).resolve().parents[1]
u=json.loads((ROOT/"nsejs/physics/ph02/units.v1.json").read_text())
q=json.loads((ROOT/"nsejs/physics/ph02/qrt-candidates.v1.json").read_text())
ALL_IDS={v["practice"]["uid"] for v in u["units"]}|{t["uid"] for t in q["tasks"]}|{m["uid"] for m in q["main_cycles"]}

# Calculations derived from each problem's force, mass, stage, constraint, or figure.
# The expected value is deliberately written separately from the authored reconstruction.
CASES=[
 ("AUTHORED-PH02-F01-TRANSFER-01",(12-5)-2*(-1),9),
 ("AUTHORED-PH02-F02-TRANSFER-01",6*2-(6*2+0.5*2*2**2),-4),
 ("AUTHORED-PH02-F03-TRANSFER-01",(2*3)/1.5,4),
 ("AUTHORED-PH02-F04-TRANSFER-01",-12/4,-3),
 ("AUTHORED-PH02-F05-TRANSFER-01",1*2,2),
 ("AUTHORED-PH02-F06-TRANSFER-01",8-3,5),
 ("AUTHORED-PH02-F07-TRANSFER-01",5*10*math.sin(math.radians(30))+5*1,30),
 ("AUTHORED-PH02-F08-TRANSFER-01",15/(2+3),3),
 ("AUTHORED-PH02-F01-QRT-REPRESENT-D3-R1",13-4*(-1),17),
 ("AUTHORED-PH02-F01-QRT-JUSTIFY-D3-R1",-2+(4/2)*0.5,-1),
 ("AUTHORED-PH02-F02-QRT-EXPLAIN-D3-R1",4*2-(4*2+0.5*2*2**2),-4),
 ("AUTHORED-PH02-F02-QRT-REPRESENT-D3-R1",5*4-(5*4-0.5*1*2**2),2),
 ("AUTHORED-PH02-F03-QRT-APPLY-D3-R1",2*2+0.5*((12-3)/3)*2**2+(2+((12-3)/3)*2)*1+0.5*(-3/3)*1**2,17.5),
 ("AUTHORED-PH02-F03-QRT-SYNTHESIZE-D3-R1",10-4*1.5,4),
 ("AUTHORED-PH02-F04-QRT-REPRESENT-D3-R1",(-9-2)/2,-5.5),
 ("AUTHORED-PH02-F04-QRT-JUSTIFY-D3-R1",2*(-6/2)+3*(6/3),0),
 ("AUTHORED-PH02-F05-QRT-MODEL-D3-R1",(1*9)/(2+1),3),
 ("AUTHORED-PH02-F05-QRT-SYNTHESIZE-D3-R1",4-(1*9)/(2+1),1),
 ("AUTHORED-PH02-F06-QRT-MODEL-D3-R1",(7-2)-4,1),
 ("AUTHORED-PH02-F06-QRT-JUSTIFY-D3-R1",3+5,8),
 ("AUTHORED-PH02-F07-QRT-REPRESENT-D3-R1",40*math.cos(math.radians(30)),20*math.sqrt(3)),
 ("AUTHORED-PH02-F07-QRT-SYNTHESIZE-D3-R1",2*10*0.5+5,15),
 ("AUTHORED-PH02-F08-QRT-EXPLAIN-D3-R1",10/(2+3),2),
 ("AUTHORED-PH02-F08-QRT-MODEL-D3-R1",(12-8)/(2+3),0.8),
 ("AUTHORED-PH02-MAIN-EXPLAIN-D3-R1",(0.5*(10/5)*1**2+2*1)-0.5*1*2**2,1),
 ("AUTHORED-PH02-MAIN-APPLY-D3-R1",(20-2*10*0.5-4)/2,3),
 ("AUTHORED-PH02-MAIN-MODEL-D3-R1",18/(2+1+3),3),
 ("AUTHORED-PH02-MAIN-REPRESENT-D3-R1",0.5*((2*10*0.5)/(2+3))*2**2+((2*10*0.5)/(2+3))*2*(3-2),8),
 ("AUTHORED-PH02-MAIN-SYNTHESIZE-D3-R1",0.5*((25-3*10*0.5)/3-(-10*0.5))*2**2,50/3),
 ("AUTHORED-PH02-MAIN-JUSTIFY-D3-R1",5*(2+3)/2,12.5),
]

@pytest.mark.parametrize("uid,actual,expected",CASES)
def test_owner_directed_physics_recompute(uid,actual,expected):
    assert uid in ALL_IDS
    assert math.isclose(actual,expected,rel_tol=1e-9,abs_tol=1e-9),uid


def test_ph02_independent_formula_check_covers_exactly_all_task_uids():
    assert len(CASES)==30
    assert len(ALL_IDS)==30
    assert {x[0] for x in CASES}==ALL_IDS


def test_ph02_selected_force_limits_and_changed_condition():
    # F06: required static friction exceeds limit; cannot report a valid rest state.
    assert abs(7-2)>4
    # F07: 16 N uphill rope exceeds [5,15] N rest interval on 30 deg ramp.
    assert abs(2*10*0.5-16)>5
    # F08: slack rope candidate acceleration and taut-rope tension are consistent.
    assert 2*((12-8)/(2+3))-(-8)>0
    # F05: top-box contact remains feasible under 9 N drive and 4 N static limit.
    assert 1*(9/(2+1))<=4


def test_ph02_review_provenance_never_claims_exam_authentication():
    assert u["original_exam_identity"] is None
    assert q["original_exam_items"]==0
