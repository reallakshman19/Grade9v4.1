/* PH03 R3 native authored-learning candidate.
 * Source, QRT, science, B1–B7 and academic release all HOLD.
 * Browser-local attempts are revision-bound self-study records, not secure exam custody. */
"use strict";
const mount=document.querySelector("[data-ph03-r3]");
if(!mount)throw Error("Missing native PH03 mount");
const unit=mount.dataset.unit,mode=mount.dataset.mode;
if(!/^(P01|P02|P04|P05|P06|P07)$/.test(unit)||!["learn","practice"].includes(mode))throw Error("Unregistered PH03 page");
const base=new URL("./",import.meta.url),physics=new URL("../../",base);
const $=id=>document.getElementById(id);
const escapeHtml=s=>String(s==null?"":s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const htmlList=(xs,tag="ol")=>"<"+tag+">"+xs.map(x=>"<li>"+escapeHtml(x)+"</li>").join("")+"</"+tag+">";
const url=(path)=>new URL(path,base).href;
const chapter=new URL("learn/chapter.html?ph=PH03",physics).href;
const canonical=(kind,id=unit)=>new URL((kind==="learn"?"textbook":"core1")+"/PH03/"+id+"/index.html",physics).href;
const sourceUrl=url("source-ledger.v1.html");
const readUrl=async path=>{const r=await fetch(url(path),{cache:"no-store"});if(!r.ok)throw Error("Required content unavailable: "+path);return r.arrayBuffer()};
const hex=buffer=>Array.from(new Uint8Array(buffer),b=>b.toString(16).padStart(2,"0")).join("");
const digest=async(algorithm,bytes)=>hex(await crypto.subtle.digest(algorithm,bytes));
const encoder=new TextEncoder(),decoder=new TextDecoder("utf-8",{fatal:true});
const parse=bytes=>JSON.parse(decoder.decode(bytes));
const blobSha=async bytes=>{const header=encoder.encode("blob "+bytes.byteLength+"\0"),merged=new Uint8Array(header.length+bytes.byteLength);merged.set(header);merged.set(new Uint8Array(bytes),header.length);return digest("SHA-1",merged)};
let content,firstImage,promptImage,postCache=null,solutionImage=null,revision,storeKey,exposureKey,rec,revisionSafe=false,exitCheck=null;
const fail=err=>{mount.innerHTML='<article class="hold"><h1>Learning path on HOLD</h1><p>'+escapeHtml(err.message||err)+'</p><p>No answers or mastery were released. You can return to the '+link(chapter,"chapter overview")+'.</p></article>'};
const link=(href,label,cls="")=>'<a'+(cls?' class="'+escapeHtml(cls)+'"':"")+' href="'+escapeHtml(href)+'">'+escapeHtml(label)+'</a>';
const figure=(image,caption)=>'<figure><img src="'+escapeHtml(image.url)+'" width="940" height="345" alt="'+escapeHtml(image.alt)+'"><figcaption>'+escapeHtml(caption)+'</figcaption></figure>';
const loadFigure=async(kind)=>{const bytes=await readUrl(content.figures[kind]);if(bytes.byteLength<250)throw Error("Missing or truncated "+kind+" SVG");
 const s=decoder.decode(bytes);if(!/<svg[\s>]/.test(s)||/<image[\s>]/i.test(s))throw Error("Invalid vector figure: "+kind);
 const objectUrl=URL.createObjectURL(new Blob([bytes],{type:"image/svg+xml"}));const img=new Image();img.src=objectUrl;
 try{await img.decode();if(!img.naturalWidth)throw Error("SVG has zero dimensions")}catch(err){URL.revokeObjectURL(objectUrl);throw Error("Figure decode failure: "+kind)}
 return {url:objectUrl,sha:await digest("SHA-256",bytes),blobSha:await blobSha(bytes),alt:"Original PH03 "+unit+" "+kind+" diagram (authored, not source-exam reproduction)"};
};
const probe=()=>{const name="G9V41:PH03:R3:probe";localStorage.setItem(name,"ok");if(localStorage.getItem(name)!=="ok")throw Error("Storage readback failed");localStorage.removeItem(name)};
const readRecord=()=>{const raw=localStorage.getItem(storeKey);if(!raw)return{revision,hints:0,events:[]};
 const x=JSON.parse(raw);if(x.revision!==revision||!Array.isArray(x.events)||!Number.isInteger(x.hints)||x.hints<0||x.hints>3)throw Error("Invalid revision-bound record");
 if(x.first){if(!x.first.at||!Array.isArray(x.first.skipped)||!x.first.fields||!Object.prototype.hasOwnProperty.call(x.first,"prediction"))throw Error("Invalid first response");}
 return x};
const expose=async()=>{await navigator.locks.request(exposureKey,async()=>{if(localStorage.getItem(exposureKey))return;const raw=JSON.stringify({unit,mode,at:new Date().toISOString(),revision});localStorage.setItem(exposureKey,raw);if(localStorage.getItem(exposureKey)!==raw)throw Error("Learning exposure write failure")})};
const save=async(kind,transform)=>{try{
 await navigator.locks.request(storeKey,async()=>{const old=readRecord(),next=transform(old);if(!next||next===old){rec=old;return}
 const value={...next,events:[...old.events,{kind,at:new Date().toISOString()}]},raw=JSON.stringify(value);
 localStorage.setItem(storeKey,raw);if(localStorage.getItem(storeKey)!==raw)throw Error("Attempt write/readback failure");rec=value});
 await renderPractice();
}catch(err){fail(err)}};
const skipped=id=>$(id)?.dataset.skipped==="true";
const buttonSkip=(id,disabled,wasSkipped)=>disabled?(wasSkipped?'<span class="skip-record">Skipped · no credit</span>':""):'<button type="button" class="skip-button" data-skip="'+escapeHtml(id)+'" aria-pressed="false" aria-label="Skip '+escapeHtml(id)+' (no credit)">Skip</button>';
const textarea=(id,label,disabled=false,value="",oldSkipped=[])=>'<div class="question-field"><label for="'+escapeHtml(id)+'">'+escapeHtml(label)+'</label><textarea rows="4" id="'+escapeHtml(id)+'" '+(disabled?"disabled":"")+'>'+escapeHtml(value)+'</textarea>'+buttonSkip(id,disabled,oldSkipped.includes(id))+'</div>';
const fieldHTML=(fields,prefix,values={},disabled=false,oldSkipped=[])=>'<div class="field-grid">'+fields.map(field=>{
 const id=prefix+field.id,v=values[field.id],sk=oldSkipped.includes(id);
 const input=field.type==="choice"?'<fieldset id="'+escapeHtml(id)+'" '+(disabled?"disabled":"")+'><legend>'+escapeHtml(field.label)+'</legend>'+field.options.map(o=>'<label class="option"><input type="radio" name="'+escapeHtml(id)+'" value="'+escapeHtml(o.value)+'" '+(o.value===v?"checked ":"")+(disabled?"disabled":"")+'>'+escapeHtml(o.text)+'</label>').join("")+'</fieldset>':
 '<label for="'+escapeHtml(id)+'">'+escapeHtml(field.label)+' <small>('+escapeHtml(field.unit)+')</small></label><input type="number" step="any" id="'+escapeHtml(id)+'" value="'+escapeHtml(v==null?"":v)+'" '+(disabled?"disabled":"")+'>';
 return '<div class="question-field">'+input+buttonSkip(id,disabled,sk)+'</div>';
 }).join("")+'</div>';
const getText=id=>{if(skipped(id))return null;const el=$(id),v=el?.value.trim();if(!v)throw Error("Enter "+id+" or select Skip (no credit)");return v};
const getFields=(fields,prefix)=>{const values={};for(const f of fields){
 const id=prefix+f.id;if(skipped(id)){values[f.id]=null;continue}
 if(f.type==="choice"){const v=document.querySelector('input[name="'+id+'"]:checked')?.value||"";if(!f.options.some(o=>o.value===v))throw Error("Choose "+f.label+" or Skip");values[f.id]=v}
 else{const raw=$(id)?.value.trim();if(!raw)throw Error("Enter "+f.label+" or Skip");const v=Number(raw);if(!Number.isFinite(v))throw Error("Enter a finite number for "+f.label);values[f.id]=v;}
 }return values};
const skipIds=(prefix,fields)=>fields.map(f=>prefix+f.id).filter(skipped);
const note=(s)=>{const el=$("ph03-status");if(el)el.textContent=s};
mount.addEventListener("click",event=>{const b=event.target.closest("button[data-skip]");if(!b||!mount.contains(b))return;const target=$(b.dataset.skip);if(!target||b.disabled)return;
 const next=!skipped(b.dataset.skip);target.dataset.skipped=String(next);target.disabled=next;
 b.textContent=next?"Undo skip":"Skip";b.setAttribute("aria-pressed",String(next));
 note(next?"Field explicitly skipped (unanswered; no mastery credit). Undo skip to try it before saving.":"Skip undone. Answer the field or choose Skip again.");
});
const same=(a,b)=>typeof b==="number"?typeof a==="number"&&Number.isFinite(a)&&Math.abs(a-b)<=1e-6:a===b;
const firstMismatch=(fields,expected,order)=>{for(const k of order){if(fields?.[k]==null)return"insufficient";if(!same(fields[k],expected[k]))return k}return"structured_match"};
const stateSummary=x=>{const skips=x?.skipped||[];return skips.length?"Skipped "+escapeHtml(skips.join(", "))+" · no credit.":"Completed fields recorded · free-text still ungraded."};
const safeModel=(kind,v)=>{
 const fmt=x=>Number(x.toFixed(3)).toString();let label="",value="",explain="";
 switch(kind){
 case"signed-momentum":{const P=2*v+6,K=v*v+6;label="Signed total momentum "+fmt(P)+" kg·m/s",value="Total kinetic energy "+fmt(K)+" J";explain="2 kg at variable v plus 3 kg at +2 m/s; both velocities use the same lab frame.";break;}
 case"impulse-pulse":{const J=.5*.4*v,V=-1+J/2;label="Triangular impulse "+fmt(J)+" N·s",value="Illustrative 2 kg cart: v_final "+fmt(V)+" m/s";explain="Area of a 0.4 s triangle; its force peak, not its mean, is being varied.";break;}
 case"third-law":{label="A (2 kg) velocity "+fmt(-v/2)+" m/s",value="B (4 kg) velocity "+fmt(v/4)+" m/s";explain="A receives −J and B receives +J; pair momentum stays zero in this isolated demonstration.";break;}
 case"recoil":{label="Platform (8 kg) velocity "+fmt(-2*v/8)+" m/s",value="Load (2 kg) velocity +"+fmt(v)+" m/s";explain="The load's speed is LAB-measured, and the initially resting pair has zero total momentum.";break;}
 case"sticking":{const V=2*v/5,K=.5*2*v*v,after=.5*5*V*V;label="Joined 5 kg velocity "+fmt(V)+" m/s",value="Contact kinetic energy converted "+fmt(K-after)+" J";explain="Teaching masses 2 kg and 3 kg stick; do not assume kinetic energy conservation.";break;}
 case"reachability":{const stop=v===0?Infinity:9/(20*v),stillMoving=v===0||9-30*v>1e-9;label="Stopping distance "+(Number.isFinite(stop)?fmt(stop)+" m":"unbounded without friction"),value=stillMoving?"Reaches 1.5 m obstacle with speed "+fmt(Math.sqrt(Math.max(0,9-30*v)))+" m/s":"Stops before the obstacle: no impact";explain="Teaching assembly begins at +3 m/s; static contact never follows if friction stops it early.";break;}
 default:throw Error("Unknown physical model");
 }
 return {label,value,explain};
};
function writeHeader(current){
 return '<p class="eyebrow">NSEJS Physics · PH03 Momentum and Collisions</p><h1>'+escapeHtml(content.title)+'</h1>'+
 '<p class="hold"><strong>AUTHOR CANDIDATE · ACADEMIC HOLD.</strong> '+escapeHtml(content.scope)+' · Source/rights, independent science, QRT and B1–B7 not accepted. '+(content.scope==="EXTENSION_REVIEW"?"Extension review only; not promoted to mandatory syllabus.":"Not an authenticated original examination question.")+'</p>'+
 '<nav aria-label="PH03 journey">'+link(chapter,"Chapter overview")+link(canonical("learn"),"Learn")+link(canonical("practice"),"Try it")+link(sourceUrl,"Source status (HOLD)")+'</nav>';
}
function modelHTML(){return '<div class="model"><h3>Move one physical parameter</h3><label for="model-slider">'+escapeHtml(content.model.label)+'</label>'+
 '<input id="model-slider" type="range" min="'+content.model.min+'" max="'+content.model.max+'" step="'+content.model.step+'" value="'+content.model.value+'">'+
 '<output id="model-output" for="model-slider" aria-live="polite"></output><p id="model-context"></p><p class="mini">Teaching example, intentionally different from the fresh Try-it problem.</p></div>';}
function renderLearn(){
 const sections=content.sections.map((s,i)=>'<section><h2>'+(i+1)+'. '+escapeHtml(s.heading)+'</h2><p>'+escapeHtml(s.body)+'</p></section>').join("");
 const examples=content.worked.map((w,i)=>'<section class="worked"><h3>Worked '+(i+1)+' · '+escapeHtml(w.name)+'</h3><p>'+escapeHtml(w.setup)+'</p>'+htmlList(w.steps)+'<p class="check"><strong>Independent check:</strong> '+escapeHtml(w.check)+'</p></section>').join("");
 mount.innerHTML=writeHeader()+"<article>"+'<p class="lead">Before the challenge: '+escapeHtml(content.prereq)+'</p>'+
 '<h2>Learning goals</h2>'+htmlList(content.goals)+"<h2>Connected explanation</h2>"+sections+
 figure(firstImage,"Author-created worked-model diagram. This is NOT a reconstruction of any NSEJS source figure.")+examples+
 '<section><h2>Common wrong route</h2><p><strong>Temptation:</strong> '+escapeHtml(content.trap.wrong)+'</p><p><strong>Repair:</strong> '+escapeHtml(content.trap.repair)+'</p></section>'+
 modelHTML()+'<section><h2>Conditions and validity boundaries</h2>'+htmlList(content.assumptions)+'</section>'+
 '<section class="core1a-exit"><h2>Independent synthesis check</h2><p>'+escapeHtml(exitCheck.question)+'</p><p class="mini">Think through the mechanism before revealing the explanation. This is optional Core1A study, not a graded Core1B attempt or an exam question.</p><details><summary>Compare the reasoning</summary><p>'+escapeHtml(exitCheck.answer)+'</p><p><strong>Independent check:</strong> '+escapeHtml(exitCheck.check)+'</p></details></section>'+
 '<p class="actions">'+link(canonical("practice"),"Try a fresh changed problem","primary")+link(sourceUrl,"See related source status")+'</p></article>';
 $("model-slider").oninput=()=>{const v=Number($("model-slider").value),m=safeModel(content.model.kind,v);$("model-output").textContent=m.label+" · "+m.value;$("model-context").textContent=m.explain};$("model-slider").dispatchEvent(new Event("input"));
}
let modelLoading=null;
async function loadPost(){
 if(!rec?.first)throw Error("Protected answer requested before first attempt");
 if(postCache)return postCache;
 if(!modelLoading)modelLoading=(async()=>{const bytes=await readUrl("post-"+unit+".json"),sha=await blobSha(bytes);if(sha!==content.postBlobSha1)throw Error("Postattempt byte pin mismatch");
 const p=parse(bytes);if(p.id!==unit||p.revision!==content.revision||p.academic!=="HOLD"||p.schema!=="g9-ph03-postattempt/v1")throw Error("Postattempt identity mismatch");
 return p;})();
 postCache=await modelLoading;return postCache;
}
function compareBlock(fields,expected,skipList){
 if((skipList||[]).length||Object.values(fields||{}).some(v=>v===null))return "Some fields were explicitly skipped: ungraded, no mastery credit.";
 return Object.keys(expected).every(k=>same(fields[k],expected[k]))?"Structured values match the author model; written reasoning is NOT independently assessed.":"Some structured values differ from the model; this is not a mastery verdict.";
}
async function renderPractice(){
 rec=readRecord();
 const first=rec.first;
 const sketch=first?'<h3>First attempt preserved</h3><p class="mini">'+stateSummary(first)+'</p>':"";
 mount.innerHTML=writeHeader()+'<article><h2>Fresh transfer problem · '+escapeHtml(unit)+'</h2><p class="lead">'+escapeHtml(content.prompt.stem)+'</p>'+
 figure(promptImage,"Authored question-facing diagram. Answer-bearing annotations are excluded.")+
 '<p class="hold">Skip is optional: blank fields are recorded as unanswered and earn no credit. Free-text is not automatically assessed; answers appear only after a saved first attempt.</p>'+
 '<div id="ph03-first"></div><div id="ph03-after"></div><p id="ph03-status" class="status" role="status" aria-live="polite"></p></article>';
 $("ph03-first").innerHTML=textarea("first-prediction","01 · Predict before calculation: "+content.prompt.prediction,!!first,first?.prediction,first?.skipped||[])+
 fieldHTML(content.prompt.fields,"first-",first?.fields||{},!!first,first?.skipped||[])+textarea("first-reason","02 · Explain your strategy",!!first,first?.reason,first?.skipped||[])+
 (first?sketch:'<button class="primary" id="save-first">Save first response (or explicit skips)</button>');
 note(first?"First response saved at "+first.at+". "+stateSummary(first):"Ready to record a first response; no answer material has been requested.");
 if(!first){
 $("save-first").onclick=()=>{try{
 const prediction=getText("first-prediction"),reason=getText("first-reason"),fields=getFields(content.prompt.fields,"first-"),
 sk=["first-prediction","first-reason"].filter(skipped).concat(skipIds("first-",content.prompt.fields));
 save("first",old=>old.first?old:{...old,first:{prediction,reason,fields,skipped:sk,at:new Date().toISOString(),assisted:false,sourceRole:content.sourceRole,learningExposed:!!localStorage.getItem(exposureKey)}});
 }catch(err){note(err.message)}};
 return;
 }
 const post=await loadPost();
 let h='<section><h2>After durable first attempt</h2><p class="mini">Hints and reconstruction are comparison resources, not proof of mastery.</p>';
 if(!rec.revealed){
 h+=post.hints.slice(0,rec.hints).map((x,i)=>'<p class="hint">Hint '+(i+1)+' · '+escapeHtml(x)+'</p>').join("");
 if(rec.hints<3)h+='<button id="next-hint">Next hint ('+(rec.hints+1)+' of 3)</button> ';
 h+='<button id="reveal">Compare reconstruction</button>';
 }else{
 if(!solutionImage){solutionImage=await loadFigure("solution");if(content.solutionBlobSha1&&solutionImage.blobSha!==content.solutionBlobSha1)throw Error("Solution figure byte pin mismatch");}
 h+='<h3>03 · Model reconstruction</h3>'+htmlList(post.steps)+figure(solutionImage,"Solution-role diagram fetched only after first attempt and comparison request.");
 const mismatch=(first.skipped.length?"insufficient":firstMismatch(first.fields,post.expected,post.firstErrorOrder));
 const guidance=mismatch==="structured_match"?"All structured values match; free-text reasoning remains ungraded.":mismatch==="insufficient"?"First attempt contained explicit unanswered fields. No independent diagnostic or credit can be inferred.":post.diagnostics[mismatch];
 h+='<div class="feedback"><h3>04 · Diagnose the first divergence</h3><p>'+escapeHtml(guidance)+'</p><p class="mini">Inspect the written first attempt yourself; this computer checks only selected structured fields.</p></div>';
 if(!rec.diagnosis)h+=textarea("diag-text","Quote the actual first wrong step, or choose Skip.")+'<button id="save-diagnosis">Save diagnosis</button>';
 else{
 h+=rec.diagnosis.skipped?'<p class="skip-record">Diagnosis skipped · no mastery credit</p>':'<p class="feedback">Recorded diagnosis: '+escapeHtml(rec.diagnosis.text)+'</p>';
 h+='<h3>05 · Repair the reasoning</h3>'+fieldHTML(content.prompt.fields,"repair-",rec.repair?.fields||{},!!rec.repair,rec.repair?.skipped||[]);
 if(!rec.repair)h+=textarea("repair-reason","Explain how the model should be reconstructed, or Skip.")+'<button id="save-repair">Save repair</button>';
 else {
 h+='<p class="feedback">'+escapeHtml(compareBlock(rec.repair.fields,post.expected,rec.repair.skipped))+'</p>'+
 '<p class="mini">Repair explanation: '+escapeHtml(rec.repair.reason||"Skipped; no credit")+'</p>'+
 '<h3>06 · Changed-condition transfer</h3><p>'+escapeHtml(content.prompt.boundaryPrompt)+'</p>'+
 fieldHTML(content.prompt.boundaryFields,"bound-",rec.boundary?.fields||{},!!rec.boundary,rec.boundary?.skipped||[]);
 if(!rec.boundary)h+=textarea("boundary-reason","Explain which physical assumption changed, or Skip.")+'<button id="save-boundary">Save boundary attempt</button>';
 else if(!rec.boundaryRevealed)h+='<p class="mini">Boundary attempt saved. Compare only when ready.</p><button id="compare-boundary">Compare changed-condition model</button>';
 else{
 h+='<h3>07 · Boundary comparison</h3>'+htmlList(post.boundarySteps)+
 '<p class="feedback">'+escapeHtml(compareBlock(rec.boundary.fields,post.boundaryExpected,rec.boundary.skipped))+'</p>';
 h+='<h3>08 · Return to source evidence</h3><p>Source locators are not independently qualified originals; this is an authored transfer, not an examination admission.</p>';
 h+=!rec.sourceReturn?'<button id="record-return">Record source-status return</button>':'<p>Source status return recorded · academic HOLD.</p>';
 h+='<p class="actions">'+link(sourceUrl,"View source evidence and exclusions")+link(chapter,"Back to all seven topics")+'</p>';
 }
 }
 }
 }
 h+="</section>";$("ph03-after").innerHTML=h;
 if($("next-hint"))$("next-hint").onclick=()=>save("hint",old=>old.first&&!old.revealed&&old.hints<3?{...old,hints:old.hints+1}:old);
 if($("reveal"))$("reveal").onclick=()=>save("reveal",old=>old.first&&!old.revealed?{...old,revealed:true}:old);
 if($("save-diagnosis"))$("save-diagnosis").onclick=()=>{try{const text=getText("diag-text"),sk=skipped("diag-text");save("diagnosis",old=>old.revealed&&!old.diagnosis?{...old,diagnosis:{text,skipped:sk,at:new Date().toISOString()}}:old)}catch(err){note(err.message)}};
 if($("save-repair"))$("save-repair").onclick=()=>{try{const reason=getText("repair-reason"),fields=getFields(content.prompt.fields,"repair-"),sk=skipIds("repair-",content.prompt.fields).concat(skipped("repair-reason")?["repair-reason"]:[]);save("repair",old=>old.diagnosis&&!old.repair?{...old,repair:{reason,fields,skipped:sk,at:new Date().toISOString()}}:old)}catch(err){note(err.message)}};
 if($("save-boundary"))$("save-boundary").onclick=()=>{try{const reason=getText("boundary-reason"),fields=getFields(content.prompt.boundaryFields,"bound-"),sk=skipIds("bound-",content.prompt.boundaryFields).concat(skipped("boundary-reason")?["boundary-reason"]:[]);save("boundary",old=>old.repair&&!old.boundary?{...old,boundary:{reason,fields,skipped:sk,at:new Date().toISOString()}}:old)}catch(err){note(err.message)}};
 if($("compare-boundary"))$("compare-boundary").onclick=()=>save("boundary-reveal",old=>old.boundary&&!old.boundaryRevealed?{...old,boundaryRevealed:true}:old);
 if($("record-return"))$("record-return").onclick=()=>save("source-return",old=>old.boundaryRevealed&&!old.sourceReturn?{...old,sourceReturn:{status:"SOURCE_AUTHENTICITY_HOLD",at:new Date().toISOString(),sourceRole:content.sourceRole}}:old);
}
async function initialize(){
 try{
 if(!crypto?.subtle||!navigator.locks)throw Error("WebCrypto and cross-tab Web Locks are required for revision-bound attempt safety");
 probe();const bytes=await readUrl(unit+".json");content=parse(bytes);
 if(content.schema!=="g9-ph03-authored-lesson/v1"||content.academic!=="HOLD"||content.id!==unit||!content.postBlobSha1||!content.figures||content.sourceRole!=="AUTHOR_EXPOSITION_AND_TRANSFER_NOT_EXAM")throw Error("Unexpected PH03 content or release state");
 firstImage=await loadFigure("guide");
 if(mode==="practice")promptImage=await loadFigure("prompt");
 revision=await digest("SHA-256",encoder.encode(JSON.stringify([decoder.decode(bytes),firstImage.sha,promptImage?.sha||"",content.postBlobSha1,content.solutionBlobSha1||""])));
 storeKey="G9V41:PH03:R3:"+unit+":"+revision;exposureKey="G9V41:PH03:R3:EXPOSE:"+unit+":"+content.revision;
 revisionSafe=true;
 if(mode==="learn"){const exitPacket=parse(await readUrl("exit-checks.v1.json"));if(exitPacket.schema!=="g9-ph03-core1a-exit/v1"||exitPacket.academic!=="HOLD"||exitPacket.source_role!=="AUTHORED_TEACHING_NOT_EXAM")throw Error("Invalid Core1A exit packet");exitCheck=exitPacket.units?.[unit];if(!exitCheck||![exitCheck.question,exitCheck.answer,exitCheck.check].every(x=>typeof x==="string"&&x.trim()))throw Error("Missing Core1A independent synthesis");await expose();renderLearn()}else await renderPractice();
 window.addEventListener("storage",ev=>{if(mode!=="practice"||!revisionSafe)return;if(ev.key===storeKey||ev.key===null){try{const fresh=readRecord();if(JSON.stringify(fresh)!==JSON.stringify(rec))renderPractice().catch(fail)}catch(err){fail(err)}}});
 }catch(err){fail(err)}
}
await initialize();
