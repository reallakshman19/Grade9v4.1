(()=>{"use strict";
function ensureSearchAssets(base,link){
 if(!document.querySelector('link[data-g9-search-css]')){
  const l=document.createElement('link');l.rel='stylesheet';l.setAttribute('data-g9-search-css','');l.href=link('css/site-search.css');document.head.appendChild(l);
 }
 if(!window.Grade9Search&&!document.querySelector('script[data-g9-search-js]')){
  const s=document.createElement('script');s.setAttribute('data-g9-search-js','');s.src=link('js/site-search.js');document.head.appendChild(s);
 }
}
function mount(){
 const entry=document.querySelector("script[data-grade9-nav]");if(!entry?.src)return;
 const base=new URL("./",entry.src),link=path=>new URL(path,base).href;
 ensureSearchAssets(base,link);
 if(document.getElementById("grade9-universal-nav")||document.querySelector("header.mast"))return;
 const here=location.pathname,architecture=/\/(?:architecture|docs)\//.test(here),examples=/\/batches\//.test(here),nsejs=/\/nsejs\//.test(here);
 const current=architecture?"architecture":nsejs?"nsejs":here.includes("/mathematics/")?"mathematics":here.includes("/chemistry/")?"chemistry":"physics";
 const host=document.createElement("div");host.id="grade9-universal-nav";const shadow=host.attachShadow({mode:"open"});
 const css=document.createElement("style");css.textContent=[
 ":host{all:initial;display:block;position:relative;z-index:5;font-family:system-ui,-apple-system,Segoe UI,sans-serif}",
 "*,*:before,*:after{box-sizing:border-box}",
 ".primary{background:#11364d;color:white;border-bottom:1px solid #2a6778}",
 ".primary-in,.context-in{width:min(1280px,calc(100% - 34px));margin:0 auto;display:flex;align-items:center;gap:14px;flex-wrap:wrap}",
 ".primary-in{min-height:58px;padding:7px 0}",
 ".brand{display:inline-flex;align-items:center;gap:9px;color:#fff;text-decoration:none;font-size:15px;font-weight:850;white-space:nowrap;margin-right:auto}",
 ".mark{display:grid;place-items:center;font-size:12px;background:#208e82;width:34px;height:34px;border-radius:9px}",
 ".subjects{display:flex;align-items:center;flex-wrap:wrap;gap:5px}",
 ".subjects a{color:#d7ecf3;text-decoration:none;font-size:13px;font-weight:700;border-radius:8px;padding:9px 13px;min-height:40px;display:inline-flex;align-items:center;gap:5px}",
 ".subjects a:hover,.subjects a[aria-current=page]{background:#b5e9dc;color:#16443f}",
 ".nav-search-btn{display:inline-flex;align-items:center;gap:7px;background:rgba(255,255,255,0.14);border:1px solid rgba(255,255,255,0.28);color:#fff;border-radius:8px;padding:7px 12px;font-size:13px;font-weight:750;cursor:pointer;min-height:38px;margin-left:4px;transition:all 0.15s ease}",
 ".nav-search-btn:hover{background:rgba(255,255,255,0.24);border-color:#fff}",
 ".nav-search-btn kbd{font-size:10px;background:rgba(0,0,0,0.3);border:1px solid rgba(255,255,255,0.22);border-radius:4px;padding:1px 5px;font-family:inherit}",
 ".context{background:#eaf5f5;border-bottom:1px solid #cce5e2;color:#215366}",
 ".context-in{min-height:40px;padding:5px 0;gap:7px 17px}",
 ".crumb{font-size:12px;font-weight:800;letter-spacing:.01em;color:#386c72;margin-right:auto;white-space:nowrap}",
 ".shortcuts{display:flex;align-items:center;gap:3px 9px;flex-wrap:wrap}",
 ".shortcuts a{display:inline-flex;align-items:center;text-decoration:none;font-size:12px;font-weight:750;color:#256274;border-radius:7px;padding:5px 10px;min-height:31px}",
 ".shortcuts a:hover,.shortcuts a[aria-current=page]{background:#caeae5;color:#164f4e}",
 "a:focus-visible,button:focus-visible{outline:3px solid #c9912f;outline-offset:2px}",
 "@media(max-width:900px){.primary-in,.context-in{width:calc(100% - 24px)}.subjects a{font-size:12px;padding:8px 10px}.context-in{gap:4px 12px}.crumb{width:100%;margin:0}.brand{font-size:14px}}",
 "@media(max-width:590px){.brand{width:100%;margin-right:0}.subjects{width:100%;justify-content:space-between}.subjects a{padding:7px 6px;font-size:11px}.nav-search-btn kbd{display:none}.context-in{padding-block:7px}.shortcuts a{font-size:11px;padding:5px 7px}}"
 ].join("");
 const primary=document.createElement("div");primary.className="primary";const top=document.createElement("div");top.className="primary-in";
 const brand=document.createElement("a");brand.className="brand";brand.href=link("index.html");const symbol=document.createElement("span");symbol.className="mark";symbol.textContent="G9";brand.append(symbol,document.createTextNode("Grade9"));top.append(brand);
 const nav=document.createElement("nav");nav.className="subjects";nav.setAttribute("aria-label","Subjects and architecture");
 for(const [key,label,destination] of [["physics","⚛ Physics","physics/index.html"],["mathematics","∑ Maths","mathematics/index.html"],["chemistry","⚗ Chemistry","chemistry/index.html"],["nsejs","🏆 NSEJS","nsejs/index.html"],["architecture","◇ Architecture","architecture/index.html"]]){
  const a=document.createElement("a");a.href=link(destination);a.textContent=label;if(current===key)a.setAttribute("aria-current","page");nav.append(a)
 }
 const sBtn=document.createElement("button");sBtn.type="button";sBtn.className="nav-search-btn";sBtn.setAttribute("data-g9-action","search");sBtn.title="Search Grade9 (Ctrl/⌘ K)";sBtn.innerHTML='🔍 <span>Search</span> <kbd>Ctrl K</kbd>';
 sBtn.onclick=()=>{if(window.Grade9Search&&window.Grade9Search.open){window.Grade9Search.open({scope:nsejs?"nsejs":"all"});}};
 nav.append(sBtn);
 top.append(nav);primary.append(top);shadow.append(css,primary);
 const context=document.createElement("div");context.className="context";const inside=document.createElement("div");inside.className="context-in";
 const crumb=document.createElement("span");crumb.className="crumb";crumb.textContent=architecture?"Architecture / Learning design":nsejs?(here.includes("/core1/")?"NSEJS / Core 1 Master Lessons":here.includes("/physics/")?"NSEJS / Physics Track":here.includes("/chemistry/")?"NSEJS / Chemistry Track":here.includes("/biology/")?"NSEJS / Biology Track":"NSEJS / Junior Science"):examples?"Physics / WPE / Examples":"Physics / Work, Power & Energy";inside.append(crumb);
 const shortcut=document.createElement("nav");shortcut.className="shortcuts";shortcut.setAttribute("aria-label",architecture?"Architecture resources":nsejs?"NSEJS track shortcuts":"WPE chapter shortcuts");
 const items=architecture?[["Guidebook","architecture/guidebook.html"],["Production checklist","architecture/production-checklist.html"],["Pipeline Flowchart","architecture/pipeline-flowchart.html"],["WPE chapter","physics/wpe/index.html"]]:nsejs?[["Hub","nsejs/index.html"],["Physics","nsejs/physics/index.html"],["Physics Q-Bank","nsejs/physics/question-bank.html"],["Core 1 Lessons","nsejs/physics/core1/index.html"],["Chemistry","nsejs/chemistry/index.html"],["Chemistry Q-Bank","nsejs/chemistry/question-bank.html"],["Biology","nsejs/biology/index.html"],["Biology Q-Bank","nsejs/biology/question-bank.html"],["Core 2 Map","nsejs/core2/index.html"]]:[["Chapter","physics/wpe/index.html"],["Learn","preview/physics-wpe.html"],["Learn → Challenge","physics/wpe/learn-challenge.html"],["Practice","preview/practice.html"],["Question Bank","physics/wpe/question-bank.html"],["Examples","preview/batches/index.html"],["My progress","preview/progress.html"]];
 for(const [label,destination] of items){const a=document.createElement("a");a.href=link(destination);a.textContent=label;if(here===new URL(destination,base).pathname)a.setAttribute("aria-current","page");shortcut.append(a)}
 inside.append(shortcut);context.append(inside);shadow.append(context);document.body.insertBefore(host,document.body.firstChild)
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",mount,{once:true});else mount();
})();