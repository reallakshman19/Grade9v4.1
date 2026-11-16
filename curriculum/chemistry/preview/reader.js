"use strict";
/* Chemistry Core1A/B candidate renderer: no external libraries, never uses source text as HTML. */
(() => {
const root=document.getElementById("chem-textbook");
if(!root)return;
const source=root.dataset.source, memory=new Map();
const requested=new URLSearchParams(location.search);
function el(tag, cls, text){const x=document.createElement(tag);if(cls)x.className=cls;if(text!==undefined)x.textContent=String(text);return x}
function add(parent,child){parent.appendChild(child);return child}
function p(parent,text,cls=""){add(parent,el("p",cls,text))}
function section(parent,title,cls){const v=add(parent,el("section",cls));add(v,el("h3","",title));return v}
function list(parent,items){const ol=add(parent,el("ol"));for(const item of items)add(ol,el("li","",item));return ol}
function renderSpine(parent,book){
 const spine=book.chapter_spine;if(!spine)return;
 const box=add(parent,el("section","chapter-spine"));add(box,el("h2","","The chapter's central question"));p(box,spine.central_question,"bridge");
 const layout=add(box,el("div","spine-columns"));
 const prep=add(layout,el("div"));add(prep,el("h3","","What you need first"));list(prep,spine.prior_knowledge);
 const journey=add(layout,el("div"));add(journey,el("h3","","How the understanding grows"));list(journey,spine.journey);
 const terms=add(box,el("details","glossary"));add(terms,el("summary","","Key vocabulary — open when needed"));
 const termList=add(terms,el("dl","terms"));
 for(const [term,definition] of Object.entries(spine.key_terms)){add(termList,el("dt","",term));add(termList,el("dd","",definition))}
}
function renderDive(article,s){
 const dive=s.deep_dive;if(!dive)return;
 const idea=add(article,el("aside","big-idea"));add(idea,el("h3","","The big idea"));p(idea,dive.big_idea);
 const path=section(article,"Build the reasoning, one link at a time","reasoning-path");list(path,dive.reasoning_path);
 const activity=section(article,"Investigate the idea","investigation");
 add(activity,el("h4","",dive.discovery.title));
 p(activity,dive.discovery.setup);
 const predict=add(activity,el("div","predict-question"));add(predict,el("strong","","Before you uncover the explanation"));p(predict,dive.discovery.predict);
 const detail=add(activity,el("details","investigation-answer"));add(detail,el("summary","","Reveal the observation, interpretation and limits"));
 p(detail,"Observation: "+dive.discovery.observation);
 p(detail,"Interpretation: "+dive.discovery.interpretation);
 p(detail,"Limit of this investigation: "+dive.discovery.limits);
 const bridge=add(article,el("p","concept-bridge","Connection to the next idea: "+dive.connection));
}

function safeId(x){return String(x).replace(/[^a-z0-9-]/gi,"-").toLowerCase()}
function stored(key){try{return localStorage.getItem(key)}catch(e){return null}}
function persist(key,value){try{localStorage.setItem(key,value);return localStorage.getItem(key)===value}catch(e){return false}}
function showDemand(parent,d,unit,subId,version){
 const wrap=add(parent,el("section","demand"));
 if(!parent.querySelector("#practice-"+safeId(subId)))wrap.id="practice-"+safeId(subId);
 add(wrap,el("span","tag",d.template_ref));add(wrap,el("h4","",d.title));
 p(wrap,d.core1a_explanation);
 const worked=add(wrap,el("div","worked"));add(worked,el("strong","","Core1A — completed construction"));p(worked,d.worked_reasoning);
 p(wrap,"Independent check: "+d.independent_check,"mini");
 const form=add(wrap,el("div","attempt"));
 add(form,el("h4","","Core1B — predict, attempt, reconstruct, diagnose, repair, boundary"));
 p(form,d.core1b.attempt,"learner-task");
 const key="g9chem-first-attempt:"+unit+":"+version+":"+subId+":"+d.instance_id;
 const predictKey=key+":prediction",hintKey=key+":hint-depth";
 const st=add(form,el("p","mini"));
 const prediction=add(form,el("section","prediction-stage"));
 add(prediction,el("h4","","1 · Predict"));
 p(prediction,d.core1b.predict);
 const predictionLabel=add(prediction,el("label","","Make a qualitative prediction, specify the model/conditions, and justify your expectation."));
 const predictionField=add(prediction,el("textarea","prediction-input"));
 predictionField.setAttribute("aria-label",d.title+" independent prediction");
 predictionLabel.htmlFor="prediction-"+safeId(d.instance_id);predictionField.id=predictionLabel.htmlFor;
 const predictButton=add(prediction,el("button","predict-submit","Save prediction and begin first attempt"));
 const firstStep=add(form,el("section","first-attempt"));
 add(firstStep,el("h4","","2 · First attempt"));
 const label=add(firstStep,el("label","","Write your first reasoning attempt before receiving model feedback."));
 const field=add(firstStep,el("textarea"));
 field.setAttribute("aria-label",d.title+" first attempt");
 label.htmlFor="response-"+safeId(d.instance_id);field.id=label.htmlFor;
 const submit=add(firstStep,el("button","","Save first attempt and begin reconstruction"));
 const helper=add(form,el("section","hint-ladder"));helper.hidden=true;
 add(helper,el("h4","","Optional progressive help — records assisted exposure"));
 p(helper,"Hints are authored candidates. They are saved before reveal and do not grade your answer.","mini");
 const hintContents=add(helper,el("div","hint-contents"));
 const hintButton=add(helper,el("button","hint-submit","Reveal next hint"));
 const post=add(form,el("div","post"));post.hidden=true;
 const stageOrder=[
  {id:"reconstruct",title:"Reconstruct",prompt:d.core1b.reconstruct},
  {id:"diagnose",title:"Diagnose",prompt:d.core1b.diagnose},
  {id:"repair",title:"Repair",prompt:d.core1b.repair},
  {id:"boundary",title:"Boundary test",prompt:d.core1b.boundary}
 ];
 const hintDepth=()=>Math.min(d.hints.length,Math.max(0,Number(stored(hintKey)||0)||0));
 function renderHints(){
  const depth=hintDepth();hintContents.replaceChildren();
  for(let i=0;i<depth;i++)p(hintContents,"H"+(i+1)+": "+d.hints[i],"hint-revealed");
  hintButton.disabled=depth>=d.hints.length;
  hintButton.textContent=depth>=d.hints.length?"All available hints viewed":"Reveal hint "+(depth+1)+" of "+d.hints.length;
 }
 function renderCommitted(){
  if(stored(key)===null)return;
  field.value=stored(key);field.disabled=true;submit.disabled=true;firstStep.hidden=false;
  prediction.hidden=true;helper.hidden=false;renderHints();
  post.replaceChildren();post.hidden=false;
  add(post,el("h4","","First attempt saved"));
  if(stored(predictKey)===null)p(post,"Legacy first attempt: no separately recorded prediction exists. The earlier response is preserved without inventing a prediction.","mini");
  else p(post,"Your prediction and first attempt were stored separately for this exact content revision.","mini");
  let complete=true;
  for(const stage of stageOrder){
   const stageKey=key+":stage:"+stage.id;
   const stageBox=add(post,el("section","core1b-stage"));
   add(stageBox,el("h4","",stage.title));p(stageBox,stage.prompt);
   const saved=stored(stageKey);
   if(saved!==null){p(stageBox,"Your saved response: "+saved,"stage-saved");continue}
   complete=false;
   const stageLabel=add(stageBox,el("label","","Write independent "+stage.title.toLowerCase()+" reasoning before continuing."));
   const stageField=add(stageBox,el("textarea","stage-input"));
   stageField.setAttribute("aria-label",stage.title+" independent response");
   stageLabel.htmlFor="stage-"+safeId(d.instance_id)+"-"+stage.id;stageField.id=stageLabel.htmlFor;
   const stageButton=add(stageBox,el("button","stage-submit","Save "+stage.title+" response"));
   stageButton.addEventListener("click",()=>{
    if(!stageField.value.trim()){st.textContent="A written "+stage.title.toLowerCase()+" response is required.";stageField.focus();return}
    if(stored(stageKey)!==null){renderCommitted();return}
    if(!persist(stageKey,stageField.value)){st.textContent="Storage unavailable: stage response not durably saved. Model remains locked.";return}
    renderCommitted();
   });break;
  }
  if(complete){
   const closure=add(post,el("section","model-closure"));
   add(closure,el("h4","","Model response"));p(closure,d.core1b.model_response);
   st.textContent="All independent stages saved. Compare your model and the author's candidate response; academic correctness is not certified.";
  }else st.textContent="Your first answer remains locked. Complete each separate stage to view the model response.";
 }
 function renderStart(){
  const first=stored(key),pred=stored(predictKey);
  if(first!==null){renderCommitted();return}
  post.hidden=true;prediction.hidden=pred!==null;
  firstStep.hidden=pred===null;helper.hidden=pred===null;
  predictionField.value=pred||"";predictionField.disabled=pred!==null;
  if(pred!==null)renderHints();
  st.textContent=pred===null?"Predict independently before attempting; no answer or hints have been disclosed.":"Prediction saved. Attempt the independent task, with optional recorded hints.";
 }
 predictButton.addEventListener("click",()=>{
  if(!predictionField.value.trim()){st.textContent="Write your prediction and reason before starting.";predictionField.focus();return}
  if(stored(predictKey)===null&&!persist(predictKey,predictionField.value)){
   st.textContent="Storage unavailable: prediction could not be preserved; the first attempt stays locked.";return;
  }
  renderStart();
 });
 hintButton.addEventListener("click",()=>{
  if(stored(predictKey)===null&&stored(key)===null){st.textContent="Save a prediction first.";return}
  const depth=hintDepth();if(depth>=d.hints.length)return;
  if(!persist(hintKey,String(depth+1))){st.textContent="Storage unavailable: hint exposure could not be saved, so no hint was revealed.";return}
  renderHints();
 });
 submit.addEventListener("click",()=>{
  if(stored(predictKey)===null){st.textContent="Commit an independent prediction before your first attempt.";return}
  if(!field.value.trim()){st.textContent="Explain your reasoning first; empty attempts do not unlock the next stage.";field.focus();return}
  if(stored(key)===null&&!persist(key,field.value)){
   st.textContent="Storage unavailable: the first attempt could not be preserved. Nothing is unlocked; your text remains editable.";return;
  }
  renderCommitted();
 });
 renderStart();
}
function draw(book){
 root.replaceChildren();
 const hero=add(root,el("header","hero"));add(hero,el("div","eyebrow","NSEJS Chemistry · Draft Core1A + Core1B textbook"));add(hero,el("h1","",book.title));p(hero,book.introduction);p(hero,"Academic status: "+book.academic_status+" · Scope: "+book.scope_note,"meta");
 const notice=add(hero,el("p","note","Authored curriculum candidate, not a reviewed official textbook or authenticated NSEJS question. Do not use these draft solutions as evidence of academic approval."));
 renderSpine(root,book);
 const layout=add(root,el("div","textbook-layout"));const toc=add(layout,el("nav","toc"));toc.setAttribute("aria-label","Chapter contents");add(toc,el("h3","","Contents"));
 const area=add(layout,el("main"));
 const navHost=add(area,el("div","chem-active-nav"));
 book.subtopics.forEach((s,i)=>{
  const slug=safeId(s.id);const link=add(toc,el("a","",(i+1)+". "+s.title));link.href="#"+slug;
  link.dataset.subtopic=s.id;
  const article=add(area,el("article","lesson"));article.id=slug;
  // R2 mounts one shared navigation bar for only the focused subtopic.
  // All original lessons and attempt keys remain in the DOM unchanged.
  add(article,el("div","eyebrow",s.id+" · "+s.scope));add(article,el("h2","",s.title));
  p(article,s.entry_question,"bridge");
  renderDive(article,s);
  const chapterText=section(article,"The connected scientific explanation","core1a-prose");
  for(const paragraph of s.core1a_paragraphs)p(chapterText,paragraph);
  if(s.representation){const v=section(article,"Represent it faithfully","worked");if(s.figure_ref){const fig=add(v,el("figure","chem-figure"));const img=add(fig,el("img"));img.src=s.figure_ref;img.alt=s.figure_alt||s.title;img.loading="lazy";img.decoding="async";img.style.width="100%";img.style.height="auto";img.style.borderRadius="10px";add(fig,el("figcaption","mini",s.figure_alt||"Chemistry representation"));}p(v,s.representation)}
  if(s.worked_example){const w=section(article,"Worked example — all steps visible","worked");p(w,s.worked_example.problem);const list=add(w,el("ol"));for(const step of s.worked_example.steps)add(list,el("li","",step));p(w,"Result: "+s.worked_example.result);p(w,"Independent check: "+s.worked_example.check,"mini")}
  if(s.misconception){const m=section(article,"A tempting wrong route — and its repair","misconception");p(m,"Wrong: "+s.misconception.wrong);p(m,"Why it fails: "+s.misconception.why);p(m,"Repair: "+s.misconception.repair)}
  add(article,el("h3","","Three reasoning demands — learn, then reconstruct"));
  for(const d of s.demands)showDemand(article,d,book.unit_id,s.id,book.content_sha256);
  const back=add(article,el("p","chapter-return"));
  const backLink=add(back,el("a","","Return to Chemistry chapter list"));
  backLink.href="../../../nsejs/chemistry/index.html#chem-chapters";
  if(s.source_notes){const sn=section(article,"Sources and limitations","source");p(sn,s.source_notes)}
 });
 if(book.chapter_spine){const close=add(root,el("section","chapter-closure"));add(close,el("h2","","Chapter synthesis"));p(close,book.chapter_spine.chapter_closure);p(close,"Before beginning the next unit, explain this chapter's main claim without looking at the worked examples, then test it against one new observation.","mini")}
 add(root,el("footer","foot","Grade9v4.1 Chemistry authored self-study · Source status is shown separately from practice. Core1A explanations precede protected Core1B reconstruction."));
 // A single focused subtopic is visible while the unchanged complete book remains
 // in the DOM for stable first-attempt IDs, print and legacy anchor compatibility.
 const allLessons=[...area.querySelectorAll(":scope > article.lesson")];
 const links=[...toc.querySelectorAll("a[data-subtopic]")];
 const chapterNumber=el("p","chem-focus-position");
 toc.insertBefore(chapterNumber,links[0]||null);
 function focus(id,mode="study",push=false,scroll=true){
   const selected=book.subtopics.find(s=>s.id===id)||book.subtopics[0];
   const slug=safeId(selected.id),effectiveMode=mode==="practice"?"practice":"study";
   for(const lesson of allLessons)lesson.hidden=lesson.id!==slug;
   for(const a of links){
     const current=a.dataset.subtopic===selected.id;
     if(current)a.setAttribute("aria-current","true");else a.removeAttribute("aria-current");
   }
   chapterNumber.textContent="Subtopic "+(book.subtopics.indexOf(selected)+1)+" of "+book.subtopics.length;
   if(window.ChemLearnerNav)window.ChemLearnerNav.mountPreview(navHost,book.unit_id,selected.id,effectiveMode);
   if(push){
     const url=new URL(location.href);
     url.searchParams.set("subtopic",selected.id);
     url.searchParams.set("mode",effectiveMode);
     url.hash=(effectiveMode==="practice"?"practice-":"")+slug;
     history.pushState({subtopic:selected.id},"",url.href);
   }
   if(scroll)requestAnimationFrame(()=>{
     const target=document.getElementById((effectiveMode==="practice"?"practice-":"")+slug)
       ||document.getElementById(slug);
     target?.scrollIntoView({block:"start",behavior:"instant"});
   });
 }
 function address(){
   const params=new URLSearchParams(location.search);
   const rawHash=decodeURIComponent(location.hash.replace(/^#/,""));
   const hashKey=rawHash.replace(/^practice-/,"");
   const fromHash=book.subtopics.find(s=>safeId(s.id)===hashKey);
   const fromQuery=book.subtopics.find(s=>s.id===params.get("subtopic"));
   const selected=fromHash||fromQuery||book.subtopics[0];
   const mode=rawHash.startsWith("practice-") ||
     (!fromHash && selected===fromQuery && params.get("mode")==="practice")?"practice":"study";
   return {id:selected.id,mode,scroll:!!(fromHash||fromQuery)};
 }
 links.forEach(a=>a.addEventListener("click",event=>{
   event.preventDefault();focus(a.dataset.subtopic,"study",true);
 }));
 window.addEventListener("popstate",()=>{const route=address();focus(route.id,route.mode,false,route.scroll)});
 window.addEventListener("hashchange",()=>{const route=address();focus(route.id,route.mode,false,route.scroll)});
 const route=address();
 focus(route.id,route.mode,false,route.scroll);
}
fetch(source,{cache:"no-store"}).then(async r=>{if(!r.ok)throw Error("HTTP "+r.status);if(!crypto || !crypto.subtle)throw Error("SHA-256 content revision binding unavailable");const raw=await r.text();const dig=await crypto.subtle.digest("SHA-256",new TextEncoder().encode(raw));const revision=[...new Uint8Array(dig)].map(b=>b.toString(16).padStart(2,"0")).join("");const book=JSON.parse(raw);book.content_sha256=revision;return book}).then(draw).catch(e=>{root.replaceChildren();const err=add(root,el("div","hero"));add(err,el("h2","","Unable to load textbook candidate"));p(err,String(e)+". Serve the repository over HTTP; local file:// fetch is unsupported.")});
})();
