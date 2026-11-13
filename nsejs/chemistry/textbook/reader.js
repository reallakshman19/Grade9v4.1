/* Grade9v4.1 Chemistry Agent B — draft reader, not an academic approval engine.
 * This progressive-disclosure browser UI records a first attempt before showing
 * authored model responses. It does not claim cryptographic secrecy or mastery.
 */
(() => {
  "use strict";
  const ROOT = "../../../curriculum/chemistry/agent-b/";
  const UNITS = ["C08","C09","C10","C11","C12","C13","C14"];
  const $ = selector => document.querySelector(selector);
  const unitSel=$("#unit-select"), taskSel=$("#task-select"), lesson=$("#lesson"), nav=$("#sections");
  const status=$("#notice");
  let book=null, practice=null, currentUnit="C08", section=0, mode="study", digest=null;
  const tag=(name, text, className) => {const node=document.createElement(name);if(text!==undefined)node.textContent=String(text);if(className)node.className=className;return node;};
  const append=(parent,...children) => {for(const child of children)parent.append(child);return parent;};
  const fromQuery=new URLSearchParams(location.search).get("unit");
  if(UNITS.includes(fromQuery))currentUnit=fromQuery;
  for(const u of UNITS){const opt=tag("option",u);opt.value=u;unitSel.append(opt);}
  unitSel.value=currentUnit;
  function alertMessage(message){status.textContent=message;}
  function validBook(data,u){return data&&data.schema==="g9v41-chemistry-textbook-reader/v1"&&data.unit_id===u&&data.academic_status==="DRAFT_ACADEMIC_HOLD"&&Array.isArray(data.sections)&&data.sections.length>0;}
  function validPractice(data,u){return data&&data.schema==="g9v41-chem-core1b-six-stage-cycles/v1"&&data.unit_id===u&&data.release&&data.release.scientific_review==="HOLD"&&Array.isArray(data.cycles);}
  async function load(u){
    status.textContent="";
    lesson.replaceChildren(tag("p","Loading "+u+"…"));
    nav.replaceChildren();
    taskSel.replaceChildren();
    const bookPath=ROOT+"learner/"+u+".reader.v0.1.0.json";
    const practicePath=ROOT+"core1b/"+u+".core1b.v0.1.0.json";
    try{
      const responses=await Promise.all([fetch(bookPath,{cache:"no-store"}),fetch(practicePath,{cache:"no-store"})]);
      if(responses.some(r=>!r.ok))throw new Error("REQUIRED_REVIEW_DATA_UNAVAILABLE");
      const values=await Promise.all(responses.map(r=>r.json()));
      if(!validBook(values[0],u)||!validPractice(values[1],u))throw new Error("UNTRUSTED_CHEMISTRY_PACK");
      const ids=new Set(values[0].sections.map(s=>s.id));
      if(values[1].cycles.length!==values[0].sections.length*3||
         values[1].cycles.some(c=>!ids.has(c.subtopic_ref)||!c.attempt?.first_attempt_must_be_saved_before_feedback||c.source_role!=="AUTHORED_PRACTICE"))
        throw new Error("INCOMPLETE_OR_UNSAFE_RECONSTRUCTION_PACK");
      book=values[0];practice=values[1];currentUnit=u;section=0;
      history.replaceState(null,"","?unit="+u);
      renderNav();render();
    }catch(err){
      book=null;practice=null;lesson.replaceChildren(tag("h2","This author draft is unavailable."),tag("p",err.message));
      alertMessage("No substitute data or answers were fabricated. Academic status remains HOLD.");
    }
  }
  function renderNav(){
    nav.replaceChildren();
    book.sections.forEach((s,i)=>{
      const btn=tag("button",s.id.split(".")[1]+" · "+s.title);
      btn.type="button";btn.setAttribute("aria-current",String(i===section));
      btn.addEventListener("click",()=>{section=i;renderNav();render();});
      nav.append(btn);
    });
  }
  function setMode(value){
    mode=value;$("#show-study").setAttribute("aria-pressed",String(value==="study"));
    $("#show-practice").setAttribute("aria-pressed",String(value==="practice"));
    render();
  }
  function heading(s){
    append(lesson,tag("div",s.id+" · "+s.scope+" · UNREVIEWED","eyebrow"),tag("h2",s.title));
  }
  function render(){
    if(!book||!practice)return;
    const s=book.sections[section];
    lesson.replaceChildren();
    heading(s);
    const cycles=practice.cycles.filter(c=>c.subtopic_ref===s.id);
    taskSel.replaceChildren();
    for(const c of cycles){const opt=tag("option",c.operation+" · "+c.band_proposal+" (candidate)");opt.value=c.cycle_id;taskSel.append(opt);}
    taskSel.disabled=mode!=="practice";
    if(mode==="study")return renderStudy(s);
    const choice=cycles.find(c=>c.cycle_id===taskSel.dataset.desired)||cycles[0];
    taskSel.value=choice.cycle_id;taskSel.dataset.desired=choice.cycle_id;
    renderPractice(choice);
  }
  function renderStudy(s){
    append(lesson,tag("h3","Start with the scientific phenomenon"),tag("p",s.hook,"hook"));
    append(lesson,tag("h3","Construct the scientific explanation"));
    for(const p of s.teaching){lesson.append(tag("p",p));}
    for(const src of s.figures||[]){const fig=tag("img");fig.className="figure";fig.src=src;fig.alt="Original authored Chemistry diagram for "+s.title;fig.loading="lazy";lesson.append(fig);}
    const example=tag("section",undefined,"note");append(example,tag("h3","Completed worked conceptual construction"),tag("p",s.worked));lesson.append(example);
    append(lesson,tag("h3","Plausible wrong path and repair"),tag("p",s.misconception));
    append(lesson,tag("h3","Boundary or independent check"),tag("p",s.boundary));
    const bottom=tag("section",undefined,"note");append(bottom,tag("p","Next: reconstruct the ideas independently using the three protected Core1B tasks. These are authored practice, not official NSEJS source questions."));lesson.append(bottom);
  }
  async function taskRevision(c){
    const raw=JSON.stringify({cycle:c.cycle_id,prompt:c.attempt.prompt,model:c.attempt.post_commit_closure.model_response,boundary:c.boundary_test.answer});
    if(!crypto||!crypto.subtle)throw new Error("NO_SECURE_REVISION_HASH");
    const buf=await crypto.subtle.digest("SHA-256",new TextEncoder().encode(raw));
    return Array.from(new Uint8Array(buf),x=>x.toString(16).padStart(2,"0")).join("");
  }
  function storageRead(key){
    try{
      const raw=localStorage.getItem(key);
      return {ok:true,value:raw?JSON.parse(raw):null};
    }catch(e){return {ok:false,value:null};}
  }
  function storageWrite(key,value){
    try{
      const raw=JSON.stringify(value);
      localStorage.setItem(key,raw);
      return localStorage.getItem(key)===raw;
    }catch(e){return false;}
  }
  function stage(name,content){
    const panel=tag("section",undefined,"stage");panel.append(tag("h3",name));
    if(content)panel.append(tag("p",content));
    lesson.append(panel);return panel;
  }
  function paragraph(parent,text){parent.append(tag("p",text));}
  async function renderPractice(c){
    alertMessage("");
    const taskKey="g9chem:attempt:"+c.cycle_id;
    const helpKey="g9chem:help:"+c.cycle_id;
    const main=lesson;
    try{digest=await taskRevision(c);}
    catch(e){alertMessage("Attempt protection unavailable: "+e.message);return;}
    const st=storageRead(taskKey);
    if(!st.ok){
      stage("Storage not available","Progressive answer reveal is disabled because first-attempt persistence cannot be verified. Enable local storage to use this review-only self-tutor.");
      alertMessage("STORAGE_UNAVAILABLE · No attempt can be certified or model response revealed.");
      return;
    }
    const saved=st.value;
    if(saved&&saved.revision!==digest){
      stage("Stored attempt belongs to a different content revision","This task has changed since the original attempt. The previous attempt is preserved and its old solution is not reinterpreted as a new result. Start with a clean controlled profile for this revised authored task.");
      alertMessage("STALE_REVISION_HOLD · Existing attempt preserved; no answer revealed.");
      return;
    }
    paragraph(main,"Core1B — "+c.operation+" · candidate "+c.band_proposal+" · source: AUTHORED PRACTICE. The model answer only becomes visible after a saved original attempt.");
    const p=stage("Stage 1 — Predict",c.predict.prompt);
    const a=stage("Stage 2 — Independent attempt",c.attempt.prompt);
    const pred=tag("textarea");pred.id="prediction-answer";pred.setAttribute("aria-label","Initial prediction");pred.placeholder="Write a prediction and the condition it depends on…";
    const attempt=tag("textarea");attempt.id="original-answer";attempt.setAttribute("aria-label","Original independent reasoning");attempt.placeholder="Construct your complete explanation, model or representation…";
    p.append(tag("label","Your prediction","write"),pred);
    a.append(tag("label","Your original reasoning","write"),attempt);
    if(saved){
      pred.value=saved.prediction;attempt.value=saved.attempt;pred.readOnly=true;attempt.readOnly=true;
      const note=tag("div","Original response saved against this exact task revision. It cannot be overwritten by hints, feedback or refresh.","saved");a.append(note);
    }else{
      const helper=tag("div",undefined,"task-actions");
      const expos=storageRead(helpKey);let exposures=expos.ok&&expos.value&&expos.value.revision===digest?expos.value.levels:[];
      for(const hint of c.attempt.hints){
        const b=tag("button","Reveal "+hint.id+" (support exposure)");b.type="button";
        b.addEventListener("click",()=>{
          if(b.dataset.shown)return;
          b.dataset.shown="true";b.disabled=true;
          helper.append(tag("p",hint.id+": "+hint.text,"small"));
          exposures=[...new Set([...exposures,hint.id])];
          if(!storageWrite(helpKey,{revision:digest,levels:exposures})){alertMessage("HINT_EXPOSURE_NOT_PERSISTED · Independent status cannot be claimed.");}
        });helper.append(b);
      }
      a.append(helper);
      const submit=tag("button","Commit original answer","primary");submit.type="button";submit.id="commit-attempt";
      submit.addEventListener("click",()=>{
        if(pred.value.trim().length<8||attempt.value.trim().length<20){alertMessage("Write a substantive prediction and independent explanation before committing.");return;}
        const help=storageRead(helpKey);const levels=help.ok&&help.value&&help.value.revision===digest?help.value.levels:exposures;
        const record={revision:digest,cycle_id:c.cycle_id,prediction:pred.value,attempt:attempt.value,help_exposure:levels,recorded_at:new Date().toISOString(),source_role:"AUTHORED_PRACTICE"};
        if(!storageWrite(taskKey,record)){alertMessage("STORAGE_UNAVAILABLE · Original response could not be saved. Model response remains hidden.");return;}
        render();
      });a.append(submit);
      return;
    }
    const r=stage("Stage 3 — Reconstruct","Compare your written construction with the model after—not before—your original attempt.");
    for(const x of c.reconstruct.asks){append(r,tag("h4",x.ask),tag("p",x.model_response));}
    const model=tag("div",undefined,"note");append(model,tag("h4","Model response (post-commit)"),tag("p",c.attempt.post_commit_closure.model_response));r.append(model);
    const diag=stage("Stage 4 — Diagnose","Identify the most important difference between your original explanation and the model, not just a missing word.");
    paragraph(diag,c.diagnose.diagnostic_prompt);diag.append(tag("p","Diagnostic: "+c.diagnose.wrong_idea,"small"));
    const repair=stage("Stage 5 — Repair",c.repair.action);
    paragraph(repair,c.repair.explanation);
    const bound=stage("Stage 6 — Changed-condition boundary test",c.boundary_test.prompt);
    const bResponse=tag("textarea");bResponse.id="boundary-answer";bResponse.setAttribute("aria-label","Your changed-condition answer");bResponse.placeholder="Apply the model to the new condition before revealing the answer…";bound.append(bResponse);
    const button=tag("button","Reveal boundary model response");button.type="button";button.id="reveal-boundary";
    button.addEventListener("click",()=>{
      if(bResponse.value.trim().length<12){alertMessage("Write your changed-condition reasoning first.");return;}
      const record=storageRead(taskKey);
      if(!record.ok||!record.value||record.value.revision!==digest){alertMessage("STORAGE_UNAVAILABLE · Revision check failed.");return;}
      if(!storageWrite(taskKey,{...record.value,boundary_response:bResponse.value})){alertMessage("STORAGE_UNAVAILABLE · Boundary response not persisted.");return;}
      paragraph(bound,"Model response: "+c.boundary_test.answer);button.disabled=true;
    });bound.append(button);
  }
  unitSel.addEventListener("change",()=>{taskSel.dataset.desired="";load(unitSel.value);});
  taskSel.addEventListener("change",()=>{taskSel.dataset.desired=taskSel.value;render();});
  $("#show-study").addEventListener("click",()=>setMode("study"));
  $("#show-practice").addEventListener("click",()=>setMode("practice"));
  load(currentUnit);
})();
