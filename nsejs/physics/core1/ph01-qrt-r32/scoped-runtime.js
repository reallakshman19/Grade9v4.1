"use strict";
(function () {
  const $ = (id) => document.getElementById(id);
  const URL_PACK = "../../curriculum/agent1/PH01/physics-topic-package.v1_1.r3_2.json";
  const URL_SUPPORT = "../../curriculum/agent1/PH01/ph01-core1b-support.r3_2.json";
  // R3.2 is a new content revision. Earlier R2/R3.1 records stay in their historical namespaces.
  const STORAGE_PREFIX = "G9V41:PH01:R32:";
  const scope = document.body.dataset.scope;
  const validScopes = new Set(["PH01-M03","PH01-M04","PH01-M05","PH01-M06","PH01-M07","PH01-M08","MAIN"]);
  let cycles = [], supports = new Map(), revision = "", current = null;
  let record = null, persistOK = false;
  const say = (value) => { $("runtimeStatus").textContent = value; };
  const canRead = () => {
    try {const k = STORAGE_PREFIX + "probe"; localStorage.setItem(k, "1");localStorage.removeItem(k);return true;}
    catch (_) {return false;}
  };
  const key = () => STORAGE_PREFIX + revision + ":" + current.id;
  const show = (id, visible) => {$(id).hidden = !visible;};
  const now = () => new Date().toISOString();
  const safe = (s) => String(s ?? "");
  const write = (id, val) => {$(id).textContent = safe(val);};
  const exposed = (code) => record && record.help_exposure.some(x => x.kind === code);
  function persist(next) {
    if (!persistOK || !current) return false;
    try {
      localStorage.setItem(key(), JSON.stringify(next));
      record = next;
      return true;
    } catch (_) {
      persistOK = false;
      say("Local storage failed. Work remains visible for copying, but no answer or hint will be unlocked.");
      return false;
    }
  }
  function exposure(kind) {
    if (!record || exposed(kind)) return true;
    const next = structuredClone(record);
    next.help_exposure.push({kind, opened_at: now()});
    return persist(next);
  }
  function hints() {
    const info = supports.get(current.id);
    const h = info.hints;
    const root = $("hintButtons");
    root.replaceChildren();
    for (const code of ["H1", "H2", "H3"]) {
      const b = document.createElement("button");
      b.className = "secondary"; b.textContent = "Open " + code;
      const order = ["H1", "H2", "H3"].indexOf(code);
      b.disabled = !record || exposed(code) ||
        (order > 0 && !exposed(["H1", "H2", "H3"][order - 1]));
      b.addEventListener("click", () => {
        if (exposure(code)) renderSaved();
      });
      root.appendChild(b);
    }
    const revealed = ["H1", "H2", "H3"].filter(x => exposed(x));
    write("hintsOpened", revealed.map(x => x + " · " + h[x]).join("\n\n") || "Hints remain closed.");
  }
  function renderSaved() {
    const saved = !!(record && record.first_answer);
    show("postAttempt", saved);
    $("saveFirst").disabled = saved || !persistOK;
    $("predictInput").disabled = saved;
    $("attemptInput").disabled = saved;
    if (saved) {
      write("savedFirst", "First response · " + record.first_answer.saved_at +
        "\nPrediction: " + record.first_answer.prediction +
        "\nReasoning: " + record.first_answer.answer);
      show("savedFirst", true);
      write("saveStatus", "First attempt is immutable in this activity. Repairs and help exposure are saved separately.");
      hints();
      const opened = exposed("RECONSTRUCT");
      show("reconstructAnswer", opened);
      if (opened) write("reconstructAnswer", current.stages.reconstruct);
      $("showReconstruct").disabled = opened || !persistOK;
      const boundaryOpened = exposed("BOUNDARY_MODEL");
      show("boundaryAnswer", boundaryOpened);
      if (boundaryOpened) write("boundaryAnswer", supports.get(current.id).boundary_solution);
      $("showBoundary").disabled = !persistOK || !record.boundary_attempts.length || boundaryOpened;
    } else {
      show("savedFirst", false);
      write("saveStatus", persistOK
        ? "First answer has not been saved. Solutions and hints stay locked."
        : "Storage is blocked. No answer, hint or mastery event can be unlocked.");
    }
  }
  function loadCycle(id) {
    current = cycles.find(c => c.id === id);
    if (!current) return;
    record = null;
    if (persistOK) {
      try {
        const stored = localStorage.getItem(key());
        if (stored) {
          const parsed = JSON.parse(stored);
          if (parsed.content_revision === revision &&
              parsed.task_id === current.id && Array.isArray(parsed.help_exposure)) record = parsed;
        }
      } catch (_) {persistOK = false;}
    }
    $("metaType").textContent = current.kind + " cycle";
    $("metaCell").textContent = current.cell_id + " · proposed, not qualified";
    $("metaRevision").textContent = "SHA-256 " + revision.slice(0, 12);
    for (const [id, text] of Object.entries({
      predictPrompt: current.stages.predict,
      attemptPrompt: current.fresh_task,
      reconstructPrompt: "Compare your saved first reasoning with the complete physical route only when you choose to reveal it.",
      diagnosePrompt: current.stages.diagnose,
      repairPrompt: current.stages.repair,
      boundaryPrompt: current.stages.boundary_test
    })) write(id, text);
    for (const t of ["predictInput", "attemptInput", "diagnoseInput", "repairInput", "boundaryInput"]) $(t).value = "";
    if (record && record.first_answer) {
      $("predictInput").value = record.first_answer.prediction;
      $("attemptInput").value = record.first_answer.answer;
    }
    say(persistOK
      ? "Candidate task loaded. First answer protection active; first response and help exposure are revision-bound."
      : "Storage unavailable. Candidate task is readable, but hints and answers cannot be unlocked.");
    show("journey", true);
    renderSaved();
  }
  async function load() {
    try {
      persistOK = canRead();
      const [a, b] = await Promise.all([fetch(URL_PACK), fetch(URL_SUPPORT)]);
      if (!a.ok || !b.ok) throw new Error("Candidate content source was not found.");
      const [rawA, rawB] = await Promise.all([a.text(), b.text()]);
      const pack = JSON.parse(rawA), support = JSON.parse(rawB);
      if (pack.schema !== "g9v41-nsejs-physics-topic-package/v1.1" ||
          pack.status !== "DRAFT_AUTHOR_EXPOSED" || pack.acceptance.release !== "HOLD" ||
          support.schema !== "g9v41-ph01-core1b-support/v1" ||
          support.status !== "AUTHOR_EXPOSED_CANDIDATE__ACADEMIC_HOLD") {
        throw new Error("Unknown or unexpectedly approved content; fail closed.");
      }
      if (!crypto || !crypto.subtle) throw new Error("Cryptographic revision hashing is unavailable.");
      const bytes = new TextEncoder().encode(rawA + "\n" + rawB);
      const digest = await crypto.subtle.digest("SHA-256", bytes);
      revision = [...new Uint8Array(digest)].map(x => x.toString(16).padStart(2, "0")).join("");
      cycles = pack.core1b;
      if (!Array.isArray(cycles) || cycles.length !== 27 || !Array.isArray(support.cycles) || pack.version !== support.package_version ||
          support.cycles.length !== cycles.length) throw new Error("Task or support inventory mismatch.");
      supports = new Map(support.cycles.map(x => [x.cycle_id, x]));
      if (supports.size !== cycles.length || new Set(cycles.map(c=>c.id)).size !== cycles.length || cycles.some(c => !supports.has(c.id) || c.runtime_verification !== "NOT_RUN" ||
          c.attempt_policy.save_first_answer_before_hint !== true)) {
        throw new Error("Missing support or invalid source authority.");
      }
      if (!validScopes.has(scope)) throw new Error("Unknown learning scope.");
      cycles = cycles.filter(c => scope === "MAIN" ? c.kind === "MAIN" : c.kind === "INSTANCE" && c.subtopic_id === scope);
      if (cycles.length !== 3 || new Set(cycles.map(c => c.cell_id)).size !== 3 || !["D3.4","D3.5","D3.6"].every(cell => cycles.some(c => c.cell_id === cell))) throw new Error("Scoped learning inventory mismatch.");
      const sorted = [...cycles].sort((x, y) => (x.kind === "MAIN" ? -1 : 1) -
        (y.kind === "MAIN" ? -1 : 1));
      for (const cycle of sorted) {
        const o = document.createElement("option");
        o.value = cycle.id;
        o.textContent = cycle.kind + " · " + cycle.cell_id + " · " +
          ({"D3.4":"MODEL","D3.5":"REPRESENT","D3.6":"SYNTHESIZE"}[cycle.cell_id]) + " · " + (cycle.kind === "MAIN" ? "integrated reasoning" : cycle.subtopic_id);
        $("cycleSelect").appendChild(o);
      }
      $("cycleSelect").addEventListener("change", () => loadCycle($("cycleSelect").value));
      loadCycle($("cycleSelect").value);
    } catch (err) {
      say("Task loading failed closed: " + safe(err.message));
      $("cycleSelect").disabled = true; show("journey", false);
    }
  }
  $("saveFirst").addEventListener("click", () => {
    if (!current || (record && record.first_answer)) return;
    const answer = $("attemptInput").value.trim();
    const prediction = $("predictInput").value.trim();
    if (!answer || !prediction) {write("saveStatus", "Write both a prediction and your own reasoning first.");return;}
    const next = {
      schema: "g9v41-ph01-first-attempt/v1",task_id: current.id,
      content_revision: revision,
      first_answer: {prediction, answer, saved_at: now()},
      help_exposure: record ? record.help_exposure : [], diagnosis_notes: [], revisions: [], boundary_attempts: [],
      mastery_status: "UNASSESSED"
    };
    if (persist(next)) renderSaved();
  });
  $("showReconstruct").addEventListener("click", () => {
    if (record && exposure("RECONSTRUCT")) renderSaved();
  });
  $("saveDiagnose").addEventListener("click", () => {
    const note = $("diagnoseInput").value.trim();
    if (!record || !note) return;
    const next = structuredClone(record);
    next.diagnosis_notes.push({text: note, saved_at: now(),kind: "LEARNER_SELF_REPORT_NOT_DIAGNOSIS"});
    if (persist(next)) { $("diagnoseInput").value = ""; say("Self-report saved separately from your first attempt."); }
  });
  $("saveRepair").addEventListener("click", () => {
    const note = $("repairInput").value.trim();
    if (!record || !note) return;
    const next = structuredClone(record);
    next.revisions.push({text: note, saved_at: now(),helped: next.help_exposure.length > 0});
    if (persist(next)) { $("repairInput").value = ""; say("Repair saved; the first attempt remains unchanged."); }
  });
  $("saveBoundary").addEventListener("click", () => {
    const answer = $("boundaryInput").value.trim();
    if (!record || !answer) return;
    const next = structuredClone(record);
    next.boundary_attempts.push({text: answer,saved_at: now(),exposed_before_attempt: next.help_exposure.map(x=>x.kind)});
    if (persist(next)) { say("Changed-condition response saved before its model was shown."); renderSaved(); }
  });
  $("showBoundary").addEventListener("click", () => {
    if (record && record.boundary_attempts.length && exposure("BOUNDARY_MODEL")) renderSaved();
  });
  for (const link of document.querySelectorAll("[data-textbook-help]")) link.addEventListener("click", (event) => {
    if (!current) {event.preventDefault(); say("Wait until a candidate task is loaded before opening linked help."); return;}
    if (record && record.first_answer) {
      if (!exposure("TEXTBOOK_AFTER_FIRST")) {
        event.preventDefault();
        say("Cannot record linked-help exposure. Copy your attempt before leaving.");
      }
    } else {
      const exposureList = record && Array.isArray(record.help_exposure)
        ? record.help_exposure : [];
      const ok = persistOK && persist({
        schema: "g9v41-ph01-exposure-pre-first/v1",task_id: current.id,
        content_revision: revision, first_answer: null,
        help_exposure: exposureList.some(x => x.kind === "TEXTBOOK_BEFORE_FIRST")
          ? exposureList : [...exposureList, {kind: "TEXTBOOK_BEFORE_FIRST",opened_at:now()}],
        diagnosis_notes: [], revisions: [], boundary_attempts: [], mastery_status: "UNASSESSED"
      });
      if (!ok) {
        event.preventDefault();
        say("Cannot record linked-help exposure. Open the textbook separately outside this protected activity.");
      }
    }
  });
  load();
})();

