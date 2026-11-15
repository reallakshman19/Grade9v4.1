const $=id=>document.getElementById(id),root=$("root");
const e=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const p=s=>"<p>"+e(s)+"</p>", link=(url,label)=>'<a href="'+e(url)+'">'+e(label)+'</a>';
const get=async path=>{const r=await fetch(path,{cache:"no-store"});if(!r.ok)throw Error("Missing "+path);return r.json()};
const hash=async data=>Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(JSON.stringify(data)))),b=>b.toString(16).padStart(2,"0")).join("");
const stage=new URLSearchParams(location.search).get("stage")||"source";
const d=await get("content.v1.json");
if(d.release!=="HOLD")throw Error("Unexpected release state");
if(stage==="learn"){
 root.replaceChildren($("learn").content.cloneNode(true));
 const update=()=>{const u=Number($("speed").value),P=8+u,V=P/3,L=0.5*(2/3)*(4-u)**2;$("simout").textContent="Partner "+u+" m/s · total momentum "+P.toFixed(1)+" kg·m/s · joined velocity "+V.toFixed(2)+" m/s · impact loss "+L.toFixed(2)+" J";
 for(const [id,n] of [["pbar1",8],["pbar2",u],["pbar3",P]]){$(id).setAttribute("x",String(280+Math.min(0,n*10)));$(id).setAttribute("width",String(Math.abs(n*10)))}};
 $("speed").oninput=update;update();
}else if(["source","challenge","core2"].includes(stage)){
 const source=stage==="source",challenge=stage==="challenge", t=source?d.source:challenge?d.task:d.core2;
 const model=(await get("models.v1.json"))[source?"source":challenge?"task":"core2"];
 if(model.uid!==(source?t.id:t.uid)||(!source&&model.revision!==t.revision))throw Error("Exact task/model identity mismatch");
 const title=source?"Core2 · original-paper checkpoint":challenge?"Core1B · fresh reconstruction":"Core2 · authored assessment";
 const prompt=source?"Open IAPT's original unsolved paper, page 7, question 39. Record your own prediction and reasoning. Original paper/figure not republished; source custody and rights remain HOLD.":t.prompt;
 root.innerHTML='<article><h2>'+e(title)+'</h2><p class="meta">'+e(source?t.id:t.uid+" · "+t.revision)+'</p>'+p(prompt)+(source?'<p class="actions"><a href="'+e(t.paper)+'#page=7" target="_blank" rel="noopener">Open IAPT paper · Q39</a></p>':'<figure><img id="promptfig" alt="Question-facing schematic, only stated conditions"><figcaption>Authored schematic · not to scale.</figcaption></figure>')+'<label for="prediction">01 · Prediction'+(challenge?": "+e(t.prediction):"")+'</label><textarea id="prediction"></textarea><label for="attempt">02 · First reasoning attempt</label><textarea id="attempt"></textarea>'+(stage==="core2"?'<fieldset id="opts"><legend>Choose one option</legend>'+t.options.map((x,i)=>'<label><input name="opt" type="radio" value="'+String.fromCharCode(65+i)+'">'+e(x)+'</label>').join("")+'</fieldset>':'')+'<div id="helpers"></div><button id="commit" disabled>Save first attempt</button><p id="status" role="status">Checking exact revision…</p><div id="post"></div></article>';
 const status=s=>$("status").textContent=s;
 let rec=null;
 try{
  if(!crypto?.subtle||!navigator.locks)throw Error("SHA-256 or cross-tab lock unavailable");
  let figBytes=null;
  if(!source){const r=await fetch(t.figure,{cache:"no-store"});if(!r.ok)throw Error("Required figure missing");const bytes=await r.arrayBuffer();if(bytes.byteLength<100)throw Error("Invalid figure bytes");figBytes=Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",bytes)),b=>b.toString(16).padStart(2,"0")).join("");const url=URL.createObjectURL(new Blob([bytes],{type:"image/svg+xml"}));$("promptfig").src=url;await $("promptfig").decode();if(!$("promptfig").naturalWidth)throw Error("Figure decode failed");}
  const revision=await hash([t,model,figBytes,d.source.id]);const storageKey="G9V41:PH03:R1:"+stage+":"+(t.uid||t.id)+":"+revision;
  const read=()=>{const raw=localStorage.getItem(storageKey);if(!raw)return {revision,hints:0,events:[]};const x=JSON.parse(raw);if(x.revision!==revision||!Array.isArray(x.events)||!Number.isInteger(x.hints)||x.hints<0||x.hints>3)throw Error("Saved state invalid");return x};
  const probe=storageKey+":probe";localStorage.setItem(probe,"1");if(localStorage.getItem(probe)!=="1")throw Error("Storage readback failed");localStorage.removeItem(probe);rec=read();
  const fail=err=>{$("post").replaceChildren();$("helpers").replaceChildren();$("commit").disabled=true;status("HOLD: "+err.message+"; no further disclosure.")};
  const save=async(fn,kind)=>{try{await navigator.locks.request(storageKey,async()=>{const old=read(),changed=fn(old);if(!changed||changed===old){rec=old;return}const next={...changed,events:[...old.events,{kind,at:new Date().toISOString()}]},raw=JSON.stringify(next);localStorage.setItem(storageKey,raw);if(localStorage.getItem(storageKey)!==raw)throw Error("Attempt readback failed");rec=next});render()}catch(err){fail(err)}};
  const stageSave=(field,value,requires)=>save(old=>{if(!old.first||!requires(old)||old[field])return old;return {...old,[field]:value}},field);
  function render(){
   const first=rec.first;
   $("helpers").replaceChildren();
   if(!source&&!rec.revealed){const h=document.createElement("div");for(const hint of model.hints.slice(0,rec.hints)){const el=document.createElement("p");el.textContent=hint;h.append(el)}if(rec.hints<3){const b=document.createElement("button");b.id="hint";b.textContent="Reveal hint "+(rec.hints+1)+" of 3";b.onclick=()=>save(old=>old.revealed||old.hints>=3?old:{...old,hints:old.hints+1},"hint");h.append(b)}$("helpers").append(h)}
   if(!first){$("commit").disabled=false;status("Ready. First response and hint exposure are revision-bound.");return}
   $("prediction").value=first.prediction;$("attempt").value=first.attempt;$("prediction").disabled=$("attempt").disabled=$("commit").disabled=true;
   document.querySelectorAll("input[name=opt]").forEach(x=>{x.checked=x.value===first.option;x.disabled=true});
   status("First response preserved · "+(first.hints>0?"assisted":"unassisted")+" · exact revision.");
   let h="";
   if(source){h='<h3>Source attempt saved</h3><p>Study the construction and return after independent practice.</p><p class="actions">'+link("?stage=learn","Open Core1A guide")+'</p><label for="retry">Separate reattempt after learning</label><textarea id="retry">'+e(rec.retry||"")+'</textarea><button id="retrySave" '+(rec.retry?"disabled":"")+'>Save source reattempt</button>';
    if(rec.retry)h+='<h3>Source comparison · candidate HOLD</h3>'+p(model.reconstruction)+p(model.check);
   }else{
    if(!rec.revealed)h='<button id="reveal">Compare reconstruction</button>';
    if(rec.revealed){h='<h3>03 · Reconstruction</h3>'+p(model.reconstruction)+p(model.alternative||model.check);
     if(challenge){h+='<h3>04 · Diagnose the first divergence</h3><p>Select only an observed divergence from your saved response, not a guessed learner trait.</p>';
      h+=rec.diagnosis?p(rec.diagnosis):'<label for="diagnosisChoice">Observed divergence</label><select id="diagnosisChoice"><option value="">Choose</option>'+model.diagnosis_choices.map(([v,label])=>'<option value="'+e(v)+'">'+e(label)+'</option>').join("")+'</select><label for="diagnosisText">Evidence from your response</label><textarea id="diagnosisText"></textarea><button id="diagnose">Save diagnosis</button>';
      if(rec.diagnosis)h+='<h3>05 · Repair</h3>'+p(model.repair)+(rec.repair?p(rec.repair):'<label for="repair">Repaired reasoning</label><textarea id="repair"></textarea><button id="repairSave">Save repair</button>');
      if(rec.repair)h+='<h3>06 · Changed-condition transfer</h3>'+p(model.boundaryPrompt)+(rec.boundary?p(rec.boundary):'<label for="boundary">Independent boundary response</label><textarea id="boundary"></textarea><button id="boundarySave">Save boundary attempt</button>');
      if(rec.boundary)h+=rec.boundaryReveal?p(model.boundaryModel)+'<p class="actions">'+link("?stage=source","Return to original source")+link("?stage=core2","Try authored Core2")+'</p>':'<button id="boundaryReveal">Compare boundary</button>';
     }else h+='<p class="actions">'+link("?stage=source","Return to original source")+'</p>';
    }
   }
   $("post").innerHTML=h;
   if($("retrySave")){$("retry").disabled=!!rec.retry;$("retrySave").onclick=()=>{const v=$("retry").value.trim();if(v)stageSave("retry",v,()=>true)}}
   if($("reveal"))$("reveal").onclick=()=>stageSave("revealed",true,()=>true);
   if($("diagnose"))$("diagnose").onclick=()=>{const c=$("diagnosisChoice").value,v=$("diagnosisText").value.trim();if(c&&v)stageSave("diagnosis",c+": "+v,old=>old.revealed)};
   if($("repairSave"))$("repairSave").onclick=()=>{const v=$("repair").value.trim();if(v)stageSave("repair",v,old=>old.diagnosis)};
   if($("boundarySave"))$("boundarySave").onclick=()=>{const v=$("boundary").value.trim();if(v)stageSave("boundary",v,old=>old.repair)};
   if($("boundaryReveal"))$("boundaryReveal").onclick=()=>stageSave("boundaryReveal",true,old=>old.boundary);
  }
  $("commit").onclick=()=>{const prediction=$("prediction").value.trim(),attempt=$("attempt").value.trim(),option=document.querySelector("input[name=opt]:checked")?.value||null;if(!prediction||!attempt||(stage==="core2"&&!option))return status("Prediction, reasoning and any required option are necessary.");save(old=>old.first?old:{...old,first:{prediction,attempt,option,hints:old.hints,assisted:old.hints>0,at:new Date().toISOString()}},"first")};
  window.addEventListener("storage",evt=>{if(evt.key===storageKey){try{rec=read();render()}catch(err){fail(err)}}});render();
 }catch(err){status("HOLD: "+err.message+"; no further disclosure.");$("commit").disabled=true}
}else root.textContent="HOLD: unknown stage.";
