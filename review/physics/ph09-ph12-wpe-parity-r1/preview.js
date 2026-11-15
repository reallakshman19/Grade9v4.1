/* PH09–PH12 R2 author-only source → Core1A → protected Core1B → source-return preview.
 * All cases are original authored examples, never authenticated NSEJS source items.
 * Local storage provides review UX, not tamper-resistant examination custody.
 */
(() => {
  "use strict";
  const ROOT = document.querySelector("#parity-preview");
  if (!ROOT) return;
  const $ = id => document.getElementById(id);
  const REVISION = "g9-physics-ph09-ph12-author-preview-r1-20261115";
  const TOPICS = ["PH09", "PH10", "PH11", "PH12"];
  let cases = [], adapters = {}, current = null, record = null, datasetRevision = null, blocked = false;

  function say(id, message) { $(id).textContent = message; }
  function adapterPath(topic) {
    const revision = topic === "PH11" ? "wpe-parity-r3.v1.json" : "wpe-parity-r2.v1.json";
    return "../../../nsejs/physics/curriculum/topics/" + topic +
      "/topic-adapter." + topic + "." + revision;
  }
  function currentAdapter() { return current && adapters[current.chapter]; }
  function storageAvailable() {
    try {
      const probe = "__g9_ph09_ph12_preview_probe__";
      localStorage.setItem(probe, "1");
      const yes = localStorage.getItem(probe) === "1";
      localStorage.removeItem(probe);
      return yes;
    } catch (_) { return false; }
  }
  function storageKey() {
    return REVISION + ":" + current.subtopic_id + ":" + datasetRevision;
  }
  function freshRecord() {
    return { revision: datasetRevision, subtopic_id: current.subtopic_id,
      source_first: null, first: null, reconstruction_comparison: null,
      diagnosis: null, revisions: [], boundary_answer: null,
      source_return: null, exposures: [] };
  }
  function readRecord() {
    try {
      const raw = localStorage.getItem(storageKey());
      if (!raw) return freshRecord();
      const data = JSON.parse(raw);
      if (data.revision !== datasetRevision || data.subtopic_id !== current.subtopic_id ||
          !Array.isArray(data.revisions) || !Array.isArray(data.exposures) ||
          !Object.prototype.hasOwnProperty.call(data, "source_first") ||
          !Object.prototype.hasOwnProperty.call(data, "first") ||
          !Object.prototype.hasOwnProperty.call(data, "diagnosis") ||
          !Object.prototype.hasOwnProperty.call(data, "boundary_answer")) return null;
      if (data.source_first && typeof data.source_first.answer !== "string") return null;
      if (data.first && (!data.source_first ||
          typeof data.first.predict !== "string" ||
          typeof data.first.attempt !== "string")) return null;
      if (data.reconstruction_comparison && !data.first) return null;
      if (data.diagnosis && !data.reconstruction_comparison) return null;
      if (data.revisions.length && !data.diagnosis) return null;
      if (data.boundary_answer && !data.revisions.length) return null;
      if (data.source_return && !data.boundary_answer) return null;
      return data;
    } catch (_) { return null; }
  }
  function writeRecord(next) {
    try {
      const serialized = JSON.stringify(next);
      localStorage.setItem(storageKey(), serialized);
      if (localStorage.getItem(storageKey()) !== serialized) return false;
      record = next;
      return true;
    } catch (_) { return false; }
  }
  function lock(why) {
    blocked = true;
    ROOT.querySelectorAll("textarea, button").forEach(n => { n.disabled = true; });
    $("post-attempt").hidden = true;
    $("diagnose-stage").hidden = true;
    $("repair-stage").hidden = true;
    $("boundary-stage").hidden = true;
    $("source-return-stage").hidden = true;
    clearReview();
    say("attempt-status", why + " Review is locked; no protected reasoning will be shown.");
    say("source-status", why + " Source-first checkpoint locked.");
  }
  function list(id, items) {
    const dest = $(id);
    dest.replaceChildren();
    for (const item of items) {
      const li = document.createElement("li");
      li.textContent = item;
      dest.appendChild(li);
    }
  }
  function clearReview() {
    $("reconstruct-list").replaceChildren();
    for (const id of ["diagnose", "repair", "boundary", "source-return-question"])
      say(id, "");
    for (const id of ["reconstruct-response", "diagnosis-response", "revision",
      "boundary-response", "source-return-response"])
      $(id).value = "";
  }
  function reset() {
    clearReview();
    $("prereqs").replaceChildren();
    $("worked-solution").replaceChildren();
    for (const id of ["teach-title", "topic-meta", "conditions", "teaching-model",
      "worked-question", "worked-check", "misconception", "protected-work",
      "fresh-task", "predict-prompt", "attempt-prompt"]) say(id, "");
    for (const id of ["source-attempt", "first-predict", "first-attempt"]) $(id).value = "";
    $("source-checkpoint").hidden = true;
    $("journey").hidden = true;
    $("post-attempt").hidden = true;
    for (const id of ["diagnose-stage", "repair-stage", "boundary-stage", "source-return-stage"])
      $(id).hidden = true;
    $("orientation-help").hidden = true;
    for (const id of ["source-save", "source-learn", "first-predict", "first-attempt",
      "help-button", "save-first", "reveal", "reconstruct-response", "save-reconstruct",
      "diagnosis-response", "save-diagnosis", "revision", "save-revision",
      "boundary-response", "save-boundary", "source-return-response", "save-source-return"])
      $(id).disabled = true;
    for (const id of ["source-status", "attempt-status", "revision-status",
      "stage-status", "source-return-status"]) say(id, "");
  }
  function sourceSaved() { return record && record.source_first; }
  function sourceStart() {
    if (blocked || !current || !record || record.source_first) return;
    const answer = $("source-attempt").value.trim();
    if (answer.length < 10) {
      say("source-status", "Write your own initial model and reasoning before continuing.");
      return;
    }
    const next = { ...record, source_first: { answer, at: new Date().toISOString() } };
    if (!writeRecord(next)) { lock("Source-first attempt could not be persisted."); return; }
    $("source-attempt").disabled = true;
    $("source-save").disabled = true;
    $("source-learn").disabled = false;
    say("source-status", "Original source-style attempt saved independently. Open Core1A when ready.");
  }
  function renderTeaching() {
    if (!current || !sourceSaved()) return;
    say("teach-title", current.chapter + " · " + current.name);
    say("topic-meta", current.subtopic_id +
      " · Original teaching candidate · Source and QRT independent review HOLD");
    say("conditions", current.science_conditions);
    list("prereqs", current.prerequisites);
    say("teaching-model", current.core1a.model);
    say("worked-question", current.core1a.worked_a);
    list("worked-solution", current.core1a.worked_solution);
    say("worked-check", current.core1a.check);
    say("misconception", current.core1a.misconception);
    // Never mount the protected author move or its formula-bearing attempt guidance.
    say("protected-work", "Select your own model, variables, checks and reasoning independently.");
    say("fresh-task", current.core1b.original_b);
    say("predict-prompt", current.core1b.predict);
    say("attempt-prompt", "Record the model you chose and defend each step without viewing feedback.");
  }
  function openTeaching() {
    if (blocked || !sourceSaved()) return;
    renderTeaching();
    $("journey").hidden = false;
    $("first-predict").disabled = Boolean(record.first);
    $("first-attempt").disabled = Boolean(record.first);
    $("help-button").disabled = false;
    $("save-first").disabled = Boolean(record.first);
    $("reveal").disabled = !record.first;
    if (record.first) {
      $("first-predict").value = record.first.predict;
      $("first-attempt").value = record.first.attempt;
      say("attempt-status", "First challenge attempt saved at " + record.first.at +
        ". Reopen reconstruction deliberately; original reasoning is preserved.");
    } else {
      say("attempt-status", "Predict and attempt the NEW challenge independently before reconstruction.");
    }
  }
  function choose(id) {
    reset();
    blocked = false;
    current = cases.find(x => x.subtopic_id === id) || null;
    record = null;
    if (!current) return;
    const adapter = currentAdapter();
    if (!adapter || adapter.task.subtopic_id !== id || adapter.source.exam_source_uid !== null) {
      lock("Topic-adapter/source identity mismatch.");
      return;
    }
    $("source-checkpoint").hidden = false;
    say("source-question", adapter.source.stem);
    $("source-adapter-link").setAttribute("href", adapterPath(current.chapter));
    // Source-first gate: teaching and transfer are NOT mounted even in hidden DOM
    // until a valid source-style first attempt is durably recorded.
    const sub = current.subtopic_id;
    const base = "../../../nsejs/physics/curriculum/topics/" + current.chapter + "/";
    const a = (current.chapter === "PH09" || current.chapter === "PH10") ?
      base + "subtopics/" + sub + "/core1a.html" : base + "index.html";
    const b = (current.chapter === "PH09" || current.chapter === "PH10") ?
      base + "subtopics/" + sub + "/core1b.html" : base + "core1b-preview.html";
    $("core1a-existing").setAttribute("href", a);
    $("core1b-existing").setAttribute("href", b);
    if (!storageAvailable()) { lock("Local storage is unavailable."); return; }
    record = readRecord();
    if (!record) { lock("Stale or corrupt content-bound attempt record."); return; }
    const first = record.source_first;
    $("source-attempt").disabled = Boolean(first);
    $("source-save").disabled = Boolean(first);
    $("source-learn").disabled = !first;
    if (first) {
      $("source-attempt").value = first.answer;
      say("source-status", "Original source-style attempt saved at " + first.at +
        "; you may continue to Core1A.");
    } else {
      say("source-status", "Attempt this separate author checkpoint before viewing Core1A.");
    }
  }
  function exposed(type) {
    if (blocked || !current || !record) return false;
    const next = { ...record,
      exposures: [...record.exposures, { type, at: new Date().toISOString() }] };
    if (!writeRecord(next)) { lock("Help or feedback exposure could not be persisted."); return false; }
    return true;
  }
  function help() {
    if (!sourceSaved() || !exposed("ORIENTATION_HELP")) return;
    $("orientation-help").hidden = false;
    say("attempt-status", "Nondecisive help exposed and recorded. Continue independently.");
  }
  function saveFirst() {
    if (blocked || !sourceSaved() || record.first || $("journey").hidden) return;
    const predict = $("first-predict").value.trim();
    const attempt = $("first-attempt").value.trim();
    if (!predict || !attempt) {
      say("attempt-status", "Prediction AND independent reasoning are both required.");
      return;
    }
    const next = { ...record, first: { predict, attempt, at: new Date().toISOString() } };
    if (!writeRecord(next)) { lock("First challenge attempt could not be persisted."); return; }
    $("first-predict").disabled = true;
    $("first-attempt").disabled = true;
    $("save-first").disabled = true;
    $("reveal").disabled = false;
    say("attempt-status", "First challenge answer persisted, without exposing the solution.");
  }
  function showDiagnostic() {
    if (!record.reconstruction_comparison) return;
    $("diagnose-stage").hidden = false;
    say("diagnose", current.core1b.diagnose);
    $("diagnosis-response").disabled = Boolean(record.diagnosis);
    $("save-diagnosis").disabled = Boolean(record.diagnosis);
    if (record.diagnosis) $("diagnosis-response").value = record.diagnosis.answer;
  }
  function showRepair() {
    if (!record.diagnosis) return;
    $("repair-stage").hidden = false;
    say("repair", current.core1b.repair);
    $("revision").disabled = false;
    $("save-revision").disabled = false;
  }
  function showBoundary() {
    if (!record.revisions.length) return;
    $("boundary-stage").hidden = false;
    say("boundary", current.core1b.boundary);
    $("boundary-response").disabled = Boolean(record.boundary_answer);
    $("save-boundary").disabled = Boolean(record.boundary_answer);
    if (record.boundary_answer) $("boundary-response").value = record.boundary_answer.answer;
  }
  function showSourceReturn() {
    if (!record.boundary_answer) return;
    $("source-return-stage").hidden = false;
    say("source-return-question", currentAdapter().source.stem);
    $("source-return-response").disabled = Boolean(record.source_return);
    $("save-source-return").disabled = Boolean(record.source_return);
    if (record.source_return) $("source-return-response").value = record.source_return.answer;
  }
  function reveal() {
    if (blocked || !sourceSaved() || !record.first) {
      say("attempt-status", "Persist an independent first attempt before reconstruction.");
      return;
    }
    if (!exposed("RECONSTRUCTION")) return;
    // Materialize only reconstruction. Later stage prompts are NOT mounted yet.
    $("post-attempt").hidden = false;
    list("reconstruct-list", current.core1b.reconstruction);
    $("reconstruct-response").disabled = Boolean(record.reconstruction_comparison);
    $("save-reconstruct").disabled = Boolean(record.reconstruction_comparison);
    if (record.reconstruction_comparison) {
      $("reconstruct-response").value = record.reconstruction_comparison.answer;
      showDiagnostic();
    }
    if (record.diagnosis) showRepair();
    if (record.revisions.length) showBoundary();
    if (record.boundary_answer) showSourceReturn();
    say("stage-status", "Compare your own first explanation with the reconstruction before diagnosis.");
  }
  function saveReconstruct() {
    if (blocked || !record.first || $("post-attempt").hidden || record.reconstruction_comparison) return;
    const answer = $("reconstruct-response").value.trim();
    if (!answer) { say("stage-status", "Write a comparison with your original evidence."); return; }
    const next = { ...record, reconstruction_comparison: { answer, at: new Date().toISOString() } };
    if (!writeRecord(next)) { lock("Reconstruction comparison could not be saved."); return; }
    $("reconstruct-response").disabled = true;
    $("save-reconstruct").disabled = true;
    showDiagnostic();
    say("stage-status", "Comparison persisted; diagnose using evidence from your actual answer.");
  }
  function saveDiagnosis() {
    if (blocked || !record.reconstruction_comparison || record.diagnosis || $("diagnose-stage").hidden) return;
    const answer = $("diagnosis-response").value.trim();
    if (!answer) { say("stage-status", "Record evidence for or against the misconception."); return; }
    const next = { ...record, diagnosis: { answer, at: new Date().toISOString() } };
    if (!writeRecord(next)) { lock("Diagnostic evidence could not be persisted."); return; }
    $("diagnosis-response").disabled = true;
    $("save-diagnosis").disabled = true;
    showRepair();
    say("stage-status", "Diagnostic evidence saved; now repair the model.");
  }
  function saveRevision() {
    if (blocked || !record.diagnosis || $("repair-stage").hidden) return;
    const answer = $("revision").value.trim();
    if (!answer) { say("revision-status", "Write the repaired reasoning first."); return; }
    const next = { ...record, revisions: [...record.revisions,
      { answer, at: new Date().toISOString() }] };
    if (!writeRecord(next)) { lock("Repair revision could not be persisted."); return; }
    $("revision").value = "";
    showBoundary();
    say("revision-status", "Revision saved separately (" + record.revisions.length +
      "); original challenge attempt remains unchanged.");
  }
  function saveBoundary() {
    if (blocked || !record.revisions.length || $("boundary-stage").hidden || record.boundary_answer) return;
    const answer = $("boundary-response").value.trim();
    if (!answer) { say("stage-status", "Write your own boundary-case reasoning."); return; }
    const next = { ...record, boundary_answer: { answer, at: new Date().toISOString() } };
    if (!writeRecord(next)) { lock("Boundary transfer could not be persisted."); return; }
    $("boundary-response").disabled = true;
    $("save-boundary").disabled = true;
    showSourceReturn();
    say("stage-status", "Boundary response preserved before returning to the authored source checkpoint.");
  }
  function saveSourceReturn() {
    if (blocked || !record.boundary_answer || $("source-return-stage").hidden || record.source_return) return;
    const answer = $("source-return-response").value.trim();
    if (!answer) { say("source-return-status", "Write a revised, independent source-checkpoint response."); return; }
    const next = { ...record, source_return: { answer, at: new Date().toISOString() } };
    if (!writeRecord(next)) { lock("Source return could not be persisted."); return; }
    $("source-return-response").disabled = true;
    $("save-source-return").disabled = true;
    say("source-return-status", "Source return saved without overwriting the first source or Core1B attempts. This is NOT proof of learner mastery.");
  }
  async function start() {
    try {
      const response = await fetch("./FOUR_WPE_PARITY_REFERENCE_CANDIDATES_R1.json",
        { cache: "no-store", credentials: "same-origin" });
      if (!response.ok) throw new Error("Author case HTTP " + response.status);
      const raw = await response.text();
      const data = JSON.parse(raw);
      if (data.schema !== "g9v41-physics-ph09-ph12-reference-constructions/v1" ||
          data.mode !== "AUTHOR_EXPOSED_REFERENCE_CANDIDATES_ONLY" ||
          data.publication !== "REVIEW_DATA_NOT_STUDENT_ASSIGNED" ||
          data.authority?.student_release !== "HOLD" ||
          !Array.isArray(data.cases) || data.cases.length !== 4)
        throw new Error("Source/academic author-only case authority mismatch");
      let versionMaterial = raw;
      for (const topic of TOPICS) {
        const url = adapterPath(topic);
        const result = await fetch(url, { cache: "no-store", credentials: "same-origin" });
        if (!result.ok) throw new Error(topic + " adapter HTTP " + result.status);
        const adapterRaw = await result.text();
        const adapter = JSON.parse(adapterRaw);
        const expectedSchema = topic === "PH11"
          ? "g9v41-physics-wpe-parity-topic-adapter-r3/v1"
          : "g9v41-physics-wpe-parity-topic-adapter-r2/v1";
        const expectedStatus = topic === "PH11"
          ? "AUTHOR_EXPOSED_ADVERSARIAL_REVIEW__INDEPENDENT_QRT_HOLD"
          : "AUTHOR_EXPOSED_QRT_PROPOSAL__INDEPENDENT_HOLD";
        if (adapter.schema !== expectedSchema ||
            adapter.topic_id !== topic ||
            adapter.academic_status !== expectedStatus ||
            adapter.source?.not_an_official_exam !== true ||
            adapter.source.exam_source_uid !== null ||
            adapter.assertions?.owner_release !== "HOLD" ||
            adapter.assertions?.independent_qrt !== "NOT_RUN" ||
            adapter.task?.qrt_independent !== "NOT_RUN")
          throw new Error(topic + " candidate adapter not fail-closed");
        const factors = Object.values(adapter.task.factor_evidence);
        if (factors.length !== 5 || factors.some(f => !Number.isInteger(f.score) ||
            f.score < 0 || f.score > 2 || !f.evidence.trim()) ||
            factors.reduce((n, f) => n + f.score, 0) !== adapter.task.proposed_total)
          throw new Error(topic + " factor evidence malformed");
        adapters[topic] = adapter;
        versionMaterial += "\n--ADAPTER--\n" + adapterRaw;
      }
      if (!crypto || !crypto.subtle) throw new Error("SHA-256 not available on secure origin");
      const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(versionMaterial));
      datasetRevision = Array.from(new Uint8Array(digest), n => n.toString(16).padStart(2, "0")).join("");
      cases = data.cases;
      if (new Set(cases.map(x => x.chapter)).size !== 4 ||
          cases.some(x => !adapters[x.chapter] ||
            adapters[x.chapter].task.subtopic_id !== x.subtopic_id ||
            adapters[x.chapter].task.protected_decisive_work !== x.core1b.protected_work ||
            adapters[x.chapter].source.stem === x.core1b.original_b))
        throw new Error("Source–adapter–Core1A/B link invalid");
      const options = cases.map(item => {
        const opt = document.createElement("option");
        opt.value = item.subtopic_id;
        opt.textContent = item.chapter + " · " + item.name;
        return opt;
      });
      $("chapter-choice").replaceChildren(...options);
      $("chapter-choice").disabled = false;
      $("chapter-choice").addEventListener("change", value => choose(value.target.value));
      const params = new URLSearchParams(location.search);
      const desired = params.get("case");
      choose(cases.some(x => x.subtopic_id === desired) ? desired : cases[0].subtopic_id);
      $("chapter-choice").value = current.subtopic_id;
      say("load-status", "Four source → teaching → transfer candidate routes loaded. Independent academic/QRT evidence HOLD.");
    } catch (err) {
      $("chapter-choice").disabled = true;
      $("source-checkpoint").hidden = true;
      $("journey").hidden = true;
      $("post-attempt").hidden = true;
      say("load-status", "Cannot begin unqualified/invalid route: " + String(err.message || err));
    }
  }
  $("source-save").addEventListener("click", sourceStart);
  $("source-learn").addEventListener("click", openTeaching);
  $("help-button").addEventListener("click", help);
  $("save-first").addEventListener("click", saveFirst);
  $("reveal").addEventListener("click", reveal);
  $("save-reconstruct").addEventListener("click", saveReconstruct);
  $("save-diagnosis").addEventListener("click", saveDiagnosis);
  $("save-revision").addEventListener("click", saveRevision);
  $("save-boundary").addEventListener("click", saveBoundary);
  $("save-source-return").addEventListener("click", saveSourceReturn);
  start();
})();
