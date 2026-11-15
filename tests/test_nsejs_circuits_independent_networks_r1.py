"""Independent network-equation cross-checks for the owner-supplied circuit worksheet.

These checks are *not* QRT, source-rights, academic, or official-exam acceptance.
Original source diagrams were inspected in circuit.pdf pages 3–12 and modeled as
two-terminal resistor graphs; the solver deliberately does not reuse author steps.
"""
from __future__ import annotations
import itertools
import json
from fractions import Fraction
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "nsejs" / "data"
Q1 = json.loads((DATA / "circuits-level1-core2-candidates.v1.json").read_text())["questions"]
Q2 = json.loads((DATA / "circuits-level2-core2-candidates.v1.json").read_text())["questions"]


def effective(edges, start, end):
    """Unit-current nodal solve with exact rational arithmetic and zero-wire contraction."""
    parent = {}

    def find(n):
        parent.setdefault(n, n)
        if parent[n] != n:
            parent[n] = find(parent[n])
        return parent[n]

    def join(a, b):
        parent[find(a)] = find(b)

    for u, v, resistance in edges:
        if Fraction(resistance) == 0:
            join(u, v)
    s, t = find(start), find(end)
    if s == t:
        return Fraction(0)
    nodes = sorted({find(u) for a, b, _ in edges for u in (a, b)} | {s, t}, key=str)
    others = [n for n in nodes if n != t]
    pos = {n: i for i, n in enumerate(others)}
    size = len(others)
    m = [[Fraction(0) for _ in range(size + 1)] for _ in range(size)]
    m[pos[s]][size] = Fraction(1)
    for a, b, ohms in edges:
        if Fraction(ohms) == 0:
            continue
        a, b = find(a), find(b)
        if a == b:
            continue
        conductance = Fraction(1) / Fraction(ohms)
        for n in (a, b):
            if n != t:
                m[pos[n]][pos[n]] += conductance
        if a != t and b != t:
            m[pos[a]][pos[b]] -= conductance
            m[pos[b]][pos[a]] -= conductance
    for k in range(size):
        pivot = next((i for i in range(k, size) if m[i][k] != 0), None)
        if pivot is None:
            raise AssertionError("Disconnected resistor network")
        m[k], m[pivot] = m[pivot], m[k]
        div = m[k][k]
        m[k] = [x / div for x in m[k]]
        for i in range(size):
            if i == k:
                continue
            mult = m[i][k]
            m[i] = [x - mult*y for x, y in zip(m[i], m[k])]
    return m[pos[s]][size]


def cube(r):
    vertices = list(itertools.product([0, 1], repeat=3))
    return [(a, b, r) for a, b in itertools.combinations(vertices, 2)
            if sum(x != y for x, y in zip(a, b)) == 1]


def k4(r):
    return [(a, b, r) for a, b in itertools.combinations("ABCD", 2)]


SQUARE = [("A","B",6),("B","C",6),("C","D",6),("D","A",6),("A","C",6)]
L2_GRAPHS = {
    1: ([("A","B",2),("A","M",1),("M","B",3),("A","B",4)],"A","B",Fraction(1)),
    2: ([("A","X",2),("X","B",3),("X","Y",4),("Y","B",2)],"A","B",Fraction(4)),
    3: ([("A","B",6),("A","X",3),("X","B",2),("X","B",0)],"A","B",Fraction(2)),
    4: ([("A","C",6),("C","B",9),("A","D",4),("D","B",6),("C","D",10)],"A","B",Fraction(6)),
    5: ([("A","C",2),("C","B",6),("A","D",6),("D","B",8),("C","D",4)],"A","B",Fraction(5)),
    6: ([("A","C",6),("C","B",12),("A","D",12),("D","B",6)],"A","B",Fraction(9)),
    7: ([(i,(i+1)%6,6) for i in range(6)],0,1,Fraction(5)),
    8: (SQUARE,"A","C",Fraction(3)),
    9: (SQUARE,"B","D",Fraction(6)),
    10: ([("A","B",6),("B","C",6),("C","D",6),("D","A",6)]
          +[("O",n,6) for n in "ABCD"],"A","C",Fraction(4)),
    11: ([( (x,y), (x+1,y),4) for x in range(2) for y in range(3)]
          + [( (x,y), (x,y+1),4) for x in range(3) for y in range(2)],
          (0,0),(2,2),Fraction(6)),
    12: ([("A","B",6),("B","M",3),("M","C",3),("C","A",6)],"A","M",Fraction(9,2)),
    13: ([("P","Q",12),("P","Q",12),("P","Q",12)],"P","Q",Fraction(4)),
    14: (cube(12),(0,0,0),(1,0,0),Fraction(7)),
    15: (cube(8),(0,0,0),(1,1,0),Fraction(6)),
    16: (k4(10),"A","B",Fraction(5)),
    17: ([("A","N1",8),("N1","B",8),("N1","N2",8),("N2","B",8),
          ("N2","N3",8),("N3","B",8)],"A","B",Fraction(13)),
}


@pytest.mark.parametrize("number", list(L2_GRAPHS))
def test_l2_nodal_graph_matches_worksheet_key(number):
    edges, source, sink, expected = L2_GRAPHS[number]
    assert effective(edges, source, sink) == expected, number
    q = Q2[number-1]
    assert q["source_id"] == f"NSEJS-CIRC-L2-Q{number:02d}"
    assert q["answer"].split(":",1)[0] in "A B C D".split()
    assert q["academic_admission"] == "HOLD"


def test_l2_switch_open_vs_closed():
    edges, s, t, open_r = L2_GRAPHS[6]
    assert effective(edges,s,t) == Fraction(9)
    assert effective(edges+[("C","D",0)],s,t) == Fraction(8)
    assert Q2[5]["answer"].startswith("B:")


def test_l2_infinite_ladder_fixed_point_and_convergence():
    # R = 4 + (3*R)/(3+R), with R>0; root R=6 ohms.
    val = Fraction(6)
    assert val == 4 + 3*val/(3+val)
    # Finite truncations converge from 7 Ω toward 6 Ω.
    approx = Fraction(7)
    for _ in range(12):
        approx = 4 + 3*approx/(3+approx)
    assert abs(approx - val) < Fraction(1,10_000)
    assert Q2[17]["answer"].startswith("D:")


def test_l2_three_resistors_exhaust_series_parallel_cases():
    r = Fraction(6)
    obtainable = {3*r, r/3, r+(r*r)/(r+r), (2*r*r)/(3*r)}
    assert obtainable == {Fraction(18),Fraction(2),Fraction(9),Fraction(4)}
    assert Fraction(12) not in obtainable
    assert Q2[18]["answer"].startswith("A:")


def test_l2_monotonicity_candidate_key():
    # Check representative passive networks; not a proof of general monotonicity.
    base=[("A","C",2),("C","B",5),("A","D",7),("D","B",3)]
    r=effective(base,"A","B")
    assert effective(base+[("C","D",4)],"A","B") <= r
    assert effective(base+[("C","D",0)],"A","B") <= r
    assert effective(base[:-1],"A","B") >= r
    assert Q2[19]["answer"].startswith("C, D:")


def test_level1_source_figure_networks_with_independent_nodal_solver():
    assert effective([("P","Q",4),("P","Q",8)],"P","Q") == Fraction(8,3)
    assert effective([("A","X",4),("X","B",6),("X","B",3)],"A","B") == Fraction(6)
    assert effective([("A","C",2),("C","B",4),("A","D",3),("D","B",6),("C","D",5)],"A","B") == Fraction(18,5)
    assert effective(cube(12),(0,0,0),(1,1,1)) == Fraction(10)
    assert effective([("A","X",4),("X","B",2),("A","B",3)],"A","B") == Fraction(2)
    assert effective([("A","X",6),("X","B",3)],"A","B") == Fraction(9)
    assert Q1[12]["answer"].startswith("C:")
    assert Q1[15]["answer"].startswith("B:")
    assert Q1[17]["answer"].startswith("B:")
    assert Q1[18]["answer"].startswith("D:")
    assert Q1[20]["answer"].startswith("C:")
    assert Q1[32]["answer"].startswith("A:")


def test_level1_source_graph_power_and_switch_examples():
    assert Fraction(12) / effective(
      [("A","X",4),("X","B",6),("X","B",3)],"A","B") == Fraction(2)
    assert Fraction(6) / (4+2) == Fraction(1)
    assert Fraction(6) / 2 == Fraction(3)
    assert Fraction(9) * Fraction(3)/(6+3) == Fraction(3)
    assert Q1[21]["answer"].startswith("A, C:")


def test_q18_level1_svg_declares_exact_five_source_edges_without_solution():
    from xml.etree import ElementTree as ET
    p=ROOT/"nsejs/assets/fig_nsejs_circ_l1_q18.svg"
    root=ET.parse(p).getroot()
    texts=" ".join(e.text or "" for e in root.iter() if e.tag.endswith("text"))
    desc=" ".join(e.text or "" for e in root.iter() if e.tag.endswith("desc"))
    for edge in ("AC 2 ohms","CB 4 ohms","AD 3 ohms","DB 6 ohms","CD 5 ohms"):
        assert edge in desc
    assert texts.count("Ω") == 5
    assert "3.6" not in texts
