/* PH05 source-attempt checkpoint: candidate learning state only, no question/key copied to UI. */
const mount = document.getElementById("sourceCheckpoint");
const params = new URL(location.href).searchParams;
const requested = params.get("source");
const ownerPath = "../textbook/PH05/index.html";
const state = { entry:null, saved:null, key:null, revision:null };
const el = (tag,text,cl) => { const x=document.createElement(tag); if(text!==undefined)x.textContent=text; if(cl)x.className=cl; return x; };
const addLink = (parent,label,url) => { const a=el("a",label); a.href=url; if(url.startsWith("https:")){a.target="_blank";a.rel="noopener noreferrer"} parent.appendChild(a);return a; };
function error(message) {
  mount.replaceChildren(el("p","HOLD · "+message,"error"));
  const back=el("p");addLink(back,"Return to PH05 question-led journey",ownerPath);mount.appendChild(back);
}
function safeString(value){return typeof value==="string"&&value.length>0&&value.length<12000;}
async function sha(raw){if(!globalThis.crypto?.subtle)throw Error("Revision hash service unavailable");
 const bytes=new TextEncoder().encode(raw);
 return Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",bytes)),b=>b.toString(16).padStart(2,"0")).join("");
}
function loadSaved(){
 try {
  const raw=localStorage.getItem(state.key);
  if(!raw)return null;
  const x=JSON.parse(raw);
  if(!x||x.source_uid!==state.entry.source_uid||x.revision!==state.revision||!safeString(x.prediction)||!safeString(x.first_reasoning)||!Array.isArray(x.exposure)||!x.first_at)
    throw Error("Stored record does not match current question revision");
  return x;
 }catch(e){throw Error("Saved first attempt cannot be verified; do not erase or overwrite it: "+String(e.message||e));}
}
function store(x){
 const raw=JSON.stringify(x);
 localStorage.setItem(state.key,raw);
 if(localStorage.getItem(state.key)!==raw)throw Error("Storage read-back mismatch");
 state.saved=x;
}
function stage(){
 const e=state.entry;
 mount.replaceChildren();
 const badge=el("p","Original question · "+e.locator+" · source authority: PUBLIC IAPT PAPER/KEY CROSSCHECK · academic and independent QRT HOLD","fine");
 mount.appendChild(badge);
 const top=el("section","", "card");
 top.appendChild(el("h2","1 · Open the original examination question"));
 top.appendChild(el("p",e.neutral_prompt));
 const intro=el("p");addLink(intro,"Open the official IAPT question paper (no solution)",e.official_paper_url+"#page="+e.official_paper_page);top.appendChild(intro);
 top.appendChild(el("p","Find the exact question number shown above. Read the original options in the paper; do not open the answer key yet.","fine"));
 mount.appendChild(top);
 const first=el("section",undefined,"step");
 first.appendChild(el("h2","2 · Preserve your independent first reasoning"));
 const pred=el("textarea"),reason=el("textarea");
 pred.id="firstPrediction";reason.id="firstReasoning";
 pred.setAttribute("aria-label","Your initial prediction");
 reason.setAttribute("aria-label","Your first independent reasoning");
 pred.placeholder="What do you predict before calculating?";reason.placeholder="Which system, physical law, derivation and check will you use?";
 const predLabel=el("label","Prediction");predLabel.htmlFor=pred.id;
 const reasonLabel=el("label","Your reasoning");reasonLabel.htmlFor=reason.id;
 first.append(predLabel,pred,reasonLabel,reason);
 const submit=el("button","Protect first attempt");submit.type="button";first.appendChild(submit);
 const status=el("p", "", "status");status.setAttribute("role","status");first.appendChild(status);
 mount.appendChild(first);
 const help=el("section",undefined,"card");help.id="afterFirst";help.hidden=true;
 help.appendChild(el("h2","3 · Study the decisive reasoning and attempt a fresh transfer"));
 help.appendChild(el("p","These tasks are authored teaching candidates, not certified original D3/D4 questions."));
 const learn=el("p");
 e.core1a.forEach((unit,i)=>{if(i)learn.append(" · ");const a=addLink(learn,"Learn Core1A "+unit,"../textbook/PH05/"+unit+"/index.html");a.addEventListener("click",event=>{try{recordExposure("core1a_"+unit)}catch(err){event.preventDefault();error(String(err.message||err))}})});
 help.appendChild(learn);
 const target=e.transfer.includes("MAIN")?"main":e.core1a[0];
 const transferP=el("p");
 const transfer=addLink(transferP,"Try protected author-created transfer ("+e.transfer_demand+")","../core1/PH05/"+target+"/index.html?task="+encodeURIComponent(e.transfer)+"&source="+encodeURIComponent(e.source_uid));
 transfer.addEventListener("click",event=>{try{recordExposure("core1b_transfer")}catch(err){event.preventDefault();error(String(err.message||err))}});
 help.appendChild(transferP);
 help.appendChild(el("h2","4 · Return to the original paper"));
 const backP=el("p");const back=addLink(backP,"Revisit exact IAPT source question",e.official_paper_url+"#page="+e.official_paper_page);
 back.addEventListener("click",event=>{try{recordExposure("source_return")}catch(err){event.preventDefault();error(String(err.message||err))}});
 help.appendChild(backP);
 help.appendChild(el("p","Your first attempt remains unchanged after hints or lessons. Read the paper again and evaluate your reasoning yourself; no academic pass is awarded.","fine"));
 mount.appendChild(help);
 function refresh(){
  if(state.saved){
   pred.value=state.saved.prediction;reason.value=state.saved.first_reasoning;
   pred.disabled=true;reason.disabled=true;submit.disabled=true;submit.hidden=true;help.hidden=false;
   status.textContent="First prediction and reasoning preserved for this exact local question revision; timestamp "+state.saved.first_at+".";
  }else{help.hidden=true;status.textContent="Core1A and transfer links unlock only after a stored first attempt."}
 }
 function recordExposure(kind){if(!state.saved)throw Error("First attempt not committed");
  store({...state.saved,exposure:[...state.saved.exposure,{kind,at:new Date().toISOString()}]});}
 submit.addEventListener("click",()=>{
  if(state.saved)return;
  const p=pred.value.trim(),r=reason.value.trim();
  if(p.length<3||r.length<20||p.length>4000||r.length>10000){status.textContent="Write a prediction and at least 20 characters of independent reasoning before committing.";return}
  try{store({source_uid:e.source_uid,revision:state.revision,first_at:new Date().toISOString(),prediction:p,first_reasoning:r,exposure:[]});refresh()}
  catch(err){error("Unable to persist first attempt. No assistance unlocked. "+String(err.message||err))}
 });
 refresh();
}
try{
 const r=await fetch("./source-to-learning.v1.json",{cache:"no-store"});
 if(!r.ok)throw Error("Source register HTTP "+r.status);
 const d=await r.json();
 if(d.schema!=="g9v41-ph05-source-to-learning/v1"||d.academic_status!=="HOLD"||d.admitted_original_d3_d4!==0)throw Error("Unapproved/unknown source register");
 if(!requested)throw Error("No original question selected");
 const e=d.source_candidates.find(x=>x.source_uid===requested);
 if(!e||e.corpus_id!==null||e.source_status!=="EXTERNAL_CUSTODY_HOLD"||
    !e.official_paper_url?.startsWith("https://iapt.org.in/")||!e.transfer||!safeString(e.neutral_prompt)||!Array.isArray(e.core1a))
    throw Error("Unsupported external source candidate; no invented substitute");
 state.entry=e;
 state.revision=await sha(JSON.stringify([e.source_uid,e.locator,e.official_paper_url,e.official_paper_page,e.neutral_prompt,e.core1a,e.transfer]));
 state.key="G9V41:PH05:SOURCE_FIRST:"+e.source_uid+":"+state.revision;
 state.saved=loadSaved();
 // Verify storage service before showing any post-attempt controls.
 const probe=state.key+":probe";localStorage.setItem(probe,"verified");
 if(localStorage.getItem(probe)!=="verified")throw Error("Storage is not writable");
 localStorage.removeItem(probe);
 stage();
}catch(e){error(String(e.message||e))}
