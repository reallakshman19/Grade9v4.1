/* Wave 3: source-first NSEJS Mechanics learner routing, with no Core2 key or
 * WPE engine rewrites. An authored source gets a link ONLY when full question
 * revision, lesson revision, task ownership and HOLD provenance match. */
(function () {
  "use strict";
  const ROOT = document.getElementById("questions");
  const NOTICE = document.getElementById("learning-return-status");
  if (!ROOT || !NOTICE) return;

  const HEX = /^[a-f0-9]{64}$/;
  const UID = "g9:PHYSICS:G9-AUTH-MECH-001";
  const SOURCE_ID = "G9-AUTH-MECH-001";
  const SOURCE = "../data/physics-authored-practice-r1.json";
  const ROUTE = "../data/source-learning-bridge-tech-preview.v1.json";
  const LESSON = "../data/mechanics-wpe-teaching-pilot.v1.json";
  const LINK = "learn-mechanics.html";
  const params = new URLSearchParams(location.search);
  const returnRequested = params.has("source_uid") || params.has("source_revision");
  let accepted = null, pending = false, once = false;

  function block(message) {
    NOTICE.textContent = "HOLD · " + message +
      " No original-question identity, answer approval or learner success is inferred.";
    NOTICE.dataset.state = "HOLD";
    NOTICE.hidden = false;
  }

  async function bytesHash(raw) {
    if (!crypto?.subtle) throw Error("SHA256_UNAVAILABLE");
    const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(raw));
    return Array.from(new Uint8Array(digest), b => b.toString(16).padStart(2, "0")).join("");
  }

  /* Must be byte-for-byte equivalent to the revisionPayload used by the
   * unchanged Core2 reader and Wave 1 source_learning_bridge.py. */
  function revisionPayload(q) {
    return JSON.stringify({
      uid:"g9:PHYSICS:" + q.source_id,
      source_id:q.source_id, original_id:q.id,
      stem:q.stem, options:q.options, answer:q.answer,
      question_type:q.question_type,
      figures:q.source_figures || [],
      figure_note:q.figure_note || "",
      reasoning:q.steps || [],
      boundary:q.check || ""
    });
  }

  async function fetchData(path) {
    const response = await fetch(path, {cache:"no-store", credentials:"same-origin"});
    if (!response.ok) throw Error("MISSING_REQUIRED_PREVIEW_DATA:" + path);
    return response.json();
  }

  function validRoute(route, bridge, source, lesson) {
    if (bridge?.schema !== "grade9-nsejs-source-learning-bridge/v1" ||
        bridge.academic_admission !== "HOLD" ||
        bridge.route_status !== "TECHNICAL_PREVIEW" ||
        bridge.preview_authority !== "AUTHORED_TECHNICAL_ONLY_NOT_ACADEMIC_ADMISSION" ||
        !Array.isArray(bridge.routes) || bridge.routes.length !== 1) return false;
    if (!route || route.question_uid !== UID || route.source_id !== SOURCE_ID ||
        route.content_revision_sha256 !== source?.content_revision_sha256 ||
        !HEX.test(route.content_revision_sha256) ||
        route.lesson_status !== "READY_FOR_TECHNICAL_PREVIEW" ||
        route.lesson_revision !== lesson?.lesson?.revision ||
        route.lesson_id !== lesson.lesson.id ||
        route.task_a_id !== lesson?.tasks?.A?.id ||
        route.task_b_id !== lesson?.tasks?.B?.id ||
        !route.transfer_id || new Set([route.task_a_id,route.task_b_id,route.transfer_id]).size !== 3 ||
        route.subject !== "PHYSICS" || route.topic !== "MECHANICS" ||
        route.origin !== "AUTHORED_PRACTICE_NOT_OFFICIAL_EXAM" ||
        route.original_source_status !== route.origin ||
        route.academic_admission !== "HOLD" ||
        route.source_collection !== "nsejs/data/physics-authored-practice-r1.json" ||
        route.source_return?.page !== "nsejs/physics/question-bank.html" ||
        route.source_return.topic !== "mechanics" ||
        route.source_return.question_uid !== UID ||
        route.source_return.content_revision_sha256 !== route.content_revision_sha256 ||
        !source || source.question_uid !== UID ||
        source.academic_admission !== "HOLD" ||
        source.origin !== route.origin ||
        lesson.academic_admission !== "HOLD" ||
        lesson.source_return?.question_uid !== UID ||
        lesson.source_return?.content_revision_sha256 !== route.content_revision_sha256 ||
        lesson.source_return?.route_status !== "TECHNICAL_PREVIEW" ||
        lesson.engine !== "window.WPEGapJourneys") return false;
    return true;
  }

  async function bind() {
    const [bridge,collection,lesson] = await Promise.all([
      fetchData(ROUTE), fetchData(SOURCE), fetchData(LESSON)
    ]);
    const route = bridge?.routes?.[0];
    const candidates = collection?.questions;
    if (collection?.schema_version !== "nsejs-authored-practice/v1" ||
        collection.source_claim !== "AUTHORED_PRACTICE_NOT_OFFICIAL_EXAM" ||
        collection.academic_release !== "HOLD" ||
        !Array.isArray(candidates)) throw Error("UNQUALIFIED_SOURCE_COLLECTION");
    const matches = candidates.filter(q => q && q.source_id === SOURCE_ID);
    if (matches.length !== 1) throw Error("SOURCE_AMBIGUOUS_OR_MISSING");
    const question = matches[0];
    if (question.id !== SOURCE_ID || question.category !== "AUTHORED_PRACTICE" ||
        question.origin !== "GRADE9_ORIGINAL_AUTHORING_NOT_EXAM" ||
        question.topic !== "MECHANICS" ||
        question.qrt_adjudication !== "HOLD" ||
        question.science_review !== "HOLD" ||
        question.review_state !== "NOT_ADMITTED") throw Error("UNQUALIFIED_AUTHOR_PROVENANCE");
    if (!validRoute(route,bridge,lesson.source,lesson))
      throw Error("ROUTE_LESSON_SOURCE_REVISION_OR_READINESS_MISMATCH");
    if (await bytesHash(revisionPayload(question)) !== route.content_revision_sha256)
      throw Error("SOURCE_BYTES_CHANGED");
    return route;
  }

  function safeReturnFragment() {
    // A malformed percent-encoded fragment must produce a visible HOLD, not
    // an unhandled URIError that prevents all source-return diagnostics.
    try { return decodeURIComponent(location.hash.slice(1)); }
    catch (_) { return null; }
  }

  function reconcile() {
    if (!accepted) return;
    const route = accepted;
    const cards = ROOT.querySelectorAll("article.card[data-question-uid]");
    for (const card of cards) {
      if (card.dataset.questionUid !== UID) continue;
      if (card.dataset.contentRevision !== route.content_revision_sha256) {
        if (returnRequested) block("Source card revision does not match the requested lesson");
        continue;
      }
      if (card.querySelector("#nsejs-authored-learning-route")) continue;
      const holder = document.createElement("div");
      holder.id = "nsejs-authored-learning-route";
      holder.className = "nsejs-learning-route";
      const label = document.createElement("p");
      label.textContent = "Core1A → Core1B authored Mechanics: learn why the collision and the later friction use different models. Technical preview; academic HOLD.";
      const link = document.createElement("a");
      link.textContent = "Open six-stage Mechanics learning →";
      link.className = "nsejs-learning-touch-link";
      const url = new URL(LINK, location.href);
      url.searchParams.set("source_uid", UID);
      url.searchParams.set("source_revision", route.content_revision_sha256);
      link.href = url.href;
      holder.append(label,link);
      card.append(holder);
    }
    if (once || !returnRequested) return;
    const returnedUID = params.get("source_uid");
    const returnedRevision = params.get("source_revision");
    if (returnedUID !== UID || returnedRevision !== route.content_revision_sha256 ||
        params.get("topic") !== "mechanics" ||
        (params.has("uid") && params.get("uid") !== UID) ||
        safeReturnFragment() !== "question-" + SOURCE_ID) {
      block("Requested return has invalid source UID, revision, topic or fragment");
      once = true; return;
    }
    const target = Array.from(cards).find(c =>
      c.dataset.questionUid === returnedUID &&
      c.dataset.contentRevision === returnedRevision);
    if (!target) return; // Core2 candidate cards may still be loading asynchronously.
    once = true;
    target.classList.add("nsejs-exact-source-return");
    target.setAttribute("tabindex", "-1");
    target.focus({preventScroll:true});
    target.scrollIntoView({block:"start",behavior:"instant"});
    NOTICE.textContent = "Exact authored Mechanics source revision verified and focused. The saved learner work is local, not a verified exam result. Academic HOLD.";
    NOTICE.dataset.state = "PREVIEW";
    NOTICE.hidden = false;
  }

  // Async Core2 card creation may append the right card after the route data loads.
  // A small observer is simpler and safer than changing its integrity or grading code.
  const observer = new MutationObserver(() => {
    if (pending) return;
    pending = true;
    queueMicrotask(() => {pending=false; reconcile();});
  });
  observer.observe(ROOT,{childList:true,subtree:false});
  bind().then(route => {accepted=route;reconcile();}).catch(error => {
    accepted = null;
    if (returnRequested) block("Source-linked learning route unavailable: " + error.message);
  });
})();
