/* Preserve historic question-bank deep links while making chapters the default learner entrypoint. */
(function(){
"use strict";
function init(){
  const bank=document.getElementById("g9-explore-bank");
  if(!bank)return;
  const q=new URLSearchParams(location.search);
  const hash=location.hash;
  const hasBankQuery=["topic","q","exam","difficulty","sort"].some(k=>q.has(k));
  if(hasBankQuery||/^#(?:question-|topicWorkspace|topic-view|questions|qb-)/.test(hash)||hash==="#g9-explore-bank"){
    bank.open=true;
  }
  const ph=q.get("from");
  if(ph && /^PH(?:0[1-9]|1[0-2])$/.test(ph) && (hasBankQuery||hash)){
    const target=new URL("learn/chapter.html",location.href);
    target.searchParams.set("ph",ph);
    const unit=q.get("unit");
    if(unit && /^(?:M|F)\d{2}$|^PH\d{2}-\d{2}$/.test(unit))target.hash=unit;
    const a=document.createElement("a");
    a.className="g9-bank-return";
    a.href=target.href;
    a.textContent="← Return to "+ph+" learning";
    const body=bank.querySelector(".g9-bank-archive-body");
    if(body)body.prepend(a);
  }
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init,{once:true});
else init();
})();
