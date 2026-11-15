/* Stable PH05 route resolver; archived task state is never migrated or relabelled. */
export async function renderCanonicalPH05(mount,uid,role){
 const p=new URLSearchParams(location.search);
 if(p.has("task")||p.get("legacy")==="1"||uid==="PH05-MAIN")return false;
 const base=new URL("./source-led-r2/",import.meta.url);
 const response=await fetch(new URL("packages.v1.json",base),{cache:"no-store"});
 if(!response.ok)throw Error("Source-led package registry unavailable");
 const d=await response.json();if(d.release!=="HOLD")throw Error("Unexpected candidate release");
 const u=d.stable_subtopics.find(x=>x.id===uid);if(!u)throw Error("Unknown canonical syllabus identity");
 const el=(tag,text)=>{const n=document.createElement(tag);if(text)n.textContent=text;return n};
 const link=(text,params)=>{const n=el("a",text);n.className="action";const url=new URL("index.html",base);for(const [k,v] of Object.entries(params))url.searchParams.set(k,v);n.href=url.href;return n};
 mount.replaceChildren(el("h1",u.id+" · "+u.title),el("p","Original educational candidate · SOURCE/QRT/ACADEMIC HOLD · "+u.scope));
 for(const id of u.packages){const pack=d.packages.find(p=>p.id===id);if(!pack)throw Error("Missing package "+id);const s=el("section");s.append(el("h2",id+" · "+pack.title),el("p","Historical sources: "+pack.source_locators.join(", ")));if(role==="learn"){s.append(link("Learn this construction",{package:id,stage:"learn"}));for(const source of pack.source_locators)s.append(link("Original source checkpoint: "+source,{package:id,source}));}else{for(const t of pack.tasks)s.append(link(t.cell+" · "+t.uid,{package:id,task:t.uid}));}mount.append(s)}
 const a=el("a","Archived earlier candidate and its saved attempts (not current syllabus mapping)");a.href="?legacy=1";mount.append(a);
 document.title=u.id+" · "+u.title+" · "+(role==="learn"?"Core1A":"Core1B");
 const header=document.querySelector("header h1");if(header)header.textContent=u.id+" · "+u.title;
 return true;
}
