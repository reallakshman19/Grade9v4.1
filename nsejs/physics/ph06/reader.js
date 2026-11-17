const root=document.getElementById("root");
const base=new URL("./",import.meta.url);
const $=id=>document.getElementById(id);
const e=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const para=s=>"<p>"+e(s)+"</p>";
const fetchText=async path=>{const r=await fetch(new URL(path,base),{cache:"no-store"});if(!r.ok)throw Error("Missing "+path);return r.text()};
const link=(path,label)=>'<a class="action" href="'+e(new URL(path,base).href)+'">'+e(label)+'</a>';
const digest=async text=>Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(text))),b=>b.toString(16).padStart(2,"0")).join("");
const timestamp=()=>new Date().toISOString();
const nativeSkipButton=id=>'<button type="button" class="native-skip" data-native-skip="'+e(id)+'" aria-pressed="false" aria-label="Skip '+e(id)+' (no credit)">Skip</button>';
root.addEventListener("click",event=>{const button=event.target.closest("button[data-native-skip]");if(!button||!root.contains(button))return;
 const field=$(button.dataset.nativeSkip);if(!field||button.disabled)return;
 const next=field.dataset.skipped!=="true";field.dataset.skipped=String(next);field.disabled=next;
 button.textContent=next?"Undo skip":"Skip";button.setAttribute("aria-pressed",String(next));
 const status=$("status");if(status)status.textContent=next?"Explicitly skipped: unanswered; no mastery credit. Undo to answer.":"Skip undone; enter a response or skip.";
});
const sha1Blob=async text=>{const bytes=new TextEncoder().encode(text),head=new TextEncoder().encode("blob "+bytes.length+"\0");const merged=new Uint8Array(head.length+bytes.length);merged.set(head);merged.set(bytes,head.length);return Array.from(new Uint8Array(await crypto.subtle.digest("SHA-1",merged)),b=>b.toString(16).padStart(2,"0")).join("")};
const exposureKey="G9V41:PH06:EXPOSURE:R2";
const exposures=()=>{try{const x=JSON.parse(localStorage.getItem(exposureKey)||"[]");return Array.isArray(x)?x:null}catch{return null}};
const recordExposure=(kind)=>{try{const old=exposures();if(!old)return;localStorage.setItem(exposureKey,JSON.stringify([...old,{kind,at:Date.now()}].slice(-100)))}catch{}};
async function protectedStore(key,hash,render){
 if(!globalThis.crypto?.subtle||!navigator.locks)throw Error("SHA-256 or cross-tab locking unavailable");
 const read=()=>{const raw=localStorage.getItem(key);if(!raw)return null;const r=JSON.parse(raw);if(r.hash!==hash||!Array.isArray(r.events)||(!r.first&&!Object.prototype.hasOwnProperty.call(r,"prediction"))|| (r.first&&(!Object.prototype.hasOwnProperty.call(r.first,"reasoning")||!Object.prototype.hasOwnProperty.call(r.first,"prediction")) ))throw Error("Invalid stored attempt");return r};
 const probe=key+":probe";localStorage.setItem(probe,"1");if(localStorage.getItem(probe)!=="1")throw Error("Storage readback failed");localStorage.removeItem(probe);
 const save=async fn=>{try{await navigator.locks.request(key,async()=>{const old=read(),next=fn(old);if(!next)throw Error("No attempt");const raw=JSON.stringify(next);localStorage.setItem(key,raw);if(localStorage.getItem(key)!==raw)throw Error("Write/readback mismatch");await render(next)})}catch(err){fail(err)}};
 window.addEventListener("storage",ev=>{if(ev.key===key){try{const r=read();if(!r)throw Error("Saved first attempt removed");Promise.resolve(render(r)).catch(fail)}catch(err){fail(err)}}});
 return {read,save};
}
function fail(err){if($("stage")){$("stage").replaceChildren();$("stage").textContent="HOLD: "+err.message;return}if($("post"))$("post").replaceChildren();if($("commit"))$("commit").disabled=true;if($("status"))$("status").textContent="HOLD: "+err.message;else root.textContent="HOLD: "+err.message}
const first=(hash,prediction,reasoning,option)=>({hash,first:{prediction,reasoning,option,at:timestamp(),time:Date.now(),exposure:exposures()?.length?"LOCAL_PRIOR_EXPOSURE_RECORDED":"UNKNOWN_NO_LOCAL_EXPOSURE_RECORDED"},events:[],hints:0,revealed:false});
try{
 const sourceRaw=await fetchText("source.v1.json"),source=JSON.parse(sourceRaw);
 if(source.status!=="LOCATOR_ONLY_HOLD")throw Error("Unexpected source state");
 const srcQuery=new URLSearchParams(location.search).get("source");
 if(srcQuery&&srcQuery!==source.locator)throw Error("Incorrect source identity");
 if(root.dataset.role==="source"){
  const hash=await digest(sourceRaw),key="G9V41:PH06:SOURCE:"+source.uid+":"+hash;
  root.innerHTML='<p class="notice">Read the publisher paper at printed question 38, page 7. No original stem, key or answer is reproduced. Source byte custody and rights are unresolved.</p><a class="action" href="'+e(source.paper+'#page='+source.page)+'" target="_blank" rel="noopener">Open publisher paper</a><fieldset><legend>First option (single correct)</legend>'+["A","B","C","D"].map(x=>'<label><input type="radio" name="option" value="'+x+'"> '+x+'</label>').join("")+'</fieldset><label for="prediction">Prediction</label><textarea id="prediction"></textarea><label for="attempt">First reasoning</label><textarea id="attempt"></textarea><button id="commit" disabled>Save first source attempt</button><p id="status" role="status">Checking storage…</p><div id="post"></div>';
  let store;
  function draw(r){if(!r){$("commit").disabled=false;$("status").textContent="Ready";return}
   $("prediction").value=r.first.prediction;$("attempt").value=r.first.reasoning;document.querySelectorAll('input[name="option"]').forEach(n=>{n.checked=n.value===r.first.option;n.disabled=true});$("prediction").disabled=$("attempt").disabled=$("commit").disabled=true;
   $("status").textContent="First source attempt saved. No source key unlocked. Prior exposure: "+(r.first.exposure||"UNKNOWN")+". Browser history is not independent evidence."; $("post").innerHTML=link("../textbook/PH06/U06/index.html?source="+source.locator,"Learn Archimedes") +link("../textbook/PH06/U08/index.html?source="+source.locator,"Learn multilayer construction");
   if(r.transferComplete&&r.transferComplete.sourceFirstAt===r.first.at){$("post").insertAdjacentHTML("beforeend",'<label for="retry">Reconstruct source reasoning after the transfer</label><textarea id="retry"></textarea><button id="retrySave">Save separate reattempt</button>');if(r.retry){$("retry").value=r.retry;$("retry").disabled=$("retrySave").disabled=true}$("retrySave").onclick=()=>{const v=$("retry").value.trim();if(v)store.save(old=>old.retry?old:{...old,retry:v,events:[...old.events,{kind:"source_reattempt",at:timestamp()}]})}}
  }
  store=await protectedStore(key,hash,draw);
  $("commit").onclick=()=>{const prediction=$("prediction").value.trim(),reasoning=$("attempt").value.trim(),option=document.querySelector('input[name="option"]:checked')?.value;if(!prediction||!reasoning||!option){$("status").textContent="Select an option and record both responses.";return}store.save(old=>old||first(hash,prediction,reasoning,option))};
  draw(store.read());
 }else{
  const raw=await fetchText("task.v1.json"),task=JSON.parse(raw),manifestRaw=await fetchText("protected-assets.r3.json"),manifest=JSON.parse(manifestRaw);
  if(task.uid!==manifest.task_uid||task.revision!==manifest.task_revision||task.academic!=="HOLD"||task.source_locator!==source.locator||manifest.schema!=="g9v41-ph06-protected-assets/v1"||manifest.status!=="AUTHOR_CANDIDATE_ACADEMIC_HOLD")throw Error("Task/asset manifest/source revision mismatch");
  const figure=await fetchText(task.figure);const doc=new DOMParser().parseFromString(figure,"image/svg+xml");if(doc.querySelector("parsererror,script,foreignObject")||doc.documentElement.localName!=="svg")throw Error("Invalid required SVG");
  let model=null,bf=null,solutionURL=null,boundaryURL=null,postLoading=null;
  const hash=await digest(JSON.stringify([raw,sourceRaw,figure,manifestRaw])),key="G9V41:PH06:R3:"+task.uid+":"+hash;
  // Use the exact verified figure bytes, not a second independent fetch.
  const imageURL=URL.createObjectURL(new Blob([figure],{type:"image/svg+xml"}));
  const sh=await digest(sourceRaw),sk="G9V41:PH06:SOURCE:"+source.uid+":"+sh;
  function sourceFirst(){try{const old=JSON.parse(localStorage.getItem(sk)||"null");return old?.hash===sh&&old.first?.reasoning?old.first:null}catch{return null}}
  const sourceAtStart=sourceFirst();
  const fields=task.fields;
  const trail=["Predict","Attempt","Reconstruct","Diagnose","Repair","Boundary test"];
  const fieldHTML=(x,prefix)=>'<div class="field"><label for="'+prefix+x.id+'">'+e(x.label)+'</label>'+(x.type==="select"?'<select id="'+prefix+x.id+'"><option value="">Choose your model</option>'+x.options.map(o=>'<option value="'+e(o)+'">'+e(o)+'</option>').join("")+'</select>':'<input id="'+prefix+x.id+'" type="'+(x.type==="number"?"number":"text")+'" '+(x.type==="number"?'step="any"':'')+'>')+nativeSkipButton(prefix+x.id)+'</div>';
  const collect=(xs,prefix)=>Object.fromEntries(xs.map(x=>{const field=$(prefix+x.id);if(field.dataset.skipped==="true")return[x.id,null];const value=field.value.trim();if(!value)throw Error("Answer "+x.label+" or select Skip (no credit)");if(x.type==="number"&&!Number.isFinite(Number(value)))throw Error("Nonfinite "+x.label);return[x.id,value]}));
  const checks=(rules,values)=>rules.map(x=>{const v=values?.[x.id];const skipped=v===null;const match=!skipped&&v!==""&&v!==undefined&&(typeof x.expected==="number"?Number.isFinite(Number(v))&&Math.abs(Number(v)-x.expected)<=x.tol:v===x.expected);return{id:x.id,match,skipped,repair:skipped?"Explicitly unanswered; no credit and no misconception inferred.":x.repair}});
  const firstIssue=r=>r.first.skipped?.length?null:checks(model.rubric,r.first.fields).find(x=>!x.match);
  const feedback=(rules,values,xs)=>'<div class="review-fields">'+checks(rules,values).map(x=>'<p class="'+(x.match?"match":"mismatch")+'"><strong>'+e(xs.find(y=>y.id===x.id).label)+': </strong>'+e(x.match?"Matches authored reference; justify it in your explanation.":x.repair)+'</p>').join("")+'</div>';
  const snapshot=r=>'<details class="snapshot"><summary>Your preserved first attempt</summary><dl><dt>Prediction</dt><dd>'+e(r.first.prediction??"Explicitly skipped (no credit)")+'</dd>'+fields.map(x=>'<dt>'+e(x.label)+'</dt><dd>'+e(r.first.fields[x.id]??"Unanswered (no credit)")+'</dd>').join("")+'<dt>Reasoning</dt><dd>'+e(r.first.reasoning??"Explicitly skipped (no credit)")+'</dd></dl></details>';
  async function ensurePost(){
    if(model)return;
    if(!postLoading)postLoading=(async()=>{
      const [modelRaw,solutionFigure,boundaryFigure]=await Promise.all([fetchText("model.v1.json"),fetchText("figures/u08-reconstruct.svg"),fetchText("figures/u08-boundary.svg")]);
      if(await sha1Blob(modelRaw)!==manifest.model_blob_sha1||await sha1Blob(solutionFigure)!==manifest.solution_blob_sha1||await sha1Blob(boundaryFigure)!==manifest.boundary_blob_sha1)throw Error("Postattempt asset byte pin mismatch");
      const parsed=JSON.parse(modelRaw);if(parsed.uid!==task.uid||parsed.revision!==task.revision||!Array.isArray(parsed.boundaryFields)||!Array.isArray(parsed.hints))throw Error("Postattempt model identity mismatch");
      for(const svg of [solutionFigure,boundaryFigure]){const doc=new DOMParser().parseFromString(svg,"image/svg+xml");if(doc.querySelector("parsererror,script,foreignObject")||doc.documentElement.localName!=="svg")throw Error("Invalid postattempt SVG")}
      model=parsed;bf=model.boundaryFields;
      solutionURL=URL.createObjectURL(new Blob([solutionFigure],{type:"image/svg+xml"}));
      boundaryURL=URL.createObjectURL(new Blob([boundaryFigure],{type:"image/svg+xml"}));
    })();
    await postLoading;
  }
  const stageFig=(url,alt)=>'<figure><img src="'+e(url)+'" alt="'+e(alt)+'"><figcaption>'+e(alt)+'</figcaption></figure>';
  root.innerHTML='<p class="notice">Authored transfer · not an original examination question. '+e(task.uid)+' · '+e(task.revision)+'. Local practice, not secure exam evidence.</p><ol class="stage-trail" id="trail"></ol><section class="stage-card" id="stage"><p id="status" role="status">Checking figure and storage…</p></section>';
  // Decode exact required prompt bytes before enabling prediction or attempt.
  const verified=new Image();verified.src=imageURL;await verified.decode();if(!verified.naturalWidth)throw Error("Required figure not rendered");
  let store;
  const advance=(fn)=>store.save(old=>fn(old));
  async function render(r){
    const stage=r?.stage??0;
    if(stage>=2){if(!r?.first)throw Error("Postattempt access without durable first response");await ensurePost();}
    if(!Number.isInteger(stage)||stage<0||stage>5||stage>1&&(!r.first?.fields||!r.first?.reasoning))throw Error("Invalid saved stage");
    $("trail").innerHTML=trail.map((label,i)=>'<li '+(i===stage?'aria-current="step"':i<stage?'class="done"':'')+'>'+(i+1)+'. '+e(label)+'</li>').join("");
    let h='<h2 id="stageTitle" tabindex="-1">'+(stage+1)+' · '+trail[stage]+'</h2><p id="status" role="status">Ready · '+(r?.first?"first attempt preserved":"no first attempt committed")+'</p>';
    if(stage<2){
      h+=para(task.prompt)+stageFig(imageURL,"Initial configuration only; unknown interface, not to scale.");
      if(stage===0)h+='<label for="prediction">'+e(task.prediction)+'</label><textarea id="prediction"></textarea>'+nativeSkipButton("prediction")+'<button id="predictSave">Save prediction → Attempt</button>';
      else h+='<p class="thinking"><strong>Your prediction:</strong> '+e(r.prediction??"Explicitly skipped (no credit)")+'</p><p>Decide the model and show your own calculation. Leave a numerical field blank if unsure; explain why.</p>'+fields.map(x=>fieldHTML(x,"a-")).join("")+'<label for="attempt">Your independent reasoning and units</label><textarea id="attempt"></textarea>'+nativeSkipButton("attempt")+'<button id="commit">Commit first attempt</button><div id="post"></div>';
    }else if(stage===2){
      h+=snapshot(r)+'<p>Compare your own model with the authored reference. Numeric/model checks are not a grade of your explanation.</p><div id="post">'+model.hints.slice(0,r.hints).map(para).join("");
      if(!r.revealed){if(r.hints<3)h+='<button id="hint">Next hint</button>';h+='<button id="reveal">Compare reconstruction</button>'}
      else{h+=feedback(model.rubric,r.first.fields,fields)+'<h3>Worked reconstruction</h3><ol>'+model.reconstructionSteps.map(x=>'<li><strong>'+e(x[0])+'.</strong> '+e(x[1])+'</li>').join("")+'</ol>'+stageFig(solutionURL,"Reconstructed initial and loaded geometry, with actual immersed lengths.")+'<h3>Pressure-walk check</h3>'+para(model.alternative)+'<h3>Reasoning rubric</h3><ul>'+model.reasoningRubric.map(x=>'<li>'+e(x)+'</li>').join("")+'</ul><button id="compare">Compare → Diagnose</button>'}h+='</div>';
    }else if(stage===3){
      const issue=firstIssue(r);
      h+=snapshot(r)+feedback(model.rubric,r.first.fields,fields)+'<p class="thinking" id="firstIssue">'+e(r.first.skipped?.length?"Insufficient evidence: one or more first-response fields were explicitly skipped; no misconception or credit inferred.":issue?"Possible first divergence: "+fields.find(x=>x.id===issue.id).label+". "+issue.repair:"All checked values/models match; examine your explanation and assumptions. This does not establish correct reasoning.")+'</p><label for="diagnosisField">Which step will you examine?</label><select id="diagnosisField"><option value="">Choose a step</option>'+fields.map(x=>'<option value="'+e(x.id)+'">'+e(x.label)+'</option>').join("")+'<option value="reason">My explanation or assumptions</option></select><label for="diagnosis">What caused the divergence, or what justifies your correct model?</label><textarea id="diagnosis"></textarea>'+nativeSkipButton("diagnosis")+'<button id="diagnose">Save diagnosis → Repair</button>';
    }else if(stage===4){
      h+=snapshot(r)+para("Your diagnosis: "+r.diagnosis.why)+para(model.rubric.find(x=>x.id===r.diagnosis.field)?.repair||"Check your force balance, geometry and conditions.")+'<label for="repair">Reconstruct the corrected reasoning and explain what changed</label><textarea id="repair"></textarea>'+nativeSkipButton("repair")+'<button id="repairSave">Save repair → Boundary test</button>';
    }else{
      h+=snapshot(r)+para("Your repair: "+r.repair)+para(model.boundaryPrompt);
      if(!r.boundary)h+=bf.map(x=>fieldHTML(x,"b-")).join("")+'<label for="boundary">Explain the model choice and calculation</label><textarea id="boundary"></textarea>'+nativeSkipButton("boundary")+'<button id="boundarySave">Commit boundary reasoning</button>';
      else {h+=para("Your changed-condition reasoning: "+r.boundary.why);if(!r.boundaryRevealed)h+='<button id="boundaryReveal">Compare boundary</button>';else h+=feedback(bf,r.boundary.fields,bf)+para(model.boundaryModel)+stageFig(boundaryURL,"Changed-condition upper-only equilibrium.")+'<p>Completion records a practice journey, not mastery. Skipped responses earn no credit and cannot unlock an independent source-reattempt claim.</p><button id="sourceReturn">Return to exact source checkpoint</button>'}
    }
    $("stage").innerHTML=h;
    const btn=(id,fn)=>{if($(id))$(id).onclick=fn};
    const required=(id)=>{const field=$(id);if(field?.dataset.skipped==="true")return null;const v=field?.value.trim();if(!v){$("status").textContent="Write your answer or choose Skip (no credit).";return undefined}return v};
    btn("predictSave",()=>{const v=required("prediction");if(v!==undefined)advance(old=>old||{hash,stage:1,prediction:v,predictionSkipped:v===null,predictionAt:Date.now(),events:[{kind:"prediction",at:timestamp(),skipped:v===null}],hints:0,revealed:false,sourceFirstAt:sourceAtStart?.at||null,sourceFirstTime:sourceAtStart?.time||null})});
    btn("commit",()=>{try{const why=required("attempt");if(why===undefined)return;const entries=collect(fields,"a-");const skips=fields.filter(x=>entries[x.id]===null).map(x=>"a-"+x.id).concat(why===null?["attempt"]:[]);advance(old=>old.stage!==1?old:{...old,stage:2,first:{prediction:old.prediction,reasoning:why,fields:entries,skipped:skips,at:timestamp(),time:Date.now(),sourceFirstAt:old.sourceFirstAt,exposure:exposures()||null},events:[...old.events,{kind:"first_attempt",at:timestamp(),skipped:skips.length>0}]})}catch(err){$("status").textContent=err.message}});
    const change=(expected,fn)=>advance(old=>old.stage===expected?fn(old):old);
    btn("hint",()=>change(2,old=>!old.revealed&&old.hints<3?{...old,hints:old.hints+1,events:[...old.events,{kind:"hint",at:timestamp()}]}:old));
    btn("reveal",()=>change(2,old=>old.revealed?old:{...old,revealed:true,events:[...old.events,{kind:"reveal",at:timestamp()}]}));
    if(r?.revealed)recordExposure("challenge_reconstruction");
    btn("compare",()=>change(2,old=>old.revealed?{...old,stage:3}:old));
    btn("diagnose",()=>{const why=required("diagnosis"),field=$("diagnosisField").value;if(why===undefined)return;if(!field&&why!==null){$("status").textContent="Choose a reasoning step or Skip.";return}change(3,old=>({...old,stage:4,diagnosis:{field:why===null?"skipped":field,why,skipped:why===null},events:[...old.events,{kind:"diagnosis",at:timestamp(),skipped:why===null}]}))});
    btn("repairSave",()=>{const why=required("repair");if(why!==undefined)change(4,old=>({...old,stage:5,repair:why,repairSkipped:why===null,events:[...old.events,{kind:"repair",at:timestamp(),skipped:why===null}]}))});
    btn("boundarySave",()=>{try{const why=required("boundary");if(why===undefined)return;const vals=collect(bf,"b-");const skipped=bf.filter(x=>vals[x.id]===null).map(x=>"b-"+x.id).concat(why===null?["boundary"]:[]);change(5,old=>old.boundary?old:{...old,boundary:{why,fields:vals,skipped,at:timestamp()},events:[...old.events,{kind:"boundary",at:timestamp(),skipped:skipped.length>0}]})}catch(err){$("status").textContent=err.message}});
    btn("boundaryReveal",()=>change(5,old=>old.boundary?{...old,boundaryRevealed:true,events:[...old.events,{kind:"boundary_reveal",at:timestamp()}]}:old));
    btn("sourceReturn",async()=>{try{await navigator.locks.request(sk,async()=>{const old=JSON.parse(localStorage.getItem(sk)||"null");if(!old)return;if(old.hash!==sh||!old.first?.reasoning)throw Error("Invalid source first response");if(r.predictionSkipped||r.first.skipped?.length||r.diagnosis?.skipped||r.repairSkipped||r.boundary?.skipped?.length)return;if(!r.sourceFirstAt||old.first.at!==r.sourceFirstAt||!old.first.time||old.first.time>r.predictionAt||r.first.time<r.predictionAt){return}const updated=JSON.stringify({...old,transferComplete:{task:task.uid,hash,sourceFirstAt:old.first.at,at:timestamp()}});localStorage.setItem(sk,updated);if(localStorage.getItem(sk)!==updated)throw Error("Source return save failed")});location.href=new URL("source-checkpoint.html",base).href}catch(err){fail(err)}});
    $("stageTitle").focus({preventScroll:true});
  }
  store=await protectedStore(key,hash,render);
  await render(store.read());
 }
}catch(err){fail(err)}
