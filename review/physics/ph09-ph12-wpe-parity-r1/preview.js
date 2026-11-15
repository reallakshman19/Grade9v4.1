/* PH09–PH12 WPE-parity author-only preview.
 * This browser UI retains a first attempt locally before showing reconstruction.
 * Neither the public JSON nor localStorage constitutes secure examination custody.
 */
(() => {
  "use strict";
  const ROOT = document.querySelector("#parity-preview");
  if (!ROOT) return;
  const $ = id => document.getElementById(id);
  const REVISION = "g9-physics-ph09-ph12-author-preview-r1-20261115";
  let cases = [], current = null, record = null, storageOK = false, blocked = false, datasetRevision = null;

  function say(id, message) { $(id).textContent = message; }
  function storageAvailable() {
    try {
      const probe = "__g9_ph09_ph12_preview_probe__";
      localStorage.setItem(probe, "1");
      const ok = localStorage.getItem(probe) === "1";
      localStorage.removeItem(probe);
      return ok;
    } catch (_) { return false; }
  }
  function storageKey() {
    return REVISION + ":" + current.subtopic_id + ":" + datasetRevision;
  }
  function freshRecord() {
    return { revision: datasetRevision, subtopic_id: current.subtopic_id,
      first: null, exposures: [], revisions: [] };
  }
  function readRecord() {
    try {
      const raw = localStorage.getItem(storageKey());
      if (!raw) return freshRecord();
      const next = JSON.parse(raw);
      if (next.revision !== datasetRevision ||
          next.subtopic_id !== current.subtopic_id ||
          !Object.prototype.hasOwnProperty.call(next, "first") ||
          !Array.isArray(next.revisions) ||
          !Array.isArray(next.exposures)) return null;
      if (next.first && (typeof next.first.predict !== "string" ||
          typeof next.first.attempt !== "string")) return null;
      return next;
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
  function lock(message) {
    blocked = true;
    for (const id of ["first-predict", "first-attempt", "help-button",
      "save-first", "reveal", "revision", "save-revision"])
      $(id).disabled = true;
    $("post-attempt").hidden = true;
    say("attempt-status", message +
      " Attempt/reconstruction is locked until browser storage is writable and valid.");
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
  function resetResponse() {
    for (const id of ["first-predict", "first-attempt", "revision"]) $(id).value = "";
    $("orientation-help").hidden = true;
    $("post-attempt").hidden = true;
    // Do not leave the prior task's revealed solution in a hidden DOM subtree.
    $("reconstruct-list").replaceChildren();
    for (const id of ["diagnose", "repair", "boundary"]) say(id, "");
    say("revision-status", "");
    say("attempt-status", "No first attempt recorded.");
  }
  function choose(id) {
    resetResponse();
    blocked = false;
    current = cases.find(item => item.subtopic_id === id) || null;
    if (!current) { $("journey").hidden = true; return; }
    $("journey").hidden = false;
    say("teach-title", current.chapter + " · " + current.name);
    say("topic-meta", current.subtopic_id + " · Author-authored concept model · Not an authenticated examination source");
    say("conditions", current.science_conditions);
    list("prereqs", current.prerequisites);
    say("teaching-model", current.core1a.model);
    say("worked-question", current.core1a.worked_a);
    list("worked-solution", current.core1a.worked_solution);
    say("worked-check", current.core1a.check);
    say("misconception", current.core1a.misconception);
    say("protected-work", "The new learner-owned decision: " + current.core1b.protected_work);
    say("fresh-task", current.core1b.original_b);
    say("predict-prompt", current.core1b.predict);
    say("attempt-prompt", current.core1b.attempt);
    $("reveal").disabled = true;
    $("revision").disabled = true;
    $("save-revision").disabled = true;
    $("help-button").disabled = true;
    $("save-first").disabled = true;
    $("first-predict").disabled = true;
    $("first-attempt").disabled = true;

    storageOK = storageAvailable();
    if (!storageOK) { lock("Local storage is disabled or inaccessible."); return; }
    record = readRecord();
    if (!record) { lock("A stale or corrupt saved attempt was found."); return; }
    const first = record.first;
    $("first-predict").disabled = Boolean(first);
    $("first-attempt").disabled = Boolean(first);
    $("help-button").disabled = false;
    $("save-first").disabled = Boolean(first);
    $("reveal").disabled = !first;
    if (first) {
      $("first-predict").value = first.predict;
      $("first-attempt").value = first.attempt;
      say("attempt-status", "Original first attempt saved at " + first.at +
        " · Help exposures: " + record.exposures.filter(x => x.type === "ORIENTATION_HELP").length +
        " · Revisions: " + record.revisions.length +
        ". Use the reconstruction button deliberately.");
    } else {
      say("attempt-status", "Predict and attempt independently. Save both before reconstruction.");
    }
  }
  function exposed(type) {
    if (blocked || !current || !record) return false;
    const next = { ...record,
      exposures: [...record.exposures, { type, at: new Date().toISOString() }] };
    if (!writeRecord(next)) { lock("Could not persist the help/reconstruction exposure."); return false; }
    return true;
  }
  function help() {
    if (!exposed("ORIENTATION_HELP")) return;
    $("orientation-help").hidden = false;
    say("attempt-status", "Nondecisive help opened and recorded. Continue your independent attempt.");
  }
  function saveFirst() {
    if (blocked || !record || record.first) return;
    const predict = $("first-predict").value.trim();
    const attempt = $("first-attempt").value.trim();
    if (!predict || !attempt) {
      say("attempt-status", "Both a prediction and an independent reasoning attempt are required.");
      return;
    }
    const next = { ...record,
      first: { predict, attempt, at: new Date().toISOString() } };
    if (!writeRecord(next)) { lock("Could not persist the first attempt."); return; }
    $("first-predict").disabled = true;
    $("first-attempt").disabled = true;
    $("save-first").disabled = true;
    $("reveal").disabled = false;
    say("attempt-status", "First prediction and reasoning saved. Original text will not be overwritten by revisions.");
  }
  function reveal() {
    if (blocked || !record || !record.first) {
      say("attempt-status", "Save your first attempt before reconstructing.");
      return;
    }
    if (!exposed("RECONSTRUCTION")) return;
    list("reconstruct-list", current.core1b.reconstruction);
    say("diagnose", current.core1b.diagnose);
    say("repair", current.core1b.repair);
    say("boundary", current.core1b.boundary);
    $("post-attempt").hidden = false;
    $("revision").disabled = false;
    $("save-revision").disabled = false;
    say("revision-status", "Write a corrected explanation or a boundary-test response; original saved work remains unchanged.");
  }
  function saveRevision() {
    if (blocked || !record || !record.first || $("post-attempt").hidden) return;
    const answer = $("revision").value.trim();
    if (!answer) { say("revision-status", "Write a revision first."); return; }
    const next = { ...record, revisions: [...record.revisions,
      { answer, at: new Date().toISOString() }] };
    if (!writeRecord(next)) { lock("Could not persist the revision."); return; }
    $("revision").value = "";
    say("revision-status", "Revision saved separately (" + record.revisions.length +
      "). Original prediction and attempt remain available above.");
  }
  async function start() {
    try {
      const response = await fetch("./FOUR_WPE_PARITY_REFERENCE_CANDIDATES_R1.json",
        { cache: "no-store", credentials: "same-origin" });
      if (!response.ok) throw new Error("HTTP " + response.status);
      const raw = await response.text();
      if (!crypto || !crypto.subtle) throw new Error("Secure-origin SHA-256 unavailable");
      const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(raw));
      datasetRevision = Array.from(new Uint8Array(digest), n => n.toString(16).padStart(2, "0")).join("");
      const data = JSON.parse(raw);
      if (data.schema !== "g9v41-physics-ph09-ph12-reference-constructions/v1" ||
          data.mode !== "AUTHOR_EXPOSED_REFERENCE_CANDIDATES_ONLY" ||
          data.publication !== "REVIEW_DATA_NOT_STUDENT_ASSIGNED" ||
          data.authority?.student_release !== "HOLD" ||
          !Array.isArray(data.cases) || data.cases.length !== 4)
        throw new Error("Unrecognized or promoted candidate evidence");
      cases = data.cases;
      const options = cases.map(item => {
        const opt = document.createElement("option");
        opt.value = item.subtopic_id;
        opt.textContent = item.chapter + " · " + item.name;
        return opt;
      });
      $("chapter-choice").replaceChildren(...options);
      $("chapter-choice").disabled = false;
      $("chapter-choice").addEventListener("change", value => choose(value.target.value));
      choose(cases[0].subtopic_id);
      say("load-status", "Four original cases loaded. All academic/source admissions are on HOLD.");
    } catch (e) {
      $("chapter-choice").disabled = true;
      $("journey").hidden = true;
      say("load-status", "Candidate data unavailable or invalid: " + String(e.message || e));
    }
  }
  $("help-button").addEventListener("click", help);
  $("save-first").addEventListener("click", saveFirst);
  $("reveal").addEventListener("click", reveal);
  $("save-revision").addEventListener("click", saveRevision);
  start();
})();
