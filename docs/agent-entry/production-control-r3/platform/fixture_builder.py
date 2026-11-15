"""Build deterministic synthetic fixtures, never real assessment or reviewer evidence."""
from __future__ import annotations
import json, hashlib, argparse, struct, zlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
def bytes_(x):return (json.dumps(x,ensure_ascii=False,indent=2)+"\n").encode()
def hash_(b):return hashlib.sha256(b).hexdigest()
def choice(id,label,options):return {"id":id,"label":label,"type":"choice","options":[{"id":k,"label":v} for k,v in options]}
def number(id,label):return {"id":id,"label":label,"type":"number"}
def text(id,label):return {"id":id,"label":label,"type":"text"}
def cc(field,expected,feedback):return {"field":field,"type":"choice","expected":expected,"feedback":feedback}
def nc(field,expected,feedback):return {"field":field,"type":"number","expected":expected,"abs_tolerance":0.001,"rel_tolerance":0,"feedback":feedback}
def fixtures():
    for name in ("physics","chemistry"):
        # Synthetic examples intentionally not NSEJS sources or Golden nominations.
        if name=="physics":
            fs=[choice("model","Model",[("sum","Total force"),("difference","Opposed forces")]),number("value","Net force (N)"),text("reason","Your reasoning")]
            bs=[choice("direction","Direction",[("left","Left"),("right","Right")]),number("magnitude","Magnitude (N)"),text("reason","Your reasoning")]
            source={"stem":"Fixture only: 5 N right, 2 N left. Find the net force.","fields":fs}
            study={"title":"Fixture: directed force","sections":[{"heading":"Opposed arrows","body":["Assign a sign to each arrow."]},{"heading":"Worked check","body":["4 N right and 1 N left give 3 N right."]}]}
            challenge={"stem":"Fixture only: 8 N right, 3 N left. Find the net force.","prediction":"Predict the direction.","fields":fs}
            feedback={"reconstruction":["Take right as positive.","Add signed forces: 8−3=5 N."],"checks":[cc("model","difference","Opposed arrows require a signed difference."),nc("value",5,"Recheck the signed force sum.")],"repair_prompt":"Recalculate using signed forces."}
            boundary={"stem":"Fixture only: 2 N right, 7 N left. Give direction and magnitude.","fields":bs}
            boundary_feedback={"model":"Left, magnitude 5 N.","checks":[cc("direction","left","The larger force points left."),nc("magnitude",5,"Magnitude is the absolute difference.")]}
            source_feedback={"model":"3 N right.","checks":[cc("model","difference","Opposed forces require signed sum."),nc("value",3,"Subtract the opposing force.")]}
        else:
            fs=[choice("model","Material ledger",[("retained","Retained solute"),("lost","Lost solute")]),number("value","Salt mass (g)"),text("reason","Your reasoning")]
            bs=[choice("direction","Concentration",[("same","Same"),("changed","Changed")]),number("magnitude","Salt removed (g)"),text("reason","Your reasoning")]
            source={"stem":"Fixture only: a mixture contains 4 g salt. Pure water evaporates; find salt mass.","fields":fs}
            study={"title":"Fixture: component ledger","sections":[{"heading":"Track components","body":["If salt is nonvolatile, pure water loss does not remove salt."]},{"heading":"Worked check","body":["A mixture containing 3 g salt still contains 3 g salt after adding water."]}]}
            challenge={"stem":"Fixture only: a mixture contains 7 g nonvolatile salt; pure water is added. Find salt mass.","prediction":"Predict if salt mass changes.","fields":fs}
            feedback={"reconstruction":["Identify the retained species.","Pure water addition does not change 7 g salt."],"checks":[cc("model","retained","Only water changes."),nc("value",7,"Use the retained salt mass.")],"repair_prompt":"Redo the component ledger."}
            boundary={"stem":"Fixture only: remove 10 g of homogeneous 20% solution. What happens to concentration and what salt mass leaves?","fields":bs}
            boundary_feedback={"model":"Concentration unchanged; 2 g salt removed.","checks":[cc("direction","same","Representative withdrawal preserves concentration."),nc("magnitude",2,"Multiply 10 g by 0.20.")]}
            source_feedback={"model":"4 g salt retained.","checks":[cc("model","retained","Water alone leaves."),nc("value",4,"Salt mass stays 4 g.")]}
        yield name,dict(source_prompt=source,study=study,challenge=challenge,hint1={"text":"Track the given quantities."},feedback=feedback,boundary=boundary,boundary_feedback=boundary_feedback,source_feedback=source_feedback)
def png_fixture():
    # Tiny deterministic arrow diagram, no text or answer.
    w,h=80,24
    rows=[]
    for y in range(h):
        row=bytearray()
        for x in range(w):
            arrow=(10<=x<=64 and 10<=y<=13) or (60<=x<=72 and abs(y-12)<=72-x)
            row.extend((31,100,112) if arrow else (245,250,251))
        rows.append(b"\0"+row)
    def chunk(tag,data):return struct.pack(">I",len(data))+tag+data+struct.pack(">I",zlib.crc32(tag+data)&0xffffffff)
    return b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",w,h,8,2,0,0,0))+chunk(b"IDAT",zlib.compress(b"".join(rows)))+chunk(b"IEND",b"")
def build(out):
    for name,assets in fixtures():
        dest=out/name;dest.mkdir(parents=True,exist_ok=True)
        uid="synthetic-"+name;rev="fixture-v1"
        manifest={"schema":"g9-assessment-manifest/v1","engine":"g9-assessment/1.0.0","uid":uid,"revision":rev,"status":"TECHNICAL_CANDIDATE_HOLD","assets":{}}
        for role,payload in assets.items():
            raw=bytes_({"schema":"g9-assessment-asset/v1","uid":uid,"revision":rev,"role":role,"payload":payload})
            file=role+".json";(dest/file).write_bytes(raw);manifest["assets"][role]={"path":file,"sha256":hash_(raw)}
        media=png_fixture();(dest/"boundary-diagram.png").write_bytes(media);manifest["assets"]["boundary"]["media"]=[{"path":"boundary-diagram.png","sha256":hash_(media),"alt":"Synthetic directional marker, not a solution."}]
        raw=bytes_(manifest);(dest/"manifest.json").write_bytes(raw)
        (dest/"index.html").write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Synthetic platform fixture — HOLD</title><style>body{{font:16px system-ui;max-width:900px;margin:auto;padding:18px}}section{{border:1px solid #9eb7c2;border-radius:10px;padding:16px;margin:12px 0}}label{{display:block;margin:12px 0}}input,select,textarea,button{{font:inherit;display:block;max-width:100%;box-sizing:border-box;margin:6px 0;padding:8px}}textarea{{width:100%}}pre{{white-space:pre-wrap;overflow-wrap:anywhere}}button{{min-height:44px}}</style></head><body><h1>Platform fixture — {name}</h1><p id="status" role="status">Loading</p><main data-assessment data-manifest="manifest.json" data-pin="{hash_(raw)}"></main><script type="module" src="../../reader.mjs"></script></body></html>''',encoding="utf-8")
def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,default=HERE/"fixtures");a=p.parse_args();build(a.output)
if __name__=="__main__":main()
