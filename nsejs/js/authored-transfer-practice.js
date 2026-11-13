/* Source-neutral Grade9 authored Core1B transfer practice: FIVE questions total.
 * This is not an official NSEJS paper, QRT adjudication or exam scoring tool.
 * Reasoning and worked responses stay hidden until first free-form response is
 * durably stored. Original exam question stems are never loaded by this reader.
 */
(() => {
  "use strict";
  const subject=document.body.dataset.authoredSubject;
  const root=document.getElementById("authored-questions");
  const notice=document.getElementById("authored-status");
  const HOSTS={CHEMISTRY:2,BIOLOGY:3};
  let sourceDigest=null;
  const tag=(name,value)=>{
    const n=document.createElement(name);
    if(value!==undefined)n.textContent=String(value);
    return n;
  };
  function fatal(code){
    if(notice){notice.textContent="HOLD · "+code+" · No authored practice loaded or approved.";notice.dataset.status="HOLD";}
    if(root)root.replaceChildren();
  }
  async function digest(raw){
    if(!crypto?.subtle)throw Error("SOURCE_REVISION_CRYPTO_UNAVAILABLE");
    const h=await crypto.subtle.digest("SHA-256",new TextEncoder().encode(raw));
    return Array.from(new Uint8Array(h),b=>b.toString(16).padStart(2,"0")).join("");
  }
  function canonical(value) {
    // Match Python's sort_keys=True / separators=(',', ':') SHA input.
    // Every authored question revision is checked from the entire real item,
    // not accepted from a declared 64-character string.
    if (Array.isArray(value)) return "["+value.map(canonical).join(",")+"]";
    if (value!==null && typeof value==="object") {
      return "{"+Object.keys(value).sort().map(k=>JSON.stringify(k)+":"+canonical(value[k])).join(",")+"}";
    }
    return JSON.stringify(value);
  }
  function storageKey(q){
    return ["g9","nsejs","author-core1b","v1",subject,sourceDigest,q.uid,q.revision_sha256].join(":");
  }
  function read(keyValue){
    try {
      const x=JSON.parse(localStorage.getItem(keyValue)||"null");
      return x&&x.key===keyValue&&x.subject===subject&&
        x.original_exam_question===false&&typeof x.first_response==="string"&&
        x.first_response.trim().length>=15&&
        x.revision===sourceDigest?x:null;
    } catch{return null;}
  }
  function write(keyValue,value) {
    try {
      if(localStorage.getItem(keyValue)!==null)return false;
      const raw=JSON.stringify(value);
      localStorage.setItem(keyValue,raw);
      return localStorage.getItem(keyValue)===raw;
    }catch{return false;}
  }
  function render(q){
    const card=tag("article");card.className="practice-card";card.id="authored-"+encodeURIComponent(q.lesson_slug);
    card.dataset.questionUid=q.uid;
    card.dataset.questionRevision=q.revision_sha256;
    card.append(tag("h2",q.lesson_slug.replaceAll("-"," ")));
    card.append(tag("p","AUTHORED Grade9 Core1B independent transfer · Not an official NSEJS question · Academic / Science HOLD"));
    const prompt=tag("p",q.prompt);prompt.className="practice-prompt";card.append(prompt);
    const text=tag("textarea");text.rows=5;text.placeholder="Explain your approach before seeing the author's reconstruction.";
    text.setAttribute("aria-label","First response for "+q.lesson_slug);
    const save=tag("button","Save first independent response");
    save.type="button";
    const review=tag("button","Show author's unreviewed reconstruction");
    review.type="button";review.disabled=true;
    const feedback=tag("p","First response not yet saved.");feedback.setAttribute("role","status");
    const hidden=tag("section");hidden.className="author-worked";hidden.hidden=true;
    const lesson=tag("a","Open complete authored Core1A + Core1B lesson");
    lesson.href="core1/"+q.lesson_slug+"/index.html";
    lesson.className="lesson-touch";
    card.append(text,save,review,feedback,hidden,lesson);
    const key=storageKey(q);
    const previous=read(key);
    if(previous){
      text.value=previous.first_response;text.disabled=true;save.disabled=true;review.disabled=false;
      feedback.textContent="Your first local response is saved for this authored revision; NOT a grade.";
    }
    save.addEventListener("click",()=>{
      const response=text.value.trim();
      if(response.length<15){
        feedback.textContent="Please write at least 15 characters of reasoning before saving.";
        return;
      }
      const record={key,subject,revision:sourceDigest,uid:q.uid,
        original_exam_question:false,first_response:response,
        created_at:new Date().toISOString(),status:"UNVERIFIED_LOCAL_AUTHOR_PRACTICE"};
      if(!write(key,record)){
        feedback.textContent="HOLD · Storage denied or first response already exists. Reconstruction remains withheld.";
        save.disabled=true;review.disabled=true;return;
      }
      text.disabled=true;save.disabled=true;review.disabled=false;
      feedback.textContent="First response saved locally; this is not an exam score or reviewed answer.";
    });
    review.addEventListener("click",()=>{
      if(review.disabled||!read(key))return;
      // Do not even insert author answers into the DOM before the durable
      // saved first response AND a separate explicit reveal click.
      const first=tag("h3","Author's reconstruction · NOT academically reviewed");
      hidden.append(first,tag("p","Compare your approach to these authored teaching steps; not a verified official solution."));
      const list=tag("ol");
      for(const item of q.reconstruction){
        const li=tag("li");
        li.append(tag("strong",item.ask),tag("p",item.answer));
        list.append(li);
      }
      hidden.append(list,tag("h4","Boundary challenge"),tag("p",q.boundary_question),
        tag("p",q.boundary_author_response));
      hidden.hidden=false;
      review.disabled=true;
      review.textContent="Author's teaching reconstruction shown";
      if(window.MathJax?.typesetPromise)window.MathJax.typesetPromise([hidden]).catch(()=>{});
    });
    return card;
  }
  async function init(){
    if(!(subject in HOSTS)||!root||!notice)throw Error("UNRECOGNIZED_SUBJECT");
    const response=await fetch("../data/authored-core1b-transfers.v1.json",{cache:"no-store"});
    if(!response.ok)throw Error("AUTHORED_EXERCISE_MANIFEST_MISSING");
    const raw=await response.text();
    const data=JSON.parse(raw);
    if(data.schema!=="grade9-nsejs-authored-core1b-practice/v1"||
       data.source_origin!=="GRADE9_ORIGINAL_CORE1B_TRANSFER_NOT_OFFICIAL_NSEJS"||
       data.academic_admission!=="HOLD"||data.source_exam_authenticated!==false||
       data.official_exam_questions_published!==0||
       data.copy_of_original_exam_stem!==false||
       data.source_rights_review!=="HOLD"||data.authored_transfer_count!==5||
       !Array.isArray(data.items)||data.items.length!==5)
      throw Error("AUTHOR_CONTENT_OR_SOURCE_AUTHORITY_INVALID");
    const seen=new Set();
    for(const q of data.items){
      if(seen.has(q.uid)||q.original_exam_question!==false||
         q.academic_admission!=="HOLD"||q.independent_science_review!=="HOLD"||
         q.source_origin!==data.source_origin||
         !q.uid.startsWith("g9:NSEJS:AUTHORED_CORE1B:")||
         !/^[a-f0-9]{64}$/.test(q.revision_sha256)||
         typeof q.prompt!=="string"||q.prompt.length<55||
         !Array.isArray(q.reconstruction)||q.reconstruction.length<2||
         typeof q.boundary_question!=="string"||
         !/^[a-z0-9-]+$/.test(q.lesson_slug)||
         q.lesson_route!=="nsejs/"+q.subject.toLowerCase()+"/core1/"+q.lesson_slug+"/index.html")
        throw Error("AUTHOR_EXERCISE_REVISION_OR_SCOPE_INVALID");
      const revisionInput={...q};
      delete revisionInput.revision_sha256;
      if(await digest(canonical(revisionInput))!==q.revision_sha256)
        throw Error("AUTHORED_TRANSFER_REAL_CONTENT_HASH_MISMATCH");
      seen.add(q.uid);
    }
    sourceDigest=await digest(raw);
    const exercises=data.items.filter(q=>q.subject===subject);
    if(exercises.length!==HOSTS[subject])throw Error("AUTHOR_SUBJECT_CENSUS_INVALID");
    root.replaceChildren(...exercises.map(render));
    notice.textContent=exercises.length+" genuine authored Core1B transfer exercises · original exam source NOT asserted · academic HOLD";
    notice.dataset.status="AUTHORED_TECHNICAL_ONLY";
    if(window.MathJax?.typesetPromise)window.MathJax.typesetPromise([root]).catch(()=>{});
  }
  init().catch(error=>fatal(error.message||"AUTHOR_DATA_UNAVAILABLE"));
})();