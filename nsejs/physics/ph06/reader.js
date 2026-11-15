const root=document.getElementById("root");
const base=new URL("./",import.meta.url);
const $=id=>document.getElementById(id);
const e=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const para=s=>"<p>"+e(s)+"</p>";
const fetchText=async path=>{const r=await fetch(new URL(path,base),{cache:"no-store"});if(!r.ok)throw Error("Missing "+path);return r.text()};
const link=(path,label)=>'<a class="action" href="'+e(new URL(path,base).href)+'">'+e(label)+'</a>';
const digest=async text=>Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(text))),b=>b.toString(16).padStart(2,"0")).join("");
const timestamp=()=>new Date().toISOString();
async function protectedStore(key,hash,render){
 if(!globalThis.crypto?.subtle||!navigator.locks)throw Error("SHA-256 or cross-tab locking unavailable");
 const read=()=>{const raw=localStorage.getItem(key);if(!raw)return null;const r=JSON.parse(raw);if(r.hash!==hash||!r.first?.reasoning||!r.first?.prediction||!Array.isArray(r.events))throw Error("Invalid stored attempt");return r};
 const probe=key+":probe";localStorage.setItem(probe,"1");if(localStorage.getItem(probe)!=="1")throw Error("Storage readback failed");localStorage.removeItem(probe);
 const save=async fn=>{try{await navigator.locks.request(key,async()=>{const old=read(),next=fn(old);if(!next)throw Error("No attempt");const raw=JSON.stringify(next);localStorage.setItem(key,raw);if(localStorage.getItem(key)!==raw)throw Error("Write/readback mismatch");render(next)})}catch(err){fail(err)}};
 window.addEventListener("storage",ev=>{if(ev.key===key){try{const r=read();if(!r)throw Error("Saved first attempt removed");render(r)}catch(err){fail(err)}}});
 return {read,save};
}
function fail(err){if($("post"))$("post").replaceChildren();if($("commit"))$("commit").disabled=true;if($("status"))$("status").textContent="HOLD: "+err.message;else root.textContent="HOLD: "+err.message}
const first=(hash,prediction,reasoning,option)=>({hash,first:{prediction,reasoning,option,at:timestamp()},events:[],hints:0,revealed:false});
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
   $("status").textContent="First source attempt saved. No source key unlocked."; $("post").innerHTML=link("../textbook/PH06/U06/index.html","Learn Archimedes") +link("../textbook/PH06/U08/index.html?source="+source.locator,"Learn multilayer construction");
   if(r.transferComplete){$("post").insertAdjacentHTML("beforeend",'<label for="retry">Reconstruct source reasoning after the transfer</label><textarea id="retry"></textarea><button id="retrySave">Save separate reattempt</button>');if(r.retry){$("retry").value=r.retry;$("retry").disabled=$("retrySave").disabled=true}$("retrySave").onclick=()=>{const v=$("retry").value.trim();if(v)store.save(old=>old.retry?old:{...old,retry:v,events:[...old.events,{kind:"source_reattempt",at:timestamp()}]})}}
  }
  store=await protectedStore(key,hash,draw);
  $("commit").onclick=()=>{const prediction=$("prediction").value.trim(),reasoning=$("attempt").value.trim(),option=document.querySelector('input[name="option"]:checked')?.value;if(!prediction||!reasoning||!option){$("status").textContent="Select an option and record both responses.";return}store.save(old=>old||first(hash,prediction,reasoning,option))};
  draw(store.read());
 }else{
  const raw=await fetchText("task.v1.json"),modelRaw=await fetchText("model.v1.json"),task=JSON.parse(raw),model=JSON.parse(modelRaw);
  if(task.uid!==model.uid||task.revision!==model.revision||task.academic!=="HOLD"||task.source_locator!==source.locator)throw Error("Task/model/source revision mismatch");
  const figure=await fetchText(task.figure);const doc=new DOMParser().parseFromString(figure,"image/svg+xml");if(doc.querySelector("parsererror,script,foreignObject")||doc.documentElement.localName!=="svg")throw Error("Invalid required SVG");
  const hash=await digest(JSON.stringify([raw,modelRaw,sourceRaw,figure])),key="G9V41:PH06:"+task.uid+":"+hash;
  // Use the exact verified figure bytes, not a second independent fetch.
  const imageURL=URL.createObjectURL(new Blob([figure],{type:"image/svg+xml"}));
  root.innerHTML='<p class="notice">Authored transfer · not an original examination question. '+e(task.uid)+'</p>'+para(task.prompt)+'<figure><img id="promptFigure" alt="Initial float geometry, unknown interface, not to scale"><figcaption>Initial configuration only. Use given measurements; no solved final position.</figcaption></figure><label for="prediction">'+e(task.prediction)+'</label><textarea id="prediction"></textarea><label for="attempt">First independent reasoning</label><textarea id="attempt"></textarea><button id="commit" disabled>Commit first attempt</button><p id="status" role="status">Checking figure and storage…</p><div id="post"></div>';
  $("promptFigure").src=imageURL;await $("promptFigure").decode();if(!$("promptFigure").naturalWidth)throw Error("Required figure not rendered");
  let store;
  const step=(kind,value)=>store.save(old=>{if(!old)throw Error("No first attempt");const events=[...old.events,{kind,at:timestamp()}];if(kind==="hint"&&!old.revealed&&old.hints<3)return {...old,hints:old.hints+1,events};if(kind==="reveal"&&!old.revealed)return {...old,revealed:true,events};if(kind==="diagnosis"&&old.revealed&&!old.diagnosis)return {...old,diagnosis:value,events};if(kind==="repair"&&old.diagnosis&&!old.repair)return {...old,repair:value,events};if(kind==="boundary"&&old.repair&&!old.boundary)return {...old,boundary:value,events};if(kind==="boundary_reveal"&&old.boundary&&!old.boundaryRevealed)return {...old,boundaryRevealed:true,events};return old});
  function render(r){if(!r){$("commit").disabled=false;$("status").textContent="Ready. First reasoning is required before help.";return}
   $("prediction").value=r.first.prediction;$("attempt").value=r.first.reasoning;$("prediction").disabled=$("attempt").disabled=$("commit").disabled=true;
   $("status").textContent="First attempt saved · "+(r.hints?"assisted after commitment":"no hint exposure recorded");
   let h='<h2>3 · Ordered help / reconstruct</h2>'+model.hints.slice(0,r.hints).map(para).join("");
   if(!r.revealed){if(r.hints<3)h+='<button id="hint">Next hint</button>';h+='<button id="reveal">Compare reconstruction</button>'}
   if(r.revealed){h+=para(model.reconstruction)+'<h3>Pressure-walk check</h3>'+para(model.alternative)+'<h2>4 · Diagnose first divergence</h2>'+para(model.diagnosis)+(r.diagnosis?para(r.diagnosis):'<label for="diagnosis">Your diagnosis</label><textarea id="diagnosis"></textarea><button id="diagnose">Save diagnosis</button>')}
   if(r.diagnosis)h+='<h2>5 · Repair</h2>'+para(model.repair)+(r.repair?para(r.repair):'<label for="repair">Repaired model</label><textarea id="repair"></textarea><button id="repairSave">Save repair</button>');
   if(r.repair)h+='<h2>6 · Boundary transfer</h2>'+para(model.boundaryPrompt)+(r.boundary?para(r.boundary):'<label for="boundary">Boundary reasoning</label><textarea id="boundary"></textarea><button id="boundarySave">Commit boundary</button>');
   if(r.boundary&&!r.boundaryRevealed)h+='<button id="boundaryReveal">Compare boundary</button>';
   if(r.boundaryRevealed)h+=para(model.boundaryModel)+'<h2>Return to historical source</h2><button id="sourceReturn">Return to exact source checkpoint</button>';
   $("post").innerHTML=h;
   if($("hint"))$("hint").onclick=()=>step("hint");if($("reveal"))$("reveal").onclick=()=>step("reveal");
   for(const [btn,id,kind] of [["diagnose","diagnosis","diagnosis"],["repairSave","repair","repair"],["boundarySave","boundary","boundary"]])if($(btn))$(btn).onclick=()=>{const v=$(id).value.trim();if(v)step(kind,v);else $("status").textContent="Write reasoning before saving."};
   if($("boundaryReveal"))$("boundaryReveal").onclick=()=>step("boundary_reveal");
   if($("sourceReturn"))$("sourceReturn").onclick=async()=>{try{const sh=await digest(sourceRaw),sk="G9V41:PH06:SOURCE:"+source.uid+":"+sh;await navigator.locks.request(sk,async()=>{const raw=localStorage.getItem(sk);if(!raw)return;const old=JSON.parse(raw);if(old.hash!==sh||!old.first?.reasoning)throw Error("Invalid source first response");const updated=JSON.stringify({...old,transferComplete:{task:task.uid,hash,at:timestamp()}});localStorage.setItem(sk,updated);if(localStorage.getItem(sk)!==updated)throw Error("Source return save failed")});location.href=new URL("source-checkpoint.html",base).href}catch(err){fail(err)}};
  }
  store=await protectedStore(key,hash,render);
  $("commit").onclick=()=>{const prediction=$("prediction").value.trim(),reasoning=$("attempt").value.trim();if(!prediction||!reasoning){$("status").textContent="Both prediction and reasoning required";return}store.save(old=>old||first(hash,prediction,reasoning,null))};
  render(store.read());
 }
}catch(err){fail(err)}
