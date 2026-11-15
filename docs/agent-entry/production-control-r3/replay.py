#!/usr/bin/env python3
"""Reclassify the real historical merged chapter diffs under the proposed R3 freeze.
This replay is not a new independent review of those chapters.
"""
import argparse,json
from pathlib import Path
from control import changed,classify
HERE=Path(__file__).resolve().parent
CASES=[
    ("PH05","8ee775b5c31566591627e3b830cc9ff91b288251","79448de0c692153aa1f652750bc913c45d4d7342","nsejs/physics/ph05/"),
    ("PH03","d96ee920f4ee249d74790c616cd273fde8d77382","36198f29c1c002a958c5ce941e6f5de292069ebb","nsejs/physics/ph03/"),
    ("PH06","36198f29c1c002a958c5ce941e6f5de292069ebb","7a5c425f02d8a365a738bb11df1982cbe38e9f82","nsejs/physics/ph06/"),
]
def main():
    p=argparse.ArgumentParser();p.add_argument("--repo",type=Path,default=HERE.parents[2]);a=p.parse_args()
    policy=json.loads((HERE/"policy.v1.json").read_text());rows=[]
    for topic,base,head,prefix in CASES:
        files=changed(a.repo,base,head);content=[p for p in files if classify(p,policy)=="CONTENT"]
        runtime=[p for p in content if p.startswith(prefix)]
        assert runtime,(topic,files)
        assert len(content)>0
        rows.append({"topic":topic,"base":base,"head":head,"changed":len(files),"governed_content":len(content),"chapter_runtime_and_data":len(runtime),"replay":"FROZEN_UNLESS_FULL_SIGNED_GOLDEN_LANE","sample":runtime[:4]})
    print(json.dumps({"classification_replay_only":True,"academic_status":"HOLD","cases":rows},indent=2))
if __name__=="__main__":main()
