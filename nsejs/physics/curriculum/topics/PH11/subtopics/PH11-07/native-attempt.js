/* PH11-07 native technical candidate: academic/source/QRT/Owner HOLD.
 * Never fetch an answer-bearing asset before an immutable first challenge attempt.
 * Web Locks + reread serialize cooperating tabs; editable browser storage is NOT exam custody.
 * Every source/model asset is pinned by an expected Git blob digest in this code.
 */
(() => {
"use strict";
const PIN = Object.freeze({
 prompt: "1c9c22cd065ea7da1be2d970199a861b084219fe",
 postattempt: "e16d4051459337fe6fbcdd93617a0331984bcc33",
 prompt_sha256: "333bf880ec79f8f703463a77d10d2b6ef787a998284ab7ef2d4a01b05c112611",
 postattempt_sha256: "394324e67a6405bdf2cb4f7921bdf1c64e2f897fd72da42af70c7dda517f2b76"
});
const ROOT = document.getElementById("native-ph11-07");
const $ = id => document.getElementById(id);
const KEY = "g9:ph11-07:r4:" + PIN.prompt + ":" + PIN.postattempt;
let prompt = null, feedback = null, state = null, blocked = false, loadingFeedback = false;
const tell = (msg) => { $("status").textContent = msg; };
const error = msg => { blocked = true; ROOT.querySelectorAll("input,textarea,select,button").forEach(n=>n.disabled=true); tell("HOLD: "+msg+". No further answer exposure."); };
const now = () => new Date().toISOString();
const txt = (id,value) => { $(id).textContent = value == null ? "" : String(value); };
const visible = (id,show) => { $(id).hidden = !show; };
const clean = v => String(v || "").trim();
const textLength = (id,min=8) => clean($(id).value).length >= min;
const checkCrypto = () => Boolean(crypto && crypto.subtle && TextEncoder);
async function sha256(raw) {
 const hash = await crypto.subtle.digest("SHA-256",new TextEncoder().encode(raw));
 return Array.from(new Uint8Array(hash),b=>b.toString(16).padStart(2,"0")).join("");
}
async function gitBlobDigest(raw) {
 const body=new TextEncoder().encode(raw);
 const header=new TextEncoder().encode("blob "+body.length+"\u0000");
 const joined=new Uint8Array(header.length+body.length);
 joined.set(header);joined.set(body,header.length);
 const hash=await crypto.subtle.digest("SHA-1",joined);
 return Array.from(new Uint8Array(hash),b=>b.toString(16).padStart(2,"0")).join("");
}
async function fetchPinned(name,pin,pinSha256) {
 const resp=await fetch("./"+name,{cache:"no-store",credentials:"same-origin"});
 if (!resp.ok) throw Error("Pinned "+name+" unavailable ("+resp.status+")");
 const raw=await resp.text();
 const strongDigest=await sha256(raw);
 if(await gitBlobDigest(raw)!==pin || strongDigest!==pinSha256) throw Error("PIN_MISMATCH: "+name+" content differs from trusted code pins");
 return {json:JSON.parse(raw),sha256:strongDigest};
}
function newRecord() {
 return {schema:"g9v41-ph11-07-native-record/v1",uid:prompt.task.uid,revision:prompt.revision,
  prompt_pin:PIN.prompt,postattempt_pin:PIN.postattempt,seq:0,source:null,prediction:null,
  first:null,reconstructionExposure:null,reconstruction:null,diagnosis:null,repair:null,boundary:null,boundaryRepair:null,
  sourceReturn:null,events:[]};
}
function valid(r) {
 if(!r ||r.schema!=="g9v41-ph11-07-native-record/v1" ||r.uid!==prompt.task.uid ||
   r.revision!==prompt.revision||r.prompt_pin!==PIN.prompt||r.postattempt_pin!==PIN.postattempt||
   !Array.isArray(r.events)||!Number.isInteger(r.seq)||r.seq<0) return false;
 const chain=["source","prediction","first","reconstructionExposure","reconstruction","diagnosis","repair","boundary","sourceReturn"];
 let missing=false;
 for(const stage of chain){
  const value=r[stage];if(value!=null && missing)return false;
  if(value==null)missing=true;
 }
 if(r.boundaryRepair&&!r.boundary)return false;
 if(r.sourceReturn && !r.boundary?.checked && !r.boundaryRepair?.checked)return false;
 if(r.first &&(!r.first.model||!r.first.reason||!r.first.outputs))return false;
 return true;
}
function freshRead() {
 const raw=localStorage.getItem(KEY);
 if(raw===null)return newRecord();
 const parsed=JSON.parse(raw);
 if(!valid(parsed)) throw Error("Stale/corrupt content-pinned record");
 return parsed;
}
async function enter() {
 if(!navigator.locks?.request)throw Error("Web Locks unavailable; cannot serialize concurrent tabs");
 const probe=KEY+":probe";
 localStorage.setItem(probe,"ok");
 if(localStorage.getItem(probe)!=="ok")throw Error("Persistence readback failed");
 localStorage.removeItem(probe);
 state=freshRead();
}
async function commit(stage,payload,prereq) {
 if(blocked||!prompt)return false;
 if(!navigator.locks?.request){error("Web Locks unavailable");return false}
 try {
   let result=false,conflict=false;
   await navigator.locks.request(KEY,{mode:"exclusive"},async()=>{
     const latest=freshRead(); // never write a stale cached state
     if(latest[stage]!==null ||(prereq&&!latest[prereq])) {state=latest;conflict=true;return}
     const next={...latest,[stage]:{...payload,at:now()},seq:latest.seq+1,
        events:[...latest.events,{stage,at:now(),seq:latest.seq+1}]};
     if(!valid(next))throw Error("Chronology refused");
     const raw=JSON.stringify(next);
     localStorage.setItem(KEY,raw);
     if(localStorage.getItem(KEY)!==raw)throw Error("Durable readback mismatch");
     state=next;result=true;
   });
   if(conflict) {render();tell("Another tab committed a newer state. It was preserved; this tab has reloaded it. No overwrite.");}
   else if(result){render();tell("Saved "+stage+" as a separate monotonic attempt event (seq "+state.seq+").");}
   return result;
 } catch(e){error("Save failed closed: "+String(e.message||e));return false}
}
function element(tag,value){const x=document.createElement(tag);if(value!=null)x.textContent=String(value);return x}
function populateSelect(id,options,placeholder){
 const s=$(id);s.replaceChildren(element("option",placeholder));
 s.firstChild.value="";
 for(const opt of options){const o=element("option",opt.label);o.value=opt.id;s.appendChild(o)}
}
function emptyInputs(ids){for(const id of ids)$(id).value="";}
function numerical(id){
 const s=clean($(id).value);
 return /^[-+]?(?:\d+(?:\.\d*)?|\.\d+)$/.test(s)?Number(s):null;
}
function matches(given,correct,tolerance=0.01){return Number.isFinite(given)&&Math.abs(given-correct)<tolerance}
function freezeInputs(ids){for(const id of ids)$(id).disabled=true}
function preserveStage(){
 // The current UI must not keep inputs from the old stage while switching tabs.
 if(!state) return;
 if(state.source)freezeInputs(["source-model","source-reason"]);
 if(state.prediction)freezeInputs(["predict"]);
 if(state.first)freezeInputs(["task-model","first-reason","r","v","known","unknown"]);
}
function originalDiagnostics(){
 const f=state.first;
 const nums=f.outputs;
 const numerics=[["r",2],["v",6],["known",1],["unknown",3]];
 const valuesRight=numerics.every(([k,n])=>matches(Number(nums[k]),n));
 const modelRight=f.model==="mixed";
 if (!modelRight && valuesRight)return "right_values_wrong_model";
 if (!modelRight)return "wrong_topology";
 if (!valuesRight)return "correct_model_wrong_values";
 return "matched";
}
function boundaryCheck(opts){
 return opts.high==="no"&&opts.low==="no"&&matches(Number(opts.lower),2)&&matches(Number(opts.upper),6)&&
    clean(opts.reason).length>=25;
}
async function loadFeedback() {
 if(feedback||blocked||!state?.first||loadingFeedback)return Boolean(feedback);
 loadingFeedback=true;
 try{
   const asset=await fetchPinned("postattempt.v1.json",PIN.postattempt,PIN.postattempt_sha256);
   const x=asset.json;
   if(x.schema!=="g9v41-ph11-07-r4-native-feedback/v1"||x.status!=="AUTHOR_EXPOSED_CANDIDATE__ACADEMIC_HOLD"||
      x.revision!==prompt.revision||x.task_uid!==prompt.task.uid)throw Error("Answer/revision/source-role mismatch");
   feedback=x;render();return true;
 }catch(e){error("Postattempt feedback inaccessible or untrusted: "+String(e.message||e));return false}
 finally{loadingFeedback=false}
}
function render(){
 if(blocked||!state)return;
 for(const id of ["source-panel","predict-panel","first-panel","reconstruct-panel",
    "diagnose-panel","repair-panel","boundary-panel","return-panel","complete-panel"])
   visible(id,false);
 visible("source-panel",!state.source);
 visible("study-panel",Boolean(state.source));
 visible("predict-panel",Boolean(state.source)&&!state.prediction);
 visible("first-panel",Boolean(state.prediction)&&!state.first);
 visible("reconstruct-panel",Boolean(state.first)&&Boolean(feedback)&&!state.reconstruction);
 if(state.reconstructionExposure && feedback){
   $("reconstruct-list").replaceChildren(...feedback.reconstruct.map(s=>element("li",s)));
   visible("reconstruct-model",true);
 } else {
   $("reconstruct-list").replaceChildren();
   visible("reconstruct-model",false);
 }
 visible("diagnose-panel",Boolean(state.reconstruction)&&Boolean(feedback)&&!state.diagnosis);
 visible("repair-panel",Boolean(state.diagnosis)&&Boolean(feedback)&&!state.repair);
 visible("boundary-panel",Boolean(state.repair)&&Boolean(feedback)&&!state.boundary?.checked&&!state.boundaryRepair?.checked);
 visible("return-panel",Boolean(state.boundary?.checked||state.boundaryRepair?.checked)&&!state.sourceReturn);
 visible("complete-panel",Boolean(state.sourceReturn));
 if(state.source) txt("source-recap","Source first attempt saved independently; your original response cannot be replaced through this interface.");
 if(state.prediction)txt("predict-recap","Prediction saved separately at "+state.prediction.at);
 if(state.first) {
   txt("first-recap","First task reasoning and four numerical fields saved separately at "+state.first.at);
   txt("first-record",state.first.reason);
   txt("first-values",JSON.stringify({model:state.first.model,...state.first.outputs}));
 }
 if(state.reconstruction&&feedback) {
   txt("diagnosis-text",feedback.branches[originalDiagnostics()]);
   txt("diagnosis-rule","Based on frozen selected model and four saved numerical checks. This is NOT free-text reasoning assessment.");
 }
 if(state.diagnosis&&feedback) txt("repair-text",feedback.repair);
 if(state.repair) {
   txt("boundary-question",prompt.task.boundary.stem);
   if(state.boundary&&!state.boundary.checked){
     txt("boundary-result","Your saved boundary result did not match the author's four structured checks. Correct a NEW response to continue; the original boundary answer remains stored.");
     txt("boundary-model",feedback.boundary.model);
     visible("boundary-repair-panel",true);
     visible("boundary-first-panel",false);
   }else{
     visible("boundary-repair-panel",false);visible("boundary-first-panel",true);
   }
 }
 preserveStage();
}
async function start(){
 if(!ROOT)return;
 try{
  if(!checkCrypto())throw Error("Secure context / content digest unavailable");
  const asset=await fetchPinned("prompt.v1.json",PIN.prompt,PIN.prompt_sha256);
  prompt=asset.json;
  if(prompt.schema!=="g9v41-ph11-07-r4-native-prompt/v1"||
    prompt.status!=="AUTHOR_EXPOSED_CANDIDATE__ACADEMIC_HOLD"||
    prompt.source.role!=="ORIGINAL_AUTHOR_ONLY_NOT_NSEJS")throw Error("Wrong source role/schema");
  txt("source-question",prompt.source.question);
  txt("predict-question",prompt.task.prediction);
  txt("first-question",prompt.task.stem);
  txt("manifest-id",prompt.revision+" · source pin "+PIN.prompt.slice(0,12)+" · answer pin "+PIN.postattempt.slice(0,12));
  populateSelect("source-model",prompt.source.initial_model_options,"Select an initial model");
  populateSelect("task-model",prompt.task.model_options,"Select your task model");
  populateSelect("boundary-high",prompt.task.boundary.checks[0].options,"Select");
  populateSelect("boundary-low",prompt.task.boundary.checks[1].options,"Select");
  populateSelect("correct-high",prompt.task.boundary.checks[0].options,"Select");
  populateSelect("correct-low",prompt.task.boundary.checks[1].options,"Select");
  await enter();
  $("loading").hidden=true;
  render();
  if(state.first)await loadFeedback();
 }catch(e){error("Native candidate failed closed at entry: "+String(e.message||e))}
}
$("save-source").addEventListener("click",async()=>{
 if(!textLength("source-reason",20)||!$("source-model").value){tell("Choose a source model and write your own initial reasoning (20+ characters).");return}
 await commit("source",{model:$("source-model").value,reason:clean($("source-reason").value)},null);
});
$("save-prediction").addEventListener("click",async()=>{
 if(!textLength("predict",12)){tell("Record an independent prediction and reason before calculation.");return}
 await commit("prediction",{answer:clean($("predict").value)},"source");
});
$("save-first").addEventListener("click",async()=>{
 const model=$("task-model").value, reason=clean($("first-reason").value);
 const outputs={};for(const id of ["r","v","known","unknown"])outputs[id]=numerical(id);
 if(!model||reason.length<40||Object.values(outputs).some(x=>!Number.isFinite(x))){
   tell("Select a model, supply all four numerical results and 40+ characters of reasoning.");return
 }
 if(await commit("first",{model,reason,outputs,prediction_seq:state.prediction.at},"prediction"))
   await loadFeedback();
});
$("open-reconstruct").addEventListener("click",async()=>{if(feedback&&state?.first) {
 await commit("reconstructionExposure",{viewed:true},"first");
}});
$("save-reconstruction").addEventListener("click",async()=>{
 if(!feedback||!state?.reconstructionExposure||!textLength("reconstruct-response",20)){tell("First open the reconstruction and compare it with your saved attempt; cite a discrepancy or check.");return}
 await commit("reconstruction",{comparison:clean($("reconstruct-response").value)},"first");
});
$("save-diagnosis").addEventListener("click",async()=>{
 if(!feedback||!textLength("diagnosis-evidence",20)){tell("Quote actual evidence from your saved response before continuing.");return}
 await commit("diagnosis",{branch:originalDiagnostics(),evidence:clean($("diagnosis-evidence").value),automatic_text_check:false},"reconstruction");
});
$("save-repair").addEventListener("click",async()=>{
 if(!feedback||!textLength("repair-answer",30)){tell("Record a corrected argument and conservation checks before the boundary.");return}
 await commit("repair",{answer:clean($("repair-answer").value),grading:"UNGRADED_TEXT"},"diagnosis");
});
function boundaryInput(prefix){return{
 high:$(prefix+"high").value,low:$(prefix+"low").value,
 lower:numerical(prefix+"lower"),upper:numerical(prefix+"upper"),
 reason:clean($(prefix+"reason").value)}}
$("save-boundary").addEventListener("click",async()=>{
 if(!feedback||!state?.repair)return;
 const candidate=boundaryInput("boundary-");
 if(candidate.high===""||candidate.low===""||!Number.isFinite(candidate.lower)||!Number.isFinite(candidate.upper)||candidate.reason.length<25){
  tell("Answer both feasibility choices, two numeric limits and your own 25+ character reasoning.");return
 }
 const checked=boundaryCheck(candidate);
 await commit("boundary",{...candidate,checked,assisted:false,free_text_graded:false},"repair");
});
$("save-boundary-repair").addEventListener("click",async()=>{
 if(!state?.boundary||state.boundary.checked)return;
 const candidate=boundaryInput("correct-");
 if(candidate.high===""||candidate.low===""||!Number.isFinite(candidate.lower)||!Number.isFinite(candidate.upper)||candidate.reason.length<25){
  tell("Provide corrected binary decisions, both current limits and a new explanation.");return
 }
 if(!boundaryCheck(candidate)){tell("Boundary correction still fails the structured checks. Return is locked; no mastery inferred.");return}
 await commit("boundaryRepair",{...candidate,checked:true,assisted:true,free_text_graded:false},"boundary");
});
$("save-return").addEventListener("click",async()=>{
 if(!state?.boundary?.checked&&!state?.boundaryRepair?.checked)return;
 if(!textLength("source-return",25)){tell("Reattempt the original source-style problem with model and numerical checks.");return}
 await commit("sourceReturn",{answer:clean($("source-return").value),graded:false},"boundary");
});
window.addEventListener("storage",ev=>{
 if(blocked||!prompt||ev.key!==KEY)return;
 try{const latest=freshRead();if(latest.seq>state.seq){state=latest;render();tell("State updated from another tab (seq "+state.seq+").")}}
 catch(e){error("External tab changed the attempt to an invalid revision")}
});
start();
})();
