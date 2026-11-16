/* Shared DOM adapter. Text-only rendering; no subject-specific script. */
import {loadAssessment,compare,canOpen} from "./engine.mjs";
const root=document.querySelector("[data-assessment]");
const status=document.querySelector("#status");
const e=(tag,text)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n};
const add=(p,tag,text)=>{const n=e(tag,text);p.append(n);return n};
let engine,view,busy=false,blocked=false,urls=[];
const say=t=>{status.textContent=t};
function halt(err){blocked=true;root.querySelectorAll("button,input,select,textarea").forEach(n=>n.disabled=true);if(!root.children.length)root.append(e("p","Session locked. No further feedback access."));say(String(err.message||err))}
function section(title){const p=add(root,"section");add(p,"h2",title);return p}
function action(parent,label,fn){const b=add(parent,"button",label);b.type="button";b.disabled=busy;b.addEventListener("click",()=>run(fn));return b}
async function run(fn){
 if(busy||blocked)return;busy=true;root.querySelectorAll("button").forEach(b=>b.disabled=true);
 let redraw=true;try{const r=await fn();if(r.accepted===false&&r.state.events.length===view?.state.events.length)redraw=false;view=r;if(r.accepted===false)say("Not saved: "+r.reason);else say("Saved / verified. Academic HOLD.");}
 catch(err){halt(err)}finally{busy=false;if(!blocked&&view){if(redraw)draw();else root.querySelectorAll("button").forEach(b=>b.disabled=false)}}
}
function textBox(p,label,name){const l=add(p,"label",label);const input=add(l,"textarea");input.name=name;input.rows=3;return input}
function form(p,defs,kind,label){
 const inputs={};
 for(const f of defs){
  const l=add(p,"label",f.label);let n;
  if(f.type==="choice"){
   n=add(l,"select");const empty=add(n,"option","Choose");empty.value="";
   for(const o of f.options){const opt=add(n,"option",o.label);opt.value=o.id}
  }else if(f.type==="number"){n=add(l,"input");n.type="text";n.inputMode="decimal"}
  else{n=add(l,"textarea");n.rows=3}
  n.name=f.id;inputs[f.id]=n;
 }
 action(p,label,()=>{const a={};for(const f of defs){const raw=inputs[f.id].value.trim();a[f.id]=f.type==="number"?(raw!==""&&/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$/.test(raw)?Number(raw):null):raw}return engine.submit(kind,a)});
}
function openButton(p,role,label){if(canOpen(view.state,role,engine.m))action(p,label,()=>engine.open(role))}
function showSaved(p,label,record){add(p,"p",label);add(p,"pre",JSON.stringify(record,null,2))}
function results(p,r){add(p,"p",r.allMatched?"All structured checks match; free text is ungraded.":"First differing checked field: "+r.firstDivergence);for(const c of r.results)add(p,"p",c.field+": "+(c.pass?"matches":c.feedback))}
function media(p,role){for(const image of view.media[role]??[]){const fig=add(p,"figure");const img=add(fig,"img");const u=URL.createObjectURL(image.blob);urls.push(u);img.src=u;img.alt=image.alt;img.style.maxWidth="100%";add(fig,"figcaption",image.alt)}}
function draw(){
 for(const u of urls)URL.revokeObjectURL(u);urls=[];
 const {state:s,assets:a,diagnostic:d,boundaryResult:b,sourceResult:sr}=view;
 root.replaceChildren();
 add(root,"p","Technical candidate · Academic HOLD · Browser storage is not tamper-proof. Opening a resource records exposure, not reading or mastery.");
 if(!a.source_prompt){openButton(section("Source encounter"),"source_prompt","Open source prompt");return}
 if(!s.source){const p=section("Source encounter");add(p,"p",a.source_prompt.stem);media(p,"source_prompt");form(p,a.source_prompt.fields,"source","Commit source attempt");return}
 if(!a.study){openButton(section("Core1A"),"study","Open teaching");return}
 if(!a.challenge){
  const p=section(a.study.title);for(const x of a.study.sections){add(p,"h3",x.heading);for(const t of x.body)add(p,"p",t)}
  media(p,"study");openButton(p,"challenge","Open fresh challenge");return
 }
 if(!s.prediction){const p=section("1 · Predict");add(p,"p",a.challenge.stem);media(p,"challenge");add(p,"p",a.challenge.prediction);const t=textBox(p,"Initial expectation and reason","prediction");action(p,"Commit prediction",()=>engine.submit("prediction",t.value.trim()));return}
 if(!s.first){const p=section("2 · Attempt");add(p,"p",a.challenge.stem);media(p,"challenge");showSaved(p,"Frozen prediction",s.prediction);
  for(const h of ["hint1","hint2","hint3"]){if(a[h])add(p,"p",h+": "+a[h].text);else openButton(p,h,"Reveal "+h+" (assisted)")}
  form(p,a.challenge.fields,"first","Commit first attempt");return
 }
 const prior=section("Preserved first attempt");showSaved(prior,"Original response",s.first);
 if(!a.feedback){openButton(section("3 · Reconstruction"),"feedback","Open worked reconstruction");return}
 if(!s.reconstruction){const p=section("3 · Reconstruction");for(const x of a.feedback.reconstruction)add(p,"p",x);media(p,"feedback");results(p,d);const t=textBox(p,"Compare your saved reasoning with the worked model","comparison");action(p,"Commit comparison",()=>engine.submit("reconstruct",t.value.trim()));return}
 if(!s.diagnosis){const p=section("4 · Diagnose");results(p,d);const l=add(p,"label","First differing checked field");const select=add(l,"select");const empty=add(select,"option","Choose");empty.value="";const none=add(select,"option","No checked divergence");none.value="none";for(const c of d.results){const o=add(select,"option",c.field);o.value=c.field}const t=textBox(p,"Explain the difference using your original response","diagnosis");action(p,"Commit diagnosis",()=>engine.submit("diagnose",{field:select.value==="none"?null:select.value,explanation:t.value.trim()}));return}
 if(!s.repairs.at(-1)?.matched){const p=section("5 · Repair");add(p,"p",a.feedback.repair_prompt);if(s.repairs.length)results(p,compare(a.challenge.fields,a.feedback.checks,s.repairs.at(-1).answer));form(p,a.challenge.fields,"repair","Commit repair");return}
 if(!a.boundary){openButton(section("6 · Boundary"),"boundary","Open changed-condition prompt");return}
 if(!s.boundary){const p=section("6 · Boundary");add(p,"p",a.boundary.stem);media(p,"boundary");form(p,a.boundary.fields,"boundary","Commit boundary response");return}
 if(!a.boundary_feedback){openButton(section("Boundary response preserved"),"boundary_feedback","Open boundary feedback");return}
 if(!b.allMatched&&!s.boundaryRepairs.at(-1)?.matched){const p=section("Boundary correction");results(p,b);add(p,"p",a.boundary_feedback.model);media(p,"boundary_feedback");if(s.boundaryRepairs.length)results(p,compare(a.boundary.fields,a.boundary_feedback.checks,s.boundaryRepairs.at(-1).answer));form(p,a.boundary.fields,"boundary_repair","Commit boundary repair");return}
 if(!s.sourceReturn){const p=section("Source return");add(p,"p",a.boundary_feedback.model);add(p,"p",a.source_prompt.stem);showSaved(p,"Original source answer",s.source);form(p,a.source_prompt.fields,"source_return","Commit source return");return}
 if(!a.source_feedback){openButton(section("Source return saved"),"source_feedback","Open source feedback");return}
 const p=section("Sequence complete — not mastery");add(p,"p",a.source_feedback.model);media(p,"source_feedback");add(p,"h3","Original source checks");results(p,view.sourceFirstResult);add(p,"h3","Return checks");results(p,sr);showSaved(p,"Original source response",s.source);showSaved(p,"Returned source response",s.sourceReturn);add(p,"p","Academic HOLD. No scientific or QRT acceptance inferred.");
}
async function start(){
 try{
  engine=await loadAssessment({manifestURL:new URL(root.dataset.manifest,location.href).href,expectedHash:root.dataset.pin});
  view=await engine.snapshot();draw();
  window.addEventListener("storage",ev=>{if((ev.key===engine.key||ev.key===null)&&!busy&&!blocked)run(()=>engine.snapshot())});
 }catch(err){halt(err)}
}
start();
