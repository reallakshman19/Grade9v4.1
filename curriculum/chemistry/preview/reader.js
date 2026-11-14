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
function stored(key){try{return localStorage.getItem(key)}catch(e){return memory.get(key)||null}}
function persist(key,value){try{localStorage.setItem(key,value);return true}catch(e){memory.set(key,value);return false}}
function showDemand(parent,d,unit,subId,version){
 const wrap=add(parent,el("section","demand"));
 if(!parent.querySelector("#practice-"+safeId(subId)))wrap.id="practice-"+safeId(subId);
 add(wrap,el("span","tag",d.template_ref));add(wrap,el("h4","",d.title));
 p(wrap,d.core1a_explanation);
 const worked=add(wrap,el("div","worked"));add(worked,el("strong","", "Core1A — completed construction"));p(worked,d.worked_reasoning);
 p(wrap,"Independent check: "+d.independent_check,"mini");
 const form=add(wrap,el("div","attempt"));add(form,el("h4","","Core1B — reconstruct the idea"));
 p(form,"Predict: "+d.core1b.predict);
 p(form,d.core1b.attempt,"learner-task");
 const label=add(form,el("label","", "Write your first reasoning attempt before revealing the reconstruction."));const field=add(form,el("textarea"));field.setAttribute("aria-label",d.title+" first attempt");label.htmlFor="response-"+safeId(d.instance_id);field.id=label.htmlFor;
 const hints=[];
 for(let i=0;i<d.hints.length;i++){const dt=add(form,el("details"));dt.hidden=true;hints.push(dt);add(dt,el("summary","","Hint "+(i+1)));p(dt,d.hints[i])}
 const key="g9chem-first-attempt:"+unit+":"+version+":"+subId+":"+d.instance_id;
 const submit=add(form,el("button","", "Save first attempt and reveal reconstruction"));
 const post=add(form,el("div","post"));post.hidden=true;
 const st=add(form,el("p","mini"));
 const buildPost=()=>{hints.forEach(hint=>{hint.hidden=false});post.replaceChildren();add(post,el("h4","","Reconstruct"));p(post,d.core1b.reconstruct);add(post,el("h4","","Diagnose"));p(post,d.core1b.diagnose);add(post,el("h4","","Repair"));p(post,d.core1b.repair);add(post,el("h4","","Boundary test"));p(post,d.core1b.boundary);add(post,el("h4","","Model response"));p(post,d.core1b.model_response);post.hidden=false;field.disabled=true;submit.disabled=true;st.textContent=memory.has(key)?"Browser storage unavailable. Your first answer is protected only for this open page session; refreshing may lose it.":"First-attempt text was preserved for this exact content revision; changes to the question require a new revision."};
 const first=stored(key);if(first!==null){field.value=first;buildPost()}
 submit.addEventListener("click",()=>{if(!field.value.trim()){st.textContent="Explain your reasoning first; empty attempts do not unlock the solution.";field.focus();return}if(stored(key)===null){const ok=persist(key,field.value);if(!ok){st.textContent="Storage unavailable: the first attempt could not be preserved. Nothing is unlocked; your text remains editable.";return}}buildPost()})
}
function draw(book){
 root.replaceChildren();
 const hero=add(root,el("header","hero"));add(hero,el("div","eyebrow","NSEJS Chemistry · Draft Core1A + Core1B textbook"));add(hero,el("h1","",book.title));p(hero,book.introduction);p(hero,"Academic status: "+book.academic_status+" · Scope: "+book.scope_note,"meta");
 const notice=add(hero,el("p","note","Authored curriculum candidate, not a reviewed official textbook or authenticated NSEJS question. Do not use these draft solutions as evidence of academic approval."));
 renderSpine(root,book);
 const layout=add(root,el("div","textbook-layout"));const toc=add(layout,el("nav","toc"));toc.setAttribute("aria-label","Chapter contents");add(toc,el("h3","","Contents"));
 const area=add(layout,el("main"));
 book.subtopics.forEach((s,i)=>{
  const slug=safeId(s.id);const link=add(toc,el("a","",(i+1)+". "+s.title));link.href="#"+slug;
  const article=add(area,el("article","lesson"));article.id=slug;
  if(window.ChemLearnerNav)window.ChemLearnerNav.mountPreview(article,book.unit_id,s.id,requested.get("subtopic")===s.id&&requested.get("mode")==="practice"?"practice":"study");
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
 const requestId=requested.get("subtopic");
 if(requestId&&book.subtopics.some(s=>s.id===requestId)){
   const wanted=requested.get("mode")==="practice"?"practice-"+safeId(requestId):safeId(requestId);
   requestAnimationFrame(()=>document.getElementById(wanted)?.scrollIntoView({block:"start"}));
 }
}
fetch(source,{cache:"no-store"}).then(async r=>{if(!r.ok)throw Error("HTTP "+r.status);if(!crypto || !crypto.subtle)throw Error("SHA-256 content revision binding unavailable");const raw=await r.text();const dig=await crypto.subtle.digest("SHA-256",new TextEncoder().encode(raw));const revision=[...new Uint8Array(dig)].map(b=>b.toString(16).padStart(2,"0")).join("");const book=JSON.parse(raw);book.content_sha256=revision;return book}).then(draw).catch(e=>{root.replaceChildren();const err=add(root,el("div","hero"));add(err,el("h2","","Unable to load textbook candidate"));p(err,String(e)+". Serve the repository over HTTP; local file:// fetch is unsupported.")});
})();
