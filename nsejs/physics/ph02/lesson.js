/* PH02 Core1A candidate renderer: original content, source/QRT academic HOLD. */
const el=document.querySelector("[data-ph02-lesson]");
const uid=el?.dataset.unit;
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const p=s=>"<p>"+esc(s)+"</p>";
function figure(u){
 const title=esc(u.figure.caption);
 const base='viewBox="0 0 660 240" role="img" aria-label="'+title+'" xmlns="http://www.w3.org/2000/svg"';
 const defs='<defs><marker id="arrow" markerWidth="9" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0 0 L9 4 L0 8 Z" fill="#186d86"/></marker></defs>';
 const line=(x1,y1,x2,y2)=>'<line x1="'+x1+'" y1="'+y1+'" x2="'+x2+'" y2="'+y2+'" stroke="#186d86" stroke-width="5" marker-end="url(#arrow)"/>';
 const text=(x,y,v)=>'<text x="'+x+'" y="'+y+'" font-size="18" fill="#123f56" font-family="system-ui">'+esc(v)+'</text>';
 let shapes='';
 switch(u.figure.kind){
 case "bus":
   shapes='<rect x="155" y="100" width="370" height="92" rx="12" fill="#d5eaf2" stroke="#1d536a" stroke-width="3"/><circle cx="215" cy="198" r="17" fill="#38576a"/><circle cx="465" cy="198" r="17" fill="#38576a"/><rect x="270" y="111" width="85" height="40" fill="white" stroke="#1d536a"/><circle cx="310" cy="122" r="10" fill="#dba466"/>'+line(280,75,405,75)+text(190,50,"object: v₀ ground frame")+text(385,60,"vehicle Δv");
   break;
 case "pair":
   shapes='<rect x="140" y="105" width="120" height="65" rx="9" fill="#d4ece8" stroke="#16585f" stroke-width="3"/><rect x="400" y="105" width="120" height="65" rx="9" fill="#e2eafa" stroke="#294d7b" stroke-width="3"/>'+text(185,144,"A")+text(450,144,"B")+line(272,116,365,116)+line(385,158,290,158)+text(290,83,"A on B →")+text(292,195,"← B on A");
   break;
 case "stack":
   shapes='<rect x="180" y="152" width="310" height="50" rx="7" fill="#c6dae4" stroke="#1d536a" stroke-width="3"/><rect x="277" y="99" width="116" height="51" rx="7" fill="#f8d8a6" stroke="#87602c" stroke-width="3"/>'+text(320,132,"A")+text(310,184,"B")+line(390,122,492,122)+line(298,115,298,50)+line(355,130,355,209)+text(405,104,"friction →")+text(152,43,"normal ↑")+text(371,224,"weight ↓");
   break;
 case "ramp":
   shapes='<path d="M110 190 L520 190 L520 50 Z" fill="#e3e8f1" stroke="#2c5569" stroke-width="3"/><rect x="340" y="90" width="56" height="40" rx="5" transform="rotate(-18.9 368 110)" fill="#f9d6a4" stroke="#76563b" stroke-width="3"/>'+line(365,100,365,175)+line(365,100,315,132)+line(365,100,333,42)+text(378,168,"mg ↓")+text(203,149,"mg sinθ ↙")+text(310,35,"N ↖")+text(490,210,"θ");
   break;
 case "connected":
   shapes='<rect x="118" y="120" width="135" height="72" rx="7" fill="#d2e6ef" stroke="#24566a" stroke-width="3"/><rect x="350" y="120" width="150" height="72" rx="7" fill="#d6ecdf" stroke="#176348" stroke-width="3"/><line x1="253" y1="150" x2="350" y2="150" stroke="#555" stroke-width="4"/><circle cx="150" cy="194" r="14" fill="#3e5365"/><circle cx="215" cy="194" r="14" fill="#3e5365"/><circle cx="385" cy="194" r="14" fill="#3e5365"/><circle cx="465" cy="194" r="14" fill="#3e5365"/>'+line(500,148,603,148)+text(152,150,"A · 2 kg")+text(386,150,"B · 3 kg")+text(535,125,"pull");
   break;
 default:
   shapes='<rect x="278" y="98" width="112" height="65" rx="9" fill="#dceaf1" stroke="#244a60" stroke-width="3"/>'+text(306,137,"object")+line(265,128,145,128)+line(400,128,528,128)+text(120,97,u.figure.left)+text(408,97,u.figure.right);
 }
 return '<figure class="figure"><svg '+base+'>'+defs+shapes+'</svg><figcaption>'+title+'</figcaption></figure>';
}
function render(u){
 document.title=u.id+" · "+u.title+" — PH02 textbook candidate";
 const lessonPath="../../../core1/PH02/"+u.id.split("-").at(-1)+"/index.html";
 el.innerHTML='<h1>'+esc(u.title)+'</h1>'+
 '<p class="notice"><strong>AUTHOR-EXPOSED CANDIDATE · ACADEMIC HOLD.</strong> This original lesson is not a verified exam item, approved QRT tile or published course standard.</p>'+
 '<p class="fine">Stable subtopic: '+esc(u.id)+' · Scope: '+esc(u.scope)+' · Source/exam custody: HOLD</p>'+
 '<section><h2>A1 · Observe and ask</h2>'+p(u.phenomenon)+'<h3>Learning target</h3>'+p(u.competency)+'</section>'+
 '<section><h2>A2 · What you already need</h2><p>Read any unfamiliar prerequisite first; this text does not certify those prerequisite lessons.</p><ul>'+u.prerequisites.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul></section>'+
 '<section><h2>A3 · Construct the model</h2>'+p(u.mechanism)+'</section>'+
 '<section><h2>A4 · Derive and check the rule</h2><div class="card math">'+p(u.warrant)+'</div><p>Check the frame, sign convention, unit and applicability before accepting a numerical result. For a new model the original scientific warrant still requires independent review.</p></section>'+
 '<section><h2>A5 · Read the physical representation</h2>'+figure(u)+'</section>'+
 '<section><h2>A6 · Three progressive worked examples</h2>'+u.progression.map(([level,q,a])=>'<div class="example"><h3>'+esc(level)+'</h3><p><strong>Question:</strong> '+esc(q)+'</p><p><strong>Reasoned solution:</strong> '+esc(a)+'</p></div>').join('')+'</section>'+
 '<section><h2>A7 · Worked anchor and independent check</h2><div class="example"><p><strong>Problem:</strong> '+esc(u.anchor.problem)+'</p><p><strong>Solution and check:</strong> '+esc(u.anchor.solution)+'</p></div></section>'+
 '<section><h2>A8 · Diagnose a tempting wrong idea</h2><p><strong>Tempting claim:</strong> '+esc(u.misconception.wrong)+'</p><p><strong>Why it fails:</strong> '+esc(u.misconception.why)+'</p><p><strong>Repair:</strong> '+esc(u.misconception.repair)+'</p></section>'+
 '<section><h2>A9 · Counterexample, limit and synthesis</h2><div class="card"><h3>Changed condition</h3>'+p(u.boundary.case)+p(u.boundary.check)+'</div><h3>Independent exit check</h3><p>'+esc(u.synthesis.question)+'</p><details><summary>Reveal the reasoned exit answer</summary>'+p(u.synthesis.answer)+'</details></section>'+
 '<section><h2>Apply what you learned in a different construction</h2><p>The protected transfer changes the decisive move. Your first answer must be saved before hints or model reasoning become visible.</p><a class="action" href="'+lessonPath+'">Open '+esc(u.id)+' Core1B transfer</a></section>'+
 '<p class="fine">Sources for scope screening only: <a href="https://iapt.org.in/">IAPT NSEJS 2026</a> and <a href="https://cbseacademic.nic.in/curriculum_2027.html">CBSE 2026–27 curriculum index</a>. No original question, diagram or key is reproduced.</p>';
}
try{
 if(!el||!uid)throw Error("Missing exact unit identity");
 const resp=await fetch(new URL("./units.v1.json",import.meta.url),{cache:"no-store"});
 if(!resp.ok)throw Error("PH02 data unavailable: HTTP "+resp.status);
 const data=await resp.json(); const u=data.units.find(x=>x.id===uid);
 if(data.schema!=="g9v41-ph02-author-candidate-content/v1"||!u||data.academic_status!=="HOLD")throw Error("Invalid/missing PH02 candidate and status");
 render(u);
 const bridgeResponse=await fetch(new URL("./teaching-bridges.v1.json",import.meta.url),{cache:"no-store"});
 if(!bridgeResponse.ok)throw Error("Core1A operation bridges unavailable; HTTP "+bridgeResponse.status);
 const bridgeData=await bridgeResponse.json();
 const bridges=bridgeData.bridges?.[uid];
 if(bridgeData.schema!=="g9v41-ph02-core1a-operation-bridges/v1"||
    bridgeData.status!=="AUTHOR_EXPOSED_CANDIDATE__ACADEMIC_HOLD"||
    !Array.isArray(bridges)||bridges.length!==2||new Set(bridges.map(b=>b.op)).size!==2)
   throw Error("Missing or invalid Core1A operation bridge; HOLD");
 const bridgeSection=document.createElement("section");
 bridgeSection.id="additional-constructions";
 bridgeSection.innerHTML='<h2>A10 · Build the additional reasoning constructions</h2>'+
   '<p>These two general methods prepare different reasoning operations without disclosing their protected transfer problems.</p>'+
   bridges.map(b=>'<div class="example"><h3>'+esc(b.op)+' · '+esc(b.title)+'</h3>'+p(b.teaching)+
      '<p><strong>Different worked illustration:</strong> '+esc(b.worked)+'</p>'+
      '<p><strong>Independent condition check:</strong> '+esc(b.check)+'</p></div>').join('');
 el.appendChild(bridgeSection);
}catch(err){el.textContent="PH02 lesson is unavailable; status remains HOLD. "+String(err.message||err);el.className="error";}
