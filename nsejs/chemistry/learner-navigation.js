/* Single Chemistry C01-C14 learner navigation (author-created courses, not original exam admission). */
(() => {
 "use strict";
 const ownScript=document.currentScript;
 if(!ownScript?.src)return;
 const scriptBase=new URL(ownScript.src);
 const hub=new URL("index.html",scriptBase);
 const source=new URL("learner-navigation.v1.json",scriptBase);
 const style=new URL("learner-navigation.css",scriptBase);
 if(!document.querySelector('link[data-chemistry-journey]')){
   const link=document.createElement("link");link.rel="stylesheet";link.href=style.href;
   link.dataset.chemistryJourney="true";document.head.append(link);
 }
 const state=new WeakMap();
 const registry=fetch(source,{cache:"no-store"}).then(async response=>{
   if(!response.ok)throw Error("Chemistry chapter index HTTP "+response.status);
   const data=await response.json();
   if(data.schema!=="g9v41-chemistry-learner-navigation/v1"||data.units?.length!==14||
     data.units.reduce((n,u)=>n+u.subtopics.length,0)!==84)throw Error("Invalid Chemistry chapter registry");
   return data;
 });
 const node=(type,cls,content)=>{
   const element=document.createElement(type);if(cls)element.className=cls;
   if(content!==undefined)element.textContent=String(content);return element;
 };
 const link=(label,url,cls)=>{
   const element=node("a",cls,label);element.href=String(url);return element;
 };
 const slug=value=>String(value).replace(/[^a-z0-9-]/gi,"-").toLowerCase();
 function unitData(data,unit){
   return data.units.find(item=>item.id===unit)||null;
 }
 function destination(data,unit,subtopic,mode="study"){
   const row=unitData(data,unit);
   if(!row)throw Error("Unknown Chemistry unit: "+unit);
   const url=new URL(row.chapter_href,hub);
   if(row.reader==="preview"){
     if(subtopic)url.searchParams.set("subtopic",subtopic);
     if(mode==="practice")url.searchParams.set("mode","practice");
     if(subtopic)url.hash=(mode==="practice"?"practice-":"")+slug(subtopic);
   }else{
     url.searchParams.set("unit",unit);
     if(subtopic)url.searchParams.set("subtopic",subtopic);
     url.searchParams.set("mode",mode==="practice"?"practice":"study");
   }
   return url.href;
 }
 function examUrl(){
   const url=new URL("../core2/question-map.html",hub);
   if(location.origin===hub.origin&&location.href.length<1300)url.searchParams.set("return",location.href);
   url.hash="chemistry";return url.href;
 }
 function allSubtopics(data){
   return data.units.flatMap(u=>u.subtopics.map(s=>({...s,unit:u.id,unitTitle:u.title})));
 }
 function mount(host,unit,subtopic,mode){
   if(!host)return;
   const version=(state.get(host)||0)+1;state.set(host,version);
   return registry.then(data=>{
     if(state.get(host)!==version||!host.isConnected)return;
     const u=unitData(data,unit),idx=u?.subtopics.findIndex(s=>s.id===subtopic)??-1;
     if(!u||idx<0)return;
     host.querySelector(":scope > .chem-journey-nav")?.remove();
     const current=u.subtopics[idx],ordered=allSubtopics(data),n=ordered.findIndex(s=>s.id===subtopic);
     const nav=node("nav","chem-journey-nav");
     nav.setAttribute("aria-label","Chemistry lesson steps and next subtopic");
     const crumbs=node("div","chem-journey-crumbs");
     crumbs.append(link("NSEJS",new URL("../index.html",hub)));
     crumbs.append(node("span","","›"));
     crumbs.append(link("Chemistry chapters",hub.href));
     crumbs.append(node("span","","›"));
     crumbs.append(node("span","",u.id+" · "+current.title));nav.append(crumbs);
     const subtitle=node("p","chem-journey-context",u.id+" / "+current.id+" · Original Chemistry learning material");
     nav.append(subtitle);
     const steps=node("div","chem-journey-steps");
     const a=link("1 · Learn",destination(data,unit,subtopic,"study"),"chem-journey-step");
     const b=link("2 · Try it",destination(data,unit,subtopic,"practice"),"chem-journey-step");
     const c=link("3 · Exam practice / source status",examUrl(),"chem-journey-step chem-exam-link");
     if(mode==="practice")b.setAttribute("aria-current","step");
     else a.setAttribute("aria-current","step");
     steps.append(a,b,c);nav.append(steps);
     const guidance=node("p","chem-journey-scope","Core1A / Core1B are authored self-study; the question map lists identities and source status, not necessarily readable original exam questions.");
     nav.append(guidance);
     const help=node("details","chem-journey-help");
     help.append(node("summary","","Need more help?"));
     const support=node("div","chem-journey-help-inner");
     if(u.help.length)u.help.forEach(item=>support.append(link(item.label,new URL(item.href,hub))));
     else support.append(node("p","","Review this chapter's worked examples and misconception repair before trying another task."));
     help.append(support);nav.append(help);
     const neighbours=node("div","chem-journey-neighbours");
     if(n>0){const p=ordered[n-1];neighbours.append(link("‹ Previous · "+p.title,destination(data,p.unit,p.id),"chem-prev"));}
     else neighbours.append(node("span","chem-journey-edge","First Chemistry subtopic"));
     neighbours.append(link("Chapter list",hub.href+"#chem-chapters","chem-chapter-return"));
     if(n<ordered.length-1){const next=ordered[n+1];neighbours.append(link("Next · "+next.title+" ›",destination(data,next.unit,next.id),"chem-next"));}
     else neighbours.append(node("span","chem-journey-edge","End of Chemistry chapters"));
     nav.append(neighbours);
     host.prepend(nav);
   }).catch(error=>{console.warn("Chemistry navigation unavailable; original lesson remains usable",error);});
 }
 window.ChemLearnerNav=Object.freeze({
   registry, destination, examUrl,
   mountPreview:(article,unit,subtopic,mode)=>mount(article,unit,subtopic,mode||"study"),
   mountNative:(article,unit,subtopic,mode)=>mount(article,unit,subtopic,mode||"study")
 });
})();
