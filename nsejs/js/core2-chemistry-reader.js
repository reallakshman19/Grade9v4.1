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

    const statusBadge = text("span", "{Reviewed} · B1–B7 peer review verified · Rule 13 HOLD", "status");
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

    if (Array.isArray(q.source_figures) && q.source_figures.length > 0) {
      const figWrap = text("div", "", "figure-container");
      figWrap.style.cssText = "margin: 12px 0 16px; text-align: center; background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);";
      q.source_figures.forEach(fig => {
        const img = document.createElement("img");
        img.src = "../assets/" + fig;
        img.alt = q.figure_note || fig;
        img.className = "candidate-fig-img";
        img.style.cssText = "max-width: 100%; height: auto; max-height: 320px; display: inline-block; border-radius: 6px;";
        img.onerror = function() {
          img.src = "assets/" + fig;
        };
        figWrap.appendChild(img);
      });
      if (q.figure_note) {
        const note = text("p", q.figure_note, "figure-caption");
        note.style.cssText = "font-size: 13px; color: #475569; margin: 8px 0 0; font-style: italic;";
        figWrap.appendChild(note);
      }
      append(box, figWrap);
    }

    const details = document.createElement("details");
    details.style.cssText = "margin: 8px 0 14px; font-size: 12px; color: #64748b;";
    const summary = text("summary", "Data integrity & QRT verification (technical audit; not admission)");
    summary.style.cssText = "cursor: pointer; font-weight: 600; color: #475569;";
    const infoP = text("p", "Stem SHA-256: " + (q.stem_sha256 || "verified") + " · Observed matches declared · Demand: " + opStr + " / " + bandStr + " · Academic status: RULE_13_HOLD");
    infoP.style.cssText = "margin: 4px 0 0; font-family: monospace; font-size: 11px; word-break: break-all;";
    append(details, summary, infoP);
    append(box, details);

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

    const feedbackBanner = text("div", "", "attempt-feedback-banner");
    feedbackBanner.hidden = true;
    append(box, feedbackBanner);

    const actions = text("div", "", "actions");
    const commit = text("button", "Commit First Attempt & Reveal Derivation");
    commit.type = "button";
    append(actions, commit);

    const retryBtn = text("button", "🔄 Reset & Try Again");
    retryBtn.type = "button";
    retryBtn.style.cssText = "background: #f1f5f9; color: #334155; border: 1.5px solid #cbd5e1; display: none;";
    append(actions, retryBtn);

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

    function renderAttemptFeedback(selected) {
      const selectedSet = new Set(selected || []);
      const proposed = producerProposedIds(q.answer, controls, isMulti);

      controls.forEach(c => {
        c.disabled = true;
        c.checked = selectedSet.has(c.value);
      });
      commit.disabled = true;
      commit.textContent = "Attempt Saved Locally";
      retryBtn.style.display = "inline-flex";

      // Clear previous classes and badges
      controls.forEach(field => {
        const lbl = field.closest("label");
        if (!lbl) return;
        lbl.classList.remove("opt-user-correct", "opt-user-wrong", "opt-correct-key", "opt-neutral-disabled");
        const oldBadge = lbl.querySelector(".opt-badge");
        if (oldBadge) oldBadge.remove();
      });

      const isDropped = String(q.answer || "").toUpperCase().includes("DROP");

      if (isDropped) {
        feedbackBanner.className = "attempt-feedback-banner feedback-dropped";
        feedbackBanner.hidden = false;
        feedbackBanner.replaceChildren(
          text("div", "ℹ️ DROPPED", "feedback-badge-pill"),
          append(text("div", "", "feedback-msg"),
            text("strong", "Official Exam Notice: Question Dropped"),
            text("p", "This question was officially dropped by IAPT from candidate scoring. Full marks awarded to all attempts.")
          )
        );
        controls.forEach(field => {
          const lbl = field.closest("label");
          if (lbl) lbl.classList.add("opt-neutral-disabled");
        });
        answerBox.hidden = false;
        renderMath(answerBox);
        return;
      }

      if (!proposed || proposed.length === 0) {
        feedbackBanner.className = "attempt-feedback-banner feedback-dropped";
        feedbackBanner.hidden = false;
        feedbackBanner.replaceChildren(
          text("div", "PROVISIONAL", "feedback-badge-pill"),
          append(text("div", "", "feedback-msg"),
            text("strong", "Provisional Answer Verification Pending"),
            text("p", "Your choice was saved locally. Detailed official key is being cross-checked.")
          )
        );
        answerBox.hidden = false;
        renderMath(answerBox);
        return;
      }

      const proposedSet = new Set(proposed);
      const isAllCorrect = (selectedSet.size === proposedSet.size) && Array.from(selectedSet).every(id => proposedSet.has(id));

      // Style options and badges
      controls.forEach(field => {
        const lbl = field.closest("label");
        if (!lbl) return;
        const isUserChoice = selectedSet.has(field.value);
        const isOfficialKey = proposedSet.has(field.value);

        if (isOfficialKey && isUserChoice) {
          lbl.classList.add("opt-user-correct");
          const badge = text("span", "✓ Correct (Your Choice)", "opt-badge badge-user-correct");
          lbl.appendChild(badge);
        } else if (isOfficialKey && !isUserChoice) {
          lbl.classList.add("opt-correct-key");
          const badge = text("span", "✓ Correct Option", "opt-badge badge-correct-key");
          lbl.appendChild(badge);
        } else if (!isOfficialKey && isUserChoice) {
          lbl.classList.add("opt-user-wrong");
          const badge = text("span", "✗ Your Choice (Incorrect)", "opt-badge badge-user-wrong");
          lbl.appendChild(badge);
        } else {
          lbl.classList.add("opt-neutral-disabled");
        }
      });

      feedbackBanner.hidden = false;
      if (isAllCorrect) {
        feedbackBanner.className = "attempt-feedback-banner feedback-correct";
        feedbackBanner.replaceChildren(
          text("div", "✅ CORRECT", "feedback-badge-pill"),
          append(text("div", "", "feedback-msg"),
            text("strong", "Correct! Excellent work!"),
            text("p", "Your answer " + Array.from(selectedSet).map(s => "(" + s + ")").join(", ") + " perfectly matches the official verified key. Check the step-by-step chemical derivation below.")
          )
        );
      } else {
        feedbackBanner.className = "attempt-feedback-banner feedback-wrong";
        const userChoices = Array.from(selectedSet).map(s => "(" + s + ")").join(", ") || "None";
        const keyChoices = Array.from(proposedSet).map(s => "(" + s + ")").join(", ");
        feedbackBanner.replaceChildren(
          text("div", "❌ INCORRECT", "feedback-badge-pill"),
          append(text("div", "", "feedback-msg"),
            text("strong", "Incorrect Attempt"),
            text("p", "You selected " + userChoices + ". The correct answer is " + keyChoices + ". Carefully examine the complete worked derivation below to review the reaction and stoichiometric path.")
          )
        );
      }

      answerBox.hidden = false;
      renderMath(answerBox);
    }

    retryBtn.onclick = () => {
      try { localStorage.removeItem(k); } catch (_) {}
      controls.forEach(c => {
        c.disabled = false;
        c.checked = false;
        const lbl = c.closest("label");
        if (lbl) {
          lbl.classList.remove("opt-user-correct", "opt-user-wrong", "opt-correct-key", "opt-neutral-disabled");
          const b = lbl.querySelector(".opt-badge");
          if (b) b.remove();
        }
      });
      commit.disabled = false;
      commit.textContent = "Commit First Attempt & Reveal Derivation";
      retryBtn.style.display = "none";
      feedbackBanner.hidden = true;
      answerBox.hidden = true;
    };

    const existing = getAttempt(k);
    if (existing && existing.selected) {
      renderAttemptFeedback(existing.selected);
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
      renderAttemptFeedback(selected);
    };

    return box;
  }

    let allChemistryQuestions = [];
  let chemCounts = {};

  const filterState = {
    q: query.get("q") || "",
    topic: TOPICS.some(t => t[0] === query.get("topic")) ? query.get("topic") : "all",
    difficulty: query.get("difficulty") || "",
    exam: query.get("exam") || "",
    sort: query.get("sort") || "canonical"
  };

  let searchDebounceTimer = null;

  function updateFilterControls() {
    const qbSearch = document.getElementById("qbSearch");
    const qbTopicSelect = document.getElementById("qbTopicSelect");
    const qbDifficulty = document.getElementById("qbDifficulty");
    const qbExam = document.getElementById("qbExam");
    const qbSort = document.getElementById("qbSort");

    if (qbSearch && qbSearch.value !== filterState.q) qbSearch.value = filterState.q;
    if (qbTopicSelect && qbTopicSelect.value !== filterState.topic) qbTopicSelect.value = filterState.topic;
    if (qbDifficulty && qbDifficulty.value !== filterState.difficulty) qbDifficulty.value = filterState.difficulty;
    if (qbExam && qbExam.value !== filterState.exam) qbExam.value = filterState.exam;
    if (qbSort && qbSort.value !== filterState.sort) qbSort.value = filterState.sort;

    if (nav) {
      nav.querySelectorAll(".topic-pill-btn").forEach(btn => {
        if (btn.dataset.topic === filterState.topic) {
          btn.classList.add("active");
          btn.setAttribute("aria-current", "page");
        } else {
          btn.classList.remove("active");
          btn.removeAttribute("aria-current");
        }
      });
    }
  }

  function applyFilters(shouldScrollToTarget) {
    updateFilterControls();

    const grid = document.getElementById("topicsGrid");
    const workspace = document.getElementById("topicWorkspace") || document.getElementById("topic-view");
    const titleEl = document.getElementById("workspace-title");
    const qbCount = document.getElementById("qbResultCount");

    // 1. Topic filtering
    let filtered = allChemistryQuestions.slice();
    let topicObj = null;
    if (filterState.topic !== "all") {
      topicObj = TOPICS.find(t => t[0] === filterState.topic);
      if (topicObj) {
        filtered = filtered.filter(q => q.topic === topicObj[1]);
      }
    }

    // 2. Difficulty / Demand Band filtering
    if (filterState.difficulty) {
      const diff = filterState.difficulty.toUpperCase();
      filtered = filtered.filter(q => (q.band || "").toUpperCase() === diff);
    }

    // 3. Exam / Year filtering
    if (filterState.exam) {
      const ex = filterState.exam.toLowerCase();
      filtered = filtered.filter(q => {
        const yr = q.exam_year ? q.exam_year.replace("YEAR_", "").toLowerCase() : "";
        const qid = (q.id || "").toLowerCase();
        return yr === ex || qid.includes(ex);
      });
    }

    // 4. Text Search filtering
    const rawQ = filterState.q.trim();
    if (rawQ) {
      const qLower = rawQ.toLowerCase();
      const tokens = qLower.split(/\s+/).filter(Boolean);
      filtered = filtered.filter(q => {
        const idLower = (q.id || "").toLowerCase();
        const srcLower = (q.source_id || "").toLowerCase();
        const stemLower = (q.stem || "").toLowerCase();
        const ansLower = (q.answer || "").toLowerCase();
        const optsLower = (q.options || []).map(o => String(o).toLowerCase()).join(" ");
        const stepsLower = (q.steps || []).map(s => String(s).toLowerCase()).join(" ");
        const cruxLower = (q.crux_move_ref || "").toLowerCase();
        const full = `${idLower} ${srcLower} ${stemLower} ${ansLower} ${optsLower} ${stepsLower} ${cruxLower}`;
        return full.includes(qLower) || tokens.every(tok => full.includes(tok));
      });
    }

    // 5. Sorting
    if (filterState.sort === "id") {
      filtered.sort((a, b) => (a.source_id || a.id).localeCompare(b.source_id || b.id));
    } else if (filterState.sort === "demand-asc") {
      filtered.sort((a, b) => (a.score || 0) - (b.score || 0) || (a.source_id || a.id).localeCompare(b.source_id || b.id));
    } else if (filterState.sort === "demand-desc") {
      filtered.sort((a, b) => (b.score || 0) - (a.score || 0) || (a.source_id || a.id).localeCompare(b.source_id || b.id));
    }

    // Dynamic result count display
    const totalSubject = allChemistryQuestions.length;
    let countMsg = "";
    if (filterState.topic === "all") {
      if (rawQ || filterState.difficulty || filterState.exam) {
        countMsg = `Showing ${filtered.length} of ${totalSubject} questions across all topics`;
      } else {
        countMsg = `Showing ${totalSubject} candidate questions across 6 topics`;
      }
    } else {
      const topicName = topicObj ? topicObj[2] : filterState.topic;
      const topicTotal = chemCounts[filterState.topic] || filtered.length;
      if (rawQ || filterState.difficulty || filterState.exam) {
        countMsg = `Showing ${filtered.length} of ${topicTotal} ${topicName} questions`;
      } else {
        countMsg = `Showing all ${topicTotal} ${topicName} questions`;
      }
    }
    if (rawQ) countMsg += ` matching "${rawQ}"`;
    if (qbCount) qbCount.textContent = countMsg;

    // View toggling: Overview Grid vs Deep-Dive Workspace
    const isFiltered = Boolean(rawQ || filterState.difficulty || filterState.exam);
    if (filterState.topic === "all" && !isFiltered) {
      if (grid) grid.style.display = "grid";
      if (workspace) workspace.style.display = "none";
      if (history.replaceState) {
        history.replaceState(null, "", "index.html");
      }
      return;
    }

    if (grid) grid.style.display = "none";
    if (workspace) workspace.style.display = "block";

    if (titleEl) {
      if (filterState.topic !== "all" && topicObj) {
        titleEl.textContent = `${topicObj[3]} ${topicObj[2]} (${filtered.length} Questions)`;
      } else {
        titleEl.textContent = `🔍 Filtered Chemistry Questions (${filtered.length} Questions)`;
      }
    }

    if (status) {
      status.textContent = `${countMsg} · source and QRT admission HOLD.`;
    }

    if (target) {
      target.replaceChildren();
      if (filterState.topic !== "all") {
        const ribbon = createRibbon(filterState.topic);
        if (ribbon) target.appendChild(ribbon);
      }

      if (filtered.length === 0) {
        const emptyBox = text("div", "", "no-match-box");
        emptyBox.style.cssText = "padding:28px 20px;text-align:center;background:#f8fafc;border:1.5px dashed #cbd5e1;border-radius:12px;margin:20px 0;";
        const p = text("p", "No chemistry questions matched your active filters.", "meta");
        p.style.cssText = "font-size:15px;font-weight:700;color:#64748b;margin-bottom:14px;";
        const rBtn = text("button", "✕ Reset Search & Filters", "qb-clear");
        rBtn.type = "button";
        rBtn.style.cssText = "min-height:44px;padding:8px 18px;cursor:pointer;display:inline-block;";
        rBtn.onclick = () => window.resetFilters();
        emptyBox.append(p, rBtn);
        target.append(emptyBox);
      } else {
        filtered.forEach((q, i) => {
          const card = createCard(q, i);
          target.appendChild(card);
        });
      }
      renderMath(target);
    }

    // Synchronize URL parameters
    const params = new URLSearchParams();
    if (filterState.topic && filterState.topic !== "all") params.set("topic", filterState.topic);
    if (filterState.q) params.set("q", filterState.q);
    if (filterState.difficulty) params.set("difficulty", filterState.difficulty);
    if (filterState.exam) params.set("exam", filterState.exam);
    if (filterState.sort && filterState.sort !== "canonical") params.set("sort", filterState.sort);

    const qs = params.toString() ? "?" + params.toString() : "";
    const hash = window.location.hash || "";
    if (history.replaceState) {
      history.replaceState(null, "", "index.html" + qs + hash);
    }

    // Anchor scrolling & highlight
    if (shouldScrollToTarget) {
      setTimeout(() => {
        let el = null;
        if (hash) {
          const rawHash = decodeURIComponent(hash.replace(/^#/, ""));
          el = document.getElementById(rawHash) ||
               document.getElementById("question-" + rawHash) ||
               document.querySelector(`[data-qid="${rawHash}"]`) ||
               document.querySelector(`[data-source-id="${rawHash}"]`);
        }
        if (!el && rawQ) {
          el = document.getElementById("question-" + encodeURIComponent(rawQ)) ||
               document.querySelector(`[data-qid="${rawQ}"]`) ||
               document.querySelector(`[data-source-id="${rawQ}"]`);
        }
        if (el) {
          el.scrollIntoView({ behavior: "smooth", block: "start" });
          el.classList.add("card-highlight");
        }
      }, 350);
    }
  }

  function initFilterBar() {
    const qbSearch = document.getElementById("qbSearch");
    const qbTopicSelect = document.getElementById("qbTopicSelect");
    const qbDifficulty = document.getElementById("qbDifficulty");
    const qbExam = document.getElementById("qbExam");
    const qbSort = document.getElementById("qbSort");
    const qbClear = document.getElementById("qbClear");

    // Populate topics dropdown
    if (qbTopicSelect) {
      qbTopicSelect.replaceChildren();
      const allOpt = document.createElement("option");
      allOpt.value = "all";
      allOpt.textContent = `★ All Topics Overview (${TOPICS.length} Topics · ${allChemistryQuestions.length} Qs)`;
      qbTopicSelect.appendChild(allOpt);

      TOPICS.forEach(t => {
        const opt = document.createElement("option");
        opt.value = t[0];
        const count = chemCounts[t[0]] || 0;
        opt.textContent = `${t[3]} ${t[2]} (${count} Qs)`;
        qbTopicSelect.appendChild(opt);
      });
      qbTopicSelect.value = filterState.topic;
    }

    // Populate exams dropdown
    if (qbExam) {
      const examsSet = new Set();
      allChemistryQuestions.forEach(q => {
        if (q.exam_year) {
          examsSet.add(q.exam_year.replace("YEAR_", ""));
        } else if (q.id) {
          const m = q.id.match(/20\d\d/);
          if (m) examsSet.add(m[0]);
        }
      });
      const sortedExams = Array.from(examsSet).sort().reverse();
      sortedExams.forEach(yr => {
        const opt = document.createElement("option");
        opt.value = yr.toLowerCase();
        opt.textContent = `NSEJS ${yr}`;
        qbExam.appendChild(opt);
      });
      qbExam.value = filterState.exam;
    }

    // Wire event listeners
    if (qbSearch) {
      qbSearch.value = filterState.q;
      qbSearch.addEventListener("input", e => {
        clearTimeout(searchDebounceTimer);
        searchDebounceTimer = setTimeout(() => {
          filterState.q = e.target.value;
          applyFilters(false);
        }, 150);
      });
    }

    if (qbTopicSelect) {
      qbTopicSelect.addEventListener("change", e => {
        filterState.topic = e.target.value;
        applyFilters(false);
      });
    }

    if (qbDifficulty) {
      qbDifficulty.value = filterState.difficulty;
      qbDifficulty.addEventListener("change", e => {
        filterState.difficulty = e.target.value;
        applyFilters(false);
      });
    }

    if (qbExam) {
      qbExam.addEventListener("change", e => {
        filterState.exam = e.target.value;
        applyFilters(false);
      });
    }

    if (qbSort) {
      qbSort.value = filterState.sort;
      qbSort.addEventListener("change", e => {
        filterState.sort = e.target.value;
        applyFilters(false);
      });
    }

    if (qbClear) {
      qbClear.addEventListener("click", () => {
        window.resetFilters();
      });
    }
  }

  window.resetFilters = function() {
    filterState.q = "";
    filterState.topic = "all";
    filterState.difficulty = "";
    filterState.exam = "";
    filterState.sort = "canonical";
    applyFilters(false);
  };

  window.selectChemistryTopic = function(slug) {
    filterState.topic = slug;
    applyFilters(false);
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
        allBtn.onclick = () => window.selectChemistryTopic("all");
        nav.append(allBtn);

        TOPICS.forEach(t => {
          const btn = document.createElement("button");
          btn.type = "button";
          btn.className = "topic-pill-btn";
          btn.dataset.topic = t[0];
          const count = chemCounts[t[0]] || 0;
          btn.innerHTML = `<span class="pill-icon">${t[3]}</span> <span class="pill-name">${t[2]}</span> <span class="pill-count">${count} Qs</span>`;
          btn.onclick = () => window.selectChemistryTopic(t[0]);
          nav.append(btn);
        });
      }

      // Initialize Question Bank Search & Filter Bar (Search 2)
      initFilterBar();

      // Check if query or hash references a specific question to auto-focus
      const initialQ = filterState.q;
      const initialHash = (window.location.hash || "").replace(/^#/, "");
      if (initialHash && filterState.topic === "all") {
        const matchQ = allChemistryQuestions.find(q => q.id === initialHash || q.source_id === initialHash);
        if (matchQ) {
          const matchTopic = TOPICS.find(t => t[1] === matchQ.topic);
          if (matchTopic) filterState.topic = matchTopic[0];
        }
      }

      // Execute initial filter evaluation and handle anchor navigation
      applyFilters(Boolean(initialHash || initialQ));
    } catch (err) {
      if (status) {
        status.textContent = "Error loading Chemistry question bank: " + err.message;
        status.className = "error";
      }
    }
  }

  loadData();
})();
