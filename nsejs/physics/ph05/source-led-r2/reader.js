const root=document.getElementById("root");
const e=(s)=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const para=s=>"<p>"+e(s)+"</p>";
const figure=(src,caption)=>'<figure><img src="'+e(src)+'" alt="'+e(caption)+'"><figcaption>'+e(caption)+'</figcaption></figure>';
const get=async path=>{const r=await fetch(path,{cache:"no-store"});if(!r.ok)throw Error("Missing "+path);return r.json()};
const data=await get("packages.v1.json");if(data.release!=="HOLD")throw Error("Unexpected release");
const params=new URL(location.href).searchParams;
const pack=data.packages.find(p=>p.id===params.get("package"));
const task=pack?.tasks.find(t=>t.uid===params.get("task"));
const source=params.get("source");
const sourceRecord=pack&&data.census.source_records.find(x=>x.id===source&&pack.source_locators.includes(x.id));
const checkpoint=!!sourceRecord&&!params.has("task")&&params.get("stage")!=="learn";
const href=(p,t)=>"?package="+encodeURIComponent(p.id)+(t?"&task="+encodeURIComponent(t.uid):"&stage=learn")+(sourceRecord?"&source="+encodeURIComponent(sourceRecord.id):"");
const checkpointHref=(p,id)=>"?package="+encodeURIComponent(p.id)+"&source="+encodeURIComponent(id);
const sourceLinks=p=>(sourceRecord?[sourceRecord.id]:p.source_locators).map(id=>{const record=data.census.source_records.find(x=>x.id===id);return record?.paper?'<a class="action" href="'+checkpointHref(p,id)+'">Return to source checkpoint: '+e(id)+'</a>':para(id+" · publisher paper custody unresolved")}).join("");
if(!pack){root.innerHTML='<p>Choose a reasoning package. The seven stable syllabus IDs are retained in the register; these are construction packages, not new syllabus identities.</p>'+data.packages.map(p=>'<article><h2>'+e(p.id+" · "+p.title)+'</h2><p class="meta">'+e(p.primary_subtopic+" · "+p.source_locators.join(", "))+'</p><p>'+e(p.lesson)+'</p><div class="actions">'+p.source_locators.map(id=>'<a class="action" href="'+checkpointHref(p,id)+'">Source: '+e(id)+'</a>').join('')+'<a class="action" href="'+href(p)+'">Learn this construction</a></div></article>').join("");}
else if(checkpoint){
 root.innerHTML='<a href="?">All packages</a><article><h2>Original-source checkpoint</h2>'+para(sourceRecord.id+" · "+sourceRecord.prompt_tag)+'<p class="meta">Public locator only. Source authenticity, key and figure custody remain HOLD. Open the unsolved paper, not a solution.</p>'+(sourceRecord.paper?'<a class="action" href="'+e(sourceRecord.paper)+'" target="_blank" rel="noopener">Open publisher paper</a>':para("Publisher paper unavailable; source checkpoint cannot be attempted."))+'<label for="sp">First prediction</label><textarea id="sp"></textarea><label for="sa">First reasoning attempt</label><textarea id="sa"></textarea><button id="sc" disabled>Save source attempt</button><p id="ss" role="status"></p><div id="next"></div></article>';
 const $=id=>document.getElementById(id);
 try{
 if(!sourceRecord.paper||!crypto?.subtle||!navigator.locks)throw Error("Source paper or protected storage unavailable");
 const hash=Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(JSON.stringify(sourceRecord)))),b=>b.toString(16).padStart(2,"0")).join("");
 const key="G9V41:PH05:R2:SOURCE:"+sourceRecord.id+":"+hash;
 const read=()=>{const raw=localStorage.getItem(key);if(!raw)return null;const r=JSON.parse(raw);if(r.hash!==hash||!r.prediction||!r.attempt)throw Error("Invalid source checkpoint");return r};
 const draw=r=>{if(r){$("sp").value=r.prediction;$("sa").value=r.attempt;$("sp").disabled=$("sa").disabled=$("sc").disabled=true;$("ss").textContent="First source reasoning preserved. Return to this checkpoint after learning."; $("next").innerHTML='<a class="action" href="'+href(pack)+'">Open Core1A guide</a><label for="retry">Reattempt after learning (separate from first response)</label><textarea id="retry"></textarea><button id="retrySave">Save reattempt</button>';if(r.retry){$("retry").value=r.retry;$("retry").disabled=$("retrySave").disabled=true} $("retrySave").onclick=()=>{const retry=$("retry").value.trim();if(retry)save(old=>{if(!old)throw Error("Missing first source attempt");return {...old,retry:old.retry||retry}})}}else{$("sc").disabled=false;$("ss").textContent="Save both responses before opening the guide from this route."}};
 const save=async change=>{try{await navigator.locks.request(key,async()=>{const next=change(read());const raw=JSON.stringify(next);localStorage.setItem(key,raw);if(localStorage.getItem(key)!==raw)throw Error("Write/read mismatch");draw(next)})}catch(err){$("next").replaceChildren();$("sc").disabled=true;$("ss").textContent="HOLD: "+err.message}};
 $("sc").onclick=()=>{const prediction=$("sp").value.trim(),attempt=$("sa").value.trim();if(prediction&&attempt)save(old=>old||{hash,prediction,attempt,at:new Date().toISOString()});else $("ss").textContent="Both responses required"};
 draw(read());
 }catch(err){$("ss").textContent="HOLD: "+err.message}
}
else if(!task){root.innerHTML='<a href="?">All packages</a><article><h2>'+e(pack.title)+'</h2><p class="meta">'+e(pack.primary_subtopic+" · "+pack.source_locators.join(", "))+'</p><h3>01 · Learn to reason</h3>'+para(pack.lesson)+figure(pack.guide,"Guided example — authored WPE-style representation")+(pack.id==="P06"?figure("figures/p06-energy-ledger.svg","Guided example: energy allocation, not challenge answer"):"")+'<h3>Worked progression</h3>'+pack.examples.map((x,i)=>'<div class="example"><strong>'+e(["Foundation","Connected","Advanced"][i])+'</strong>'+para(x.prompt)+para(x.solution)+'</div>').join("")+'<h3>Conditions and wrong route</h3>'+para(pack.condition)+para(pack.misconception)+'<h3>02 · Fresh challenge</h3><div class="actions">'+pack.tasks.map(t=>'<a class="action" href="'+href(pack,t)+'">'+e(t.cell+" · candidate "+t.uid.split("-").at(-1))+'</a>').join("")+'</div></article>';}
else{
 const status=msg=>{const n=document.getElementById("status");if(n)n.textContent=msg};
 root.innerHTML='<a href="'+href(pack)+'">Return to guide</a><section class="panel"><h2>'+e(pack.title+" · "+task.cell+" candidate")+'</h2><p class="meta">'+e(task.uid+" · "+task.revision)+'</p>'+para(task.prompt)+figure(task.figure,"Question-facing schematic — stated conditions only")+'<label for="prediction">Prediction: '+e(task.prediction)+'</label><textarea id="prediction"></textarea><label for="attempt">First reasoning attempt</label><textarea id="attempt"></textarea><button id="commit" disabled>Save first attempt</button><p id="status" role="status">Checking revision and storage…</p><div id="post"></div></section>';
 const $=id=>document.getElementById(id);
 try{
 if(!crypto?.subtle||!navigator.locks)throw Error("SHA-256 or cross-tab locking unavailable; protected practice blocked");
 const modelData=await get("models.v1.json");
 const model=modelData.models.find(m=>m.uid===task.uid&&m.revision===task.revision);
 if(!model||modelData.status!=="AUTHOR_ONLY_HOLD")throw Error("Missing exact model");
 const figResp=await fetch(task.figure,{cache:"no-store"});if(!figResp.ok)throw Error("Missing exact prompt figure");
 const fig=await figResp.text();
 const digest=async text=>Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(text))),b=>b.toString(16).padStart(2,"0")).join("");
 const hash=await digest(JSON.stringify([task,model,fig]));
 const key="G9V41:PH05:R2:"+task.uid+":"+task.revision+":"+hash;
 const read=()=>{let s=localStorage.getItem(key);if(!s)return null;const r=JSON.parse(s);if(r.hash!==hash||!r.prediction||!r.attempt||!Array.isArray(r.events))throw Error("Invalid saved state");return r};
 let rec=read();
 const probe=key+":probe";localStorage.setItem(probe,"1");if(localStorage.getItem(probe)!=="1")throw Error("Storage readback failed");localStorage.removeItem(probe);
 const save=async(fn)=>{try{await navigator.locks.request(key,async()=>{const old=read();const next=fn(old);if(!next)return;const raw=JSON.stringify(next);localStorage.setItem(key,raw);if(localStorage.getItem(key)!==raw)throw Error("Write/read mismatch");rec=next});render()}catch(err){$("post").replaceChildren();$("commit").disabled=true;status("HOLD: "+err.message+"; no assistance unlocked")}};
 const step=(kind,change)=>save(old=>{if(!old)throw Error("No saved first attempt");if(kind==="hint")change={hints:Math.min(3,(old.hints||0)+1)};if(kind==="diagnosis"&&(!old.revealed||old.diagnosis))return old;if(kind==="repair"&&(!old.diagnosis||old.repair))return old;if(kind==="boundary"&&(!old.repair||old.boundary))return old;if(kind==="boundary_model"&&!old.boundary)return old;return {...old,...change,events:[...old.events,{kind,at:new Date().toISOString()}]}});
 function render(){if(!rec){$("commit").disabled=false;status("Ready. Save a prediction and reasoning before assistance.");return}
 $("prediction").value=rec.prediction;$("attempt").value=rec.attempt;$("prediction").disabled=$("attempt").disabled=$("commit").disabled=true;
 status("First attempt saved for exact revision. Local self-study protection, not exam security.");
 let h='<h3>03 · Ordered assistance</h3>'+model.hints.slice(0,rec.hints||0).map((x,i)=>para("H"+(i+1)+": "+x)).join("");
 if((rec.hints||0)<3&&!rec.revealed)h+='<button id="hint">Next hint</button> ';
 if(!rec.revealed)h+='<button id="reveal">Compare reconstruction</button>';
 if(rec.revealed){h+='<h3>04 · Reconstruction</h3>'+para(model.reconstruction)+'<h4>Independent check</h4>'+para(model.alternative)+'<h3>05 · Diagnose</h3>'+para(model.diagnosis);
 h+=rec.diagnosis?para(rec.diagnosis):'<label for="diagnosis">Record first divergence</label><textarea id="diagnosis"></textarea><button id="diagnose">Save diagnosis</button>';
 if(rec.diagnosis){h+='<h3>06 · Repair</h3>'+para(model.repair)+(rec.repair?para(rec.repair):'<textarea aria-label="Repaired reasoning" id="repair"></textarea><button id="repairSave">Save repair</button>')}
 if(rec.repair){h+='<h3>07 · Boundary transfer</h3>'+para(model.boundaryPrompt)+(rec.boundary?para(rec.boundary):'<textarea aria-label="Boundary reasoning" id="boundary"></textarea><button id="boundarySave">Save boundary attempt</button>')}
 if(rec.boundary&&!rec.boundaryReveal)h+='<button id="boundaryReveal">Compare boundary</button>';
 if(rec.boundaryReveal)h+=para(model.boundaryModel)+'<h3>08 · Return to original source</h3><p class="meta">Source paper only; independent custody and academic review HOLD.</p><div class="actions">'+sourceLinks(pack)+'</div>';
 }
 $("post").innerHTML=h;
 if($("hint"))$("hint").onclick=()=>step("hint",{hints:Math.min(3,(rec.hints||0)+1)});
 if($("reveal"))$("reveal").onclick=()=>step("reconstruction",{revealed:true});
 for(const [button,input,field] of [["diagnose","diagnosis","diagnosis"],["repairSave","repair","repair"],["boundarySave","boundary","boundary"]])if($(button))$(button).onclick=()=>{let value=$(input).value.trim();if(!value)return status("Reasoning required");step(field,{[field]:value})};
 if($("boundaryReveal"))$("boundaryReveal").onclick=()=>step("boundary_model",{boundaryReveal:true});
 }
 $("commit").onclick=()=>{const prediction=$("prediction").value.trim(),attempt=$("attempt").value.trim();if(!prediction||!attempt)return status("Both prediction and reasoning are required");save(old=>old||{hash,prediction,attempt,events:[],hints:0,at:new Date().toISOString()})};
 window.addEventListener("storage",event=>{if(event.key===key){try{rec=read();render()}catch(err){$("post").replaceChildren();$("commit").disabled=true;status("HOLD: "+err.message)}}});
 render();
 }catch(err){status("HOLD: "+err.message+"; no assistance unlocked")}
}
