"use strict";
/* Chemistry Core1A/B candidate renderer: no external libraries, never uses source text as HTML. */
(() => {
const root=document.getElementById("chem-textbook");
if(!root)return;
const source=root.dataset.source, memory=new Map();
function el(tag, cls, text){const x=document.createElement(tag);if(cls)x.className=cls;if(text!==undefined)x.textContent=String(text);return x}
function add(parent,child){parent.appendChild(child);return child}
function p(parent,text,cls=""){add(parent,el("p",cls,text))}
function section(parent,title,cls){const v=add(parent,el("section",cls));add(v,el("h3","",title));return v}
function safeId(x){return String(x).replace(/[^a-z0-9-]/gi,"-").toLowerCase()}
function stored(key){try{return localStorage.getItem(key)}catch(e){return memory.get(key)||null}}
function persist(key,value){try{localStorage.setItem(key,value);return true}catch(e){memory.set(key,value);return false}}
function showDemand(parent,d,unit,subId,version){
 const wrap=add(parent,el("section","demand"));
 add(wrap,el("span","tag",d.template_ref));add(wrap,el("h4","",d.title));
 p(wrap,d.core1a_explanation);
 const worked=add(wrap,el("div","worked"));add(worked,el("strong","", "Core1A — completed construction"));p(worked,d.worked_reasoning);
 p(wrap,"Independent check: "+d.independent_check,"mini");
 const form=add(wrap,el("div","attempt"));add(form,el("h4","","Core1B — reconstruct the idea"));
 p(form,"Predict: "+d.core1b.predict);
 const label=add(form,el("label","", "Write your first attempt before the model answer appears."));const field=add(form,el("textarea"));field.setAttribute("aria-label",d.title+" first attempt");label.htmlFor="response-"+safeId(d.instance_id);field.id=label.htmlFor;
 p(form,d.core1b.attempt);
 for(let i=0;i<d.hints.length;i++){const dt=add(form,el("details"));add(dt,el("summary","","Hint "+(i+1)));p(dt,d.hints[i])}
 const key="g9chem-first-attempt:"+unit+":"+version+":"+subId+":"+d.instance_id;
 const submit=add(form,el("button","", "Save first attempt and reveal reconstruction"));
 const post=add(form,el("div","post"));post.hidden=true;
 const st=add(form,el("p","mini"));
 const buildPost=()=>{post.replaceChildren();add(post,el("h4","","Reconstruct"));p(post,d.core1b.reconstruct);add(post,el("h4","","Diagnose"));p(post,d.core1b.diagnose);add(post,el("h4","","Repair"));p(post,d.core1b.repair);add(post,el("h4","","Boundary test"));p(post,d.core1b.boundary);add(post,el("h4","","Model response"));p(post,d.core1b.model_response);post.hidden=false;field.disabled=true;submit.disabled=true;st.textContent=memory.has(key)?"Browser storage unavailable. Your first answer is protected only for this open page session; refreshing may lose it.":"First-attempt text was preserved for this exact content revision; changes to the question require a new revision."};
 const first=stored(key);if(first!==null){field.value=first;buildPost()}
 submit.addEventListener("click",()=>{if(!field.value.trim()){st.textContent="Explain your reasoning first; empty attempts do not unlock the solution.";field.focus();return}if(stored(key)===null){const ok=persist(key,field.value);if(!ok)st.textContent="Storage unavailable: first attempt is retained for this page session only."}buildPost()})
}
function draw(book){
 root.replaceChildren();
 const hero=add(root,el("header","hero"));add(hero,el("div","eyebrow","NSEJS Chemistry · Draft Core1A + Core1B textbook"));add(hero,el("h1","",book.title));p(hero,book.introduction);p(hero,"Academic status: "+book.academic_status+" · Scope: "+book.scope_note,"meta");
 const notice=add(hero,el("p","note","Authored curriculum candidate, not a reviewed official textbook or authenticated NSEJS question. Do not use these draft solutions as evidence of academic approval."));
 const layout=add(root,el("div","textbook-layout"));const toc=add(layout,el("nav","toc"));toc.setAttribute("aria-label","Chapter contents");add(toc,el("h3","","Contents"));
 const area=add(layout,el("main"));
 book.subtopics.forEach((s,i)=>{
  const slug=safeId(s.id);const link=add(toc,el("a","",(i+1)+". "+s.title));link.href="#"+slug;
  const article=add(area,el("article","lesson"));article.id=slug;
  add(article,el("div","eyebrow",s.id+" · "+s.scope));add(article,el("h2","",s.title));
  p(article,s.entry_question,"bridge");
  for(const paragraph of s.core1a_paragraphs)p(article,paragraph);
  if(s.representation){const v=section(article,"Represent it faithfully","worked");if(s.figure_ref){const fig=add(v,el("figure","chem-figure"));const img=add(fig,el("img"));img.src=s.figure_ref;img.alt=s.figure_alt||s.title;img.loading="lazy";img.decoding="async";img.style.width="100%";img.style.height="auto";img.style.borderRadius="10px";add(fig,el("figcaption","mini",s.figure_alt||"Chemistry representation"));}p(v,s.representation)}
  if(s.worked_example){const w=section(article,"Worked example — all steps visible","worked");p(w,s.worked_example.problem);const list=add(w,el("ol"));for(const step of s.worked_example.steps)add(list,el("li","",step));p(w,"Result: "+s.worked_example.result);p(w,"Independent check: "+s.worked_example.check,"mini")}
  if(s.misconception){const m=section(article,"A tempting wrong route — and its repair","misconception");p(m,"Wrong: "+s.misconception.wrong);p(m,"Why it fails: "+s.misconception.why);p(m,"Repair: "+s.misconception.repair)}
  add(article,el("h3","","Three reasoning demands — learn, then reconstruct"));
  for(const d of s.demands)showDemand(article,d,book.unit_id,s.id,book.content_sha256);
  if(s.source_notes){const sn=section(article,"Sources and limitations","source");p(sn,s.source_notes)}
 });
 add(root,el("footer","foot","Grade9v4.1 Chemistry draft · No academic approval inferred from software validation. Core1A explanations precede Core1B protected decisions. All tasks are authored practice unless a separately verified source identity is supplied."));
}
fetch(source,{cache:"no-store"}).then(async r=>{if(!r.ok)throw Error("HTTP "+r.status);if(!crypto || !crypto.subtle)throw Error("SHA-256 content revision binding unavailable");const raw=await r.text();const dig=await crypto.subtle.digest("SHA-256",new TextEncoder().encode(raw));const revision=[...new Uint8Array(dig)].map(b=>b.toString(16).padStart(2,"0")).join("");const book=JSON.parse(raw);book.content_sha256=revision;return book}).then(draw).catch(e=>{root.replaceChildren();const err=add(root,el("div","hero"));add(err,el("h2","","Unable to load textbook candidate"));p(err,String(e)+". Serve the repository over HTTP; local file:// fetch is unsupported.")});
})();
