/* PH05 Core1A candidate renderer: original content, source/QRT academic HOLD. */
const el=document.querySelector("[data-ph05-lesson]");
const uid=el?.dataset.unit;
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const p=s=>"<p>"+esc(s)+"</p>";
function figure(u){
 const title=esc(u.figure.caption);
 const base='viewBox="0 0 660 240" role="img" aria-label="'+title+'" xmlns="http://www.w3.org/2000/svg"';
 const defs='<defs><marker id="arrow" markerWidth="9" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0 0 L9 4 L0 8 Z" fill="#186d86"/></marker></defs>';
 const line=(x1,y1,x2,y2)=>'<line x1="'+x1+'" y1="'+y1+'" x2="'+x2+'" y2="'+y2+'" stroke="#186d86" stroke-width="4" marker-end="url(#arrow)"/>';
 const text=(x,y,v)=>'<text x="'+x+'" y="'+y+'" font-size="16" fill="#123f56" font-family="system-ui">'+esc(v)+'</text>';
 let shapes='';
 switch(u.figure.kind){
 case "gravity_pair":
   shapes='<circle cx="180" cy="120" r="45" fill="#cbe6ea" stroke="#186d86" stroke-width="3"/>'+
          '<circle cx="480" cy="120" r="28" fill="#e8d8c8" stroke="#8c5828" stroke-width="3"/>'+
          line(180,120,310,120)+line(480,120,350,120)+
          '<line x1="180" y1="185" x2="480" y2="185" stroke="#7799aa" stroke-width="2" stroke-dasharray="4 4"/>'+
          text(160,126,"m₁")+text(470,126,"m₂")+text(220,105,"F₁₂ →")+text(380,105,"← F₂₁")+
          text(310,205,"distance r");
   break;
 case "planet_scale":
   shapes='<circle cx="200" cy="120" r="50" fill="#d8ecf8" stroke="#25648a" stroke-width="3"/>'+
          '<circle cx="460" cy="120" r="70" fill="#d4eae4" stroke="#1b6e58" stroke-width="3"/>'+
          text(175,115,"M, R")+text(165,140,"g = g₀")+
          text(435,115,"2M, 2R")+text(430,140,"g = g₀/2");
   break;
 case "altitude_depth":
   shapes='<circle cx="160" cy="120" r="65" fill="#eef6fa" stroke="#1d5c7c" stroke-width="2"/>'+
          '<line x1="280" y1="200" x2="620" y2="200" stroke="#335566" stroke-width="2"/>'+
          '<line x1="280" y1="200" x2="280" y2="30" stroke="#335566" stroke-width="2"/>'+
          '<path d="M280 200 L400 60 Q 480 140 600 175" fill="none" stroke="#0e6878" stroke-width="4"/>'+
          text(250,45,"g(r)")+text(600,220,"r")+text(390,220,"r = R")+text(375,50,"Peak: g₀");
   break;
 case "apparent_weight":
   shapes='<rect x="220" y="40" width="220" height="150" rx="8" fill="#f2f7fa" stroke="#225577" stroke-width="3"/>'+
          '<rect x="270" y="150" width="120" height="25" fill="#cbe3ea" stroke="#186d86" stroke-width="2"/>'+
          '<circle cx="330" cy="90" r="20" fill="#edd6b8"/>'+
          '<line x1="330" y1="110" x2="330" y2="150" stroke="#333" stroke-width="4"/>'+
          line(360,130,360,80)+line(360,130,360,180)+
          text(375,85,"N (scale)")+text(375,185,"mg (gravity)");
   break;
 case "kepler_orbit":
   shapes='<ellipse cx="330" cy="120" rx="200" ry="85" fill="none" stroke="#206680" stroke-width="3"/>'+
          '<circle cx="149" cy="120" r="14" fill="#e59832" stroke="#9e5808" stroke-width="2"/>'+
          '<circle cx="130" cy="120" r="8" fill="#1b7280"/>'+
          '<circle cx="530" cy="120" r="8" fill="#1b7280"/>'+
          line(130,120,130,70)+line(530,120,530,95)+
          text(155,96,"Sun")+text(75,125,"Perihelion: rₚ")+text(75,65,"vₚ (fast)")+
          text(465,145,"Aphelion: rₐ")+text(485,85,"vₐ (slow)");
   break;
 case "satellite_energy":
   shapes='<circle cx="240" cy="120" r="50" fill="#d8ecf8" stroke="#1c5d80" stroke-width="3"/>'+
          '<circle cx="240" cy="120" r="110" fill="none" stroke="#7799aa" stroke-width="2" stroke-dasharray="4 4"/>'+
          '<circle cx="350" cy="120" r="9" fill="#1b6e58"/>'+
          line(350,120,350,60)+
          text(220,126,"Earth")+text(365,126,"Satellite (m)")+text(365,70,"vₒ = √(GM/r)")+
          text(460,100,"E = -GMm/(2r)")+text(460,130,"K = +GMm/(2r)")+text(460,160,"U = -GMm/r");
   break;
 case "escape_well":
   shapes='<line x1="80" y1="50" x2="580" y2="50" stroke="#446677" stroke-width="2" stroke-dasharray="4 4"/>'+
          '<path d="M120 210 Q 180 180 320 80 Q 420 55 560 52" fill="none" stroke="#167a6e" stroke-width="4"/>'+
          text(480,40,"E = 0 (Escape threshold)")+
          text(90,225,"Surface: -GMm/R")+text(280,160,"U(r) = -GMm/r")+
          line(120,200,120,100)+text(130,110,"v_escape = √(2GM/R)");
   break;
 default:
   shapes='<circle cx="330" cy="120" r="45" fill="#dceaf1" stroke="#244a60" stroke-width="3"/>'+text(310,126,"body");
 }
 return '<figure class="figure"><svg '+base+'>'+defs+shapes+'</svg><figcaption>'+title+'</figcaption></figure>';
}
function render(u){
 document.title=u.id+" · "+u.title+" — PH05 authored textbook";
 const lessonPath="../../../core1/PH05/"+u.id.split("-").at(-1)+"/index.html";
 el.innerHTML='<h1>'+esc(u.title)+'</h1>'+
 '<p class="notice"><strong>OWNER-AUTHORIZED AUTHORED LESSON · AI-CHECKED.</strong> Original educational material for self-study; not an authenticated past NSEJS paper or an independently certified curriculum.</p>'+
 '<p class="fine">Stable subtopic: '+esc(u.id)+' · Scope: '+esc(u.scope)+' · Source identity: original authored material; no past-paper admission</p>'+
 '<section><h2>A1 · Observe and ask</h2>'+p(u.phenomenon)+'<h3>Learning target</h3>'+p(u.competency)+'</section>'+
 '<section><h2>A2 · What you already need</h2><p>Read any unfamiliar prerequisite first; this text does not certify those prerequisite lessons.</p><ul>'+u.prerequisites.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul></section>'+
 '<section><h2>A3 · Construct the model</h2>'+p(u.mechanism)+'</section>'+
 '<section><h2>A4 · Derive and check the rule</h2><div class="card math">'+p(u.warrant)+'</div><p>Check the frame, sign convention, unit and applicability before accepting a numerical result. For a new model the original scientific warrant still requires independent review.</p></section>'+
 '<section><h2>A5 · Read the physical representation</h2>'+figure(u)+'</section>'+
 '<section><h2>A6 · Three progressive worked examples</h2>'+u.progression.map(([level,q,a])=>'<div class="example"><h3>'+esc(level)+'</h3><p><strong>Question:</strong> '+esc(q)+'</p><p><strong>Reasoned solution:</strong> '+esc(a)+'</p></div>').join('')+'</section>'+
 (u.source_bridge ? '<section><h2>A6b · NSEJS reasoning bridge (author proposed, QRT HOLD)</h2><p class="fine">'+esc(u.source_bridge.source_locator)+'</p>'+p(u.source_bridge.teaching)+'<div class="example"><h3>Different worked construction</h3>'+p(u.source_bridge.worked)+'</div><h3>Boundary check</h3>'+p(u.source_bridge.check)+'</section>' : '')+
 '<section><h2>A7 · Worked anchor and independent check</h2><div class="example"><p><strong>Problem:</strong> '+esc(u.anchor.problem)+'</p><p><strong>Solution and check:</strong> '+esc(u.anchor.solution)+'</p></div></section>'+
 '<section><h2>A8 · Diagnose a tempting wrong idea</h2><p><strong>Tempting claim:</strong> '+esc(u.misconception.wrong)+'</p><p><strong>Why it fails:</strong> '+esc(u.misconception.why)+'</p><p><strong>Repair:</strong> '+esc(u.misconception.repair)+'</p></section>'+
 '<section><h2>A9 · Counterexample, limit and synthesis</h2><div class="card"><h3>Changed condition</h3>'+p(u.boundary.case)+p(u.boundary.check)+'</div><h3>Independent exit check</h3><p>'+esc(u.synthesis.question)+'</p><details><summary>Reveal the reasoned exit answer</summary>'+p(u.synthesis.answer)+'</details></section>'+
 '<section><h2>Apply what you learned in a different construction</h2><p>The protected transfer changes the decisive move. Your first answer must be saved before hints or model reasoning become visible.</p><a class="action" href="'+lessonPath+'">Open '+esc(u.id)+' Core1B transfer</a></section>'+
 '<p class="fine">Sources for scope screening only: <a href="https://iapt.org.in/">IAPT NSEJS 2026</a> and <a href="https://cbseacademic.nic.in/curriculum_2027.html">CBSE 2026–27 curriculum index</a>. No original question, diagram or key is reproduced.</p>';
}
try{
 if(!el||!uid)throw Error("Missing exact unit identity");
 const resp=await fetch(new URL("./units.v1.json",import.meta.url),{cache:"no-store"});
 if(!resp.ok)throw Error("PH05 data unavailable: HTTP "+resp.status);
 const data=await resp.json(); const u=data.units.find(x=>x.id===uid);
 if(data.schema!=="g9v41-ph05-author-candidate-content/v1"||!u||data.academic_status!=="HOLD")throw Error("Invalid/missing PH05 candidate and status");
 render(u);
}catch(e){
 if(el){el.className="error";el.textContent="PH05 lesson load failed: "+e.message;}
}
