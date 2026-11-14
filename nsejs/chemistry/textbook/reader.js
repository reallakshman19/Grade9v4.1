/* Grade9v4.1 Chemistry — P00 native reader integration R1.
 * Author candidates, not academic approval, official NSEJS questions, or exam security.
 * B02 unreviewed S1/S2/S3 assets are POST-COMMIT ONLY until R02 independently
 * qualifies each stage. First attempts and exposures are distinct immutable records.
 */
(() => {
  "use strict";
  const ROOT = "../../../curriculum/chemistry/agent-b/";
  const REPO_ROOT = "../../../";
  const UNITS = ["C08","C09","C10","C11","C12","C13","C14"];
  const B02 = new Set(["C10","C11"]);
  const $ = selector => document.querySelector(selector);
  const unitSel = $("#unit-select"), taskSel = $("#task-select");
  const lesson = $("#lesson"), nav = $("#sections"), notice = $("#notice");
  const view = {book:null,practice:null,supplemental:[],visuals:null,visualById:new Map(),
    unit:"C08",section:0,mode:"study",taskId:"",revision:"",generation:0};
  let loadGeneration=0, renderGeneration=0;
  const objectUrls=[];
  const initialParams=new URLSearchParams(location.search);
  const requestedUnit=initialParams.get("unit");
  const requestedSubtopic=initialParams.get("subtopic");
  const requestedTask=initialParams.get("task");
  const requestedMode=initialParams.get("mode");
  const sourceContext=initialParams.get("source");
  const returnRaw=initialParams.get("return");
  const tag=(name,value,cls)=>{
    const el=document.createElement(name);
    if(value!==undefined)el.textContent=String(value);
    if(cls)el.className=cls;
    return el;
  };
  const add=(parent,...children)=>{for(const child of children)parent.append(child);return parent;};
  const message=text=>{notice.textContent=text;};
  const unitTasks=()=>[...(view.practice?.cycles||[]),...view.supplemental];
  const idOf=task=>task.cycle_id||task.task_id;
  const subtopicOf=task=>task.subtopic_ref||task.subtopic_id;
  const isSupplemental=task=>!!task.task_id;
  const currentSection=()=>view.book?.sections?.[view.section];
  const tasksForSection=()=>unitTasks().filter(t=>subtopicOf(t)===currentSection()?.id);
  const revisionKey=(type,task)=>"g9chem:"+type+":v2:"+idOf(task)+":"+view.revision;
  const text=(parent,value,cls)=>add(parent,tag("p",value,cls));
  const block=(title,detail)=>{
    const section=tag("section",undefined,"stage");add(section,tag("h3",title));
    if(detail)text(section,detail);
    add(lesson,section);
    return section;
  };
  const button=(label,handler,cls)=>{
    const b=tag("button",label,cls);b.type="button";b.addEventListener("click",handler);return b;
  };
  const isValidTaskId=id=>typeof id==="string"&&/^[A-Z0-9][A-Z0-9-]{4,115}$/.test(id);
  const isValidUnit=u=>UNITS.includes(u);
  const safeReturn=(()=>{
    if(!returnRaw||returnRaw.length>500||/[\\]/.test(returnRaw))return null;
    try {
      const url=new URL(returnRaw,location.href);
      const chemistryRoot=new URL("../",location.href).pathname;
      if(url.origin!==location.origin||!url.pathname.startsWith(chemistryRoot)
        ||!url.pathname.endsWith(".html")||url.username||url.password)return null;
      return url.href;
    }catch(e){return null;}
  })();
  function updateSourceReturn(){
    const target=$("#source-return");
    if(!target)return;
    target.replaceChildren();
    if(!safeReturn)return;
    const a=tag("a","Return to previous Chemistry resource (supplied route)");
    a.href=safeReturn;
    target.append(a);
    if(sourceContext&&/^[A-Za-z0-9_.-]{1,100}$/.test(sourceContext)){
      target.append(tag("span"," · Context: "+sourceContext+" (not an admitted NSEJS question)","small"));
    }
  }
  function updateUrl(push=false){
    const query=new URLSearchParams();
    query.set("unit",view.unit);
    if(currentSection())query.set("subtopic",currentSection().id);
    query.set("mode",view.mode);
    if(view.mode==="practice"&&view.taskId)query.set("task",view.taskId);
    if(sourceContext&&/^[A-Za-z0-9_.-]{1,100}$/.test(sourceContext))query.set("source",sourceContext);
    if(safeReturn)query.set("return",returnRaw);
    const target=location.pathname+"?"+query.toString();
    const current=location.pathname+location.search;
    if(target!==current){
      if(push)history.pushState(null,"",target);
      else history.replaceState(null,"",target);
    }
  }
  async function digestHex(algorithm,bytes){
    if(!globalThis.crypto?.subtle)throw new Error("NO_SECURE_REVISION_HASH");
    const bytesOut=await crypto.subtle.digest(algorithm,bytes);
    return Array.from(new Uint8Array(bytesOut),x=>x.toString(16).padStart(2,"0")).join("");
  }
  async function revisionFor(book,practice,supplemental,visuals){
    // Include every field of Core1A, Core1B, supplemental and visual path/blob
    // manifest. Conservative unit-level revision: any change invalidates
    // previous attempts, rather than silently accepting an old task answer.
    const canonical=JSON.stringify({schema:"g9chem-full-unit-v2",book,practice,
      supplemental:supplemental||[],visuals:visuals||null});
    return digestHex("SHA-256",new TextEncoder().encode(canonical));
  }
  function storageRead(key){
    try {const raw=localStorage.getItem(key);return {ok:true,value:raw?JSON.parse(raw):null};}
    catch(e){return {ok:false,value:null};}
  }
  function storageWrite(key,value){
    try {const raw=JSON.stringify(value);localStorage.setItem(key,raw);return localStorage.getItem(key)===raw;}
    catch(e){return false;}
  }
  function cleanObjectUrls(){
    for(const x of objectUrls.splice(0))URL.revokeObjectURL(x);
  }
  function validBook(data,unit){
    return data&&data.schema==="g9v41-chemistry-textbook-reader/v1"
      &&data.unit_id===unit&&data.academic_status==="DRAFT_ACADEMIC_HOLD"
      &&Array.isArray(data.sections)&&data.sections.length>0;
  }
  function validPractice(data,unit,sectionIds){
    if(!data||data.schema!=="g9v41-chem-core1b-six-stage-cycles/v1"||
      data.unit_id!==unit||data.release?.scientific_review!=="HOLD"||
      !Array.isArray(data.cycles)||data.cycles.length!==sectionIds.size*3)return false;
    const idSet=new Set();
    const perSection=new Map();
    for(const c of data.cycles){
      if(!sectionIds.has(c.subtopic_ref)||!isValidTaskId(c.cycle_id)
        ||idSet.has(c.cycle_id)||c.source_role!=="AUTHORED_PRACTICE"
        ||!c.attempt?.first_attempt_must_be_saved_before_feedback
        ||!Array.isArray(c.attempt.hints)||c.attempt.hints.length!==3)return false;
      idSet.add(c.cycle_id);
      perSection.set(c.subtopic_ref,(perSection.get(c.subtopic_ref)||0)+1);
    }
    return [...sectionIds].every(id=>perSection.get(id)===3);
  }
  function validSupplemental(data,unit,sectionIds,existingIds){
    if(!data||!Array.isArray(data.records)||data.records.length!==8
      ||data.counts?.tasks!==8||data.counts?.native_cycles_added!==0)return false;
    const matching=data.records.filter(r=>sectionIds.has(r.subtopic_id));
    if(matching.length!==4)return false;
    const allIds=new Set(data.records.map(r=>r.task_id));
    if(allIds.size!==8)return false;
    return matching.every(r=>isValidTaskId(r.task_id)&&!existingIds.has(r.task_id)
      &&r.source_role==="AUTHORED_TRANSFER_NOT_ORIGINAL_EXAM"
      &&r.source_admission==="HOLD"&&r.academic_status==="HOLD"
      &&r.attempt?.first_attempt_must_be_saved_before_feedback);
  }
  function validVisualManifest(data,unit,taskIds){
    if(!data||data.counts?.tasks!==47||data.counts?.stages!==141
       ||data.counts?.qualified!==0||!Array.isArray(data.records)
       ||data.records.length!==47)return false;
    const seen=new Set(),paths=new Set();
    for(const row of data.records){
      if(!isValidTaskId(row.task_id)||seen.has(row.task_id)
         ||row.status!=="AUTHOR_VISUAL_CANDIDATE_RUNTIME_HOLD"
         ||!Array.isArray(row.stages)||row.stages.length!==3)return false;
      seen.add(row.task_id);
      for(let i=0;i<3;i++){
        const s=row.stages[i];
        if(s.id!=="S"+(i+1)||!["CLARIFY","CORRELATE","OPEN_THE_WAY"].includes(s.role)
           ||s.independent_status!=="UNREVIEWED"
           ||s.exposure!=="P00_SEQUENCED_OPTIONAL_PRE_ATTEMPT_HOLD"
           ||typeof s.git_blob!=="string"||!/^[a-f0-9]{40}$/.test(s.git_blob)
           ||typeof s.path!=="string"
           ||!/^curriculum\/chemistry\/agent-b\/figures\/b02-stages\/[a-z0-9-]+\.svg$/.test(s.path)
           ||paths.has(s.path))return false;
        paths.add(s.path);
      }
    }
    if(paths.size!==141)return false;
    const unitRows=data.records.filter(x=>x.task_id.startsWith("CORE1B-"+unit+"-"));
    // Supplemental IDs do not encode unit; the task set is authoritative.
    return [...taskIds].every(id=>seen.has(id))&&unitRows.length===({C10:18,C11:21}[unit]);
  }
  async function fetchJson(url){
    const response=await fetch(url,{cache:"no-store"});
    if(!response.ok)throw new Error("REQUIRED_REVIEW_DATA_UNAVAILABLE");
    return response.json();
  }
  async function load(unit,opts={}){
    const gen=++loadGeneration;
    ++renderGeneration;
    cleanObjectUrls();
    lesson.replaceChildren(tag("p","Loading "+unit+" author-draft Chemistry…"));
    nav.replaceChildren();taskSel.replaceChildren();message("");
    if(!isValidUnit(unit)){fail("INVALID_UNIT_ROUTE");return;}
    const extra=B02.has(unit);
    try{
      const urls=[
        ROOT+"learner/"+unit+".reader.v0.1.0.json",
        ROOT+"core1b/"+unit+".core1b.v0.1.0.json"
      ];
      if(extra)urls.push(ROOT+"qrt/B02-core2-targeted-transfers.v0.5.0.json",
                         ROOT+"qrt/B02-C10-C11-staged-visuals.v0.7.0.json");
      const values=await Promise.all(urls.map(fetchJson));
      if(gen!==loadGeneration)return;
      const [book,practice,sup,visuals]=values;
      const ids=new Set(book?.sections?.map(x=>x.id)||[]);
      if(!validBook(book,unit)||ids.size!==book.sections.length
         ||!validPractice(practice,unit,ids))throw new Error("UNTRUSTED_CHEMISTRY_PACK");
      const nativeIds=new Set(practice.cycles.map(x=>x.cycle_id));
      const supplemental=extra?(sup?.records||[]).filter(x=>ids.has(x.subtopic_id)):[];
      if(extra&&(!validSupplemental(sup,unit,ids,nativeIds)
                ||!validVisualManifest(visuals,unit,new Set([...nativeIds,
                   ...supplemental.map(x=>x.task_id)]))))
        throw new Error("B02_STAGE_OR_TASK_JOIN_HOLD");
      const revision=await revisionFor(book,practice,supplemental,extra?visuals:null);
      if(gen!==loadGeneration)return;
      const sectionIdx=opts.subtopic?book.sections.findIndex(x=>x.id===opts.subtopic):0;
      if(sectionIdx<0)throw new Error("UNKNOWN_SUBTOPIC_HOLD");
      let taskId="";
      if(opts.task){
        const all=[...practice.cycles,...supplemental];
        const task=all.find(x=>idOf(x)===opts.task);
        if(!task)throw new Error("UNKNOWN_TASK_HOLD");
        if(opts.subtopic&&subtopicOf(task)!==opts.subtopic)throw new Error("TASK_SUBTOPIC_MISMATCH");
        if(!opts.subtopic){
          const idx=book.sections.findIndex(x=>x.id===subtopicOf(task));
          if(idx<0)throw new Error("TASK_SUBTOPIC_MISMATCH");
          opts.subtopic=book.sections[idx].id;
        }
        taskId=opts.task;
      }
      view.book=book;view.practice=practice;
      view.supplemental=supplemental;view.visuals=extra?visuals:null;
      view.visualById=new Map(extra?visuals.records.map(x=>[x.task_id,x]):[]);
      view.revision=revision;view.unit=unit;
      view.section=opts.subtopic?book.sections.findIndex(x=>x.id===opts.subtopic):sectionIdx;
      view.mode=opts.mode==="practice"||(opts.task&&opts.mode!=="study")
        ?"practice":"study";
      view.taskId=taskId;
      unitSel.value=unit;
      renderNavigation();render(!!opts.push);
      if(opts.initial&&returnRaw&&!safeReturn)message("UNSAFE_SOURCE_RETURN_IGNORED · Only same-site Chemistry HTML routes are permitted.");
    }catch(e){
      if(gen!==loadGeneration)return;
      fail(e.message||"REQUIRED_DATA_UNAVAILABLE");
    }
  }
  function fail(code){
    view.book=null;view.practice=null;view.supplemental=[];view.visualById.clear();
    lesson.replaceChildren(tag("h2","This author draft is unavailable."),tag("p",code));
    message("FAIL_CLOSED · No substitute task, answer, or academic qualification was fabricated.");
  }
  function renderNavigation(){
    nav.replaceChildren();
    for(const [i,s] of view.book.sections.entries()){
      const b=button(s.id.split(".")[1]+" · "+s.title,()=>{
        view.section=i;view.taskId="";renderNavigation();render(true);
      });
      b.setAttribute("aria-current",String(i===view.section));
      nav.append(b);
    }
  }
  function heading(section){
    add(lesson,tag("div",section.id+" · "+section.scope+" · UNREVIEWED","eyebrow"),
      tag("h2",section.title));
  }
  function render(push=false){
    if(!view.book||!view.practice)return;
    ++renderGeneration;cleanObjectUrls();
    const section=currentSection();
    if(!section){fail("UNKNOWN_SUBTOPIC_HOLD");return;}
    lesson.replaceChildren();heading(section);
    const tasks=tasksForSection();
    taskSel.replaceChildren();
    for(const task of tasks){
      const label=(isSupplemental(task)?"Supplemental · ":"")+
        (task.operation||task.kind)+" · "+(task.band_proposal||task.band_author)+" (candidate)";
      const option=tag("option",label);option.value=idOf(task);taskSel.append(option);
    }
    taskSel.disabled=view.mode!=="practice";
    $("#show-study").setAttribute("aria-pressed",String(view.mode==="study"));
    $("#show-practice").setAttribute("aria-pressed",String(view.mode==="practice"));
    if(view.mode==="study"){
      view.taskId="";renderStudy(section);
    }else{
      const selected=tasks.find(x=>idOf(x)===view.taskId)||tasks[0];
      if(!selected){fail("NO_TASK_FOR_SUBTOPIC");return;}
      view.taskId=idOf(selected);taskSel.value=view.taskId;
      renderPractice(selected,renderGeneration);
    }
    updateUrl(push);updateSourceReturn();
  }
  function renderStudy(section){
    add(lesson,tag("h3","Start with the scientific phenomenon"),tag("p",section.hook,"hook"),
      tag("h3","Construct the scientific explanation"));
    for(const paragraph of section.teaching)text(lesson,paragraph);
    for(const src of section.figures||[]){
      const fig=tag("img");fig.className="figure";fig.src=src;
      fig.alt="Original authored Chemistry explanatory diagram: "+section.title;
      fig.loading="lazy";add(lesson,fig);
    }
    const example=block("Completed worked conceptual construction",section.worked);
    example.classList.add("note");
    add(lesson,tag("h3","Plausible wrong path and repair"),tag("p",section.misconception),
      tag("h3","Boundary or independent check"),tag("p",section.boundary));
    block("Read, then reconstruct independently",
      "Three native Core1B tasks per subtopic are authored practice. C10/C11 also have "+
      "held supplemental tasks and post-commit-only unreviewed S1/S2/S3 visual candidates. "+
      "None is an admitted original NSEJS question.");
  }
  function storeStageExposure(task,stageId,revision){
    const key=revisionKey("stage-exposure",task);
    const old=storageRead(key);
    if(!old.ok)return false;
    const levels=old.value?.levels||[];
    return storageWrite(key,{revision,levels:[...new Set([...levels,stageId])],
      status:"POST_COMMIT_AUTHOR_VISUAL_UNREVIEWED",source_role:"AUTHORED_PRACTICE"});
  }
  async function verifiedSvgUrl(asset){
    const res=await fetch(REPO_ROOT+asset.path,{cache:"no-store"});
    if(!res.ok)throw new Error("STAGE_ASSET_FETCH_HOLD");
    const bytes=new Uint8Array(await res.arrayBuffer());
    const head=new TextEncoder().encode("blob "+bytes.length+"\0");
    const blob=new Uint8Array(head.length+bytes.length);
    blob.set(head);blob.set(bytes,head.length);
    if((await digestHex("SHA-1",blob))!==asset.git_blob)throw new Error("STAGE_BLOB_MISMATCH_HOLD");
    const svg=new TextDecoder("utf-8",{fatal:true}).decode(bytes);
    if(!/<svg[\s>]/i.test(svg)||!/<title[\s>]/i.test(svg)||!/<desc[\s>]/i.test(svg)
       ||/<(?:script|foreignObject|iframe|image)\b/i.test(svg)
       ||/\bon[a-z]+\s*=/i.test(svg)
       ||/\b(?:href|xlink:href)\s*=/i.test(svg))throw new Error("UNSAFE_SVG_HOLD");
    const xml=new DOMParser().parseFromString(svg,"image/svg+xml");
    if(xml.querySelector("parsererror")||xml.documentElement.localName!=="svg")
      throw new Error("INVALID_SVG_HOLD");
    const url=URL.createObjectURL(new Blob([bytes],{type:"image/svg+xml"}));
    objectUrls.push(url);
    return url;
  }
  function visualStages(task,renderEpoch){
    const row=view.visualById.get(idOf(task));
    if(!row)return;
    const group=block("S1–S3 candidate visual support (post-commit only)");
    text(group,"These 3 unreviewed SVGs are optional REVIEW visuals, not approved pre-attempt hints. "+
      "All S1/S2/S3 exposure is logged separately. The first response was already committed.","small");
    const actions=tag("div",undefined,"task-actions");
    for(const asset of row.stages){
      const output=tag("div",undefined,"visual-result");
      const b=button("Inspect "+asset.id+" · "+asset.role+" (unreviewed)",async()=>{
        if(b.disabled)return;
        b.disabled=true;
        if(renderEpoch!==renderGeneration)return;
        const saved=storageRead(revisionKey("attempt",task));
        if(!saved.ok||saved.value?.revision!==view.revision){
          message("VISUAL_REVEAL_HELD · Commit a first response for the exact revision.");
          b.disabled=false;return;
        }
        try {
          const uri=await verifiedSvgUrl(asset);
          if(renderEpoch!==renderGeneration)return;
          if(!storeStageExposure(task,asset.id,view.revision)){
            message("STAGE_EXPOSURE_NOT_PERSISTED · Visual remains concealed.");
            b.disabled=false;return;
          }
          const figure=tag("figure",undefined,"stage-figure");
          const img=tag("img");img.src=uri;
          img.alt=asset.id+" "+asset.role+": "+asset.candidate_visual_job+
            ". Unreviewed authored visual; scientific and W-protection approval pending.";
          img.loading="eager";img.decoding="async";
          add(figure,img,tag("figcaption",
            asset.id+" · "+asset.role+" · UNREVIEWED · post-commit exposure recorded",
            "small"));
          output.replaceChildren(figure);b.textContent=asset.id+" inspected";
        }catch(error){
          message((error.message||"STAGE_ASSET_HOLD")+" · No unverified image displayed.");
          b.disabled=false;
        }
      });
      actions.append(b,output);
    }
    group.append(actions);
  }
  function renderPractice(task,renderEpoch){
    const id=idOf(task),revision=view.revision;
    const attemptKey=revisionKey("attempt",task);
    const savedResult=storageRead(attemptKey);
    if(!savedResult.ok){
      block("Storage unavailable","First attempts cannot be certified; model answers and S1–S3 candidate "+
        "visuals remain concealed. Enable local storage for this review-only self-tutor.");
      message("STORAGE_UNAVAILABLE · Fail closed.");
      return;
    }
    const saved=savedResult.value;
    const legacy=storageRead("g9chem:attempt:"+id);
    let previousV2=false;
    try{
      const prefix="g9chem:attempt:v2:"+id+":";
      for(let i=0;i<localStorage.length;i++){
        const key=localStorage.key(i);
        if(key&&key.startsWith(prefix)&&key!==attemptKey)previousV2=true;
      }
    }catch(e){
      // Current persistent storage status has already been checked above.
    }
    if(previousV2&&!saved){
      block("STALE_REVISION_HOLD — earlier first response retained",
        "This lesson or an associated hint, task or SVG source changed. Its prior "+
        "response remains stored with its old digest and is not silently treated "+
        "as an attempt on the new revision. You may commit a new independent answer.");
    }
    if(legacy.ok&&legacy.value&&!saved){
      block("Earlier attempt preserved","A legacy attempt for this task exists under an earlier "+
        "partial-revision key. It has NOT been imported or reinterpreted; a new independent "+
        "attempt will be saved with the complete unit-content digest.");
    }
    text(lesson,"Core1B · "+(task.operation||task.kind)+" · proposed "+
      (task.band_proposal||task.band_author)+" · AUTHOR DRAFT. "+
      "The canonical full-unit revision binds textbook, native/supplemental tasks, and staged asset pins.");
    const predict=block("Stage 1 — Predict",task.predict?.prompt||"State a testable prediction.");
    const attemptSection=block("Stage 2 — Independent attempt",task.attempt.prompt);
    const prediction=tag("textarea"),answer=tag("textarea");
    prediction.id="prediction-answer";prediction.setAttribute("aria-label","Initial prediction");
    prediction.placeholder="State your prediction and the condition behind it.";
    answer.id="original-answer";answer.setAttribute("aria-label","Original independent reasoning");
    answer.placeholder="Build your own explanation, model or representation.";
    add(predict,tag("label","Your prediction","write"),prediction);
    add(attemptSection,tag("label","Your first complete reasoning","write"),answer);
    if(!saved){
      const helper=tag("div",undefined,"task-actions");
      const helpKey=revisionKey("help",task);
      const old=storageRead(helpKey);
      if(!old.ok){block("Help exposure storage unavailable",
        "First-attempt and H1–H3 exposure cannot be persisted. Help and model responses are held.");
        message("STORAGE_UNAVAILABLE · Help exposure not certifiable.");
        return;}
      const seen=new Set(old.value?.revision===revision?old.value.levels||[]:[]);
      const hints=task.attempt.hints||[];
      const helpLabels=["H1","H2","H3"];
      hints.forEach((hint,index)=>{
        const label=helpLabels[index],shown=seen.has(label);
        const detail=tag("p",shown?label+": "+hint.text:"","small");
        const btn=button(shown?label+" already exposed":"Reveal "+label+" (assisted, logged)",()=>{
          if(btn.disabled)return;
          if(index>0&&!seen.has(helpLabels[index-1])){
            message("HELP_ORDER_HOLD · Reveal earlier support first.");return;
          }
          const next=[...new Set([...seen,label])];
          if(!storageWrite(helpKey,{revision,levels:next,status:"AUTHOR_HINT_ASSISTED"})){
            message("HINT_EXPOSURE_NOT_PERSISTED · Help remains concealed.");return;
          }
          seen.add(label);detail.textContent=label+": "+hint.text;
          btn.disabled=true;btn.textContent=label+" exposed";
          message("ASSISTED_ATTEMPT · Help exposure recorded. Independent unaided status is not claimed.");
        });
        if(shown)btn.disabled=true;
        helper.append(btn,detail);
      });
      attemptSection.append(helper);
      const commit=button("Commit original answer",()=>{
        if(renderEpoch!==renderGeneration)return;
        if(prediction.value.trim().length<8||answer.value.trim().length<20){
          message("Enter a substantive prediction and explanation before committing.");return;
        }
        const help=storageRead(helpKey);
        if(!help.ok){message("STORAGE_UNAVAILABLE · Help record cannot be verified.");return;}
        const levels=help.value?.revision===revision?help.value.levels||[]:[];
        const record={revision,id,prediction:prediction.value,attempt:answer.value,
          help_exposure:levels,recorded_at:new Date().toISOString(),
          source_role:isSupplemental(task)?"AUTHORED_TRANSFER_NOT_ORIGINAL_EXAM":"AUTHORED_PRACTICE",
          learner_status:levels.length?"ASSISTED":"FIRST_ATTEMPT_UNAIDED"};
        if(!storageWrite(attemptKey,record)){
          message("STORAGE_UNAVAILABLE · Answer not saved. Model solution remains concealed.");return;
        }
        render();
      },"primary");
      commit.id="commit-attempt";attemptSection.append(commit);
      return;
    }
    prediction.value=saved.prediction;answer.value=saved.attempt;
    prediction.readOnly=true;answer.readOnly=true;
    add(attemptSection,tag("div","First response preserved for this full content revision; "+
      "it cannot be overwritten by hint, visual or boundary review.","saved"));
    if(saved.help_exposure?.length)
      text(attemptSection,"Assisted attempt: "+saved.help_exposure.join(", ")+
        " were exposed before the first response.","small");
    const reconstruct=block("Stage 3 — Reconstruct",
      "Compare your first reasoning with this worked reconstruction.");
    if(Array.isArray(task.reconstruct?.asks)){
      for(const item of task.reconstruct.asks){
        add(reconstruct,tag("h4",item.ask),tag("p",item.model_response));
      }
    }else{
      text(reconstruct,task.reconstruct?.prompt);
      text(reconstruct,task.reconstruct?.model_response);
    }
    const model=tag("div",undefined,"note");
    add(model,tag("h4","Model response · POST-COMMIT"),
      tag("p",task.attempt.post_commit_closure.model_response));
    reconstruct.append(model);
    const diagnosis=block("Stage 4 — Diagnose",
      task.diagnose.diagnostic_prompt||task.diagnose.prompt);
    if(task.diagnose.wrong_idea)text(diagnosis,"Plausible wrong route: "+task.diagnose.wrong_idea);
    const repair=block("Stage 5 — Repair",task.repair.action||task.repair.prompt);
    if(task.repair.explanation)text(repair,task.repair.explanation);
    const boundary=block("Stage 6 — Changed-condition boundary test",task.boundary_test.prompt);
    const bKey=revisionKey("boundary",task),oldBoundary=storageRead(bKey);
    if(!oldBoundary.ok){text(boundary,"Storage unavailable; boundary model answer held.");return;}
    const value=oldBoundary.value?.revision===revision?oldBoundary.value:null;
    const boundaryInput=tag("textarea");boundaryInput.id="boundary-answer";
    boundaryInput.setAttribute("aria-label","Your changed-condition reasoning");
    boundaryInput.placeholder="Apply the repaired model under the new condition…";
    boundary.append(boundaryInput);
    if(value){
      boundaryInput.value=value.response;boundaryInput.readOnly=true;
      text(boundary,"Model response (post boundary answer): "+task.boundary_test.answer);
    }else{
      const reveal=button("Save boundary answer and reveal model",()=>{
        if(boundaryInput.value.trim().length<12){
          message("Write your changed-condition reasoning first.");return;
        }
        const original=storageRead(attemptKey);
        if(!original.ok||original.value?.revision!==revision){
          message("BOUNDARY_REVISION_HOLD · First attempt unavailable.");return;
        }
        if(!storageWrite(bKey,{revision,response:boundaryInput.value,
            recorded_at:new Date().toISOString()})){
          message("STORAGE_UNAVAILABLE · Boundary response not saved.");return;
        }
        boundaryInput.readOnly=true;reveal.disabled=true;
        text(boundary,"Model response (post boundary answer): "+task.boundary_test.answer);
      });
      reveal.id="reveal-boundary";boundary.append(reveal);
    }
    if(B02.has(view.unit))visualStages(task,renderEpoch);
  }
  unitSel.addEventListener("change",()=>{
    view.taskId="";load(unitSel.value,{mode:"study",push:true});
  });
  taskSel.addEventListener("change",()=>{
    view.taskId=taskSel.value;render(true);
  });
  $("#show-study").addEventListener("click",()=>{
    view.mode="study";render(true);
  });
  $("#show-practice").addEventListener("click",()=>{
    view.mode="practice";render(true);
  });
  window.addEventListener("popstate",()=>{
    const q=new URLSearchParams(location.search);
    load(q.get("unit")||"C08",{subtopic:q.get("subtopic"),
      task:q.get("task"),mode:q.get("mode")});
  });
  for(const unit of UNITS){
    const opt=tag("option",unit);opt.value=unit;unitSel.append(opt);
  }
  if(requestedUnit&&!isValidUnit(requestedUnit)){
    fail("INVALID_UNIT_ROUTE");
  }else{
    load(requestedUnit||"C08",{subtopic:requestedSubtopic,
      task:requestedTask,mode:requestedMode,initial:true});
  }
})();
