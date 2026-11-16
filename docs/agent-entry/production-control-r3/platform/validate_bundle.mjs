/* Trusted executable validator: candidate JSON is stdin data, never imported/executed. */
import {readFileSync} from "node:fs";
import {validateManifest,validateAsset,compare} from "./engine.mjs";
const b=JSON.parse(readFileSync(0,"utf8")),m=validateManifest(b.manifest);
const roles=Object.keys(m.assets);
if(Object.keys(b.assets).length!==roles.length||!roles.every(r=>Object.hasOwn(b.assets,r)))throw Error("BUNDLE_ROLE_COVERAGE");
const a={};for(const r of roles)a[r]=validateAsset(m,r,b.assets[r]);
for(const [prompt,rubric] of [["challenge","feedback"],["boundary","boundary_feedback"],["source_prompt","source_feedback"]]){
 const defs=a[prompt].fields,checks=a[rubric].checks;
 const answer=Object.fromEntries(defs.map(f=>[f.id,f.type==="text"?"Ungraded fixture text":checks.find(c=>c.field===f.id)?.expected]));
 if(!compare(defs,checks,answer).allMatched)throw Error("INVALID_RUBRIC_EXPECTED_VALUES");
}
console.log(JSON.stringify({status:"STRUCTURAL_ONLY",uid:m.uid,engine:m.engine,challenge_fields:a.challenge.fields.filter(f=>f.type!=="text").map(f=>f.id),challenge_stem:a.challenge.stem}));
