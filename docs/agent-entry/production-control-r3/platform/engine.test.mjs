import test from "node:test";
import assert from "node:assert/strict";
import {webcrypto} from "node:crypto";
import {readFile} from "node:fs/promises";
import {fileURLToPath} from "node:url";
import {Assessment,loadAssessment,digest,compare,validateAsset,validateManifest,replay} from "./engine.mjs";
const ROOT=new URL("./fixtures/",import.meta.url);
const crypto=webcrypto;
function mem(){const map=new Map();return {map,getItem:k=>map.get(k)??null,setItem:(k,v)=>map.set(k,v)}}
function locks(){let tail=Promise.resolve();return {request:(_k,_o,f)=>{const p=tail.then(f);tail=p.catch(()=>{});return p}}}
async function setup(name="physics",storage=mem(),lock=locks(),alter=null){
 const dir=new URL(name+"/",ROOT),url="https://fixture.invalid/"+name+"/";
 const raw=await readFile(new URL("manifest.json",dir));const expectedHash=await digest(raw,crypto);const requests=[];
 const fetcher=async uri=>{requests.push(uri.split("/").at(-1));const name=uri.split("/").at(-1);let bytes=await readFile(new URL(name,dir));if(alter)bytes=alter(name,bytes);return new Response(bytes)};
 const e=await loadAssessment({manifestURL:url+"manifest.json",expectedHash,fetcher,crypto,storage,locks:lock});
 return {e,storage,lock,requests,fetcher,expectedHash,url};
}
const ans=(model,value,reason="own reasoning")=>({model,value,reason});
const bnd=(direction,magnitude,reason="own boundary reasoning")=>({direction,magnitude,reason});
async function accepted(p){const r=await p;assert.equal(r.accepted,true,r.reason);return r}
async function start(e,model="difference",v=3){await accepted(e.open("source_prompt"));await accepted(e.submit("source",ans(model,v)));await accepted(e.open("study"));await accepted(e.open("challenge"));await accepted(e.submit("prediction","My prediction"))}
async function feedback(e,a){await accepted(e.submit("first",a));await accepted(e.open("feedback"))}
async function repair(e,answer){let v=await e.snapshot();await accepted(e.submit("reconstruct","My comparison"));await accepted(e.submit("diagnose",{field:v.diagnostic.firstDivergence,explanation:"my evidence"}));await accepted(e.submit("repair",answer))}
test("full generic physics journey, staged assets, wrong first preserved, separate boundary correction",async()=>{
 const {e,requests}=await setup();assert.deepEqual(requests,["manifest.json"]);assert.equal((await e.open("feedback")).accepted,false);
 await start(e);assert(!requests.includes("feedback.json"));assert(!requests.includes("boundary.json"));await accepted(e.open("hint1"));
 await feedback(e,ans("sum",5));let v=await e.snapshot();assert.equal(v.diagnostic.firstDivergence,"model");assert.deepEqual(v.state.first.assisted,["hint1"]);
 await repair(e,ans("difference",4));assert.equal((await e.open("boundary")).accepted,false);await accepted(e.submit("repair",ans("difference",5)));
 await accepted(e.open("boundary"));assert(!requests.includes("boundary_feedback.json"));await accepted(e.submit("boundary",bnd("right",5)));
 assert.equal((await e.submit("source_return",ans("difference",3))).accepted,false);
 await accepted(e.open("boundary_feedback"));assert.equal((await e.submit("source_return",ans("difference",3))).accepted,false);
 await accepted(e.submit("boundary_repair",bnd("left",5)));await accepted(e.submit("source_return",ans("difference",3)));await accepted(e.open("source_feedback"));
 v=await e.snapshot();assert.equal(v.academicStatus,"HOLD");assert.equal(v.state.first.answer.model,"sum");assert.equal(v.state.boundary.direction,"right");assert.equal(v.state.repairs.length,2);assert.equal(v.sourceResult.allMatched,true);
});
test("same engine chemistry without code changes",async()=>{
 const {e}=await setup("chemistry");await start(e,"retained",4);await feedback(e,ans("retained",6));let v=await e.snapshot();assert.equal(v.diagnostic.firstDivergence,"value");
 await repair(e,ans("retained",7));await accepted(e.open("boundary"));await accepted(e.submit("boundary",bnd("same",2)));await accepted(e.open("boundary_feedback"));await accepted(e.submit("source_return",ans("retained",4)));await accepted(e.open("source_feedback"));assert((await e.snapshot()).sourceResult.allMatched);
});
test("concurrent first and source: winner preserved; stale action rejected",async()=>{
 const storage=mem(),lock=locks();const {e:a}=await setup("physics",storage,lock);const {e:b}=await setup("physics",storage,lock);
 await accepted(a.open("source_prompt"));const p=await Promise.all([a.submit("source",ans("difference",3)),b.submit("source",ans("sum",99))]);assert.equal(p.filter(x=>x.accepted).length,1);
 await accepted(a.open("study"));await accepted(a.open("challenge"));await accepted(a.submit("prediction","frozen"));
 const r=await Promise.all([a.submit("first",ans("difference",5)),b.submit("first",ans("sum",99))]);assert.equal(r.filter(x=>x.accepted).length,1);const state=(await b.snapshot()).state;assert.equal(state.first.answer.value,5);assert.equal(state.source.value,3);
 assert.equal((await b.submit("prediction","late edit")).accepted,false);
});
test("failed write blocks session and no answer asset fetched",async()=>{
 const x=await setup();await start(x.e);x.storage.setItem=()=>{throw Error("denied")};await assert.rejects(x.e.submit("first",ans("difference",5)),/denied/);await assert.rejects(x.e.open("feedback"),/SESSION_BLOCKED/);assert(!x.requests.includes("feedback.json"));
});
test("tampered feedback rejected before use; missing locks and stale/malformed record fail",async()=>{
 const x=await setup("physics",mem(),locks(),(n,b)=>n==="feedback.json"?Buffer.from("{}"):b);
 await start(x.e);await accepted(x.e.submit("first",ans("difference",5)));await assert.rejects(x.e.open("feedback"),/ASSET_HASH/);assert(x.e.blocked);
 const y=await setup();await start(y.e);const r=JSON.parse(y.storage.getItem(y.e.key));r.events[1].seq=999;y.storage.setItem(y.e.key,JSON.stringify(r));await assert.rejects(y.e.snapshot(),/EVENT_ORDER/);
 const z=await setup("physics",mem(),{});await assert.rejects(z.e.open("source_prompt"),/PROTECTION_UNAVAILABLE/);
});
test("manifest and schemas reject answer-bearing extra keys, path escapes, role swaps and partial rubric",async()=>{
 const x=await setup();const m=x.e.m;const bad=structuredClone(m);bad.assets.study.path="../secret.json";assert.throws(()=>validateManifest(bad),/ASSET_PIN/);
 const p=JSON.parse(await readFile(new URL("physics/challenge.json",ROOT)));p.payload.answer=5;assert.throws(()=>validateAsset(m,"challenge",p),/PROMPT_SHAPE/);
 const a=JSON.parse(await readFile(new URL("physics/feedback.json",ROOT)));assert.throws(()=>validateAsset(m,"challenge",a),/ASSET_IDENTITY/);
 delete p.payload.answer;assert.throws(()=>compare(p.payload.fields,a.payload.checks.slice(0,1),ans("difference",5)),/RUBRIC_COVERAGE/);
 await assert.rejects(loadAssessment({manifestURL:x.url+"manifest.json",expectedHash:"0".repeat(64),fetcher:x.fetcher,crypto,storage:x.storage,locks:x.lock}),/MANIFEST_HASH_MISMATCH/);
});
test("invalid numeric and early stages reject without changing first; all matched no fake divergence",async()=>{
 const {e}=await setup();await start(e);assert.equal((await e.submit("first",ans("difference",null))).accepted,false);
 assert.equal((await e.submit("repair",ans("difference",5))).accepted,false);await feedback(e,ans("difference",5));
 assert.equal((await e.snapshot()).diagnostic.firstDivergence,null);await accepted(e.submit("reconstruct","checked all fields"));assert.equal((await e.submit("diagnose",{field:"model",explanation:"invented error"})).accepted,false);
 await accepted(e.submit("diagnose",{field:null,explanation:"no structured mismatch; free text not graded"}));
});
