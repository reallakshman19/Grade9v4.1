/* Contextual Chemistry skill-repair return. No state writes or attempts touched.
 * Follow only a same-origin, allowlisted C01-C14 learner route. */
(function(){
  "use strict";
  const script=document.currentScript;
  if(!script?.src)return;
  const chemistryRoot=new URL("./",script.src);
  const repoRoot=new URL("../../",chemistryRoot);
  const previewRoot=new URL("curriculum/chemistry/preview/",repoRoot);
  const native=new URL("textbook/index.html",chemistryRoot);
  const raw=new URL(location.href).searchParams.get("return");
  if(!raw||raw.length>1200||/[\u0000-\u001f\\]/.test(raw))return;
  let target;
  try{target=new URL(raw,location.href)}catch(_){return}
  if(target.origin!==location.origin||target.username||target.password)return;
  const asNative=target.pathname===native.pathname;
  const previewMatch=target.pathname.startsWith(previewRoot.pathname)
    ?target.pathname.slice(previewRoot.pathname.length).match(/^(C0[1-7])\.html$/):null;
  if(!asNative&&!previewMatch)return;
  const sub=target.searchParams.get("subtopic");
  const mode=target.searchParams.get("mode");
  if(mode&&!["study","practice"].includes(mode))return;
  if(asNative){
    const unit=target.searchParams.get("unit");
    if(!/^C(?:0[8-9]|1[0-4])$/.test(unit||""))return;
    if(sub&&!new RegExp("^CHEM-"+unit+"\\.\\d{2}$").test(sub))return;
  }else if(sub&&!new RegExp("^CHEM-"+previewMatch[1]+"\\.\\d{2}$").test(sub))return;
  const nav=document.createElement("nav");
  nav.className="chem-recovery-return";
  nav.setAttribute("aria-label","Return to your Chemistry lesson");
  const back=document.createElement("a");
  back.href=target.href;
  back.textContent="← Return to my exact Chemistry lesson";
  nav.appendChild(back);
  const note=document.createElement("p");
  note.style.fontSize=".85rem";
  note.style.margin="4px 0 0";
  note.textContent="Extra help is optional. Your saved first attempts remain in their original lesson.";
  nav.appendChild(note);
  const main=document.querySelector("main");
  if(main)main.prepend(nav);
  else(document.querySelector("header")||document.body.firstElementChild)?.after(nav);
  const css=document.createElement("link");
  css.rel="stylesheet";
  css.href=new URL("learner-navigation.css",chemistryRoot).href;
  document.head.appendChild(css);
})();
