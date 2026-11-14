/* Learner chapter renderer: links only to published, catalogued routes; no academic admission. */
(function(){
"use strict";
const mount=document.getElementById("g9-chapter-content"),crumb=document.getElementById("g9-chapter-crumb");
const ph=new URLSearchParams(location.search).get("ph")||"";
const root=new URL("../",location.href);
function tag(name,content,cls){const el=document.createElement(name);if(content!==undefined)el.textContent=content;if(cls)el.className=cls;return el;}
function add(parent,...nodes){nodes.forEach(n=>parent.append(n));return parent;}
function link(label,path,cls){const a=tag("a",label,cls);a.href=new URL(path,root).href;return a;}
function chapterLink(label,chapter,hash){const a=tag("a",label);a.href="chapter.html?ph="+chapter+(hash?"#"+encodeURIComponent(hash):"");return a;}
function resources(c){
  const r=tag("section",undefined,"g9-chapter-resources");
  add(r,tag("h2","Other ways to learn"));
  if(c.overview)add(r,link("Read the complete chapter",c.overview));
  if(c.questionTopic){const a=tag("a","Explore related candidate questions");a.href="../index.html?topic="+encodeURIComponent(c.questionTopic)+"&from="+c.id+"#topicWorkspace";r.append(a);}
  if(c.help){const a=link("Need more help? · Focused skill repair",c.help,"g9-secondary");a.search="?from="+c.id; r.append(a);}
  if(c.preview)add(r,link("Try available practice preview",c.preview,"g9-secondary"));
  add(r,tag("p","Question-bank topics are broader than this chapter. A related question is not evidence of exact exam-question coverage."));
  return r;
}
async function init(){
 if(!/^PH(?:0[1-9]|1[0-2])$/.test(ph)){mount.replaceChildren(tag("p","No valid Physics chapter selected."),link("Open Physics chapters","index.html"));return;}
 try{
 const res=await fetch("catalog.json",{cache:"no-store"});if(!res.ok)throw Error("Catalog unavailable");
 const data=await res.json();if(data.schema!=="g9v41-physics-learner-catalog/v1"||data.candidate_only!==true||!Array.isArray(data.chapters))throw Error("Catalog invalid");
 const chapter=data.chapters.find(c=>c.id===ph);if(!chapter)throw Error("Unknown chapter");
 document.title=chapter.id+" · "+chapter.title+" — NSEJS Physics";
 crumb.textContent=chapter.id;
 const head=tag("header",undefined,"g9-chapter-head");
 add(head,tag("p",chapter.id+" · Physics learning chapter"),tag("h1",chapter.title));
 add(head,tag("p",chapter.state==="learning-pairs"?"Choose one subtopic. Read its explanation before attempting its independent questions.":chapter.state==="chapter-preview"?"This chapter has reading material and an earlier practice preview. Dedicated subtopic pairs are not yet available.":"The planned chapter exists in the coverage inventory, but a native lesson route has not been published."));
 mount.replaceChildren(head);
 if(chapter.state==="unavailable"){
 const p=tag("section",undefined,"g9-chapter-unavailable");
 add(p,tag("h2","Not available yet"),tag("p","No learner page or exam preparation is presented as completed for this chapter."),chapterLink("← Back to chapter list","PH01"));
 const a=link("← All Physics chapters","index.html");a.href="../index.html#learn-physics";p.replaceChild(a,p.lastChild);mount.append(p);
 }else if(chapter.state==="chapter-preview"){
  mount.append(resources(chapter));
 }else{
  mount.append(tag("p","1 · Learn an idea   →   2 · Try it independently   →   3 · Explore related question candidates","g9-chapter-flow"));
  const grid=tag("section",undefined,"g9-chapter-lesson-grid");
  grid.setAttribute("aria-label",chapter.id+" subtopic learning choices");
  chapter.units.forEach((u,i)=>{
   const card=tag("article",undefined,"g9-lesson-card");card.id=u.id;
   const title=tag("h2",(i+1)+". "+u.title);const code=tag("p",u.id+" · Original authored lesson · academic qualification pending");
   const actions=tag("div",undefined,"g9-lesson-actions");
   add(actions,link("1 · Learn",u.learn),link("2 · Try it",u.practice,"g9-secondary"));
   add(card,title,code,actions);grid.append(card);
  });
  mount.append(grid,resources(chapter));
 }
 const note=tag("p","All authored materials and question associations retain SOURCE / QRT / B1–B7 HOLD. Passing software tests does not authenticate an NSEJS exam question.","g9-hold-note");mount.append(note);
 const foot=tag("nav",undefined,"g9-chapter-crumbs");foot.setAttribute("aria-label","Chapter navigation");
 const i=data.chapters.findIndex(c=>c.id===ph);
 if(i>0)add(foot,chapterLink("← "+data.chapters[i-1].id,data.chapters[i-1].id));
 add(foot,link("All Physics chapters","index.html"));
 foot.lastChild.href="../index.html#learn-physics";
 if(i<data.chapters.length-1)add(foot,chapterLink(data.chapters[i+1].id+" →",data.chapters[i+1].id));
 mount.append(foot);
 if(location.hash){let id=decodeURIComponent(location.hash.slice(1));const el=document.getElementById(id);if(el)requestAnimationFrame(()=>el.scrollIntoView({block:"start"}));}
 }catch(e){mount.replaceChildren(tag("p","The chapter menu could not be verified. No alternative lesson or exam claim has been substituted."),link("Return to Physics chapters","index.html"));mount.lastChild.href="../index.html#learn-physics";}
}
init();
})();
