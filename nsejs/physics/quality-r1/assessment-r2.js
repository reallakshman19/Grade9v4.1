/* WPE/PH06 R2-inspired candidate six-stage adapter, using shared protected store.
 * Separates Predict and Attempt, structured first-divergence checks, and
 * post-commit/boundary model fetching. Never awards academic mastery.
 */
import {openProtectedStore,readExposure} from "./protected-attempt-store.js";
import {assetPins,pinnedJson,sha256} from "./pinned-assets.js";

const E=(tag,text,cls)=>{const node=document.createElement(tag);if(text!==undefined)node.textContent=String(text);if(cls)node.className=cls;return node};
const add=(p,...c)=>{p.append(...c);return p};
const section=(name)=>add(E("section",undefined,"card stage"),E("h2",name));
const paragraph=(text,cls)=>E("p",text,cls);
const choice=(label,id,field)=>{
 const wrap=E("div",undefined,"field"),lab=E("label",label);lab.htmlFor=id;
 let control;
 if(field.type==="select"){
  control=E("select");for(const c of field.options){const opt=E("option",c);opt.value=c;control.append(opt)}
 }else{control=E("input");control.type="number";control.step="any";control.inputMode="decimal"}
 control.id=id;add(wrap,lab,control);return wrap;
};
const area=(label,id)=>{const wrap=E("div",undefined,"field"),lab=E("label",label);lab.htmlFor=id;const t=E("textarea");t.id=id;add(wrap,lab,t);return wrap};
const button=(text,handler)=>{const b=E("button",text);b.type="button";b.onclick=handler;return b};
const snapshot=(s)=>add(E("details",undefined,"card"),E("summary","My immutable first response"),paragraph("Prediction: "+s.prediction.value),paragraph("First explanation: "+s.first.reasoning),...Object.entries(s.first.fields).map(([key,v])=>paragraph(key+": "+(v||"Not entered"))));
function evaluate(rules,values){
 return rules.map(x=>{
  const raw=values?.[x.id]??"",empty=String(raw).trim()==="";
  const good=!empty&&(typeof x.expected==="number"
   ?Number.isFinite(Number(raw))&&Math.abs(Number(raw)-x.expected)<=x.tol:String(raw)===String(x.expected));
  return {id:x.id,match:good,status:empty?"MISSING":good?"MATCH":"REVIEW",feedback:empty?"No response for "+x.id+". "+x.repair:good?"Matches this authored reference; verify the physical reasoning.":x.repair};
 });
}
export async function startAssessment({unit,mount}){
 const pins=await assetPins();
 const predData=(await pinnedJson("prediction-prompts.v2.json","g9v41-physics-prediction/v2")).body;
 const matches=predData.units.filter(x=>x.unit===unit);
 if(matches.length!==1)throw Error("Unknown or duplicate task identity");
 const pred=matches[0];
 if(predData.source_v2_git_blob!==pins.source_sha)throw Error("Untrusted author source revision");
 const stateFingerprint=await sha256(JSON.stringify([pins.pin_blob,pins.source_sha,pred.uid,pred.revision,pins.entries.get("study-data.v2.json"),
  pins.entries.get("prediction-prompts.v2.json"),pins.entries.get("attempt-prompts.v2.json"),
  pins.entries.get("postattempt-guidance.v2.json"),pins.entries.get("boundary-models.v2.json")]));
 let store=null,current=null,work=null,guide=null,boundary=null,epoch=0,lastError="";
 const loadTask=async()=>{
  if(work)return work;
  const r=(await pinnedJson("attempt-prompts.v2.json","g9v41-physics-first-attempt/v2")).body;
  const x=r.units.filter(x=>x.uid===pred.uid&&x.unit===unit&&x.revision===pred.revision);
  if(x.length!==1||!x[0].fields?.length)throw Error("First-attempt task revision mismatch");
  work=x[0];return work;
 };
 const loadGuide=async()=>{
  if(guide)return guide;
  const r=(await pinnedJson("postattempt-guidance.v2.json","g9v41-physics-after-first/v2")).body;
  const x=r.units.filter(x=>x.uid===pred.uid&&x.unit===unit&&x.revision===pred.revision);
  if(x.length!==1||!x[0].rubric?.length||!x[0].boundaryFields?.length)throw Error("Diagnosis model revision mismatch");
  guide=x[0];return guide;
 };
 const loadBoundary=async()=>{
  if(boundary)return boundary;
  const r=(await pinnedJson("boundary-models.v2.json","g9v41-physics-after-boundary/v2")).body;
  const x=r.units.filter(x=>x.uid===pred.uid&&x.unit===unit&&x.revision===pred.revision);
  if(x.length!==1||!x[0].boundaryRubric?.length)throw Error("Boundary model revision mismatch");
  boundary=x[0];return boundary;
 };
 const enter=async(kind,payload)=>{if(!store)return;const ok=await store.act(kind,payload);if(ok)lastError="";};
 function title(s){const n=section("Candidate Core1B · "+unit);add(n,paragraph("AUTHOR-EXPOSED · original examination, blind QRT, B1–B7 and release HOLD"),
   paragraph("Your first prediction and first attempt are saved separately, revision-bound and retained through later stages. Browser-local records are not proctored evidence."),
   paragraph("Stage: "+(!s?"1 · Predict":({1:"2 · Attempt",2:"3 · Reconstruct",3:"4 · Diagnose",4:"5 · Repair",5:"6 · Boundary",6:"Boundary model",7:"Candidate cycle complete"}[s.stage]))));
  if(lastError)add(n,paragraph("HOLD: "+lastError,"error"));
  return n;
 }
 async function draw(s){
  const ticket=++epoch;current=s;
  mount.replaceChildren(title(s));
  if(!s){
   const n=section("1 · Commit your prediction before seeing the task");
   add(n,paragraph(pred.prediction),area("My initial prediction and reason","prediction-r2"));
   add(n,button("Commit prediction",()=>enter("prediction",{value:document.querySelector("#prediction-r2")?.value})));
   mount.append(n);return;
  }
  if(s.stage===1){
   mount.append(section("Loading first task after prediction commitment…"));
   try{await loadTask()}catch(e){lastError=String(e?.message||e);mount.replaceChildren(title(s));return}
   if(ticket!==epoch)return;
   const n=section("2 · First independent attempt");
   add(n,paragraph("Committed prediction: "+s.prediction.value),paragraph(work.prompt));
   for(const field of work.fields)n.append(choice(field.label,"a-"+field.id,field));
   n.append(area("Explain model choice, assumptions, signs, units and a self-check","a-reason"));
   n.append(button("Commit immutable first attempt",()=>enter("first",{
     fields:Object.fromEntries(work.fields.map(f=>[f.id,document.querySelector("#a-"+f.id)?.value.trim()||""])),
     reasoning:document.querySelector("#a-reason")?.value
   })));
   mount.replaceChildren(title(s),n);return;
  }
  mount.append(section("Loading post-attempt feedback after saved first response…"));
  try{await loadTask();await loadGuide();if(s.stage>=6)await loadBoundary()}
  catch(e){lastError=String(e?.message||e);mount.replaceChildren(title(s));return}
  if(ticket!==epoch)return;
  const blocks=[title(s),snapshot(s)];
  const checked=evaluate(guide.rubric,s.first.fields);
  const wrong=checked.find(x=>x.status!=="MATCH");
  const diagnostic=()=>{
   const n=section("Response-conditioned checks · earliest divergence first");
   add(n,paragraph("Numerical and model selections are mechanically compared with an authored candidate. Free-text reasoning remains ungraded."));
   for(const x of checked){
    const f=work.fields.find(y=>y.id===x.id);
    add(n,paragraph((f?.label||x.id)+" · "+x.status+" · "+x.feedback,x.match?"ok":x.status==="MISSING"?"small":"error"));
   }
   add(n,paragraph(wrong?"Possible first divergence: "+(work.fields.find(x=>x.id===wrong.id)?.label||wrong.id)+". "+wrong.feedback:
    "All checked model/value fields match. This does NOT establish sound reasoning; investigate scientific assumptions and warrant."));
   return n;
  };
  if(s.stage===2){
   const n=section("3 · Optional staged hints, then reconstruction");
   add(n,paragraph("Original first response is already committed. Prior guide exposure: "+s.first.exposure.status));
   for(let i=0;i<s.hints;i++)n.append(paragraph("Hint "+(i+1)+": "+guide.hints[i]));
   if(s.hints<guide.hints.length)n.append(button("Reveal next hint",()=>enter("hint",{max:guide.hints.length})));
   n.append(button("Reveal authored reconstruction",()=>enter("reveal")));
   blocks.push(n);
  }else if(s.stage===3){
   blocks.push(diagnostic());
   const n=section("4 · Diagnose your first divergence");
   add(n,paragraph("Authored reconstruction: "+guide.reconstruct),paragraph("Diagnostic principle: "+guide.diagnosis));
   const opts={id:"divergence",label:"First step to examine",type:"select",
     options:["Choose a step",...work.fields.map(x=>x.id),"reasoning_or_assumptions"]};
   add(n,choice(opts.label,"diagnosis-select",opts),area("My specific cause or justification","diagnosis-reason"));
   n.append(button("Commit diagnosis",()=>enter("diagnosis",{field:document.querySelector("#diagnosis-select")?.value,
       text:document.querySelector("#diagnosis-reason")?.value})));
   blocks.push(n);
  }else if(s.stage===4){
   blocks.push(diagnostic());
   const n=section("5 · Repair with a new reasoned model");
   add(n,paragraph("My diagnosis: "+s.diagnosis.text),paragraph("Repair orientation: "+guide.repair),
     area("My corrected physical reasoning and independent verification","repair-reason"));
   n.append(button("Commit separate repair",()=>enter("repair",{text:document.querySelector("#repair-reason")?.value})));
   blocks.push(n);
  }else if(s.stage===5){
   const n=section("6 · Unseen changed-condition boundary test");
   add(n,paragraph(guide.boundaryPrompt));
   for(const f of guide.boundaryFields)n.append(choice(f.label,"b-"+f.id,f));
   add(n,area("Explain the changed model and check the boundary","boundary-reason"));
   n.append(button("Commit boundary answer before model key",()=>enter("boundary",{
    fields:Object.fromEntries(guide.boundaryFields.map(f=>[f.id,document.querySelector("#b-"+f.id)?.value.trim()||""])),
    reasoning:document.querySelector("#boundary-reason")?.value
   })));
   blocks.push(n);
  }else if(s.stage===6){
   const n=section("Boundary answer committed · model available only now");
   add(n,paragraph("My saved boundary reasoning: "+s.boundary.reasoning));
   n.append(button("Reveal boundary model and structured checks",()=>enter("boundary_reveal")));
   blocks.push(n);
  }else{
   const n=section("Boundary result · authored comparison, not a mastery grade");
   const check=evaluate(boundary.boundaryRubric,s.boundary.fields);
   for(const x of check)n.append(paragraph(x.id+": "+x.status+" · "+x.feedback,x.match?"ok":"error"));
   add(n,paragraph("Worked model: "+boundary.boundaryModel),paragraph("Your original prediction, first calculation and later boundary response remain separately preserved."));
   blocks.push(n);
  }
  mount.replaceChildren(...blocks);
 }
 const onError=e=>{lastError=String(e?.message||e);if(store)draw(store.read()).catch(err=>{mount.append(paragraph("HOLD: "+err.message,"error"))})};
 const onChange=state=>{current=state;if(store)draw(state).catch(onError)};
 store=await openProtectedStore({uid:pred.uid,revision:pred.revision,hash:stateFingerprint,onChange,onError});
 await draw(store.read());
 return store;
}
