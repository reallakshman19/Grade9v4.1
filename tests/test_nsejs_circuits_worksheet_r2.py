"""Source completeness and neutral-figure checks for the supplied circuit worksheet.

These are technical checks, not independent source, QRT or academic approval.
"""
import base64
import hashlib
import json
import struct
import zlib
from pathlib import Path
import xml.etree.ElementTree as ET
from fractions import Fraction
from itertools import product

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "nsejs" / "data"

def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))

def questions():
    return [q for level in (1, 2) for q in load(f"circuits-level{level}-core2-candidates.v1.json")["questions"]]

def test_source_inventory_and_full_manifest():
    qs = questions()
    inv = load("circuits-worksheet-source-inventory.v1.json")
    assert len(qs) == len(inv["records"]) == 56
    assert len({q["id"] for q in qs}) == 56
    assert [q["id"] for q in qs] == [f"NSEJS-CIRC-L{level}-Q{i:02d}" for level, n in ((1,36),(2,20)) for i in range(1,n+1)]
    bank = {q["id"]:q for q in load("physics-authored-practice-r1.json")["questions"]}
    keys = "B A A ABC B C C C A D AB BCD C C D B B B D A C AC B D A A B D D C D ACD A C B C A B C B C B C B C D C D A D B A A D A CD".split()
    assert len(keys) == 56
    for q, row, key in zip(qs, inv["records"], keys):
        assert q == bank[q["id"]]
        assert q["id"] == row["id"]
        assert q["answer_ids"] == list(key)
        assert len(q["options"]) == 4
        assert [o[0] for o in q["options"]] == list("ABCD")
        assert len(q["hints"]) == len(q["steps"]) == 3
        assert all(q[k] == "HOLD" for k in ("academic_admission","science_review","qrt_adjudication"))
        assert hashlib.sha256(q["stem"].encode()).hexdigest() == q["stem_sha256"] == row["stem_sha256"]
        assert q["source_provenance"]["source_pdf_sha256"] == inv["source_pdf_sha256"]
    assert len({f for q in qs for f in q["source_figures"]}) == 28
    assert qs[36+7]["source_figures"] == qs[36+8]["source_figures"]

def png_rgb_hash(data):
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    pos, idat = 8, []
    while pos < len(data):
        n = struct.unpack(">I", data[pos:pos+4])[0]
        typ, body = data[pos+4:pos+8], data[pos+8:pos+8+n]
        assert zlib.crc32(typ+body) & 0xffffffff == struct.unpack(">I",data[pos+8+n:pos+12+n])[0]
        if typ == b"IHDR":
            w,h,depth,color,_,_,interlace = struct.unpack(">IIBBBBB", body)
            assert (depth,color,interlace)==(8,2,0)
        if typ == b"IDAT":
            idat.append(body)
        pos += n+12
    raw = zlib.decompress(b"".join(idat))
    stride = 3*w+1
    assert len(raw)==stride*h
    assert all(raw[i]==0 for i in range(0,len(raw),stride))
    return hashlib.sha256(b"".join(raw[i+1:i+stride] for i in range(0,len(raw),stride))).hexdigest()

def test_all_original_figure_pixels_and_no_solution_overlays():
    inv = load("circuits-worksheet-source-inventory.v1.json")
    seen = set()
    for row in inv["records"]:
        for name in row["source_figures"]:
            a = ROOT / "nsejs" / "assets" / name
            b = ROOT / "nsejs" / "physics" / "assets" / name
            assert a.read_bytes()==b.read_bytes()
            root = ET.fromstring(a.read_bytes())
            assert [e.tag.rsplit("}",1)[-1] for e in root] == ["title","image"]
            href = root[1].attrib["{http://www.w3.org/1999/xlink}href"]
            assert href.startswith("data:image/png;base64,")
            assert png_rgb_hash(base64.b64decode(href.split(",",1)[1])) == row["source_image_rgb_sha256"]
            seen.add(name)
    assert len(seen)==28

def effective_r(nodes, edges, A, B, r):
    # Exact unit-voltage conductance solver; no use of author formula.
    unknown = [v for v in nodes if v not in (A,B)]
    n=len(unknown)
    mat=[[Fraction(0) for _ in range(n+1)] for _ in range(n)]
    for i,v in enumerate(unknown):
        nbr=[b if a==v else a for a,b in edges if v in (a,b)]
        mat[i][i]=Fraction(len(nbr))
        for u in nbr:
            if u==A: mat[i][-1]+=1
            elif u!=B: mat[i][unknown.index(u)]-=1
    for j in range(n):
        p=next(i for i in range(j,n) if mat[i][j])
        mat[j],mat[p]=mat[p],mat[j]
        k=mat[j][j]
        mat[j]=[x/k for x in mat[j]]
        for i in range(n):
            if i!=j:
                k=mat[i][j]
                mat[i]=[a-k*b for a,b in zip(mat[i],mat[j])]
    v={A:Fraction(1),B:Fraction(0),**dict(zip(unknown,[row[-1] for row in mat]))}
    current=sum((1-v[b if a==A else a])/r for a,b in edges if A in (a,b))
    return 1/current

def test_corrected_grid_and_cube_answers():
    grid=list(product(range(3),repeat=2))
    cube=list(product(range(2),repeat=3))
    def edges(nodes):
        return [(a,b) for i,a in enumerate(nodes) for b in nodes[i+1:] if sum(abs(x-y) for x,y in zip(a,b))==1]
    assert effective_r(grid,edges(grid),(0,0),(2,2),4)==6
    assert effective_r(cube,edges(cube),(0,0,0),(1,0,0),12)==7
    assert effective_r(cube,edges(cube),(0,0,0),(1,1,0),8)==6
    assert effective_r(cube,edges(cube),(0,0,0),(1,1,1),12)==10

def test_search_mirrors_and_worksheet_routes():
    a=ROOT/"data"/"learner-search-index.v1.json"
    b=DATA/"learner-search-index.v1.json"
    assert a.read_bytes()==b.read_bytes()
    manifest=load("learner-search-manifest.v1.json")
    assert hashlib.sha256(a.read_bytes()).hexdigest()==manifest["sha256"]
    docs={d["original_id"]:d for d in json.loads(a.read_text(encoding="utf-8")) if d.get("original_id","").startswith(("NSEJS-CIRC-L1-","NSEJS-CIRC-L2-"))}
    assert len(docs)==56
    for q in questions():
        d=docs[q["id"]]
        assert "HOLD" in d["badge"] and not d["hints"]
        assert d["url"]==f"nsejs/physics/index.html?topic=circuits&q={q['id']}#{q['id']}"
        assert d["score"]==q["score"]
