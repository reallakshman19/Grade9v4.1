/* Four-chapter R1 educational candidate reader. Original exam, QRT and B1–B7 HOLD.
   Browser-local attempt ordering is NOT tamper-proof proctoring. No eval or external APIs. */
const ROOT = new URL("../../../", import.meta.url);
const mount = document.querySelector("#quality-root");
const mode = document.body.dataset.mode;
const unit = new URLSearchParams(location.search).get("unit") || "";
const chapter = new URLSearchParams(location.search).get("ph") || "";
const el=(tag,text,cls)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=String(text);if(cls)n.className=cls;return n;};
const put=(parent,...children)=>{for(const c of children)parent.append(c);return parent;};
const card=(title)=>put(el("section",undefined,"card"),el("h2",title));
const field=(label,id)=>{const block=el("div");const l=el("label",label);l.htmlFor=id;const t=el("textarea");t.id=id;put(block,l,t);return block};
const link=(text,href,cls="")=>{const a=el("a",text,cls);a.href=href;return a};
const btn=(label,action,cls="")=>{const b=el("button",label,cls);b.type="button";b.addEventListener("click",action);return b};
const note=(t)=>el("p",t,"notice");
const fail=(t)=>{mount.replaceChildren(el("p","HOLD · "+t,"error"),link("Physics chapter list","../index.html#learn-physics"))};
const SHA=async v=>{if(!crypto?.subtle||typeof TextEncoder==="undefined")throw Error("Browser digest unavailable");const bytes=new TextEncoder().encode(v);const h=await crypto.subtle.digest("SHA-256",bytes);return [...new Uint8Array(h)].map(x=>x.toString(16).padStart(2,"0")).join("")};
const gitBlobSha=async raw=>{
 const data=new TextEncoder().encode(raw);
 const header=new TextEncoder().encode("blob "+data.length+String.fromCharCode(0));
 const body=new Uint8Array(header.length+data.length);body.set(header);body.set(data,header.length);
 const digest=await crypto.subtle.digest("SHA-1",body);
 return [...new Uint8Array(digest)].map(b=>b.toString(16).padStart(2,"0")).join("");
};
function svgFigure(fig){
 const ns="http://www.w3.org/2000/svg",s=document.createElementNS(ns,"svg");
 const add=(tag,attrs,content)=>{const n=document.createElementNS(ns,tag);for(const [k,v] of Object.entries(attrs))n.setAttribute(k,String(v));if(content!==undefined)n.textContent=content;s.append(n);return n};
 s.setAttribute("viewBox","0 0 640 270");s.setAttribute("role","img");s.setAttribute("class","figure");
 s.setAttribute("aria-label",fig.caption||"Scientific construction: "+fig.kind);
 const line=(x1,y1,x2,y2,stroke="#296e88",width=3,dash="")=>add("line",{x1,y1,x2,y2,stroke,"stroke-width":width,...(dash?{"stroke-dasharray":dash}:{})});
 const text=(x,y,t)=>add("text",{x,y,"font-size":17,fill:"#123f58"},t);
 if(fig.kind==="position"){
  line(65,225,605,225);line(65,225,65,25);text(440,253,fig.xLabel);text(12,24,fig.yLabel);
  const pts=fig.points.map(([t,x])=>[65+t*67,225-x*20]);for(let i=1;i<pts.length;i++)line(...pts[i-1],...pts[i],"#0d7785",4);for(const [i,p] of pts.entries()){add("circle",{cx:p[0],cy:p[1],r:5,fill:"#b25b10"});text(p[0]+7,p[1]-12,"("+fig.points[i].join(", ")+")")}
 } else if(fig.kind==="force"){
  add("rect",{x:95,y:95,width:145,height:72,rx:11,fill:"#e7eef6",stroke:"#315b72"});add("rect",{x:385,y:95,width:145,height:72,rx:11,fill:"#e6f4e9",stroke:"#315b72"});
  text(140,139,fig.left);text(430,139,fig.right);
  line(250,114,372,114,"#b35b10",4);line(377,154,250,154,"#b35b10",4);text(255,92,"A on B →");text(253,181,"← B on A");text(68,56,fig.above);text(410,211,fig.below);
 } else if(fig.kind==="thermal"){
  add("rect",{x:245,y:85,width:155,height:110,rx:12,fill:"#deeff0",stroke:"#14647c"});text(280,142,fig.centre);
  line(65,139,238,139,"#b26713",6);line(410,139,590,139,"#b26713",6);
  text(76,110,fig.left+" →");text(453,110,"→ "+fig.right);text(95,242,"Energy conservation: ΔU = (P in − P out) Δt");
 } else if(fig.kind==="echo"){
  line(505,30,505,231,"#8e5836",6);text(512,45,"wall");
  add("circle",{cx:155,cy:194,r:7,fill:"#19627f"});add("circle",{cx:344,cy:194,r:7,fill:"#19627f"});
  text(127,222,"source S");text(319,222,"mic M");
  line(155,194,344,194,"#3e8e9b",3);line(155,194,505,95,"#b36f16",4);line(505,95,344,194,"#b36f16",4);
  text(148,255,"Direct path: blue · reflected path: orange");
 }
 return s;
}
function displayStudy(c){
 const s=c.study;mount.replaceChildren(note("Core1A teaching extension · original authored material · source/QRT/science independent review pending."),put(card(c.unit+" · "+c.title),el("p",s.phenomenon),el("p","Learning target: "+s.goal)));
 const scientific=card("Build the warranted model");put(scientific,el("p",s.model),svgFigure(s.figure),el("p","Applicable conditions and limits: "+s.assumptions));mount.append(scientific);
 const work=card("Three different worked constructions");for(const ex of s.examples){const part=el("article",undefined,"stage");put(part,el("h3",ex.level),el("p","Question: "+ex.prompt),el("p","Reasoned solution: "+ex.solution),el("p","Independent check: "+ex.check));work.append(part);}mount.append(work);
 const misc=card("Detect and repair the tempting misconception");put(misc,el("p","Tempting claim: "+s.misconception.wrong),el("p","Repair: "+s.misconception.repair));mount.append(misc);
 const exit=card("Exit check before transfer"),details=el("details");put(details,el("summary","Reveal the worked reasoning"),el("p",s.exit.answer));put(exit,el("p",s.exit.prompt),details);mount.append(exit);
 mount.append(put(card("Apply this science to a different question"),el("p","The protected task requires a different reasoning choice. Its first answer is preserved locally before hints or reconstruction; it is not an authenticated paper question."),link("Open changed-condition Core1B", "./challenge.html?unit="+encodeURIComponent(c.unit),"action"),link("Return to this chapter","../learn/chapter.html?ph="+c.chapter,"action secondary")));
}
async function displayChallenge(c){
 const q=c.challenge,fingerprint=await SHA(JSON.stringify([c.revision,c.source_revision_blob,q.uid,q.prediction,q.prompt,q.boundaryPrompt,c.model_blob]));
 let model=null,modelError="";
 async function loadPostAttemptModel(){
   if(model)return true;
   try{
     if(c.model_file!=="postattempt-models.v1.json"||!/^[0-9a-f]{40}$/.test(c.model_blob))throw Error("Model source reference invalid");
     const response=await fetch("./"+c.model_file,{cache:"no-store"});
     if(!response.ok)throw Error("Post-attempt model unavailable");
     const raw=await response.text();
     if(await gitBlobSha(raw)!==c.model_blob)throw Error("Post-attempt model revision mismatch");
     const payload=JSON.parse(raw);
     if(payload.schema!=="g9v41-four-physics-postattempt-models/v1"||payload.status!=="AUTHOR_EXPOSED_CANDIDATE__ACADEMIC_HOLD"||payload.units?.length!==4)throw Error("Post-attempt model schema mismatch");
     const matching=payload.units.filter(x=>x.uid===q.uid&&x.revision===c.revision&&x.unit===c.unit);
     if(matching.length!==1||matching[0].hints?.length!==2||!matching[0].reconstruct||!matching[0].diagnosis||!matching[0].repair||!matching[0].boundaryModel)throw Error("Model and saved attempt mismatch");
     model=matching[0];
     return true;
   }catch(e){modelError=String(e?.message||e);return false}
 }
 const key="G9V41:QUALITY-R1:"+q.uid+":"+c.revision+":"+fingerprint, preKey=key+":prehelp";
 let record=null,storageError=false;
 try{const test=key+":probe";localStorage.setItem(test,"yes");if(localStorage.getItem(test)!=="yes")throw Error("Storage readback failed");localStorage.removeItem(test);
  const raw=localStorage.getItem(key);if(raw){record=JSON.parse(raw);if(record.uid!==q.uid||record.fingerprint!==fingerprint||!record.first?.answer||!record.first?.prediction||!Array.isArray(record.exposures))throw Error("Stored attempt content identity invalid");}
 }catch(e){storageError=true}
 function persist(next){try{const raw=JSON.stringify(next);localStorage.setItem(key,raw);if(localStorage.getItem(key)!==raw)throw Error("readback mismatch");record=next;return true;}catch(e){storageError=true;draw();return false}}
 function exposure(kind,fields={}){return persist({...record,...fields,exposures:[...record.exposures,{kind,at:new Date().toISOString()}]})}
 function section(title){const s=card(title);s.classList.add("stage");return s}
 function promptBlock(parent,prompt,label,id){put(parent,el("p",prompt),field(label,id));}
 function draw(){
  mount.replaceChildren(note("Core1B · authored candidate, not a past NSEJS question or a mastery award. Local browser evidence is learner-editable, not tamper-proof."),el("p","Question ID: "+q.uid+" · revision: "+c.revision+" · content SHA-256: "+fingerprint.slice(0,16),"small"));
  const nav=card("Navigation and review context");
  const back=link("Core1A teaching and worked examples","./study.html?unit="+encodeURIComponent(c.unit),"action secondary");
  back.addEventListener("click",ev=>{if(!record?.first){try{localStorage.setItem(preKey,"opened");if(localStorage.getItem(preKey)!=="opened")throw Error("cannot record help")}catch(e){ev.preventDefault();fail("Cannot record pre-attempt help exposure; navigation blocked.");}}else{if(!exposure("linked_study_after_first"))ev.preventDefault();}});
  put(nav,back,link("Chapter overview","../learn/chapter.html?ph="+c.chapter,"action secondary"),el("p","Learning skill: "+c.adapter.reason),el("p","Why this task differs from teaching: "+q.transfer_difference));mount.append(nav);
  if(storageError){mount.append(el("p","HOLD: local storage/digest/record verification failed. No first-attempt or staged-help claim is possible. Record your reasoning outside this page if needed.","error"));return}
  const s1=section("Stage 1 · Predict before solving");put(s1,el("p",q.prediction));if(!record?.first){s1.append(field("Initial prediction and reason (at least 10 characters)","prediction"));}else s1.append(el("p",record.first.prediction));mount.append(s1);
  const s2=section("Stage 2 · Attempt independently");put(s2,el("p",q.prompt));
  if(!record?.first){put(s2,field("Show a reasoned, checked construction (at least 40 characters)","answer"),btn("Save protected first prediction + attempt",async ()=>{
    const p=document.querySelector("#prediction").value.trim(),a=document.querySelector("#answer").value.trim();if(p.length<10||a.length<40){alert("A prediction and at least 40 characters of reasoning are required; a selected answer alone is insufficient.");return}
    const preHelp=localStorage.getItem(preKey)==="opened";const next={uid:q.uid,revision:c.revision,fingerprint,first:{prediction:p,answer:a,at:new Date().toISOString()},exposures:preHelp?[{kind:"linked_study_before_first",at:new Date().toISOString()}]:[],hintCount:0,reconstruction:false,diagnosis:null,repair:null,boundary:null,boundaryModel:false};
    if(persist(next)){draw();if(await loadPostAttemptModel())draw();else draw();}
  }));}else{put(s2,el("p","Original first response, saved separately and not overwritable by this page:","ok"),el("blockquote",record.first.answer),el("p","Saved "+record.first.at+"; help exposure events: "+(record.exposures.map(x=>x.kind).join(", ")||"none"),"small"));}
  mount.append(s2);
  if(!record?.first){mount.append(el("p","Stages 3–6 are locked until the first prediction and independent reasoning have been saved. Assessment models are not requested before commitment.","small"));return;}
  if(modelError){mount.append(el("p","HOLD: post-attempt model unavailable or mismatched: "+modelError,"error"));return;}
  if(!model){mount.append(el("p","Loading checked post-attempt feedback…","small"));return;}
  const help=section("Optional orientation support · only after first attempt");
  for(let i=0;i<record.hintCount;i++)help.append(el("p","H"+(i+1)+": "+model.hints[i]));
  if(record.hintCount<model.hints.length)help.append(btn("Reveal H"+(record.hintCount+1),()=>{if(exposure("H"+(record.hintCount+1),{hintCount:record.hintCount+1}))draw()},"secondary"));
  mount.append(help);
  const s3=section("Stage 3 · Reconstruct the decisive route");
  if(!record.reconstruction)s3.append(btn("Reveal model after your saved first attempt",()=>{if(exposure("reconstruction",{reconstruction:true}))draw()},"secondary"));
  else s3.append(el("p",model.reconstruct));mount.append(s3);if(!record.reconstruction)return;
  const s4=section("Stage 4 · Diagnose first divergence");
  put(s4,el("p",model.diagnosis));
  if(!record.diagnosis){put(s4,field("My first invalid assumption, or the evidence still needed","diagnosis"),btn("Record diagnosis",()=>{const v=document.querySelector("#diagnosis").value.trim();if(v.length<20){alert("Explain the first reasoning divergence in at least 20 characters.");return}if(exposure("diagnosis",{diagnosis:v}))draw()}));}else s4.append(el("p","Recorded diagnosis: "+record.diagnosis));
  mount.append(s4);if(!record.diagnosis)return;
  const s5=section("Stage 5 · Repair the construction");put(s5,el("p",model.repair));
  if(!record.repair){put(s5,field("My repaired, checked route","repair"),btn("Save separate repaired reasoning",()=>{const v=document.querySelector("#repair").value.trim();if(v.length<30){alert("Explain the repaired route in at least 30 characters.");return}if(exposure("repair",{repair:v}))draw()}));}else s5.append(el("p","Saved repair: "+record.repair));mount.append(s5);if(!record.repair)return;
  const s6=section("Stage 6 · Boundary: unseen changed condition");put(s6,el("p",q.boundaryPrompt));
  if(!record.boundary){put(s6,field("My independent changed-condition attempt","boundary"),btn("Commit boundary attempt",()=>{const v=document.querySelector("#boundary").value.trim();if(v.length<30){alert("Explain the changed condition in at least 30 characters.");return}if(exposure("boundary_attempt",{boundary:v}))draw()}));}
  else{put(s6,el("p","Saved boundary attempt: "+record.boundary));if(!record.boundaryModel)s6.append(btn("Reveal boundary model only after attempt",()=>{if(exposure("boundary_model",{boundaryModel:true}))draw()},"secondary"));else s6.append(el("p","Conditional worked boundary reasoning: "+model.boundaryModel));}
  mount.append(s6);
 }
 if(record?.first)await loadPostAttemptModel();
 draw();
}
async function displaySources(){
 const src=new URL("../../../review/physics/ph01-ph02-ph07-ph08-r00/PHYSICS_41_ROUTE_AND_QUALITY_GATE_R00.v1.json",import.meta.url);
 const res=await fetch(src,{cache:"no-store"});if(!res.ok)throw Error("Source and qualification register unavailable");
 const register=await res.json();if(register.counts?.subtopic_rows!==41||register.rows?.length!==41)throw Error("Scope register invalid: fail closed");
 const records=chapter?register.rows.filter(x=>x.chapter===chapter):register.rows;
 if(chapter&&!["PH01","PH02","PH07","PH08"].includes(chapter))throw Error("Unsupported chapter filter");
 mount.replaceChildren(note("This is an evidence ledger, not a Core2 exam question bank. No original examination stem, figure or key has been independently authenticated and admitted within this four-chapter audit. Do not infer coverage from a link."));
 const summary=card("Evidence disposition · "+(chapter||"four selected chapters"));
 put(summary,el("p",records.length+" published candidate Core1A/Core1B route pairs; zero original-question admissions and zero independently qualified B1–B7 units."),el("p","PH07/PH08 inspected B01 bank: 17 unmatched subtopics, 6 supporting-only and 2 related producer candidates on HOLD."));mount.append(summary);
 const table=el("table"),thead=el("thead"),tr=el("tr");for(const h of ["Subtopic","Evidence relationship","Learning route","Revision-aware practice"])tr.append(el("th",h));thead.append(tr);table.append(thead);const tbody=el("tbody");
 const humanRelation={SOURCE_LOCATOR_CANDIDATE_HOLD:"Exam paper locators are under review; no authenticated question yet",AUTHORED_TRANSFER_NO_AUTHENTICATED_EXAM:"Original authored practice; no authenticated exam item",NO_MATCH_IN_INSPECTABLE_BANK:"No matching question found in inspected candidate bank",PRIMARY_RELATED_CANDIDATE_HOLD:"A related candidate exists, but it has not been authenticated",SUPPORTING_PREREQUISITE_ONLY:"A related prerequisite only, not a direct examination question"};
 for(const r of records){const row=el("tr");put(row,el("td",r.subtopic_id+" · "+r.title),el("td",(humanRelation[r.source_relation]||"Source mapping under review")+" · examination admission HOLD"));const a=el("td");a.append(link("Read existing candidate lesson",new URL("../../../"+r.core1a_path,import.meta.url).href));const b=el("td");b.append(link("Existing Core1B",new URL("../../../"+r.core1b_path,import.meta.url).href));if(["PH01-M05","PH02-F04","PH07-02","PH08-08"].includes(r.subtopic_id))put(b,el("span"," · "),link("New operation-led construction","./study.html?unit="+r.subtopic_id));put(row,a,b);tbody.append(row);}table.append(tbody);mount.append(put(el("div",undefined,"card scroll"),table));if(chapter)mount.append(link("Return to chapter","../learn/chapter.html?ph="+chapter,"action"));
}
async function init(){try{
 if(mode==="source")return await displaySources();
 if(!["study","challenge"].includes(mode)||!/^PH(?:01-M05|02-F04|07-02|08-08)$/.test(unit))throw Error("Unrecognized chapter/unit; no unrelated substitute");
 const asset=mode==="study"?"study-data.v1.json":"attempt-prompts.v1.json";
 const expected=mode==="study"?"g9v41-four-physics-core1a-study-only/v1":"g9v41-four-physics-core1b-attempt-prompts/v1";
 const res=await fetch("./"+asset,{cache:"no-store"});if(!res.ok)throw Error("Qualification learning manifest unavailable");
 const j=await res.json();if(j.schema!==expected||j.status!=="AUTHOR_EXPOSED_CANDIDATE__ACADEMIC_HOLD"||j.units?.length!==4)throw Error("Learning package invalid or version-mismatched");
 const matches=j.units.filter(x=>x.unit===unit);
 if(matches.length!==1||matches[0].source.original_exam_admission!=="HOLD"||matches[0].source.role!=="AUTHORED_TRANSFER"||matches[0].adapter.status!=="AUTHOR_PROPOSED_UNSCORED")throw Error("Source or adapter qualification boundary invalid");
 if(mode==="study")displayStudy(matches[0]);
 else{
   if(j.postattempt_model_path!=="postattempt-models.v1.json"||!/^[0-9a-f]{40}$/.test(j.postattempt_model_git_blob)||!/^[0-9a-f]{40}$/.test(j.source_package_git_blob))throw Error("Pinned source and post-attempt model revisions required");
   matches[0].source_revision_blob=j.source_package_git_blob;
   matches[0].model_file=j.postattempt_model_path;
   matches[0].model_blob=j.postattempt_model_git_blob;
   await displayChallenge(matches[0]);
 }
}catch(e){fail(String(e?.message||e));}}
init();
