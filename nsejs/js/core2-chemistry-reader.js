/* Grade9 v4.0: NSEJS Chemistry Core 2 Candidate Question Bank Reader
 * Renders verified candidate items across disciplinary topics and downloaded IAPT exam papers.
 * Preserves Rule 13 fail-closed governance: local practice attempts only; academic admission HOLD.
 */
(function () {
  "use strict";

  const TOPICS = [
    ["atomic_structure", "STRUCTURE_OF_THE_ATOM", "Atomic Structure", "⚛️"],
    ["bonding", "CHEMICAL_BONDING", "Chemical Bonding", "🔗"],
    ["mole_concept", "MOLE_CONCEPT_AND_GAS_LAWS", "Mole & Gas Laws", "⚖️"],
    ["reactions", "CHEMICAL_SUBSTANCES_AND_REACTIONS", "Chemical Reactions", "🧪"],
    ["redox", "REDOX_AND_TITRATIONS", "Redox & Titrations", "🔄"],
    ["eudiometry", "EUDIOMETRY_AND_GAS_ANALYSIS", "Eudiometry & Gases", "💨"]
  ];

  const TOPIC_RIBBONS = {
    "atomic_structure": {
      title: "Atomic Structure & Subshell Orbitals",
      links: [
        { label: "▶ Subshell Aufbau Configuration (D3 Flagship)", url: "core1/chem-electronic-structure-d3-r1/index.html" },
        { label: "▶ Bohr Atomic Transitions (Skill Repair)", url: "core1/recovery/chem-atomic-structure-r1/index.html" }
      ]
    },
    "bonding": {
      title: "Chemical Bonding & Molecular Architecture",
      links: [
        { label: "▶ Phosphorus Oxyacids & Basicity (D3 Flagship)", url: "core1/chem-phosphorus-oxyacids-d3-r1/index.html" },
        { label: "🗺️ View Core 2 267-Item Question Map", url: "../core2/question-map.html#chemistry" }
      ]
    },
    "mole_concept": {
      title: "Matter, States & Mole Concept",
      links: [
        { label: "▶ Partial Pressures & Ideal Gas (Skill Repair)", url: "core1/recovery/chem-matter-mole-r1/index.html" },
        { label: "📑 Official IAPT Source Downloads", url: "../official-sources.html" }
      ]
    },
    "reactions": {
      title: "Chemical Substances, Reactions & Equilibrium",
      links: [
        { label: "▶ Amphoteric Oxides & Stoichiometry (Skill Repair)", url: "core1/recovery/chem-chemical-substances-r1/index.html" },
        { label: "🗺️ View Core 2 267-Item Question Map", url: "../core2/question-map.html#chemistry" }
      ]
    },
    "redox": {
      title: "Redox Reactions, Oxidation States & Volumetric Titrations",
      links: [
        { label: "▶ Redox Titration & Oxidation States (Skill Repair)", url: "core1/recovery/chem-redox-titration-d3-r1/index.html" },
        { label: "📑 Official IAPT Source Downloads", url: "../official-sources.html" }
      ]
    },
    "eudiometry": {
      title: "Eudiometry & Combustion Gas Analysis",
      links: [
        { label: "▶ Combustion Eudiometry & Hydrocarbon Formulas (Skill Repair)", url: "core1/recovery/chem-eudiometry-d3-r1/index.html" },
        { label: "📑 Official IAPT Source Downloads", url: "../official-sources.html" }
      ]
    }
  };

  const status = document.getElementById("status");
  const target = document.getElementById("questions");
  const nav = document.getElementById("topicNav");
  const query = new URLSearchParams(location.search);
  const selectedSlug = TOPICS.some(t => t[0] === query.get("topic")) ? query.get("topic") : "atomic_structure";

  const text = (tag, content, className) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (content !== undefined && content !== null) node.textContent = content;
    return node;
  };
  const append = (parent, ...children) => { children.forEach(child => parent.appendChild(child)); return parent; };
  const uidOf = q => "g9:CHEMISTRY:" + (q.source_id || q.id);

  function textOption(opt, i) {
    const match = String(opt).match(/^[A-H]\s*[:.)]\s*/);
    return { id: match ? match[0].trim().charAt(0) : String.fromCharCode(65 + i), label: String(opt) };
  }

  function producerProposedIds(answer, options, isMulti) {
    const source = String(answer || "").trim().replace(/^Official Key:\s*/i, "");
    const valid = new Set(options.map(option => option.value));
    let ids;
    if (isMulti) {
      const head = source.match(/^(\(?[A-H]\)?(?:\s*(?:,|\/|&|\+|and)\s*\(?[A-H]\)?)+)(?=$|\s|[.:;])/i);
      if (!head) return null;
      ids = Array.from(head[1].matchAll(/\(([A-H])\)|\b([A-H])\b/gi), m => (m[1] || m[2]).toUpperCase());
      if (ids.length < 2) return null;
    } else {
      const head = source.match(/^\(?([A-H])\)?(?=$|\s|[.:;])/i);
      if (!head) return null;
      ids = [head[1].toUpperCase()];
    }
    return ids.length === new Set(ids).size && ids.every(id => valid.has(id)) ? ids : null;
  }

  function attemptKey(q) {
    return ["g9", "nsejs", "chemistry", "core2", encodeURIComponent(uidOf(q))].join(":");
  }
  function getAttempt(k) {
    try {
      const d = JSON.parse(localStorage.getItem(k) || "null");
      return d && d.question_uid ? d : null;
    } catch (_) { return null; }
  }
  function saveAttempt(k, d) {
    try {
      localStorage.setItem(k, JSON.stringify(d));
      return true;
    } catch (_) { return false; }
  }

  function renderMath(el) {
    if (window.MathJax && typeof window.MathJax.typesetPromise === "function") {
      window.MathJax.typesetPromise([el]).catch(function () {});
    }
  }

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

  function createCard(q, index) {
    const box = text("article", "", "card");
    box.id = "question-" + encodeURIComponent(q.source_id || q.id);
    box.dataset.sourceId = q.source_id || q.id;
    if (q.id) {
      box.dataset.qid = q.id;
      if (q.source_id && q.id !== q.source_id) {
        const anc = document.createElement("a");
        anc.id = encodeURIComponent(q.id);
        anc.className = "qb-card-anchor";
        anc.style.cssText = "position:absolute;visibility:hidden;pointer-events:none;";
        box.prepend(anc);
      }
    }
    append(box, text("h2", "Candidate " + (index + 1) + " · " + (q.source_id || q.id)));

    const opStr = (q.op || "MODEL");
    const bandStr = (q.band || "D2");
    const scoreStr = q.score ? " (Score " + q.score + ")" : "";
    const meta = text("div", "Cognitive Demand: " + opStr + " · Band: " + bandStr + scoreStr + (q.crux_move_ref ? " · Crux: " + q.crux_move_ref : ""), "meta");
    append(box, meta);

    const statusBadge = text("span", "{Core 2: Candidate Practice} · Rule 13 HOLD", "status");
    append(box, statusBadge);

    if (q.exam_year) {
      const yearStr = q.exam_year.replace("YEAR_", "");
      const examBadge = text("span", "📅 Official Exam: " + yearStr, "status");
      examBadge.style.background = "#e0f2fe";
      examBadge.style.color = "#0369a1";
      examBadge.style.borderColor = "#bae6fd";
      examBadge.style.marginLeft = "8px";
      append(box, examBadge);
    }

    const stem = text("p", String(q.stem || "").replace(/\[FIG[^\]]*\]/g, ""), "stem");
    append(box, stem);

    const group = text("div", "", "options");
    const controls = [];
    const isMulti = q.question_type === "multiple_correct_mcq";
    (q.options || []).forEach((o, i) => {
      const parsed = textOption(o, i);
      const label = document.createElement("label");
      const field = document.createElement("input");
      field.type = isMulti ? "checkbox" : "radio";
      field.name = uidOf(q);
      field.value = parsed.id;
      controls.push(field);
      append(label, field, text("span", parsed.label));
      append(group, label);
    });
    append(box, group);

    const actions = text("div", "", "actions");
    const commit = text("button", "Commit First Attempt & Reveal Derivation");
    commit.type = "button";
    append(actions, commit);

    const hints = Array.isArray(q.hints) ? q.hints : [];
    if (hints.length > 0) {
      const hintBtn = text("button", "Show Progressive Hints (" + hints.length + ")");
      hintBtn.type = "button";
      hintBtn.style.background = "#f8fafc";
      hintBtn.style.color = "#334155";
      hintBtn.style.border = "1.5px solid #cbd5e1";
      const hintBox = text("div", "", "answer");
      hintBox.hidden = true;
      hints.forEach(h => {
        append(hintBox, text("strong", h.prompt || "Hint:"), text("p", h.text || ""));
      });
      hintBtn.onclick = () => {
        hintBox.hidden = !hintBox.hidden;
        hintBtn.textContent = hintBox.hidden ? "Show Progressive Hints (" + hints.length + ")" : "Hide Progressive Hints";
      };
      append(actions, hintBtn, hintBox);
    }
    append(box, actions);

    const answerBox = text("div", "", "answer");
    answerBox.hidden = true;
    append(answerBox, text("h3", "Step-by-Step Derivation & Official Key"));
    append(answerBox, text("p", q.answer || "Official Key Pending"));
    if (Array.isArray(q.steps) && q.steps.length > 0) {
      q.steps.forEach(s => append(answerBox, text("p", s)));
    }
    if (q.check) {
      append(answerBox, text("p", "Consistency Verification: " + q.check, "ok"));
    }
    append(box, answerBox);

    const k = attemptKey(q);
    const existing = getAttempt(k);
    if (existing) {
      controls.forEach(c => {
        c.disabled = true;
        if (existing.selected && existing.selected.includes(c.value)) c.checked = true;
      });
      commit.disabled = true;
      commit.textContent = "Attempt Saved Locally";
      answerBox.hidden = false;
    }

    commit.onclick = () => {
      const selected = controls.filter(c => c.checked).map(c => c.value);
      if (selected.length === 0) {
        alert("Please select your answer option(s) before committing.");
        return;
      }
      saveAttempt(k, {
        question_uid: uidOf(q),
        selected: selected,
        timestamp: new Date().toISOString()
      });
      controls.forEach(c => c.disabled = true);
      commit.disabled = true;
      commit.textContent = "Attempt Saved Locally";
      answerBox.hidden = false;
      renderMath(answerBox);
    };

    return box;
  }

    let allChemistryQuestions = [];
  let chemCounts = {};

  function renderTopicView(slug) {
    const grid = document.getElementById("topicsGrid");
    const workspace = document.getElementById("topicWorkspace") || document.getElementById("topic-view");
    const titleEl = document.getElementById("workspace-title");

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

    if (titleEl) titleEl.textContent = topic[3] + " " + topic[2] + " (" + (chemCounts[slug] || 0) + " Questions)";

    const activeQuestions = allChemistryQuestions.filter(q => q.topic === topic[1]);
    if (status) status.textContent = "Showing " + activeQuestions.length + " questions for " + topic[2] + " (Total candidate items in Chemistry bank: " + allChemistryQuestions.length + ").";

    if (target) {
      target.replaceChildren();
      const ribbon = createRibbon(slug);
      if (ribbon) target.appendChild(ribbon);

      if (activeQuestions.length === 0) {
        target.appendChild(text("p", "No questions found for this topic.", "meta"));
      } else {
        activeQuestions.forEach((q, i) => {
          const card = createCard(q, i);
          target.appendChild(card);
        });
      }
      renderMath(target);
    }

    if (history.pushState) {
      history.pushState(null, "", "index.html?topic=" + encodeURIComponent(slug));
    }
  }

  window.selectChemistryTopic = function(slug) {
    renderTopicView(slug);
  };

  async function loadData() {
    try {
      if (status) status.textContent = "Loading candidate questions from chemistry-core2-candidates.v1.json…";
      const resp = await fetch("../data/chemistry-core2-candidates.v1.json");
      if (!resp.ok) throw new Error("HTTP " + resp.status + " while loading Chemistry question bank data.");
      const data = await resp.json();
      allChemistryQuestions = data.questions || [];

      // Calculate topic counts
      TOPICS.forEach(t => {
        const topicKey = t[1];
        chemCounts[t[0]] = allChemistryQuestions.filter(q => q.topic === topicKey).length;
      });

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
          const count = chemCounts[t[0]] || 0;
          btn.innerHTML = `<span class="pill-icon">${t[3]}</span> <span class="pill-name">${t[2]}</span> <span class="pill-count">${count} Qs</span>`;
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
    } catch (err) {
      if (status) {
        status.textContent = "Error loading Chemistry question bank: " + err.message;
        status.className = "error";
      }
    }
  }

  loadData();
})();
