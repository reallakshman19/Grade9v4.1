import {pinnedJson} from "./pinned-assets.js";
import {recordStudyView} from "./protected-attempt-store.js";
import {startAssessment} from "./assessment-r2.js";
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
  s.setAttribute("viewBox","0 0 980 270");
  const [sx,sy]=fig.source,[mx,my]=fig.receiver,wall=fig.wall;
  if(!(sx<wall&&mx<wall&&sy!==my))throw Error("Invalid source/receiver wall geometry");
  const imageX=2*wall-sx;
  // Straight line from mirrored emitter (imageX,sy) to microphone (mx,my)
  // crosses the wall at R; identical angles follow from the reflection.
  const ry=sy+(my-sy)*(imageX-wall)/(imageX-mx);
  line(wall,18,wall,242,"#8e5836",5);text(wall+13,35,"Reflecting wall");
  line(sx,sy,mx,my,"#3e8e9b",4);
  line(sx,sy,wall,ry,"#b36f16",4);line(wall,ry,mx,my,"#b36f16",4);
  line(imageX,sy,wall,ry,"#8a7da9",3,"8,6");
  line(wall-80,ry,wall+65,ry,"#647e88",2,"4,5");
  for(const [x,y,t] of [[sx,sy,"S"],[mx,my,"M"],[wall,ry,"R"],[imageX,sy,"S′ virtual"]]){
   add("circle",{cx:x,cy:y,r:6,fill:t==="R"?"#b36f16":"#19627f"});text(x+10,y-10,t);
  }
  text(140,260,"Blue direct · orange reflected · dashed virtual ray and normal");
 }
 return s;
}
async function displayStudy(c){
 const prior=await recordStudyView(c.unit,c.revision);
 const s=c.study;mount.replaceChildren(note("Core1A teaching extension · original authored material · source/QRT/science independent review pending."),put(card(c.unit+" · "+c.title),el("p",s.phenomenon),el("p","Learning target: "+s.goal)));
 mount.append(paragraph("Study exposure: "+prior+" · no local record is not proof of a first viewing.","small"));
 const scientific=card("Build the warranted model");put(scientific,el("p",s.model),svgFigure(s.figure),el("p","Applicable conditions and limits: "+s.assumptions));mount.append(scientific);
 const work=card("Three different worked constructions");for(const ex of s.examples){const part=el("article",undefined,"stage");put(part,el("h3",ex.level),el("p","Question: "+ex.prompt),el("p","Reasoned solution: "+ex.solution),el("p","Independent check: "+ex.check));work.append(part);}mount.append(work);
 const misc=card("Detect and repair the tempting misconception");put(misc,el("p","Tempting claim: "+s.misconception.wrong),el("p","Repair: "+s.misconception.repair));mount.append(misc);
 const exit=card("Exit check before transfer"),details=el("details");put(details,el("summary","Reveal the worked reasoning"),el("p",s.exit.answer));put(exit,el("p",s.exit.prompt),details);mount.append(exit);
 mount.append(put(card("Apply this science to a different question"),el("p","The protected task requires a different reasoning choice. Its first answer is preserved locally before hints or reconstruction; it is not an authenticated paper question."),link("Open changed-condition Core1B", "./challenge.html?unit="+encodeURIComponent(c.unit),"action"),link("Return to this chapter","../learn/chapter.html?ph="+c.chapter,"action secondary")));
}
async function displaySources(){
 const register=(await pinnedJson("public-source-status.v2.json","g9v41-physics-source-status-public/v2")).body;
 if(register.count!==41||register.rows?.length!==41||register.academic_review!=="HOLD")throw Error("Public source register invalid: fail closed");
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
 if(!["study","challenge"].includes(mode)||!/^PH(?:01-M05|02-F04|07-02|08-08)$/.test(unit))throw Error("Unknown candidate unit");
 if(mode==="challenge")return await startAssessment({unit,mount});
 const data=(await pinnedJson("study-data.v2.json","g9v41-physics-core1a-study/v2")).body;
 const matches=data.units.filter(x=>x.unit===unit);
 if(matches.length!==1||data.status!=="AUTHOR_EXPOSED_CANDIDATE__ACADEMIC_HOLD")throw Error("Study revision mismatch");
 await displayStudy(matches[0]);
}catch(e){fail(String(e?.message||e));}}
init();
