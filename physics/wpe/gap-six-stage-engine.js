/* R2 original source-specific physics practice reuses the merged six-stage
 * Core1A→Core1B presentation, student feedback and attempt capture from F01–F03.
 * F01–F03 and the existing C/E lessons remain untouched.
 */
(function(){
  "use strict";
  window.WPEGapJourneys=function(scenarios,config){
    if(!scenarios||!Object.keys(scenarios).length||!config?.storagePrefix)throw Error("No safe journey configuration");
    const stages=["Predict","Attempt","Reconstruct","Diagnose","Repair","Boundary test"];
  const ids=Object.keys(scenarios);
  const prefix=config.storagePrefix;
  const doc=document,svgNS="http://www.w3.org/2000/svg";
  const $=(selector,root=doc)=>root.querySelector(selector);
  const el=(tag,text,className)=>{
    const n=doc.createElement(tag);
    if(text!=null)n.textContent=text;
    if(className)n.className=className;
    return n;
  };
  const add=(parent,tag,text,className)=>{const n=el(tag,text,className);parent.append(n);return n;};
  const svg=(parent,tag,attrs,text)=>{
    const e=doc.createElementNS(svgNS,tag);
    Object.entries(attrs||{}).forEach(([k,v])=>e.setAttribute(k,String(v)));
    if(text!=null)e.textContent=text;
    parent.append(e);return e;
  };
  const svgText=(parent,x,y,t)=>svg(parent,"text",{x,y,fill:"#244e61","font-size":"15","font-weight":"700"},t);
  const svgLine=(parent,x1,y1,x2,y2,color="#719ba8",weight=3)=>svg(parent,"line",{x1,y1,x2,y2,stroke:color,"stroke-width":weight});
  const nice=n=>Number(n.toFixed(3)).toString();
  function blank(id){return {schema:1,id,stage:0,prediction:"",predictionDraft:"",draft:{},first:null,hints:[],checks:[],diagnosis:null,repair:"",boundary:null,helpHistory:[],exposure:"UNASSISTED_UNTIL_FIRST_ATTEMPT"};}
  /* R3: Task A preserves the original R2 key; Task B has a separate key.
   * No state is copied between tasks, including hints, first attempt or repair. */
  const states={},variantOf={};
  const taskKey=id=>id+(variantOf[id]==="T2"?"-T2":"");
  let storageWorks=true;
  for(const id of ids){
    try{variantOf[id]=localStorage.getItem(prefix+"selected:"+id)==="T2"?"T2":"T1";}catch(_){variantOf[id]="T1";}
    for(const key of [id,id+"-T2"]){
      let s=null;
      try{s=JSON.parse(localStorage.getItem(prefix+key)||"null");}catch(_){}
      states[key]=(s&&s.schema===1&&s.id===key&&Number.isInteger(s.stage)&&s.stage>=0&&s.stage<=5&&(s.stage<2||(s.first&&s.first.answers&&typeof s.first.answers.reason==="string")))?s:blank(key);
    }
  }
  function persist(id){const key=taskKey(id);try{localStorage.setItem(prefix+key,JSON.stringify(states[key]));return true;}catch(_){storageWorks=false;$("#save-notice").hidden=false;return false;}}
  let active=ids[0], sourceLink=null;
  function input(parent,id,field,value){
    const group=add(parent,"div",null,"field");
    const label=add(group,"label",field.label);
    const name=id+"-"+field.id;label.htmlFor=name;
    let e;
    if(field.type==="textarea"){e=add(group,"textarea");e.rows=4;}
    else if(field.type==="select"){
      e=add(group,"select");
      for(const c of field.choices)add(e,"option",c).value=c;
    }else{e=add(group,"input");e.type=field.type;e.inputMode="decimal";e.step="any";}
    e.id=name;e.dataset.field=field.id;e.value=value??(field.type==="select"?field.choices[0]:"");
    return e;
  }
  function action(parent,key,label,secondary=false){
    const b=add(parent,"button",label,secondary?"secondary":"primary");b.type="button";b.dataset.action=key;return b;
  }
  function paragraph(parent,text,cls){return add(parent,"p",text,cls);}
  function drawModel(id,val,host,readout){
    host.replaceChildren();
    svg(host,"rect",{x:0,y:0,width:640,height:265,rx:12,fill:"#f4f9fc"});
    scenarios[id].modelView(val,{host,readout,svg,svgText,svgLine,nice});
  }
  function buildGuide(host,id,data){
    const guide=add(host,"section",null,"guide");
    paragraph(guide,"CORE1A · Understand the physics first","mini");
    add(guide,"h2","Why the model works");
    paragraph(guide,data.prerequisites,"prereq");
    paragraph(guide,data.core,"big-idea");
    paragraph(guide,data.guide);
    const figure=add(guide,"figure",null,"visual");
    const scene=svg(figure,"svg",{viewBox:"0 0 640 265",role:"img","aria-label":id+" interactive physics model"});
    const cap=add(figure,"figcaption","Move the control to check how a condition changes the physical model.");
    const ctr=add(guide,"div",null,"visual-controls");
    const label=add(ctr,"label",data.slider.label);label.htmlFor="guide-slider";
    const range=add(ctr,"input");range.id="guide-slider";range.type="range";
    range.min=data.slider.min;range.max=data.slider.max;range.step=data.slider.step;range.value=data.slider.value;
    const output=add(ctr,"output",null,"model-readout");output.htmlFor="guide-slider";
    const redraw=()=>{drawModel(id,Number(range.value),scene,output);cap.textContent="Interactive model · "+data.slider.label+". This is the guided anchor, not the fresh challenge answer.";};
    range.addEventListener("input",redraw);redraw();
    const ol=add(guide,"ol",null,"guide-steps");
    for(const [name,description] of data.guideSteps){
      const li=add(ol,"li");add(li,"strong",name+". ");
      li.append(doc.createTextNode(description));
    }
    if(data.academic){
      const a=add(guide,"section",null,"academic-checkpoint");
      add(a,"h3","Check the model before trusting the formula");
      paragraph(a,data.academic.decision);
      const table=add(a,"dl",null,"academic-observations");
      for(const [name,value] of [
        ["What the picture/control can test",data.academic.observe],
        ["Conditions to verify",data.academic.validity],
        ["Try an extreme or changed case",data.academic.limit]
      ]){add(table,"dt",name);add(table,"dd",value);}
      const source=add(a,"details",null,"source-claim");
      add(source,"summary","Where this original question needs care");
      paragraph(source,data.academic.sourceBoundary);
    }
    const contrast=add(guide,"details",null,"bridge");
    add(contrast,"summary","Compare a tempting wrong approach");
    paragraph(contrast,data.wrong);
    const cond=add(guide,"details",null,"bridge");
    add(cond,"summary","Validity conditions and prerequisite bridge");
    paragraph(cond,data.conditions);
  }
  const numeric=(raw)=>raw==null||String(raw).trim()===""?NaN:Number(raw);
  function feedback(field,value){
    if(field.type==="textarea")return {status:"ungraded",text:"Your written explanation is saved, not automatically judged."};
    if(value==null||String(value).trim()===""||field.type==="select"&&value==="Choose an idea")
      return {status:"missing",text:"No model decision or value entered yet. "+field.mistake};
    const good=field.type==="select"?value===field.expected:Number.isFinite(numeric(value))&&Math.abs(numeric(value)-field.expected)<=field.tol;
    return good?{status:"matches",text:"Your entry matches this authored model. Check that your explanation also justifies it."}
      :{status:"review",text:"Review this step ("+(field.errorKind||"MODEL_OR_CALCULATION")+"): "+field.mistake};
  }
  function drawAssessment(host,fields,answer){
    const summary=add(host,"section",null,"assessment");
    add(summary,"h4","Feedback based on YOUR saved entries");
    paragraph(summary,"These checks compare selected models and numerical entries only. They do not grade explanations or prove mastery.");
    const list=add(summary,"ul");
    let firstIssue=null;
    for(const field of fields.filter(f=>f.type!=="textarea")){
      const result=feedback(field,answer[field.id]);
      if(!firstIssue&&result.status!=="matches")firstIssue={field:field.id,why:result.text};
      const li=add(list,"li");
      add(li,"strong",field.label+": ");
      li.append(doc.createTextNode(result.text));
      li.className=result.status;
    }
    return firstIssue;
  }
  function snapshot(host,s){
    const box=add(host,"section",null,"snapshot");
    add(box,"h4","Your preserved first attempt");
    if(!s.first){paragraph(box,"No first attempt saved.");return;}
    const dl=add(box,"dl");
    for(const [key,value] of Object.entries(s.first.answers)){
      add(dl,"dt",key==="reason"?"Your original explanation":key);
      add(dl,"dd",String(value));
    }
    paragraph(box,"Original prediction: "+s.prediction);
    paragraph(box,"Study cues viewed before first attempt: "+s.first.hintsUsed+". This browser record is practice history, not secure evidence.");
  }
  function stepHeader(host,s){
    const ol=add(host,"ol",null,"step-list");
    stages.forEach((label,i)=>{
      const li=add(ol,"li",(i+1)+". "+label,i===s.stage?"current":i<s.stage?"done":"pending");
      if(i===s.stage)li.setAttribute("aria-current","step");
    });
  }
  function showStage(host,id,d,focus){
    host.replaceChildren();
    const s=states[taskKey(id)];
    stepHeader(host,s);
    const box=add(host,"section",null,"stage-card");
    const title=add(box,"h3",(s.stage+1)+". "+stages[s.stage]);title.tabIndex=-1;
    const acts=add(box,"div",null,"stage-actions");
    if(s.stage===0){
      paragraph(box,"Predict BEFORE seeing the fresh reconstruction. You can write 'I'm not sure' and learn from that.");
      input(box,id,{id:"prediction",label:d.prediction,type:"textarea"},s.predictionDraft);
      action(acts,"prediction","Save prediction → Attempt");
    }else if(s.stage===1){
      paragraph(box,d.challenge,"challenge-prompt");
      paragraph(box,"Decide the physical model and record WHY before the worked solution. You may leave a number blank if unsure; write an explanation.","step-note");
      d.fields.forEach(f=>input(box,id,f,s.draft?.[f.id]));
      const h=add(box,"section",null,"hints");
      add(h,"h4","Optional progressive study cues");
      const ol=add(h,"ol",null,"hint-list");
      s.hints.forEach(i=>add(ol,"li",d.hints[i]));
      const next=action(h,"hint","Show next cue ("+s.hints.length+"/"+d.hints.length+")",true);
      next.disabled=s.hints.length>=d.hints.length;
      action(acts,"attempt","Save first attempt → Reconstruct");
    }else if(s.stage===2){
      paragraph(box,"Your first model is frozen separately. Compare its steps, not only its answer, with this reconstruction.");
      snapshot(box,s);
      drawAssessment(box,d.fields,s.first.answers);
      const worked=add(box,"section",null,"worked");add(worked,"h4","Worked reconstruction · unlocked after the attempt");
      const ol=add(worked,"ol");
      for(const [name,description] of d.worked){const li=add(ol,"li");add(li,"strong",name+". ");li.append(doc.createTextNode(description));}
      const checks=add(box,"fieldset",null,"self-check");add(checks,"legend","Which model steps did you explain?");
      ["I chose the appropriate force/energy owner.","I identified where the physical conditions change.","I justified the signs and equations.","I checked the numerical result and its units."].forEach((label,i)=>{
        const row=add(checks,"label");const c=add(row,"input");c.type="checkbox";c.value=i;c.dataset.check="true";c.checked=s.checks.includes(i);
        row.append(doc.createTextNode(" "+label));
      });
      action(acts,"reconstruct","Compare → Diagnose");
    }else if(s.stage===3){
      paragraph(box,"Start with the FIRST place your model diverged. The suggestion below uses your numerical entries, but only you can judge your written reasoning.");
      const assessment=add(box,"div");
      const issue=drawAssessment(assessment,d.fields,s.first.answers);
      const suggested=issue?issue.field:"explanation";
      paragraph(box,issue?"Possible first divergence: "+suggested+". "+issue.why:"Your numerical entries match the authored model; explain why each equation is valid, not only the arithmetic.","diagnosis-tip");
      const group=add(box,"div",null,"field");const label=add(group,"label","Where will you examine your reasoning first?");label.htmlFor="diagnosis-select";
      const select=add(group,"select");select.id="diagnosis-select";select.dataset.diagnosis="true";
      add(select,"option","Choose a step").value="";
      d.fields.filter(f=>f.type!=="textarea").forEach(f=>add(select,"option",f.label).value=f.id);
      add(select,"option","My written model / assumptions").value="explanation";
      if(s.diagnosis)select.value=s.diagnosis.field;
      input(box,id,{id:"why",label:"What caused the mismatch?",type:"textarea"},s.diagnosis?.why||"");
      action(acts,"diagnose","Save diagnosis → Repair");
    }else if(s.stage===4){
      paragraph(box,"Repair the cause, not just the final number. Keep your first attempt intact.");
      snapshot(box,s);
      const f=d.fields.find(f=>f.id===s.diagnosis?.field);
      paragraph(box,f?f.mistake:"Check conditions, system boundaries and the first unsupported inference.","diagnosis-tip");
      input(box,id,{id:"repair",label:"My corrected reasoning and why I changed it",type:"textarea"},s.repair);
      action(acts,"repair","Save repair → Boundary test");
      const review=add(box,"details",null,"review-model");add(review,"summary","Review the worked model again (optional)");
      d.worked.forEach(([h,description])=>paragraph(review,h+": "+description));
    }else if(s.stage===5){
      paragraph(box,"Make a fresh decision under a changed physical condition. Do not open its solution until you attempt it.");
      paragraph(box,d.boundary,"challenge-prompt");
      snapshot(box,s);
      paragraph(box,"Your revised model: "+s.repair,"repair-record");
      if(s.boundary===null){
        d.boundaryFields.forEach(f=>input(box,id,f,undefined));
        action(acts,"boundary","Commit boundary attempt → Check");
      }else{
        paragraph(box,"Your saved changed-condition explanation: "+(s.boundary.why||""),"step-note");
        drawAssessment(box,d.boundaryFields,s.boundary);
        const worked=add(box,"section",null,"worked");add(worked,"h4","Changed-condition reconstruction");paragraph(worked,d.boundaryCheck);
        action(acts,"history","Review my original attempt and repair",true);
        paragraph(box,"You finished this fresh problem. Return to your source question and make your OWN final reasoning decision.","done");
        if(sourceLink?.lesson===id){
          const a=add(box,"a","Return to "+sourceLink.source+" without showing its answer","return-original");
          a.href=sourceLink.href;
        }
      }
    }
    action(acts,"reset","Restart this journey (clears saved work)",true).classList.add("reset");
    box.append(acts);
    const note=add(box,"p","","status");note.setAttribute("aria-live","polite");note.dataset.notice="true";
    if(focus)title.focus({preventScroll:true});
  }
  function readValues(host){const vals={};host.querySelectorAll("[data-field]").forEach(n=>{vals[n.dataset.field]=n.value;});return vals;}
  function dispatch(host,id,data,event){
    const btn=event.target.closest("button[data-action]");
    if(!btn||!host.contains(btn))return;
    const s=states[taskKey(id)],key=btn.dataset.action;
    const warn=message=>{const n=$("[data-notice]",host);if(n)n.textContent=message;};
    if(key==="reset"){
      if(!window.confirm("Clear this lesson's saved prediction, first attempt, hints, diagnosis and repair?"))return;
      const current=taskKey(id);
      try{localStorage.removeItem(prefix+current)}catch(_){}
      states[current]=blank(current);render();return;
    }
    if(key==="hint"&&s.stage===1&&s.first===null&&s.hints.length<data.hints.length){
      const idx=s.hints.length;s.hints.push(idx);
      s.helpHistory.push({kind:"HINT_"+(idx+1),at:new Date().toISOString()});
      s.exposure="HELPED_BEFORE_FIRST_ATTEMPT";
      // Do NOT render a new field set: hints must not destroy unsaved work.
      const list=$(".hint-list",host);add(list,"li",data.hints[idx]);
      btn.textContent="Show next cue ("+s.hints.length+"/"+data.hints.length+")";
      btn.disabled=s.hints.length===data.hints.length;
      s.draft=readValues(host);
      persist(id);return;
    }
    if(key==="history"&&s.stage===5&&s.boundary!==null){
      const old=$(".history",host);if(old){old.remove();return;}
      const history=add(host,"section",null,"history");snapshot(history,s);
      paragraph(history,"Your separate repair: "+s.repair);return;
    }
    if(key==="prediction"&&s.stage===0){
      const value=$('[data-field="prediction"]',host).value.trim();
      if(!value){warn("Record your prediction—or that you are unsure—before continuing.");return;}
      s.prediction=value;s.predictionDraft="";s.stage=1;
    }else if(key==="attempt"&&s.stage===1&&s.first===null){
      const values=readValues(host);
      if(!values.reason?.trim()){warn("Explain your model (or write 'I'm not sure') before revealing the worked method.");return;}
      if(!values.model||values.model==="Choose an idea"){warn("Choose an initial model, or select 'I'm not sure yet'.");return;}
      s.first={answers:{...values},hintsUsed:s.hints.length,helpHistory:s.helpHistory.slice(),capturedAt:new Date().toISOString()};
      s.draft={};s.stage=2;
    }else if(key==="reconstruct"&&s.stage===2){
      s.checks=[...host.querySelectorAll("[data-check]:checked")].map(x=>Number(x.value));s.stage=3;
    }else if(key==="diagnose"&&s.stage===3){
      const chosen=$("[data-diagnosis]",host).value;
      if(!chosen){warn("Choose the first step to examine.");return;}
      const why=$('[data-field="why"]',host).value.trim();
      if(!why){warn("Explain what caused that difference—even if still unsure.");return;}
      s.diagnosis={field:chosen,why};s.stage=4;
    }else if(key==="repair"&&s.stage===4){
      const value=$('[data-field="repair"]',host).value.trim();
      if(!value){warn("Write how your model changed, or why you remain unsure.");return;}
      s.repair=value;s.stage=5;
    }else if(key==="boundary"&&s.stage===5&&s.boundary===null){
      const values=readValues(host);
      if(data.boundaryFields.some(f=>f.id==="model")&&(!values.model||values.model==="Choose an idea")){
        warn("Choose the changed-condition physical model before seeing the worked check.");return;
      }
      if(!values.why?.trim()){warn("Explain your changed-condition decision before seeing its check.");return;}
      s.boundary={...values,capturedAt:new Date().toISOString()};
    }else{return;}
    persist(id);render(true);
  }
  function updateProgress(){
    const count=ids.filter(x=>states[x].boundary!==null).length;
    $("#progress-label").textContent=count+" of "+ids.length+" fresh boundary challenges completed";
    $("#progress-meter").value=count;
    const extraCount=ids.filter(x=>states[x+"-T2"]?.boundary!==null).length;
    const extra=$("#transfer-progress-label");
    if(extra)extra.textContent=extraCount+" of "+ids.length+" unfamiliar-setting tasks completed";
    for(const id of ids){
      const a=$('[data-journey="'+id+'"]');
      a.classList.toggle("complete",states[id].boundary!==null);
      a.setAttribute("aria-current",id===active?"page":"false");
    }
  }
  function render(focus=false){
    const requested=location.hash.slice(1).toUpperCase();
    active=ids.includes(requested)?requested:ids[0];
    const d=scenarios[active],root=$("#journey-root");root.replaceChildren();
    $("#current-title").textContent=active+" · "+d.short;
    const article=add(root,"article",null,"lesson");
    article.id=active;
    const header=add(article,"header",null,"lesson-title");
    paragraph(header,"NEW FOCUSED REASONING CONSTRUCTION · NOT AN EXAM KEY","mini");
    add(header,"h2",d.title);paragraph(header,d.question);
    const grid=add(article,"div",null,"learning-grid");
    buildGuide(grid,active,d);
    const challenge=add(grid,"section",null,"challenge");
    const selector=add(challenge,"div",null,"variant-switch");
    selector.setAttribute("role","group");
    selector.setAttribute("aria-label","Two different problems with separate saved first attempts");
    for(const [variant,label] of [["T1","Task A · guided topic transfer"],["T2","Task B · unfamiliar setting"]]){
      const b=add(selector,"button",label,variantOf[active]===variant?"selected":"secondary");
      b.type="button";b.dataset.variant=variant;b.setAttribute("aria-pressed",String(variantOf[active]===variant));
      b.addEventListener("click",()=>{
        variantOf[active]=variant;
        try{localStorage.setItem(prefix+"selected:"+active,variant)}catch(_){}
        render(true);
      });
    }
    const problem=variantOf[active]==="T2"?{...d,...d.transfer}:d;
    paragraph(challenge,variantOf[active]==="T2"?problem.label:
      "Task A · First fresh problem (independent record)","mini");
    paragraph(challenge,"CORE1B · A genuinely different problem","mini");
    add(challenge,"h2","Predict → Attempt → Reconstruct → Diagnose → Repair → Boundary test");
    paragraph(challenge,"Task A and Task B have separate first attempts, optional cues, diagnoses, repairs and changed-condition results. Switching tasks cannot reveal the other task's worked answer.");
    const host=add(challenge,"div",null,"stage-root");host.dataset.stageRoot=active;
    host.addEventListener("click",e=>dispatch(host,active,problem,e));
    host.addEventListener("input",()=>{
      const s=states[taskKey(active)];
      if(s.stage===0)s.predictionDraft=$('[data-field="prediction"]',host)?.value||"";
      else if(s.stage===1&&s.first===null)s.draft=readValues(host);
      else return;
      persist(active);
    });
    host.addEventListener("change",()=>{
      const s=states[taskKey(active)];if(s.stage===1&&s.first===null){s.draft=readValues(host);persist(active);}
    });
    showStage(host,active,problem,focus);
    const footer=add(article,"nav",null,"lesson-footer");footer.setAttribute("aria-label","Other focused journeys");
    const n=ids.indexOf(active);
    const prev=add(footer,"a",n?"← Previous new journey":"Learn → Challenge tile");prev.href=n?"#"+ids[n-1]:"learn-challenge.html";
    const next=add(footer,"a",n<ids.length-1?"Next new journey →":"All 74 question learning routes");next.href=n<ids.length-1?"#"+ids[n+1]:"learn-challenge.html#question-routes";
    if(sourceLink?.lesson===active){
      const a=add(footer,"a","Return to "+sourceLink.source,"return-original");a.href=sourceLink.href;
    }
    const caveat=add(article,"details",null,"bridge");
    add(caveat,"summary","Source-question science caution");
    paragraph(caveat,d.sourceCaution||"This is authored practice, not approval of an original examination key.");
    updateProgress();
  }
  async function bindSource(){
    const source=new URLSearchParams(location.search).get("question");
    const box=$("#source-journey"),returnLink=$("#source-return");
    sourceLink=null;returnLink.hidden=true;
    if(!source){box.hidden=true;return;}
    box.hidden=false;$("#source-title").textContent="Your Question Bank route";
    if(!/^[A-Za-z0-9-]{2,64}$/.test(source)){$("#source-message").textContent="Invalid question identifier. No source return inferred.";return;}
    try{
      const [r,q]=await Promise.all([
        fetch(config.coveragePath,{cache:"no-store"}),
        fetch("../../workspace/output/WPE_Core2_Consolidated_20261102/native-candidate/selected_bank.review.json",{cache:"no-store"})
      ]);
      if(!r.ok||!q.ok)throw Error("route data unavailable");
      const map=await r.json(),bank=await q.json();
      if(map.schema!=="wpe-learner-coverage-r1/v1"||!Array.isArray(map.questions)||bank.questions?.length!==74)throw Error("source inventory changed");
      const found=map.questions.find(x=>x.source_id===source);
      if(!found||!bank.questions.some(x=>x.source_id===source&&x.stem_sha256===found.stem_sha256)||found.primary_lesson!==active||found.fit!=="FOCUSED_NEW")
        throw Error("source does not map to this lesson");
      sourceLink={source,lesson:active,href:"../../preview/question-status.html?question="+encodeURIComponent(source)};
      $("#source-title").textContent="Your original question: "+source;
      $("#source-message").textContent="Learn the physical operation with a DIFFERENT example. Then return to "+source+" and test your own solution. Nothing here confirms the question's coaching answer.";
      returnLink.hidden=false;returnLink.href=sourceLink.href;returnLink.textContent="Return to "+source+" without showing its answer";
      render(false);
    }catch(_){$("#source-message").textContent="This question has no verified route to the selected focused journey. No original-question return link is invented.";returnLink.hidden=true;}
  }
  for(const id of ids){
    const a=add($("#journey-navigation"),"a",id+" · "+scenarios[id].short);
    a.href="#"+id;a.dataset.journey=id;
  }
  window.addEventListener("hashchange",()=>{sourceLink=null;render();bindSource();});
  render();bindSource();

  };
})();
