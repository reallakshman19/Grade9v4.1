/* PH02 Core1B author candidate. Protected browser learning workflow, not secure examination invigilation or academic approval. */
const mount=document.querySelector("[data-ph02-practice]");
const uid=mount?.dataset.unit;
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const p=s=>"<p>"+esc(s)+"</p>";
let ptask=null, rec=null, key=null, contentFingerprint=null;
const $=id=>document.getElementById(id);
function fail(message){const b=$("runtimeStatus");if(b){b.className="error";b.textContent="HOLD: "+message;}else if(mount){mount.className="error";mount.textContent="PH02 protected task unavailable: "+message;}}
function ensureStored(value){
  try{
    const serialized=JSON.stringify(value);
    localStorage.setItem(key,serialized);
    if(localStorage.getItem(key)!==serialized)throw Error("storage round-trip mismatch");
  }catch(e){fail("Storage write/read unavailable. No answers or hints will unlock. Your input remains copyable. "+String(e.message||e));return false}
  rec=value;return true;
}
function expose(event,value){
  const next={...rec,exposure:[...(rec.exposure||[]),{kind:event,at:new Date().toISOString()}],...value};
  return ensureStored(next);
}
function loadState(){
  try{
    const raw=localStorage.getItem(key);
    if(raw){
      const x=JSON.parse(raw);
      if(!x||x.task_uid!==ptask.uid||x.revision!==ptask.revision||x.content_fingerprint!==contentFingerprint||!x.first_answer||!x.first_prediction||!Array.isArray(x.exposure))throw Error("invalid or stale stored revision");
      rec=x;
    }
    const stale=Object.keys(localStorage).filter(k=>k.startsWith("G9V41:PH02:"+ptask.uid+":")&&k!==key&&k!==key+":prehelp");
    if(stale.length)$("revisionNote").textContent="Older content revision(s) remain stored separately. Old first answers are not imported into this task.";
  }catch(e){fail("Stored data cannot be verified. Do not delete prior learner evidence. "+String(e.message||e));return false}
  return true;
}
function refresh(){
  const saved=!!rec?.first_answer;
  $("prediction").disabled=saved;$("attempt").disabled=saved;
  $("firstCommit").hidden=saved;$("postAttempt").hidden=!saved;
  if(saved){$("prediction").value=rec.first_prediction;$("attempt").value=rec.first_answer;$("firstIntegrity").textContent="First prediction and attempt saved immutably for revision "+rec.revision+" at "+rec.first_at+". Later repairs cannot overwrite them.";}
  for(let i=0;i<3;i++){const visible=saved&&(rec.hints_seen||0)>i;const node=$("hint"+(i+1));node.hidden=!visible;if(visible)node.innerHTML="<strong>H"+(i+1)+"</strong>"+p(ptask.hints[i]);}
  $("hintBtn").hidden=!saved||(rec?.hints_seen||0)>=3;
  if(saved&&(!rec.hints_seen||rec.hints_seen<3))$("hintBtn").textContent="Open H"+((rec.hints_seen||0)+1)+" support";
  $("reconstructBtn").hidden=!saved||!!rec?.reconstruct_seen;
  $("reconstruction").hidden=!saved||!rec?.reconstruct_seen;
  if(saved&&rec?.reconstruct_seen)$("reconstruction").innerHTML="<h3>Shortest defensible route</h3>"+p(ptask.reconstruction)+"<h3>Independent route/check</h3>"+p(ptask.alternative);
  $("diagnoseStage").hidden=!rec?.reconstruct_seen;
  if(rec?.reconstruct_seen)$("diagnosisGuidance").innerHTML=p(ptask.diagnosis);
  $("diagnosis").disabled=!!rec?.diagnosis_text;$("diagnoseBtn").hidden=!!rec?.diagnosis_text;
  if(rec?.diagnosis_text)$("diagnosis").value=rec.diagnosis_text;
  $("repairStage").hidden=!rec?.diagnosis_text;
  if(rec?.diagnosis_text)$("repairGuidance").innerHTML=p(ptask.repair);$("repair").disabled=!!rec?.repair_text;$("repairBtn").hidden=!!rec?.repair_text;
  if(rec?.repair_text)$("repair").value=rec.repair_text;
  $("boundaryStage").hidden=!rec?.repair_text;
  if(rec?.repair_text)$("boundaryQuestion").innerHTML=p(ptask.boundaryPrompt);
  $("boundary").disabled=!!rec?.boundary_attempt;$("boundaryBtn").hidden=!!rec?.boundary_attempt;
  if(rec?.boundary_attempt)$("boundary").value=rec.boundary_attempt;
  $("boundaryRevealBtn").hidden=!rec?.boundary_attempt||!!rec?.boundary_revealed;
  $("boundaryModel").hidden=!rec?.boundary_revealed;
  if(rec?.boundary_revealed)$("boundaryModel").innerHTML=p(ptask.boundaryModel);
  $("runtimeStatus").textContent=saved?"Candidate cycle loaded. First attempt protected; assistance and revisions logged.":"Candidate task loaded. Submit a real first prediction and reasoning before hints/reconstruction.";
  $("runtimeStatus").className="status";
}
function bind(){
 $("firstCommit").addEventListener("click",()=>{
   if(rec?.first_answer)return;
   const prediction=$("prediction").value.trim(),answer=$("attempt").value.trim();
   if(!prediction||!answer){fail("Both a prediction and an explained first attempt are required.");return;}
   let prehelp=false;
   try{prehelp=localStorage.getItem(key+":prehelp")==="1"}catch(e){fail("Storage unavailable: first attempt cannot be protected.");return;}
   const next={task_uid:ptask.uid,revision:ptask.revision,first_prediction:prediction,first_answer:answer,content_fingerprint:contentFingerprint,first_at:new Date().toISOString(),assisted_before_first:prehelp,exposure:prehelp?[{kind:"linked_lesson_pre_commit",at:new Date().toISOString()}]:[],hints_seen:0,reconstruct_seen:false};
   if(ensureStored(next))refresh();
 });
 $("hintBtn").addEventListener("click",()=>{
   if(!rec?.first_answer)return fail("Commit a first attempt before hints.");
   const n=rec.hints_seen||0;
   if(n>=3)return;
   if(expose("H"+(n+1),{hints_seen:n+1}))refresh();
 });
 $("reconstructBtn").addEventListener("click",()=>{
   if(!rec?.first_answer)return fail("Commit a first attempt before reconstruction.");
   if(expose("reconstruction",{reconstruct_seen:true}))refresh();
 });
 $("diagnoseBtn").addEventListener("click",()=>{
   if(!rec?.reconstruct_seen)return fail("Reconstruct before diagnosis.");
   const t=$("diagnosis").value.trim();
   if(!t)return fail("Record the first divergence or explicitly state uncertainty.");
   if(expose("diagnosis",{diagnosis_text:t}))refresh();
 });
 $("repairBtn").addEventListener("click",()=>{
   if(!rec?.diagnosis_text)return fail("Save diagnosis before repair.");
   const t=$("repair").value.trim();
   if(!t)return fail("Write a reasoned repaired step.");
   if(expose("repair",{repair_text:t}))refresh();
 });
 $("boundaryBtn").addEventListener("click",()=>{
   if(!rec?.repair_text)return fail("Save repair before boundary attempt.");
   const t=$("boundary").value.trim();
   if(!t)return fail("Attempt the new condition before revealing its model.");
   if(expose("boundary_attempt",{boundary_attempt:t,boundary_at:new Date().toISOString()}))refresh();
 });
 $("boundaryRevealBtn").addEventListener("click",()=>{
   if(!rec?.boundary_attempt)return fail("Boundary attempt must be persisted before answer.");
   if(expose("boundary_reconstruction",{boundary_revealed:true}))refresh();
 });
 $("helpLink").addEventListener("click",event=>{
   if(!rec?.first_answer){
     try{localStorage.setItem(key+":prehelp","1");if(localStorage.getItem(key+":prehelp")!=="1")throw Error("readback failed");}
     catch(e){event.preventDefault();fail("Cannot record pre-commit help, so lesson navigation is blocked from this attempt route.");}
   }else if(!expose("linked_lesson_post_commit",{})){event.preventDefault();}
 });
}
async function init(){
 try{
  if(!mount||!uid)throw Error("Missing exact practice identity");
  const response=await fetch(new URL("./units.v1.json",import.meta.url),{cache:"no-store"});
  if(!response.ok)throw Error("candidate data HTTP "+response.status);
  const data=await response.json();
  const qresp=await fetch(new URL("./qrt-candidates.v1.json",import.meta.url),{cache:"no-store"});
  if(!qresp.ok)throw Error("QRT source unavailable: HTTP "+qresp.status);
  const qdata=await qresp.json();
  if(data.schema!=="g9v41-ph02-author-candidate-content/v1"||data.academic_status!=="HOLD"||
      qdata.schema!=="g9v41-ph02-qrt-authored-candidates/v1"||qdata.original_exam_items!==0||
      qdata.status!=="AUTHOR_PROPOSED__INDEPENDENT_QRT_HOLD")throw Error("Invalid source/schema/status; HOLD");
  const isMain=uid==="PH02-MAIN";
  const requested=new URL(location.href).searchParams.get("task");
  const own=data.units.find(x=>x.id===uid);
  const candidates=isMain?qdata.main_cycles:(own?[own.practice,...qdata.tasks.filter(t=>t.unit===uid)]:[]);
  if(!candidates.length)throw Error("Missing exact candidate unit/cycles");
  ptask=requested?candidates.find(t=>t.uid===requested):candidates[0];
  if(!ptask||!ptask.uid||!ptask.revision)throw Error("Unknown or stale task UID; HOLD");
  const u=isMain?data.units.find(x=>x.id===ptask.unit):own;
  if(!u)throw Error("Cross-topic task owner missing; HOLD");
  // Bind learner evidence to the *actual authored contents* as well as the UID/revision.
  // A changed prompt, worked answer, hints or boundary model cannot silently reuse a previous attempt.
  if(!globalThis.crypto?.subtle || typeof TextEncoder==="undefined")throw Error("Content-digest protection unavailable");
  const fingerprintSource=JSON.stringify([ptask.uid,ptask.revision,ptask.prediction,ptask.prompt,ptask.w,
    ptask.reconstruction,ptask.alternative,ptask.hints,ptask.boundaryPrompt,ptask.boundaryModel]);
  const bytes=new TextEncoder().encode(fingerprintSource);
  const hash=await crypto.subtle.digest("SHA-256",bytes);
  contentFingerprint=Array.from(new Uint8Array(hash),b=>b.toString(16).padStart(2,"0")).join("");
  key="G9V41:PH02:"+ptask.uid+":"+ptask.revision+":"+contentFingerprint;
  const lessonHref=isMain?"../../../textbook/PH02/"+ptask.unit.slice(-3)+"/index.html":"../../../textbook/PH02/"+uid.split("-").at(-1)+"/index.html";
  const taskNav='<div id="taskNav" class="card"><strong>'+ (isMain?"Integrated MAIN candidates":"This subtopic's three operation candidates")+'</strong><div>'+candidates.map(t=>'<a class="action" href="?task='+encodeURIComponent(t.uid)+'">'+esc(t.id||t.op||t.uid)+(t.uid===ptask.uid?" · current":"")+'</a>').join('')+'</div></div>';
  document.title=uid+" · "+ptask.uid+" · Core1B protected transfer (candidate)";
  mount.innerHTML='<h1>'+esc(uid)+" · "+esc(u.title)+'</h1>'+taskNav+'<p class="notice"><strong>AUTHOR CANDIDATE · ACADEMIC/QRT HOLD.</strong> This is authored practice, not a validated NSEJS paper or qualification of learner mastery. Browser storage protects learning sequence but is not a secure invigilation boundary.</p>'+
   '<p class="fine">Exact authored UID: '+esc(ptask.uid)+' · revision: '+esc(ptask.revision)+' · digest: '+esc(contentFingerprint.slice(0,12))+'</p><p id="runtimeStatus" class="status" role="status">Loading…</p><p id="revisionNote" class="fine"></p>'+
   '<section class="step"><h2>1 · Predict before solving</h2>'+p(ptask.prediction)+'<label for="prediction">Your prediction and reason</label><textarea id="prediction"></textarea></section>'+
   '<section class="step"><h2>2 · Attempt: protect your decisive work</h2>'+p(ptask.prompt)+'<label for="attempt">Your independent calculation, model and check</label><textarea id="attempt"></textarea><button id="firstCommit" type="button">Commit prediction + first reasoning</button><p id="firstIntegrity" class="fine"></p><p><a id="helpLink" href="'+lessonHref+'">Consult this subtopic’s Core1A textbook (help exposure tracked)</a></p></section>'+
   '<div id="postAttempt" hidden><section class="step"><h2>H1–H3 · Optional ordered support</h2><p>Only after the first answer has been saved. Supports may orient, but do not count as independent first attempts.</p><button id="hintBtn" type="button" class="secondary">Open H1 support</button>'+
   u.practice.hints.map((h,i)=>'<div id="hint'+(i+1)+'" class="help" hidden></div>').join('')+'</section>'+
   '<section class="step"><h2>3 · Reconstruct after attempting</h2><button id="reconstructBtn" type="button" class="secondary">Reveal reasoned reconstruction</button><div id="reconstruction" class="answer" hidden></div></section>'+
   '<section id="diagnoseStage" class="step" hidden><h2>4 · Diagnose the first divergence</h2><div id="diagnosisGuidance"></div><label for="diagnosis">Which reasoning step diverged, or what evidence is missing?</label><textarea id="diagnosis"></textarea><button id="diagnoseBtn" type="button">Save diagnosis</button></section>'+
   '<section id="repairStage" class="step" hidden><h2>5 · Repair that step</h2><div id="repairGuidance"></div><label for="repair">Your separate repaired explanation</label><textarea id="repair"></textarea><button id="repairBtn" type="button">Save repair separately</button></section>'+
   '<section id="boundaryStage" class="step" hidden><h2>6 · Boundary: new changed condition</h2><div id="boundaryQuestion"></div><label for="boundary">Your new attempt before seeing the model</label><textarea id="boundary"></textarea><button id="boundaryBtn" type="button">Commit boundary attempt</button><button id="boundaryRevealBtn" type="button" class="secondary" hidden>Reveal boundary model</button><div id="boundaryModel" class="answer" hidden></div></section></div>'+
   '<p class="fine">There is no automatic correctness or academic status promotion. Review requires source-specific B1–B7 evidence, exact-head browser receipts and an independent R01 assessor.</p>';
  if(!loadState()){$("firstCommit").disabled=true;return;}
  bind();refresh();
 }catch(e){fail(String(e.message||e));}
}
await init();
