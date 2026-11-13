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
    ["year_2024", "YEAR_2024", "2024 Paper Code 51", "📅"],
    ["year_2023", "YEAR_2023", "2023 Exam Paper", "📅"],
    ["year_2022", "YEAR_2022", "2022 Exam Paper", "📅"],
    ["year_2021", "YEAR_2021", "2021 Exam Paper", "📅"],
    ["year_2020", "YEAR_2020", "2020 Exam Paper", "📅"]
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
        { label: "▶ Phosphorus Oxyacids & Basicity (D3 Flagship)", url: "core1/chem-phosphorus-oxyacids-d3-r1/index.html" }
      ]
    },
    "mole_concept": {
      title: "Mole Concept & Stoichiometry",
      links: [
        { label: "▶ Partial Pressures & Ideal Gas (Skill Repair)", url: "core1/recovery/chem-matter-mole-r1/index.html" },
        { label: "▶ Combustion Eudiometry (Skill Repair)", url: "core1/recovery/chem-eudiometry-d3-r1/index.html" }
      ]
    },
    "reactions": {
      title: "Chemical Substances & Redox Reactions",
      links: [
        { label: "▶ Amphoteric Oxides & Stoichiometry (Skill Repair)", url: "core1/recovery/chem-chemical-substances-r1/index.html" },
        { label: "▶ Redox Titration & Oxidation States (Skill Repair)", url: "core1/recovery/chem-redox-titration-d3-r1/index.html" }
      ]
    },
    "year_2024": {
      title: "IAPT NSEJS 2024 Code 51 Official Exam Paper",
      links: [
        { label: "📑 Official IAPT Source Downloads & Verification Dossier", url: "../official-sources.html" }
      ]
    },
    "year_2023": {
      title: "IAPT NSEJS 2023 Official Exam Paper",
      links: [
        { label: "📑 Official IAPT Source Downloads & Verification Dossier", url: "../official-sources.html" }
      ]
    },
    "year_2022": {
      title: "IAPT NSEJS 2022 Official Exam Paper",
      links: [
        { label: "📑 Official IAPT Source Downloads & Verification Dossier", url: "../official-sources.html" }
      ]
    },
    "year_2021": {
      title: "IAPT IOQJS 2021-22 Part I Official Exam Paper",
      links: [
        { label: "📑 Official IAPT Source Downloads & Verification Dossier", url: "../official-sources.html" }
      ]
    },
    "year_2020": {
      title: "IAPT IOQJS 2020-21 Part I Official Exam Paper",
      links: [
        { label: "📑 Official IAPT Source Downloads & Verification Dossier", url: "../official-sources.html" }
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
    append(box, text("h2", "Candidate " + (index + 1) + " · " + (q.source_id || q.id)));

    const opStr = (q.op || "MODEL");
    const bandStr = (q.band || "D2");
    const scoreStr = q.score ? " (Score " + q.score + ")" : "";
    const meta = text("div", "Cognitive Demand: " + opStr + " · Band: " + bandStr + scoreStr + (q.crux_move_ref ? " · Crux: " + q.crux_move_ref : ""), "meta");
    append(box, meta);

    const statusBadge = text("span", "{Core 2: Candidate Practice} · Rule 13 HOLD", "status");
    append(box, statusBadge);

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

  async function loadData() {
    try {
      status.textContent = "Loading candidate questions from chemistry-core2-candidates.v1.json…";
      const resp = await fetch("../data/chemistry-core2-candidates.v1.json");
      if (!resp.ok) throw new Error("HTTP " + resp.status + " while loading Chemistry question bank data.");
      const data = await resp.json();
      const allQuestions = data.questions || [];

      // Calculate topic counts
      const counts = {};
      TOPICS.forEach(t => {
        const topicKey = t[1];
        counts[t[0]] = allQuestions.filter(q => q.topic === topicKey).length;
      });

      // Build topicNav pills
      nav.replaceChildren();
      TOPICS.forEach(t => {
        const slug = t[0];
        const label = t[2];
        const icon = t[3];
        const count = counts[slug] || 0;
        const btn = text("a", "", "topic-pill-btn");
        btn.href = "question-bank.html?topic=" + encodeURIComponent(slug);
        if (slug === selectedSlug) btn.classList.add("active");
        append(btn,
          text("span", icon, "pill-icon"),
          text("span", label, "pill-name"),
          text("span", String(count), "pill-count")
        );
        nav.appendChild(btn);
      });

      // Filter questions for the selected topic
      const activeTopicKey = TOPICS.find(t => t[0] === selectedSlug)?.[1] || "STRUCTURE_OF_THE_ATOM";
      const activeQuestions = allQuestions.filter(q => q.topic === activeTopicKey);

      target.replaceChildren();

      // Insert ribbon if available
      const ribbon = createRibbon(selectedSlug);
      if (ribbon) target.appendChild(ribbon);

      if (activeQuestions.length === 0) {
        target.appendChild(text("p", "No questions found for this topic.", "meta"));
      } else {
        activeQuestions.forEach((q, i) => {
          const card = createCard(q, i);
          target.appendChild(card);
        });
      }

      status.textContent = "Showing " + activeQuestions.length + " questions for " + (TOPICS.find(t => t[0] === selectedSlug)?.[2] || "Chemistry") + " (Total candidate items in Chemistry bank: " + allQuestions.length + ").";
      renderMath(target);
    } catch (err) {
      status.textContent = "Error loading Chemistry question bank: " + err.message;
      status.className = "error";
    }
  }

  loadData();
})();
