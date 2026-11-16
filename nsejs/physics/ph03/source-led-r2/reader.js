const $=id=>document.getElementById(id),root=$("root");
const e=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const p=s=>"<p>"+e(s)+"</p>", link=(url,label)=>'<a href="'+e(url)+'">'+e(label)+'</a>';
const steps=items=>"<ol>"+items.map(x=>"<li>"+e(x)+"</li>").join("")+"</ol>";
const get=async path=>{const r=await fetch(path,{cache:"no-store"});if(!r.ok)throw Error("Missing "+path);return r.json()};
const digest=async bytes=>Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",bytes)),b=>b.toString(16).padStart(2,"0")).join("");
const hash=async data=>digest(new TextEncoder().encode(JSON.stringify(data)));
const params=new URLSearchParams(location.search),stage=params.get("stage")||"source",taskId=params.get("task")||"A";
const d=await get("content.v2.json"),m=await get("models.v2.json");
if(d.release!=="HOLD"||m.status!=="AUTHOR_ONLY_HOLD")throw Error("Unexpected release state");
const exposureKey="G9V41:PH03:R2:EXPOSURE";
const probe=()=>{const k=exposureKey+":probe";localStorage.setItem(k,"1");if(localStorage.getItem(k)!=="1")throw Error("Storage readback failed");localStorage.removeItem(k)};
const exposure=()=>{const raw=localStorage.getItem(exposureKey);return raw?JSON.parse(raw):null};
async function markExposure(){
 if(!navigator.locks)throw Error("Cross-tab lock unavailable");
 await navigator.locks.request(exposureKey,async()=>{if(!exposure()){const raw=JSON.stringify({stage,taskId,at:new Date().toISOString()});localStorage.setItem(exposureKey,raw);if(localStorage.getItem(exposureKey)!==raw)throw Error("Exposure write failed")}});
}
const failPage=err=>{root.textContent="HOLD: "+err.message+"; protected practice unavailable."};
const readFigure=async path=>{const r=await fetch(path,{cache:"no-store"});if(!r.ok)throw Error("Missing required figure: "+path);const bytes=await r.arrayBuffer();if(bytes.byteLength<100)throw Error("Invalid figure bytes");const url=URL.createObjectURL(new Blob([bytes],{type:"image/svg+xml"}));const im=new Image();im.src=url;await im.decode();if(!im.naturalWidth)throw Error("Invalid image");return {sha:await digest(bytes),url}};
const revisionFor=async (t,model)=>{if(!model||model.uid!==(t.uid||t.id)||model.revision!==t.revision)throw Error("Exact model identity mismatch");const figs={};for(const [role,path] of [["prompt",t.figure],["solution",model.solutionFigure],["boundary",model.boundaryFigure]])if(path)figs[role]=await readFigure(path);const revision=await hash([t,model,Object.fromEntries(Object.entries(figs).map(([k,v])=>[k,v.sha])),d.source.id]);return {revision,figs,key:"G9V41:PH03:R2:"+(t.uid||t.id)+":"+revision}};
function readRecord(ref){const raw=localStorage.getItem(ref.key);if(!raw)return {revision:ref.revision,hints:0,events:[]};const x=JSON.parse(raw);if(x.revision!==ref.revision||!Array.isArray(x.events)||!Number.isInteger(x.hints)||x.hints<0||x.hints>3)throw Error("Invalid saved record");if(x.first){const sk=Array.isArray(x.first.skipped)?x.first.skipped:[];if(!x.first.at||!(x.first.reason||sk.includes("reason"))||!(x.first.prediction||sk.includes("prediction")))throw Error("Invalid first attempt")}return x}
/* Explicit skipped fields persist as null. They never earn mastery credit. */
const skipped=id=>$(id)?.dataset.skipped==="true";
const skipButton=(id,disabled=false,wasSkipped=false)=>disabled?(wasSkipped?'<small class="skip-recorded">Skipped · no credit</small>':""):'<button type="button" class="skip-field" data-skip-target="'+e(id)+'" aria-pressed="false" aria-label="Skip '+e(id)+' (no credit)">Skip</button>';
const textArea=(id,value="",disabled=false,wasSkipped=false)=>'<textarea id="'+e(id)+'" '+(disabled?"disabled ":"")+'>'+e(value??"")+'</textarea>'+skipButton(id,disabled,wasSkipped);
const fieldHTML=(fields,prefix,values={},disabled=false,oldSkipped=[])=>'<div class="fields">'+fields.map(([k,label,choices])=>{const id=prefix+k,wasSkipped=oldSkipped.includes(id),v=values[k];
 return '<div class="field-slot"><label for="'+e(id)+'">'+e(label)+(choices?'<select id="'+e(id)+'" '+(disabled?"disabled":"")+'><option value="">Choose</option>'+choices.map(([opt,optionLabel])=>'<option value="'+e(opt)+'" '+(v===opt?"selected":"")+'>'+e(optionLabel)+'</option>').join("")+'</select>':'<input type="number" step="any" id="'+e(id)+'" value="'+e(v??"")+'" '+(disabled?"disabled":"")+'>')+'</label>'+skipButton(id,disabled,wasSkipped)+'</div>'}).join("")+'</div>';
const readFields=(fields,prefix)=>{const result={};for(const [k,label,choices] of fields){const id=prefix+k;if(skipped(id)){result[k]=null;continue}const raw=$(id).value.trim();if(!raw)throw Error("Complete "+label+" or choose Skip");if(choices){if(!choices.some(([v])=>v===raw))throw Error("Choose a valid option");result[k]=raw}else{const n=Number(raw);if(!Number.isFinite(n))throw Error("Use a finite number");result[k]=n}}return result};
const skippedFields=(fields,prefix)=>fields.map(([k])=>prefix+k).filter(skipped);
root.addEventListener("click",event=>{
 const button=event.target.closest("button[data-skip-target]");if(!button||!root.contains(button))return;
 const target=$(button.dataset.skipTarget);if(!target||button.disabled)return;
 const next=target.dataset.skipped!=="true";target.dataset.skipped=String(next);target.disabled=next;
 button.textContent=next?"Undo skip":"Skip";button.setAttribute("aria-pressed",String(next));
 button.setAttribute("aria-label",(next?"Undo skip for ":"Skip ")+button.dataset.skipTarget+(next?"":" (no credit)"));
 const statusNode=$("status");if(statusNode)statusNode.textContent=next?"Field marked skipped; no credit. Use Undo skip to answer.":"Skip undone. Answer the field before saving, or skip again.";
});
const equal=(a,b)=>typeof b==="number"?typeof a==="number"&&Math.abs(a-b)<1e-6:a===b;
const matches=(actual,expected)=>Object.entries(expected).every(([k,v])=>equal(actual?.[k],v));
const infer=(id,fields,expected)=>{if(!fields||Object.values(fields).some(x=>x===null))return "insufficient";if(id==="A"){if(!equal(fields.v,expected.v))return "sign";if(!equal(fields.u,expected.u))return "momentum";if(!equal(fields.loss,expected.loss))return "energy";return "correct"}if(!equal(fields.j,expected.j))return "sign";if(!equal(fields.isolation,expected.isolation))return "momentum";if(!equal(fields.drop,expected.drop)||!equal(fields.conversion,expected.conversion))return "energy";return "correct"};
const selection=(options,name,value,disabled=false,wasSkipped=false)=>'<fieldset id="fieldset-'+e(name)+'"><legend>Choose one option</legend>'+options.map((x,i)=>{const v=String.fromCharCode(65+i);return '<label><input type="radio" name="'+name+'" value="'+v+'" '+(v===value?"checked ":"")+(disabled?"disabled":"")+'>'+e(x)+'</label>'}).join("")+'</fieldset>'+skipButton("fieldset-"+name,disabled,wasSkipped);
const selected=name=>skipped("fieldset-"+name)?null:document.querySelector('input[name="'+name+'"]:checked')?.value||null;
const fig=(ref,alt)=>'<figure><img src="'+e(ref.url)+'" alt="'+e(alt)+'"></figure>';
if(stage==="learn"){
 try{probe();await markExposure();root.replaceChildren($("learn").content.cloneNode(true));const update=()=>{const u=Number($("speed").value),P=8+u,V=P/3,K=16+.5*u*u,Kafter=1.5*V*V,L=K-Kafter;for(const [id,n] of [["pbar1",8],["pbar2",u],["pbar3",P]]){$(id).setAttribute("x",String(380+Math.min(0,n*18)));$(id).setAttribute("width",String(Math.abs(n*18)))}const kept=728*Kafter/K;$("kept").setAttribute("width",String(kept));$("converted").setAttribute("x",String(16+kept));$("converted").setAttribute("width",String(728-kept));$("simout").textContent="Partner "+u+" m/s · P = "+P.toFixed(1)+" kg·m/s · V = "+V.toFixed(2)+" m/s · K before = "+K.toFixed(2)+" J · K after = "+Kafter.toFixed(2)+" J · converted = "+Math.max(0,L).toFixed(2)+" J";$("modelnote").textContent=P===0?"Cancellation: the pair has zero momentum and zero final kinetic energy, despite positive incoming kinetic energy.":P<0?"Reversal: the partner's negative momentum outweighs the first block's positive momentum.":u===4?"Velocity matching: zero relative speed and zero conversion in the ideal formula; no overtaking impact.":"The sign of total momentum fixes the common direction."};$("speed").oninput=update;update();for(const im of root.querySelectorAll("img")){await im.decode();if(!im.naturalWidth)throw Error("Missing teaching figure")}}catch(err){failPage(err)}
}else if(stage==="bank"){
 root.innerHTML='<article><h2>Core2 · PH03 Golden Sample bank</h2><p>This is a chapter-local candidate bank, not the full historical inventory. The source paper is linked rather than republished.</p><h3>NSEJS 2023 · Set 51 Q39</h3><p>Original source locator · text and final key checked; visual, byte and rights custody HOLD. Record your answer using the original paper.</p><p class="actions">'+link("?stage=source","Attempt original source")+'</p><h3>New authored practice · two-interval reasoning</h3><p>Separate authored MCQ, not a previous examination item.</p><p class="actions">'+link("?stage=core2","Attempt authored assessment")+'</p><h3>Existing authored practice</h3><p>Original Grade9 collision–friction practice (legacy), not an examination question.</p><p class="actions">'+link("../../learn-mechanics.html","Open existing recovery route")+'</p><p>Other historical leads remain in the source census; they are not admitted questions.</p></article>';
}else if(["source","challenge","core2"].includes(stage)){
 const source=stage==="source",challenge=stage==="challenge",t=source?d.source:challenge?d.tasks[taskId]:d.core2,model=source?m.source:challenge?m[taskId]:m.core2;
 if(!t||!model){failPage(Error("Unknown task"));throw Error("Unknown task")}
 const title=source?"Core2 · original paper checkpoint":challenge?"Core1B · "+(taskId==="A"?"Reconstruct an unknown speed":"Test two experimental claims"):"Core2 · authored assessment";
 const prompt=source?"Open the original IAPT Set 51 paper, page 7, question 39. Read its figure and four options there; record the letter and your reasoning here. The original question and figure are not republished.":t.prompt;
 const fields=challenge?t.fields:[],opts=source||stage==="core2"?t.options:null;
 root.innerHTML='<article><p class="eyebrow">'+e(t.uid||t.id)+'</p><h2>'+e(title)+'</h2>'+p(prompt)+(source?'<p class="actions"><a target="_blank" rel="noopener" href="'+e(t.paper)+'#page=7">Open IAPT paper · Q39</a></p>':'<div id="promptfigure"></div>')+'<div id="firstform"></div><button id="commit" disabled>Save first response</button><p id="status" role="status">Checking revision and storage…</p><div id="helpers"></div><div id="post"></div></article>';
 const status=s=>$("status").textContent=s;
 let ref,rec,transferRefs=[];
 try{
  probe();if(!crypto?.subtle||!navigator.locks)throw Error("SHA-256 or cross-tab lock unavailable");
  if(!source)await markExposure();
  ref=await revisionFor(t,model);
  if(!source)$("promptfigure").innerHTML=fig(ref.figs.prompt,"Authored question-facing schematic, only stated conditions");
  if(source){try{transferRefs=await Promise.all(["A","B"].map(k=>revisionFor(d.tasks[k],m[k])))}catch(_){transferRefs=[]}}
  const completedTransfer=()=>{if(transferRefs.length!==2)return null;try{const receipts=transferRefs.map(r=>{const x=readRecord(r);return x.first&&x.repair&&x.boundary&&x.boundaryReveal?{revision:r.revision,boundary:x.boundary}:null});return receipts.every(Boolean)?receipts:null}catch(_){return null}};
  rec=readRecord(ref);
  const fail=err=>{$("post").replaceChildren();$("helpers").replaceChildren();$("commit").disabled=true;status("HOLD: "+err.message+"; no further disclosure.")};
  const save=async(fn,kind)=>{try{await navigator.locks.request(ref.key,async()=>{const old=readRecord(ref),next0=fn(old);if(!next0||next0===old){rec=old;return}const next={...next0,events:[...old.events,{kind,at:new Date().toISOString()}]},raw=JSON.stringify(next);localStorage.setItem(ref.key,raw);if(localStorage.getItem(ref.key)!==raw)throw Error("Attempt readback failed");rec=next});render()}catch(err){fail(err)}};
  const stageSave=(key,value,needs)=>save(old=>old.first&&needs(old)&&!old[key]?{...old,[key]:value}:old,key);
  const checked=(actual,expected,skipList=[])=>skipList.length||Object.values(actual||{}).some(x=>x===null)?"Some fields were skipped; this response is ungraded and earns no mastery credit.":matches(actual,expected)?"Structured values match the author model. Explanation still needs review.":"Some structured values differ from the author model; compare the relevant step. This is not a mastery verdict.";
  function render(){
   const f=rec.first;
   $("firstform").innerHTML='<label for="prediction">01 · Predict'+(challenge?": "+e(t.prediction):"")+'</label>'+textArea("prediction",f?.prediction,!!f,f?.skipped?.includes("prediction"))+(opts?selection(opts,"opt",f?.option,!!f,f?.skipped?.includes("opt")):"")+fieldHTML(fields,"first-",f?.fields||{},!!f,f?.skipped||[])+'<label for="reason">02 · Explain your reasoning</label>'+textArea("reason",f?.reason,!!f,f?.skipped?.includes("reason"));
   $("commit").disabled=!!f;$("helpers").replaceChildren();$("post").replaceChildren();
   if(!f){status(source?(exposure()?"Prior R2 learning exposure recorded; this will not be a cold diagnostic.":"No recorded R2 learning exposure; outside study and legacy exposure are unknown."):"Ready. Save prediction, structured answers and reasoning before hints or comparison.");return}
   status("First response preserved · "+(source?(f.exposure?"prior R2 exposure recorded":"no recorded R2 exposure; not a certified cold attempt"):"unassisted by R2 hints before commitment")+" · exact revision."+((f.skipped?.length||0)?" Skipped fields: "+f.skipped.join(", ")+" · no credit.":""));
   let h="";
   if(source){
    h='<h3>Original selection and reasoning saved</h3><p>Complete both transfer journeys before returning to the original paper. No assessment of your answer is shown yet.</p><p class="actions">'+link("?stage=learn","Open Core1A guide")+link("?stage=challenge&task=A","Challenge A")+link("?stage=challenge&task=B","Challenge B")+'</p>';
    if(rec.retry||completedTransfer())h+='<h3>Independent return to original</h3>'+selection(opts,"retryopt",rec.retry?.option,!!rec.retry,rec.retry?.skipped?.includes("retryopt"))+'<label for="retryreason">New reasoning</label>'+textArea("retryreason",rec.retry?.reason,!!rec.retry,rec.retry?.skipped?.includes("retryreason"))+'<button id="retrySave" '+(rec.retry?"disabled":"")+'>Save separate source return</button>';
    else h+=p("Source return is locked until both exact transfer boundaries have been compared.");
    if(rec.retry)h+='<h3>Source comparison · HOLD</h3>'+p("First selected "+(f.option||"(skipped)")+"; return selected "+(rec.retry.option||"(skipped)")+". The published final key is "+model.key+".")+steps(model.steps)+p(model.check)+'<p class="actions"><a href="'+e(t.key_url)+'" target="_blank" rel="noopener">Open published final key</a></p>';
   }else{
    if(!rec.revealed){$("helpers").innerHTML=model.hints.slice(0,rec.hints).map((s,i)=>p("H"+(i+1)+" · "+s)).join("")+(rec.hints<3?'<button id="hint">Next hint ('+(rec.hints+1)+' of 3)</button>':"");h='<button id="reveal">Compare reconstruction</button>'}
    else{
     h='<h3>03 · Reconstruct the reasoning</h3>'+steps(model.steps)+p(model.check)+(ref.figs.solution?fig(ref.figs.solution,"Post-commitment solution ledger"):"");
     if(challenge){
      const category=infer(taskId,f.fields,model.expected),diag=model.diagnostics[category];
      h+='<h3>04 · Locate the first divergence</h3><div class="feedback">'+p("Structured-response check: "+diag.label)+p("This only checks the supplied fields. Inspect your saved explanation for the actual first error; no inference is made about your understanding.")+'</div>';
      h+=rec.diagnosis?p(typeof rec.diagnosis==="string"?rec.diagnosis:(rec.diagnosis.skipped?"Diagnosis skipped · no credit":rec.diagnosis.reason)):'<label for="diagtext">Quote or explain the relevant step from your original reasoning; if uncertain, say so.</label>'+textArea("diagtext")+'<button id="diagnose">Save diagnosis</button>';
      if(rec.diagnosis){
       h+='<h3>05 · Repair that reasoning step</h3><div class="feedback">'+p(diag.repair)+'</div>'+fieldHTML(fields,"repair-",rec.repair?.fields||{},!!rec.repair,rec.repair?.skipped||[]);
       h+=rec.repair?p(rec.repair.reason||"Repair explanation skipped · no credit")+p(checked(rec.repair.fields,model.expected,rec.repair.skipped)):'<label for="repairreason">Rebuild your reasoning</label>'+textArea("repairreason")+'<button id="repairSave">Save repaired response</button>';
      }
      if(rec.repair){h+='<h3>06 · Changed-condition transfer</h3>'+p(t.boundaryPrompt)+fieldHTML(t.boundaryFields,"bound-",rec.boundary?.fields||{},!!rec.boundary,rec.boundary?.skipped||[]);h+=rec.boundary?p(rec.boundary.reason||"Boundary explanation skipped · no credit"):'<label for="boundaryreason">Explain which physical assumption changed</label>'+textArea("boundaryreason")+'<button id="boundarySave">Save independent boundary response</button>'}
      if(rec.boundary)h+=rec.boundaryReveal?'<h3>Compare boundary</h3>'+steps(model.boundarySteps)+p(checked(rec.boundary.fields,model.boundaryExpected,rec.boundary.skipped))+(ref.figs.boundary?fig(ref.figs.boundary,"Boundary solution state ledger"):"")+'<p class="actions">'+link("?stage=challenge&task="+(taskId==="A"?"B":"A"),"Other challenge")+link("?stage=source","Return to original source")+link("?stage=core2","Authored Core2")+'</p>':'<button id="boundaryReveal">Compare boundary</button>';
     }else h+=p(f.skipped?.length?"Some first fields were skipped; no correct-answer credit is awarded.":f.option===model.key?"Selection matches the authored key.":"Selection differs from the authored key.")+'<p class="actions">'+link("?stage=bank","Back to bank")+'</p>';
    }
   }
   $("post").innerHTML=h;
   if($("hint"))$("hint").onclick=()=>save(old=>old.first&&!old.revealed&&old.hints<3?{...old,hints:old.hints+1}:old,"hint");
   if($("reveal"))$("reveal").onclick=()=>stageSave("revealed",true,()=>true);
   if($("diagnose"))$("diagnose").onclick=()=>{const v=$("diagtext").value.trim(),skip=skipped("diagtext");if(v||skip)stageSave("diagnosis",skip?{reason:null,skipped:true}:v,o=>o.revealed);else status("Record evidence or select Skip (no credit).")};
   if($("repairSave"))$("repairSave").onclick=()=>{try{const reason=skipped("repairreason")?null:$("repairreason").value.trim();if(!reason&&!skipped("repairreason"))throw Error("Explain the repair or select Skip");const values=readFields(fields,"repair-"),sk=[...skippedFields(fields,"repair-"),...(skipped("repairreason")?["repairreason"]:[])];stageSave("repair",{fields:values,reason,skipped:sk},o=>o.diagnosis)}catch(err){status(err.message)}};
   if($("boundarySave"))$("boundarySave").onclick=()=>{try{const reason=skipped("boundaryreason")?null:$("boundaryreason").value.trim();if(!reason&&!skipped("boundaryreason"))throw Error("Explain the changed assumption or select Skip");const values=readFields(t.boundaryFields,"bound-"),sk=[...skippedFields(t.boundaryFields,"bound-"),...(skipped("boundaryreason")?["boundaryreason"]:[])];stageSave("boundary",{fields:values,reason,skipped:sk},o=>o.repair)}catch(err){status(err.message)}};
   if($("boundaryReveal"))$("boundaryReveal").onclick=()=>stageSave("boundaryReveal",true,o=>o.boundary);
   if($("retrySave"))$("retrySave").onclick=()=>{const option=selected("retryopt"),reason=skipped("retryreason")?null:$("retryreason").value.trim(),sk=[...(skipped("fieldset-retryopt")?["retryopt"]:[]),...(skipped("retryreason")?["retryreason"]:[])];if((!option&&!sk.includes("retryopt"))||(!reason&&!sk.includes("retryreason")))return status("Choose an option, give reasoning, or explicitly Skip unanswered fields.");save(old=>{const receipts=completedTransfer();return old.first&&!old.retry&&receipts?{...old,retry:{option,reason,skipped:sk,at:new Date().toISOString(),transferReceipts:receipts}}:old},"source_retry")};
  }
  $("commit").onclick=()=>{try{const prediction=skipped("prediction")?null:$("prediction").value.trim(),reason=skipped("reason")?null:$("reason").value.trim(),option=opts?selected("opt"):null,sk=[...(skipped("prediction")?["prediction"]:[]),...(skipped("reason")?["reason"]:[]),...(opts&&skipped("fieldset-opt")?["opt"]:[])];if((!prediction&&!sk.includes("prediction"))||(!reason&&!sk.includes("reason"))||(opts&&!option&&!sk.includes("opt")))throw Error("Prediction, reasoning and required selection are necessary unless explicitly skipped.");const values=readFields(fields,"first-");sk.push(...skippedFields(fields,"first-"));const firstSave=()=>save(old=>old.first?old:{...old,first:{prediction,reason,option,fields:values,skipped:sk,hints:old.hints,at:new Date().toISOString(),exposure:source?exposure():null}},"first");if(source)navigator.locks.request(exposureKey,firstSave).catch(fail);else firstSave()}catch(err){status(err.message)}};
  window.addEventListener("storage",evt=>{if(evt.key===ref.key||evt.key===exposureKey||transferRefs.some(r=>r.key===evt.key)||evt.key===null){try{const next=readRecord(ref);if(!next.first&&!rec.first&&evt.key!==ref.key&&evt.key!==null){status("Learning exposure or transfer status changed; first response remains editable.");return}rec=next;render()}catch(err){fail(err)}}});render();
 }catch(err){status("HOLD: "+err.message+"; no further disclosure.");$("commit").disabled=true}
}else failPage(Error("Unknown stage"));
