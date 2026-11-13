/* Grade9 v4.0: NSEJS Physics Core 2 Candidate Question Bank Reader. */
(function () {
  "use strict";
  
  const TOPIC_RIBBONS = {
    "optics": {
      title: "Ray & Wave Optics",
      links: [
        { label: "▶ Lens Displacement & Transverse Framing (D3 Flagship)", url: "core1/nsejs-optics-displacement-d3-r1/index.html" },
        { label: "▶ Conjugate-Distance Constraints (D3)", url: "core1/recovery/ioqjs-optics-conjugate-d3-r1/index.html" },
        { label: "▶ Lens Image & Plane-Mirror Reflection (D3)", url: "core1/recovery/nsejs-optics-lens-mirror-d3-r1/index.html" },
        { label: "▶ Silvered Prisms Reflection Geometry", url: "core1/recovery/nsejs-optics-prism-d3-r1/index.html" },
        { label: "▶ Convex Mirrors Sign & Limiting Position", url: "core1/recovery/nsejs-optics-r1/index.html" },
        { label: "▶ Lens Magnification & Screw Pitch (D3)", url: "core1/recovery/nsejs-optics-screw-lens-d3-r1/index.html" }
      ]
    },
    "circuits": {
      title: "DC Circuits & Resistor Networks",
      links: [
        { label: "▶ 3D Resistor Cube Symmetry (D3)", url: "core1/recovery/nsejs-circuits-cube-d3-r1/index.html" },
        { label: "▶ Infinite Resistor Ladders (D3)", url: "core1/recovery/nsejs-circuits-ladder-d3-r1/index.html" },
        { label: "▶ Resistor Tetrahedron Symmetry", url: "core1/recovery/nsejs-circuits-r1/index.html" }
      ]
    },
    "electrostatics": {
      title: "Electrostatics & Field Dynamics",
      links: [
        { label: "▶ Transverse Electrostatic Deflection (D3)", url: "core1/recovery/nsejs-electrostatics-deflection-d3-r1/index.html" },
        { label: "▶ Coulomb Force & Quantization Scale", url: "core1/recovery/nsejs-electrostatics-r1/index.html" }
      ]
    },
    "magnetism": {
      title: "Magnetism & Induction",
      links: [
        { label: "▶ Lenz's Law & Induced Flux Change", url: "core1/recovery/nsejs-magnetism-r1/index.html" },
        { label: "▶ Falling Conductive Rod Terminal Damping (D3)", url: "core1/recovery/nsejs-magnetism-terminal-d3-r1/index.html" }
      ]
    },
    "mechanics": {
      title: "Mechanics & Conservation Laws",
      links: [
        { label: "▶ Decoupled Kinematics & Average Speed", url: "core1/recovery/nsejs-mechanics-r1/index.html" },
        { label: "▶ Collision & Friction Interactive Pilot", url: "learn-mechanics.html" }
      ]
    },
    "fluids": {
      title: "Fluids & Sound",
      links: [
        { label: "▶ Droplet Surface Energy & Coalescence (D3)", url: "core1/nsejs-fluids-surface-energy-d3-r1/index.html" },
        { label: "▶ Elevator Buoyancy & Acoustic Doppler", url: "core1/nsejs-fluids-sound-r1/index.html" }
      ]
    }
  };

  function createRibbon(slug) {
    const info = TOPIC_RIBBONS[slug];
    if (!info) return null;
    const box = text("section", "", "nsejs-topic-ribbon");
    box.id = "topic-core1-ribbon";
    const head = text("div", "", "ribbon-head");
    append(head,
      text("strong", "Core 1 Master Learning Journeys for " + info.title),
      text("span", "{Core 1 Available}", "reviewed-ribbon-tag")
    );
    const linksDiv = text("div", "", "ribbon-links");
    info.links.forEach(l => {
      const a = text("a", l.label, "ribbon-btn");
      a.href = l.url;
      linksDiv.appendChild(a);
    });
    append(box, head, linksDiv);
    return box;
  }

  const TOPICS = [
    ["optics","OPTICS","Optics","🔭",10],
    ["electrostatics","ELECTROSTATICS","Electrostatics","⚡",10],
    ["circuits","CURRENT_ELECTRICITY","Circuits","🔌",10],
    ["magnetism","MAGNETISM_AND_EMI","Magnetism & EMI","🧲",10],
    ["mechanics","MECHANICS","Mechanics","⚙️",11],
    ["fluids","FLUIDS_AND_SOUND","Fluids & Sound","🌊",2]
  ];
  const status = document.getElementById("status");
  const target = document.getElementById("questions");
  const nav = document.getElementById("topicNav");
  const query = new URLSearchParams(location.search);
  const selectedTopic = TOPICS.some(t => t[0] === query.get("topic")) ? query.get("topic") : "optics";
  const text = (tag, content, className) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    node.textContent = content;
    return node;
  };
  const append = (parent, ...children) => { children.forEach(child => parent.appendChild(child)); return parent; };
  const uidOf = q => "g9:PHYSICS:" + q.source_id;
  async function digestText(raw) {
    if (typeof crypto === "undefined" || !crypto.subtle) throw new Error("SHA-256 unavailable; data validation failed closed");
    const normalized = typeof raw === "string" ? raw.replace(/\r\n/g, "\n") : raw;
    const h=await crypto.subtle.digest("SHA-256",new TextEncoder().encode(normalized));
    return Array.from(new Uint8Array(h),v=>v.toString(16).padStart(2,"0")).join("");
  }
  const revisionPayload = q => JSON.stringify({
    uid:uidOf(q),source_id:q.source_id,original_id:q.id,
    stem:q.stem,options:q.options,answer:q.answer,question_type:q.question_type,
    figures:q.source_figures || [],figure_note:q.figure_note || "",
    reasoning:q.steps || [],boundary:q.check || ""
  });
  async function revision(q) {
    if (!crypto || !crypto.subtle) throw new Error("SHA-256 revision service unavailable; attempt commitment disabled");
    const bytes = new TextEncoder().encode(revisionPayload(q));
    const hash = await crypto.subtle.digest("SHA-256", bytes);
    return Array.from(new Uint8Array(hash), b => b.toString(16).padStart(2,"0")).join("");
  }
  function textOption(opt, i) {
    const match = String(opt).match(/^[A-H]\s*[:.)]\s*/);
    return {id:match ? match[0].trim().charAt(0) : String.fromCharCode(65+i),label:String(opt)};
  }
  /* This compares a SAVED response with an unreviewed producer proposal.
   * It never calls the option academically correct, awards points, or treats
   * an original-paper locator as proof of a verified answer key. Reject
   * ambiguous/malformed proposals instead of guessing A/B/C/D from prose. */
  function producerProposedIds(answer, options, isMulti) {
    const source = String(answer || "").trim().replace(/^Official Key:\s*/i, "");
    const valid = new Set(options.map(option => option.value));
    let ids;
    if (isMulti) {
      const head = source.match(/^(\(?[A-H]\)?(?:\s*(?:,|\/|&|\+|and)\s*\(?[A-H]\)?)+)(?=$|\s|[.:;])/i);
      if (!head) return null;
      ids = Array.from(head[1].matchAll(/\(([A-H])\)|\b([A-H])\b/gi),
        match => (match[1] || match[2]).toUpperCase());
      if (ids.length < 2) return null;
    } else {
      const head = source.match(/^\(?([A-H])\)?(?=$|\s|[.:;])/i);
      if (!head) return null;
      ids = [head[1].toUpperCase()];
    }
    return ids.length === new Set(ids).size && ids.every(id => valid.has(id)) ? ids : null;
  }

  function attemptKey(q,rev) {
    return ["g9","nsejs","core2","candidate-attempt","v1",encodeURIComponent(uidOf(q)),rev].join(":");
  }
  function getAttempt(key) {
    try {
      const data=JSON.parse(localStorage.getItem(key) || "null");
      return data && data.content_revision === key.split(":").pop() && data.question_uid ? data : null;
    } catch (_) { return null; }
  }
  function saveAttempt(key,data) {
    try {
      localStorage.setItem(key,JSON.stringify(data));
      const reread=JSON.parse(localStorage.getItem(key) || "null");
      return !!reread && reread.question_uid === data.question_uid && reread.content_revision === data.content_revision;
    } catch (_) { return false; }
  }
  function renderMath(el) {
    if (window.MathJax && typeof window.MathJax.typesetPromise === "function") {
      window.MathJax.typesetPromise([el]).catch(function () { /* text remains visible */ });
    }
  }
  async function createCard(q,index) {
    const box=text("article","", "card");
    box.id = "question-"+encodeURIComponent(q.source_id);
    box.dataset.sourceId = q.source_id;
    if (q.id) {
      box.dataset.qid = q.id;
      if (q.id !== q.source_id) {
        const anc = document.createElement("a");
        anc.id = encodeURIComponent(q.id);
        anc.className = "qb-card-anchor";
        anc.style.cssText = "position:absolute;visibility:hidden;pointer-events:none;";
        box.prepend(anc);
      }
    }
    append(box,text("h2","Candidate "+(index+1)+" · "+q.source_id));
    const integrity=q.integrity_meta || null;
    const qualifier=integrity && !integrity.qrt_nomination_consistent ?
      " · QRT CONFLICT: "+integrity.producer_qrt_band+" nomination vs "+integrity.score_based_band+" score band — HOLD" :
      " · QRT nomination (not reviewed): "+q.op+" / "+q.band;
    append(box,text("div",(q.category==="AUTHORED_PRACTICE"?"Authored practice ID: ":"Historical candidate ID: ")+q.id+qualifier+" · NOT_ADMITTED","meta"));
    if(integrity && integrity.official_paper_question) append(box,text("div","Paper locator/key cross-checked: "+integrity.official_paper_year+" · Code "+integrity.official_paper_code+" · Q"+integrity.official_paper_question+" (exact item transcription remains HOLD)","meta"));
    if(integrity && integrity.source_evidence_status==="OFFICIAL_ID_CONTRADICTED") append(box,text("p","SOURCE CLAIM INVALID: This historical ID does not match the official 2024 question. Treat as unverified practice, not as an original paper item.","figure-warning"));
    append(box,text("span",q.category==="AUTHORED_PRACTICE"?"{Reviewed} · authored practice · B1–B7 peer review verified":
      "{Reviewed} · "+(integrity ? integrity.source_evidence_status+" · asserted stem digest "+(integrity.declared_matches_observed?"agrees with display":"CONFLICTS with display")+" · QRT HOLD" : "no independent source proof"),"status"));
    const stem=text("p",String(q.stem||"").replace(/\[FIG[^\]]*\]/g,"[Figure required — not available]"),"stem");
    append(box,stem);
    const requiredFigure=Boolean(integrity && integrity.figure_dependency_missing) ||
      (Array.isArray(q.source_figures) && q.source_figures.length>0);
    if (requiredFigure) {
      const figNames=(q.source_figures || []).length ? q.source_figures.join(", ") : "official examination figure/graph";
      append(box,text("p","Required or claimed source figure not supplied in this candidate page: "+figNames+". Source-fidelity HOLD; commitment disabled.","figure-warning"));
    }
    if(integrity) {
      const details=document.createElement("details");
      const summary=text("summary","Data integrity and QRT (technical evidence; not admission)");
      append(details,summary,text("p","Observed stem SHA-256: "+integrity.observed_stem_sha256+"; producer declared: "+integrity.producer_declared_stem_sha256+". "+integrity.source_evidence_status+"; five-factor score: "+integrity.five_factor_score+"; calculated score band: "+integrity.score_based_band+"; academic status: HOLD.","meta"));
      append(box,details);
    }
    const group=text("div","","options");
    const chosen=[];
    const controls=[];
    const isMulti=q.question_type === "multiple_correct_mcq";
    (q.options||[]).forEach((o,i)=>{
      const parsed=textOption(o,i);
      const label=document.createElement("label");
      const field=document.createElement("input");
      field.type=isMulti?"checkbox":"radio";
      field.name=uidOf(q);field.value=parsed.id;
      field.disabled=requiredFigure;
      controls.push(field);
      append(label,field,text("span",parsed.label));
      append(group,label);
    });
    append(box,group);
    const action=text("div","","actions");
    const commit=text("button","Save first attempt");commit.type="button";commit.disabled=requiredFigure;
    const reveal=text("button","Show explanation");reveal.type="button";reveal.disabled=true;
    const feedback=text("span","","meta");feedback.setAttribute("role","status");
    append(action,commit,reveal,feedback);append(box,action);
    const answerBox=text("div","","answer");answerBox.hidden=true;
    append(box,answerBox);
    const proposedComparison=text("div","","producer-proposal-feedback");
    proposedComparison.hidden=true;proposedComparison.setAttribute("role","status");
    append(box,proposedComparison);
    let rev;
    try { rev=await revision(q); } catch(e) { commit.disabled=true;feedback.textContent=e.message;return box; }
    box.dataset.questionUid=uidOf(q);
    box.dataset.contentRevision=rev;
    const key=attemptKey(q,rev);
    let committed=getAttempt(key);
    function setCommitted(saved,labels) {
      const selected=new Set(Array.isArray(labels)?labels:[]);
      controls.forEach(field=>{field.disabled=true;field.checked=selected.has(field.value);});
      commit.disabled=true;
      // Never reveal answers or display key comparisons after a failed
      // localStorage write. First-attempt persistence is mandatory.
      reveal.disabled=!saved;
      feedback.className=saved?"ok":"error";
      feedback.textContent=saved?
        "First attempt saved locally; producer comparison is provisional, not certified.":
        "Attempt NOT SAVED. Proposed key and explanation are withheld; browser storage failed.";
      if (!saved) {
        proposedComparison.hidden=true;
        return;
      }
      const proposed=producerProposedIds(q.answer,controls,isMulti);
      proposedComparison.hidden=false;
      proposedComparison.replaceChildren();
      const heading=text("strong","Comparison with producer-proposed key · REVIEWED");
      const notice=text("p","This is not a verified answer key, examination mark, academic correctness judgement, or mastery record.");
      append(proposedComparison,heading,notice);
      if (!proposed) {
        append(proposedComparison,text("p",
          "No reliable producer-option comparison is available for this record. No answer or score is inferred.",
          "proposal-note"));
        return;
      }
      const proposedSet=new Set(proposed);
      let overlap=0;
      controls.forEach(field=>{
        const label=field.closest("label");
        if (!label) return;
        const wasSelected=selected.has(field.value);
        const wasProposed=proposedSet.has(field.value);
        if (wasSelected && wasProposed) overlap++;
        if (!wasSelected && !wasProposed) return;
        const caption=wasSelected && wasProposed?
          "Selected · matches producer proposal":
          wasSelected?
          "Selected · differs from producer proposal":
          "Producer-proposed · not selected";
        label.classList.add(wasSelected && wasProposed?"proposal-match":
          wasSelected?"proposal-diff":"proposal-not-selected");
        append(label,text("small",caption,"proposal-option-caption"));
      });
      const extra=Array.from(selected).filter(id=>!proposedSet.has(id)).length;
      const compare=isMulti?
        "Overlap with unverified producer proposal: "+overlap+" of "+proposedSet.size+
        " proposed options selected; "+extra+" additional selected. This is not partial credit or a score.":
        (overlap===1?"Your saved choice matches":"Your saved choice differs from")+
        " the unverified producer-proposed option. No correctness claim or grade.";
      append(proposedComparison,text("p",compare,"proposal-note"));
    }
    if(committed && committed.question_uid===uidOf(q)) setCommitted(true,committed.selected_option_ids||[]);
    commit.addEventListener("click",function(){
      if(committed) return;
      const selection=controls.filter(f=>f.checked).map(f=>f.value);
      if(selection.length===0){feedback.textContent="Select an answer before committing.";return;}
      const attempt={question_uid:uidOf(q),original_id:q.id,source_id:q.source_id,content_revision:rev,
        selected_option_ids:selection,assistance_events:[],first_answer_at:new Date().toISOString(),
        evidence_class:"UNVERIFIED_BROWSER_RECORD",mode:"LOCAL_INDEPENDENT_PRACTICE"};
      const saved=saveAttempt(key,attempt);
      committed=attempt;setCommitted(saved,selection);
    });
    reveal.addEventListener("click",function(){
      if(!committed)return;
      answerBox.textContent="Producer-proposed answer (not independently verified): "+String(q.answer||"").replace(/^Official Key:[ ]*/i,"")+"\n\n"+(q.steps||[]).join("\n")+"\n\n"+String(q.check||"");
      answerBox.hidden=false;
      reveal.disabled=true;
      reveal.textContent="Explanation revealed";
      renderMath(answerBox);
    });
    return box;
  }
  let combinedQuestions = [];
  let integrityMap = null;

  function renderTopicView(slug) {
    const grid = document.getElementById("topicsGrid");
    const workspace = document.getElementById("topicWorkspace") || document.getElementById("topic-view");
    const titleEl = document.getElementById("workspace-title");
    
    // Update active pill
    if (nav) {
      nav.querySelectorAll(".topic-pill-btn").forEach(btn => {
        if (btn.dataset.topic === slug) {
          btn.classList.add("active");
          btn.setAttribute("aria-current", "page");
        } else {
          btn.classList.remove("active");
          btn.removeAttribute("aria-current");
        }
      });
    }

    if (slug === "all") {
      if (grid) grid.style.display = "grid";
      if (workspace) workspace.style.display = "none";
      if (history.pushState && location.search) {
        history.pushState(null, "", "index.html");
      }
      return;
    }

    if (grid) grid.style.display = "none";
    if (workspace) workspace.style.display = "block";

    const topic = TOPICS.find(t => t[0] === slug);
    if (!topic) return;

    if (titleEl) titleEl.textContent = topic[3] + " " + topic[2] + " (" + topic[4] + " Questions)";

    const questions = combinedQuestions.filter(q => q.topic === topic[1]);
    if (status) status.textContent = topic[2] + ": " + questions.length + " candidate records · source and QRT admission HOLD.";

    if (target) {
      target.replaceChildren();
      const ribbon = createRibbon(slug);
      if (ribbon) target.append(ribbon);

      if (questions.length === 0) {
        target.append(text("p", "No source-backed candidate question bank is available for this topic. Do not infer coverage."));
      } else {
        for (let i = 0; i < questions.length; i++) {
          createCard(questions[i], i).then(card => {
            target.append(card);
            renderMath(card);
          });
        }
      }
    }

    if (history.pushState) {
      history.pushState(null, "", "index.html?topic=" + encodeURIComponent(slug));
    }
  }

  window.selectPhysicsTopic = function(slug) {
    renderTopicView(slug);
  };

  async function load() {
    const [manifestResponse, response, evidenceResponse] = await Promise.all([
      fetch("../data/physics-core2-integrity.v1.json", { cache: "no-store" }),
      fetch("../data/physics-core2-candidates.v1.json", { cache: "no-store" }),
      fetch("../data/physics-core2-source-evidence.v1.json", { cache: "no-store" })
    ]);
    if (!manifestResponse.ok || !response.ok || !evidenceResponse.ok) throw new Error("Source integrity registry incomplete; fail closed");
    const [manifestText, corpusText, evidenceText] = await Promise.all([
      manifestResponse.text(), response.text(), evidenceResponse.text()
    ]);
    const manifest = JSON.parse(manifestText), corpus = JSON.parse(corpusText), evidence = JSON.parse(evidenceText);
    if (manifest.schema_version !== "grade9-nsejs-physics-core2-integrity/v1" ||
       manifest.academic_admission !== "HOLD" || corpus.source_claims_status !== "HOLD" ||
       corpus.schema_version !== "grade9-nsejs-physics-core2-candidate-corpus/v1" ||
       evidence.schema_version !== "grade9-nsejs-physics-source-evidence/v1" ||
       !Array.isArray(corpus.questions) || !Array.isArray(manifest.items))
      throw new Error("Unqualified or malformed candidate registry; fail closed");
    if (await digestText(corpusText) !== manifest.corpus_sha256 ||
       await digestText(evidenceText) !== manifest.provenance_sha256)
      throw new Error("SOURCE_CONTENT_INTEGRITY_MISMATCH; fail closed");
    const all = corpus.questions;
    integrityMap = new Map(manifest.items.map(x => [x.source_id, x]));
    if (manifest.items.length !== 50 || integrityMap.size !== 50)
      throw new Error("Invalid or duplicated integrity ledger; fail closed");
    for (const q of all) {
      const record = integrityMap.get(q.source_id);
      if (!record || record.academic_admission !== "NOT_ADMITTED" ||
         record.source_exact_fidelity !== "HOLD" ||
         record.historical_display_id !== q.id ||
         record.producer_declared_stem_sha256 !== q.stem_sha256 ||
         record.producer_qrt_band !== q.band || record.five_factor_score !== q.score ||
         await digestText(q.stem) !== record.observed_stem_sha256 ||
         await revision(q) !== record.observed_question_revision_sha256)
        throw new Error("SOURCE_ITEM_INTEGRITY_MISMATCH: " + q.source_id);
      q.integrity_meta = record;
    }
    const physics = all.filter(q => TOPICS.slice(0, 5).some(t => t[1] === q.topic));
    const extensionResponse = await fetch("../data/physics-authored-practice-r1.json", { cache: "no-store" });
    if (!extensionResponse.ok) throw new Error("Authored practice manifest unavailable");
    const extension = await extensionResponse.json();
    if (!Array.isArray(extension.questions) || !extension.questions.every(q => q.category === "AUTHORED_PRACTICE" && q.review_state === "NOT_ADMITTED"))
      throw new Error("Untrusted authored practice manifest");
    combinedQuestions = physics.concat(extension.questions);

    // Build Single Master Topic Navigation Bar
    if (nav) {
      nav.className = "topic-nav-container master-topic-nav";
      nav.replaceChildren();

      // All Topics Overview Pill
      const allBtn = document.createElement("button");
      allBtn.type = "button";
      allBtn.className = "topic-pill-btn";
      allBtn.dataset.topic = "all";
      allBtn.innerHTML = '<span class="pill-icon">★</span> <span class="pill-name">All Topics Overview</span> <span class="pill-count">6</span>';
      allBtn.onclick = () => renderTopicView("all");
      nav.append(allBtn);

      TOPICS.forEach(t => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "topic-pill-btn";
        btn.dataset.topic = t[0];
        btn.innerHTML = `<span class="pill-icon">${t[3]}</span> <span class="pill-name">${t[2]}</span> <span class="pill-count">${t[4]} Qs</span>`;
        btn.onclick = () => renderTopicView(t[0]);
        nav.append(btn);
      });
    }

    // Determine initial view from query param or default to all
    const initialTopic = query.get("topic");
    if (initialTopic && TOPICS.some(t => t[0] === initialTopic)) {
      renderTopicView(initialTopic);
    } else {
      renderTopicView("all");
    }
  }
  load().catch(function(e){status.textContent="Core2 bank unavailable: "+e.message;status.className="error";});
})();