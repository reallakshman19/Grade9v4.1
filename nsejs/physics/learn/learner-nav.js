/* Unified Physics learner bar for existing native lesson pages.
 * Navigation-only: does not modify question state, academic admission,
 * protected first attempt, lesson assets, stored revisions, or Core2 data. */
(function(){
"use strict";
const script=document.currentScript;
if(!script||!script.src||document.getElementById("g9-learner-nav"))return;
const root=new URL("../",script.src);
const catalogUrl=new URL("catalog.json",script.src);
function url(path){return new URL(path,root).href;}
function el(name,content){const n=document.createElement(name);if(content!==undefined)n.textContent=content;return n;}
function a(label,href,cls){const n=el("a",label);n.href=href;if(cls)n.className=cls;return n;}
function mount(nav){const target=document.querySelector("main");if(target&&target.parentElement)target.parentElement.insertBefore(nav,target);else{const head=document.querySelector("header");if(head)head.after(nav);else document.body.prepend(nav);}}
function simpleFallback(){if(document.getElementById("g9-learner-nav"))return;
 const bar=el("nav");bar.id="g9-learner-nav";bar.className="g9-study-nav";bar.setAttribute("aria-label","Physics learning navigation");
 bar.append(a("← Physics chapters",url("index.html#learn-physics")));mount(bar);}
function chapterUrl(ch,u){return url("learn/chapter.html?ph="+ch+(u?"#"+encodeURIComponent(u):""));}
function questionUrl(ch,unit){const v=new URL("index.html",root);v.searchParams.set("topic",ch.questionTopic);v.searchParams.set("from",ch.id);if(unit)v.searchParams.set("unit",unit);v.hash="topicWorkspace";return v.href;}
function devArchive(){
 // Preserve historical links, but do not make children select software versions.
 const old=[...document.querySelectorAll("a[href]")].filter(x=>{
  const u=new URL(x.href,location.href);
  return /\/core1\/ph01-(?:m0[1-8]|main)-r(?:31|32|41|42|43|44|45|46)\//.test(u.pathname);
 });
 if(!old.length)return;
 const section=el("details");section.className="g9-review-versions";
 const title=el("summary","Older learning versions · reviewer archive");section.append(title);
 const list=el("ul");
 for(const x of old){const li=el("li");li.append(a(x.textContent.trim()||"Historical version",x.href));list.append(li);
  // Hide only duplicate old-version choices; original href remains archived.
  x.hidden=true;x.setAttribute("aria-hidden","true");x.tabIndex=-1;
 }
 section.append(list);
 const parent=document.querySelector("main")||document.body;parent.append(section);
}
async function load(){
 try{
  const res=await fetch(catalogUrl.href,{cache:"no-store"});
  if(!res.ok)throw Error("catalog");
  const data=await res.json();
  if(data.schema!=="g9v41-physics-learner-catalog/v1"||!Array.isArray(data.chapters))throw Error("schema");
  const here=location.pathname;
  const matches=[];
  for(const ch of data.chapters){
   if(!ch.overview)continue;
   if(here===new URL(ch.overview,root).pathname)matches.push({ch,role:"overview",unit:null,index:-1});
   if(ch.preview&&here===new URL(ch.preview,root).pathname)matches.push({ch,role:"preview",unit:null,index:-1});
   if(ch.help&&here===new URL(ch.help,root).pathname)matches.push({ch,role:"help",unit:null,index:-1});
   ch.units.forEach((unit,index)=>{
    if(here===new URL(unit.learn,root).pathname)matches.push({ch,role:"learn",unit,index});
    if(here===new URL(unit.practice,root).pathname)matches.push({ch,role:"practice",unit,index});
   });
  }
  if(!matches.length){simpleFallback();return;}
  // Recovery routes may serve several chapters; use explicit context only.
  const from=new URLSearchParams(location.search).get("from");
  const match=matches.find(m=>m.role==="help"&&m.ch.id===from)||matches.find(m=>m.role!=="help")||matches[0];
  const {ch,role,unit,index}=match;
  const refId=unit?.id||new URLSearchParams(location.search).get("unit")||"";
  const nav=el("nav");nav.id="g9-learner-nav";nav.className="g9-study-nav";nav.setAttribute("aria-label","Physics learning navigation");
  const crumb=el("div");crumb.className="g9-study-crumbs";
  crumb.append(a("NSEJS",url("../index.html")),el("span","›"),a("Physics",url("index.html#learn-physics")),el("span","›"),a(ch.id+" · "+ch.title,chapterUrl(ch.id)),el("span","›"),el("span",unit?unit.id+" · "+(role==="learn"?"Learn":"Try it"):role==="help"?"Extra help":role==="preview"?"Practice preview":"Read chapter"));
  const actions=el("div");actions.className="g9-study-actions";
  actions.append(a("← Chapter",chapterUrl(ch.id,refId)));
  if(unit){
    const reading=a("1 · Learn",url(unit.learn));if(role==="learn")reading.setAttribute("aria-current","page");actions.append(reading);
    const practice=a("2 · Try it",url(unit.practice));if(role==="practice")practice.setAttribute("aria-current","page");actions.append(practice);
  }else if(role==="help"&&refId){
    const u=ch.units.find(x=>x.id===refId);
    if(u)actions.append(a("← Back to your lesson",url(u.learn)));
  }
  if(ch.questionTopic)actions.append(a("3 · Related questions",questionUrl(ch,refId)));
  if(ch.help&&role!=="help"){
    const h=new URL(ch.help,root);h.searchParams.set("from",ch.id);if(refId)h.searchParams.set("unit",refId);
    actions.append(a("? · Extra help",h.href));
  }
  if(unit){
    if(index>0)actions.append(a("← Previous subtopic",url(ch.units[index-1].learn)));
    if(role==="learn")actions.append(a("Next · Try it →",url(unit.practice),"g9-next"));
    else if(index+1<ch.units.length)actions.append(a("Next · "+ch.units[index+1].id+" →",url(ch.units[index+1].learn),"g9-next"));
    else actions.append(a("Chapter complete · Return →",chapterUrl(ch.id),"g9-next"));
  }
  nav.append(crumb,actions);
  const css=el("link");css.rel="stylesheet";css.href=new URL("learner-navigation.css",script.src).href;document.head.append(css);
  mount(nav);
  devArchive();
 }catch(e){simpleFallback();}
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",load,{once:true});else load();
})();
