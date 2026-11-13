/* Independent Grade9 Core1A/B skill repair. The 18 original exam-source
 * modules remain HOLD. All teaching examples here are newly authored;
 * no source exam claims, certified answers or B1–B7 admission.
 */
(() => {
  "use strict";
  const root=document.getElementById("recovery-lesson");
  const status=document.getElementById("recovery-status");
  const slug=document.body.dataset.recoverySlug;
  const src="../../../../data/independent-core1-recovery.v1.json";
  const make=(type,content)=>{
    const element=document.createElement(type);
    if(content!==undefined)element.textContent=String(content);
    return element;
  };
  const canonical=x=>Array.isArray(x)?
    "["+x.map(canonical).join(",")+"]":
    x!==null&&typeof x==="object"?
    "{"+Object.keys(x).sort().map(k=>JSON.stringify(k)+":"+canonical(x[k])).join(",")+"}":
    JSON.stringify(x);
  const hash=async s=>{
    if(!crypto?.subtle)throw Error("BROWSER_SHA256_UNAVAILABLE");
    const r=await crypto.subtle.digest("SHA-256",new TextEncoder().encode(s));
    return Array.from(new Uint8Array(r),v=>v.toString(16).padStart(2,"0")).join("");
  };
  function failure(code){
    status.dataset.status="HOLD";
    status.textContent="HOLD · "+code+
      ". No protected work was revealed or saved. Historical source and academic admission remain HOLD.";
    Array.from(root.children).forEach(x=>{if(x!==status)x.remove();});
  }
  function storeKey(full,topic,kind){
    return "g9:nsejs:core1:original-authored-repair:v1:"+full+":"+
      topic.revision_sha256+":"+topic.uid+":"+kind;
  }
  function read(key,topic,kind,full){
    try{
      const raw=localStorage.getItem(key);
      if(!raw)return null;
      const v=JSON.parse(raw);
      return v&&v.key===key&&v.kind===kind&&
        v.uid===topic.uid&&v.revision===topic.revision_sha256&&
        v.full_revision===full&&
        v.academic_admission==="HOLD"&&
        typeof v.first_response==="string"&&v.first_response.trim().length>=20?
        v:null;
    }catch{return null;}
  }
  function write(key,record){
    try{
      if(localStorage.getItem(key)!==null)return false;
      const raw=JSON.stringify(record);
      localStorage.setItem(key,raw);
      return localStorage.getItem(key)===raw;
    }catch{return false;}
  }
  function stage(number,name){
    const box=make("section");box.className="stage";
    const heading=make("h2",number+". "+name);box.append(heading);
    root.append(box);return box;
  }
  function render(record,full){
    const stage1=stage(1,"Predict · Core1A teaching");
    stage1.append(make("p",record.concept),make("h3","Worked model"),
       make("p",record.worked),make("h3","Predict before calculating"),
       make("p",record.predict));
    const stage2=stage(2,"Attempt · independent Core1B transfer");
    stage2.append(make("p",record.challenge));
    const textarea=make("textarea");textarea.rows=6;
    textarea.setAttribute("aria-label","First independent Core1B reasoning");
    textarea.placeholder="Write the governing law, your calculation or reasoning, and an independent check.";
    stage2.append(textarea);
    const save=make("button","Save first Core1B response");save.type="button";
    stage2.append(save);
    const receipt=make("p","No first response saved.");
    receipt.setAttribute("role","status");stage2.append(receipt);
    const seq=[
      ["Reconstruct · proof path",record.steps],
      ["Diagnose · misconception",record.trap],
      ["Repair · method check",record.repair],
      ["Boundary test · unseen transfer",record.boundary]
    ];
    const buttons=seq.map((entry,i)=>{
      const button=make("button",(i+3)+". "+entry[0]);
      button.type="button";button.disabled=true;
      stage2.append(button);return button;
    });
    const key=storeKey(full,record,"first");
    const previous=read(key,record,"first",full);
    function committed(){
      textarea.disabled=true;save.disabled=true;
      buttons[0].disabled=false;
      receipt.textContent="First response saved for this exact authored revision. Academic/source HOLD persists.";
      receipt.dataset.status="SAVED";
    }
    if(previous){textarea.value=previous.first_response;committed();}
    save.addEventListener("click",()=>{
      const answer=textarea.value.trim();
      if(answer.length<20){
        receipt.textContent="Explain your reasoning in at least 20 characters before saving.";
        return;
      }
      const first={key,kind:"first",uid:record.uid,revision:record.revision_sha256,
        full_revision:full,academic_admission:"HOLD",first_response:answer,
        saved_at:new Date().toISOString()};
      if(!write(key,first)){
        receipt.textContent="HOLD · Browser storage unavailable or this first response already exists.";
        receipt.dataset.status="SAVE_FAILED";
        save.disabled=true;return;
      }
      committed();
    });
    buttons.forEach((button,i)=>{
      button.addEventListener("click",()=>{
        if(button.disabled||!read(key,record,"first",full))return;
        const panel=stage(i+3,seq[i][0]);
        if(i===0){
          panel.append(make("p","Authored, unreviewed explanation. Check each step against your independent answer."));
          const list=make("ol");
          for(const explanation of record.steps){
            const li=make("li",explanation);list.append(li);
          }
          panel.append(list);
        }else if(i===1||i===2){
          panel.append(make("p",seq[i][1]));
        }else{
          panel.append(make("p",record.boundary));
          const answer=make("textarea");answer.rows=3;
          answer.setAttribute("aria-label","Unseen boundary answer");
          answer.placeholder="Explain the changed assumption and resulting conclusion.";
          const next=make("button","Save boundary response");next.type="button";
          const reveal=make("button","Show authored boundary explanation");
          reveal.type="button";reveal.disabled=true;
          const note=make("p","Boundary answer not yet saved.");
          note.setAttribute("role","status");
          panel.append(answer,next,reveal,note);
          const bKey=storeKey(full,record,"boundary");
          const prev=read(bKey,record,"boundary",full);
          function boundarySaved(){
            answer.disabled=true;next.disabled=true;reveal.disabled=false;
            note.textContent="Independent boundary response saved for this revision.";
          }
          if(prev){answer.value=prev.first_response;boundarySaved();}
          next.addEventListener("click",()=>{
            if(answer.value.trim().length<20){
              note.textContent="Write at least 20 characters of boundary reasoning first.";return;
            }
            const state={key:bKey,kind:"boundary",uid:record.uid,
              revision:record.revision_sha256,full_revision:full,
              academic_admission:"HOLD",first_response:answer.value.trim(),
              saved_at:new Date().toISOString()};
            if(!write(bKey,state)){
              note.textContent="HOLD · Boundary save failed; author explanation withheld.";
              next.disabled=true;return;
            }
            boundarySaved();
          });
          reveal.addEventListener("click",()=>{
            if(!read(bKey,record,"boundary",full))return;
            panel.append(make("p",record.boundaryAnswer));
            reveal.disabled=true;
          });
        }
        button.disabled=true;
        if(buttons[i+1])buttons[i+1].disabled=false;
      });
    });
  }
  async function main(){
    if(!root||!status||!slug||!/^[a-z0-9-]+$/.test(slug))
      throw Error("UNRECOGNIZED_AUTHOR_RECOVERY_MODULE");
    const response=await fetch(src,{cache:"no-store"});
    if(!response.ok)throw Error("AUTHOR_RECOVERY_MANIFEST_UNAVAILABLE");
    const raw=await response.text(),data=JSON.parse(raw);
    if(data.schema!=="grade9-independent-core1-recovery-journeys/v1"||
       data.author_authority!=="ORIGINAL_AUTHORED_TRANSFER_NOT_SOURCE_EXAM"||
       data.academic_admission!=="HOLD"||data.source_exam_admission!=="HOLD"||
       data.original_audited_module_count_recovered!==0||
       data.original_18_modules_still_on_hold!==18||
       data.supplemental_authored_skill_journeys!==18||
       !Array.isArray(data.items)||data.items.length!==18)
      throw Error("ORIGINAL_MODULE_AUTHORITY_OR_COUNT_MISMATCH");
    const seen=new Set();
    for(const item of data.items){
      if(seen.has(item.construction)||item.academic_admission!=="HOLD"||
         item.source_question_claim!==false||
         item.original_b1b7_audit_equivalence!==false||
         item.public_mode!=="SUPPLEMENTAL_TECHNICAL_ONLY"||
         item.source_origin!==data.author_authority||
         item.stages.join(",")!=="predict,attempt,reconstruct,diagnose,repair,boundary"||
         !/^[a-f0-9]{64}$/.test(item.revision_sha256)||
         !Array.isArray(item.steps)||item.steps.length!==3||
         item.publication_route!=="nsejs/"+item.subject.toLowerCase()+
           "/core1/recovery/"+item.slug+"/index.html")
        throw Error("AUTHOR_CONTENT_OR_SOURCE_QUALIFICATION_INVALID");
      const canonicalItem={...item};delete canonicalItem.revision_sha256;
      if(await hash(canonical(canonicalItem))!==item.revision_sha256)
        throw Error("AUTHORED_FULL_ITEM_HASH_MISMATCH");
      seen.add(item.construction);
    }
    if(seen.size!==18)throw Error("NONUNIQUE_AUTHOR_RECOVERY_IDS");
    const lesson=data.items.find(x=>x.slug===slug);
    if(!lesson||document.body.dataset.recoverySlug!==slug)
      throw Error("AUTHOR_RECOVERY_LESSON_NOT_FOUND");
    const full=await hash(raw);
    status.textContent="Supplemental authored six-stage skill repair verified. Historical original Core1A/B and academic admission still HOLD.";
    status.dataset.status="AUTHORED_TECHNICAL_ONLY";
    render(lesson,full);
  }
  main().catch(error=>failure(error.message||"AUTHOR_RECOVERY_UNAVAILABLE"));
})();