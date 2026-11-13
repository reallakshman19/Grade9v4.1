/* NSEJS Core1A/B adapter to the EXISTING WPEGapJourneys implementation.
 * Does not implement a parallel six-stage state machine, assess written work,
 * authenticate an exam source, or issue academic approval.
 */
(function () {
  "use strict";
  const STAGES = ["Predict", "Attempt", "Reconstruct", "Diagnose", "Repair", "Boundary test"];
  const EXPECTED_ENGINE = "window.WPEGapJourneys";
  const ID = /^[A-Za-z0-9][A-Za-z0-9-]{2,79}$/;
  const SHA = /^[0-9a-f]{64}$/;
  const $ = selector => document.querySelector(selector);

  class ContractError extends Error {
    constructor(code) { super(code); this.name = "NSEJSWPEContractError"; }
  }
  const requireThat = (test, code) => { if (!test) throw new ContractError(code); };
  const authText = value => typeof value === "string" && value.trim().length > 0;

  async function sha256(raw) {
    requireThat(globalThis.crypto && crypto.subtle && typeof TextEncoder !== "undefined",
      "SECURE_SHA256_UNAVAILABLE");
    const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(raw));
    return Array.from(new Uint8Array(digest), b => b.toString(16).padStart(2, "0")).join("");
  }

  async function fetchJSON(relative) {
    requireThat(typeof relative === "string" && relative.startsWith("../") &&
      !relative.includes("://") && !relative.includes("\\") && !relative.includes("..//"),
      "UNSAFE_RESOURCE_PATH");
    const response = await fetch(relative, { cache: "no-store", credentials: "same-origin" });
    requireThat(response.ok, "REQUIRED_RESOURCE_UNAVAILABLE:" + relative + ":" + response.status);
    const raw = await response.text();
    try { return {raw, value: JSON.parse(raw)}; }
    catch (_) { throw new ContractError("INVALID_JSON_RESOURCE:" + relative); }
  }

  function sourcePayload(question) {
    /* Exact property order of nsejs/js/core2-physics-reader.js:revisionPayload. */
    return {
      uid: "g9:PHYSICS:" + question.source_id,
      source_id: question.source_id,
      original_id: question.id,
      stem: question.stem,
      options: question.options,
      answer: question.answer,
      question_type: question.question_type,
      figures: question.source_figures || [],
      figure_note: question.figure_note || "",
      reasoning: question.steps || [],
      boundary: question.check || ""
    };
  }

  function validateContract(contract, bridge, sourceCollection, requested) {
    requireThat(contract?.schema === "grade9-nsejs-wpe-learner-contract/v1"
      && contract.engine === EXPECTED_ENGINE && contract.subject === "PHYSICS"
      && JSON.stringify(contract.stages) === JSON.stringify(STAGES)
      && contract.academic_admission === "HOLD", "LEARNER_CONTRACT_REJECTED");
    const lesson = contract.lesson;
    const source = contract.source;
    requireThat(lesson && source && contract.tasks && contract.tasks.A && contract.tasks.B,
      "INCOMPLETE_LEARNER_CONTRACT");
    requireThat(authText(lesson.id) && ID.test(lesson.id) &&
      authText(lesson.revision) && lesson.revision !== "UNBUILT" &&
      lesson.engine_adapter === "WPE_SCENARIO_DATA_ONLY" &&
      lesson.core1a?.model?.kind === "SLIDER_MODEL" && lesson.topic === "MECHANICS",
      "NON_WPE_OR_UNBUILT_LESSON");
    const guide = lesson.core1a;
    requireThat(["prerequisites", "core", "guide", "wrong", "conditions", "question"]
      .every(k => authText(guide[k])) &&
      Array.isArray(guide.guideSteps) && guide.guideSteps.length >= 5,
      "INCOMPLETE_CORE1A");
    requireThat(source.origin === "AUTHORED_PRACTICE_NOT_OFFICIAL_EXAM"
      && source.academic_admission === "HOLD"
      && authText(source.question_uid) && SHA.test(source.content_revision_sha256),
      "UNQUALIFIED_SOURCE_IDENTITY");
    requireThat(requested.uid === source.question_uid &&
      requested.revision === source.content_revision_sha256,
      "SOURCE_UID_OR_REVISION_MISMATCH");
    requireThat(bridge?.schema === "grade9-nsejs-source-learning-bridge/v1"
      && bridge.academic_admission === "HOLD"
      && bridge.route_status === "TECHNICAL_PREVIEW"
      && bridge.preview_authority === "AUTHORED_TECHNICAL_ONLY_NOT_ACADEMIC_ADMISSION"
      && bridge.source_revision_algorithm === "core2-physics-reader-revisionPayload-sha256/v1"
      && Array.isArray(bridge.routes) && bridge.routes.length === 1,
      "UNTRUSTED_SOURCE_BRIDGE");
    const route = bridge.routes[0];
    requireThat(route.question_uid === source.question_uid &&
      route.content_revision_sha256 === source.content_revision_sha256 &&
      route.subject === "PHYSICS" && route.topic === "MECHANICS" &&
      route.origin === source.origin &&
      route.lesson_id === lesson.id && route.lesson_revision === lesson.revision &&
      route.lesson_status === "READY_FOR_TECHNICAL_PREVIEW" &&
      route.academic_admission === "HOLD" &&
      route.original_source_status === source.origin &&
      route.task_a_id === contract.tasks.A.id &&
      route.task_b_id === contract.tasks.B.id &&
      route.source_collection === "nsejs/data/physics-authored-practice-r1.json",
      "SOURCE_LESSON_OWNER_OR_REVISION_MISMATCH");
    requireThat(contract.source_return?.question_uid === source.question_uid &&
      contract.source_return.content_revision_sha256 === source.content_revision_sha256 &&
      contract.source_return.route_status === "TECHNICAL_PREVIEW" &&
      route.source_return?.question_uid === source.question_uid &&
      route.source_return.content_revision_sha256 === source.content_revision_sha256 &&
      route.source_return.page === "nsejs/physics/question-bank.html" &&
      route.source_return.topic === "mechanics",
      "SOURCE_RETURN_BINDING_INVALID");
    requireThat(sourceCollection?.schema_version === "nsejs-authored-practice/v1" &&
      sourceCollection.source_claim === "AUTHORED_PRACTICE_NOT_OFFICIAL_EXAM" &&
      sourceCollection.academic_release === "HOLD" && Array.isArray(sourceCollection.questions),
      "SOURCE_COLLECTION_UNQUALIFIED");
    const matches = sourceCollection.questions.filter(q => q?.source_id === route.source_id);
    requireThat(matches.length === 1 && matches[0].id === route.source_id &&
      matches[0].topic === "MECHANICS" &&
      matches[0].category === "AUTHORED_PRACTICE" &&
      matches[0].origin === "GRADE9_ORIGINAL_AUTHORING_NOT_EXAM" &&
      matches[0].qrt_adjudication === "HOLD" &&
      matches[0].science_review === "HOLD", "SOURCE_RECORD_PROVENANCE_REJECTED");
    const A = contract.tasks.A, B = contract.tasks.B;
    requireThat(A.id !== B.id && A.id === route.task_a_id && B.id === route.task_b_id &&
      authText(A.reasoning_demand) && authText(B.reasoning_demand) &&
      A.reasoning_demand !== B.reasoning_demand && A.challenge !== B.challenge,
      "TASK_B_NOT_INDEPENDENT");
    for (const task of [A, B]) {
      requireThat(task.first_attempt_policy === "SAVE_BEFORE_REVEAL"
        && task.written_response_grading === "UNASSESSED"
        && Array.isArray(task.fields) && task.fields.length >= 2
        && task.fields.some(f => f.id === "model" && f.type === "select")
        && task.fields.some(f => f.id === "reason" && f.type === "textarea")
        && Array.isArray(task.boundaryFields)
        && task.boundaryFields.some(f => f.id === "why" && f.type === "textarea")
        && Array.isArray(task.hints) && task.hints.length >= 2
        && Array.isArray(task.worked) && task.worked.length >= 3,
        "INCOMPLETE_TASK_OR_PREMATURE_REVEAL");
    }
    return {lesson, source, route, question: matches[0]};
  }

  function failClosed(code) {
    const status = $("#nsejs-parity-status");
    if (status) { status.textContent = "HOLD · Learning route unavailable: " + code;
      status.setAttribute("data-state", "HOLD"); }
    const root = $("#journey-root");
    if (root) {
      root.replaceChildren();
      const p = document.createElement("p"); p.setAttribute("role", "alert");
      p.textContent = "This source-bound lesson cannot safely continue. Your source question is unchanged. " +
        "No first-attempt or academic PASS is claimed.";
      root.append(p);
    }
    const returnLink = $("#nsejs-source-return");
    if (returnLink) returnLink.hidden = true;
    const storage = $("#save-notice");
    if (storage && /STORAGE/.test(code)) { storage.hidden = false;
      storage.textContent = "Browser saving failed. The lesson is blocked before answer reveal; no durable first attempt was recorded."; }
  }

  function storageProbe() {
    try {
      const key = "g9:nsejs:wpe-storage-probe";
      const value = "checked:" + Date.now();
      localStorage.setItem(key, value);
      const verified = localStorage.getItem(key) === value;
      localStorage.removeItem(key);
      return verified;
    } catch (_) { return false; }
  }

  function modelView(lesson, amount, {host, readout, svg, svgText, svgLine, nice}) {
    const p = lesson.reference_physics?.original;
    /* This is a visual illustration, not a replacement for authored science review. */
    const u = p?.u1_mps ?? 8, g = p?.g_mps2 ?? 10;
    const m1 = p?.m1_kg ?? 1, m2 = p?.m2_kg ?? 1;
    const V = (m1 * u + m2 * (p?.u2_mps ?? 0)) / (m1 + m2);
    const mu = amount;
    const distance = mu > 0 ? V * V / (2 * mu * g) : Infinity;
    const width = 470, x = 87, y = 177;
    svgLine(host, 35, y + 38, 605, y + 38, "#667f8b", 4);
    svg(host, "rect", {x, y:y-22, width:110, height:58, rx:9,
      fill:"#acd6db", stroke:"#296e80","stroke-width":2});
    svg(host, "rect", {x:x+110,y:y-22,width:110,height:58,rx:9,
      fill:"#c3d7eb",stroke:"#4676a6","stroke-width":2});
    svgText(host, x+12, y+10, "cart A+B");
    svgLine(host, x+230, y+6, x+310, y+6, "#18826b", 5);
    svgText(host, 55, 72, "Impact: stick · V=" + nice(V) + " m/s");
    svgText(host, 55, 103, "Later slide: μ=" + nice(mu));
    svgText(host, 55, 134, "Stopping distance=" + nice(distance) + " m");
    for (let i=0;i<16;i++) {
      const sx= x + 230 + i*(width-230)/16;
      svgLine(host,sx,y+40,sx+8,y+44,"#ad8546",2);
    }
    readout.textContent = "The brief collision always gives V=" + nice(V) +
      " m/s. Changing only the AFTER-impact friction to μ=" + nice(mu) +
      " changes stopping distance to " + nice(distance) +
      " m. Collision energy loss is not counted again as friction work.";
  }

  function scenarioFor(data) {
    const lesson = data.lesson, g = lesson.core1a, a = data.tasks.A, b = data.tasks.B;
    const slider = g.model;
    return {
      source: data.source.question_uid,
      title: lesson.title, short: lesson.short, question: g.question,
      prerequisites: g.prerequisites, core: g.core, guide: g.guide,
      guideSteps: g.guideSteps, wrong: g.wrong, conditions: g.conditions,
      slider: {label:slider.label, min:slider.min, max:slider.max,
               step:slider.step, value:slider.value},
      academic: g.academic, sourceCaution: lesson.sourceCaution,
      modelView:(amount,helper)=>modelView(lesson,amount,helper),
      prediction: a.prediction, challenge: a.challenge, fields: a.fields,
      hints: a.hints, worked: a.worked, boundary:a.boundary,
      boundaryFields: a.boundaryFields, boundaryCheck: a.boundaryCheck,
      transfer: {label:"Task B · genuinely different physical model",
        prediction:b.prediction,challenge:b.challenge,fields:b.fields,hints:b.hints,
        worked:b.worked,boundary:b.boundary,boundaryFields:b.boundaryFields,
        boundaryCheck:b.boundaryCheck}
    };
  }

  function sourceReturnUrl(route) {
    const relative = route.source_return.page;
    requireThat(relative === "nsejs/physics/question-bank.html", "SOURCE_RETURN_PATH_UNTRUSTED");
    const to = new URL("../../" + relative, location.href);
    to.searchParams.set("topic", route.source_return.topic);
    to.searchParams.set("source_uid", route.question_uid);
    to.searchParams.set("source_revision", route.content_revision_sha256);
    to.hash = "question-" + encodeURIComponent(route.source_id);
    return to.href;
  }

  function readState(prefix, key) {
    try {
      const record = JSON.parse(localStorage.getItem(prefix + key) || "null");
      return record && record.schema === 1 && record.id === key &&
             record.first?.answers?.reason?.trim() &&
             record.stage === 5 && record.boundary?.why?.trim() ? record : null;
    } catch (_) { return null; }
  }

  function precommitRevealAttempt(root, prefix, lessonId, action) {
    // WPE's existing engine renders its next stage even if persist() fails.
    // For the only two solution-revealing actions, commit the actual full
    // stage record to the *same* revision-scoped key before WPE handles click.
    // A small independent storage probe does not protect against quota errors.
    if (action !== "attempt" && action !== "boundary") return true;
    try {
      const selected = localStorage.getItem(prefix + "selected:" + lessonId) === "T2";
      const taskKey = lessonId + (selected ? "-T2" : "");
      const key = prefix + taskKey;
      const record = JSON.parse(localStorage.getItem(key) || "null");
      const stage = action === "attempt" ? 1 : 5;
      if (!record || record.schema !== 1 || record.id !== taskKey ||
          record.stage !== stage ||
          (action === "attempt" ? record.first !== null : record.boundary !== null))
        return true; // WPE's own validation handles invalid or stale clicks.
      const host = root.querySelector(".stage-root");
      if (!host) return false;
      const fields = {};
      host.querySelectorAll("[data-field]").forEach(node => { fields[node.dataset.field] = node.value; });
      if (action === "attempt") {
        if (!fields.reason?.trim() || !fields.model || fields.model === "Choose an idea")
          return true; // WPE will display its normal incomplete-answer warning.
        record.first = {
          answers: {...fields},
          hintsUsed: record.hints.length,
          helpHistory: record.helpHistory.slice(),
          capturedAt: new Date().toISOString()
        };
        record.draft = {};
        record.stage = 2;
      } else {
        if (!fields.why?.trim() ||
            (host.querySelector('[data-field="model"]') &&
             (!fields.model || fields.model === "Choose an idea")))
          return true;
        record.boundary = {...fields, capturedAt: new Date().toISOString()};
      }
      const serialized = JSON.stringify(record);
      localStorage.setItem(key, serialized);
      return localStorage.getItem(key) === serialized;
    } catch (_) {
      return false;
    }
  }

  async function mount(config = {}) {
    try {
      if (typeof window.WPEGapJourneys !== "function") {
        for (let i = 0; i < 20; i++) {
          await new Promise(r => setTimeout(r, 50));
          if (typeof window.WPEGapJourneys === "function") break;
        }
      }
      requireThat(typeof window.WPEGapJourneys === "function", "WPE_ENGINE_MISSING");
      const query = new URLSearchParams(location.search);
      let requestedUID = query.get("source_uid");
      let requestedRev = query.get("source_revision");
      if (!authText(requestedUID) || !SHA.test(requestedRev || "")) {
        requestedUID = "g9:PHYSICS:G9-AUTH-MECH-001";
        requestedRev = "65eadfb0dfc06b4dc3c910ade26d5f5d005efea00be5d7c4f8128b3d45c29259";
      }
      const requested = {uid: requestedUID, revision: requestedRev};
      requireThat(authText(requested.uid) && SHA.test(requested.revision || ""),
        "EXACT_SOURCE_UID_AND_REVISION_REQUIRED");
      const [data, bridgeData, sourceData] = await Promise.all([
        fetchJSON(config.contractUrl), fetchJSON(config.bridgeUrl),
        fetchJSON(config.sourceCollectionUrl)
      ]);
      const {lesson, source, route, question} =
        validateContract(data.value, bridgeData.value, sourceData.value, requested);
      const realRevision = await sha256(JSON.stringify(sourcePayload(question)));
      requireThat(realRevision === source.content_revision_sha256,
        "CURRENT_SOURCE_BYTES_DO_NOT_MATCH_QUESTION_REVISION");
      requireThat(storageProbe(), "STORAGE_UNAVAILABLE_BEFORE_FIRST_ATTEMPT");
      /* Hash the entire actual authored lesson file in addition to the source revision:
       * changing ANY learning text, worked key or numeric expectation isolates attempts.
       */
      const contractDigest = await sha256(data.raw);
      const identityHash = await sha256(
        [source.question_uid, source.content_revision_sha256,
          lesson.id, lesson.revision, contractDigest].join("\0"));
      const prefix = "g9:nsejs:wpe-parity:v1:" + identityHash + ":";
      const buttonRoot = $("#journey-root");
      requireThat(buttonRoot && $("#journey-navigation") && $("#save-notice") &&
        $("#progress-label") && $("#progress-meter") && $("#current-title") &&
        $("#source-journey") && $("#source-return") && $("#source-title") &&
        $("#source-message"), "REQUIRED_WPE_MOUNT_POINTS_MISSING");
      const sourceCaption = $("#nsejs-exact-source");
      if (sourceCaption) sourceCaption.textContent =
        "Authored Mechanics question " + route.source_id + " · source revision " +
        source.content_revision_sha256.slice(0, 12) +
        "… · technical preview · academic HOLD";
      const status = $("#nsejs-parity-status");
      if (status) {status.textContent = "Source and lesson bound · academic HOLD · local unverified practice";
        status.dataset.state = "PREVIEW";}
      const end = $("#nsejs-source-return");
      end.href = sourceReturnUrl(route);
      end.hidden = true;
      const updateReturn = () => {
        const A = readState(prefix, lesson.id);
        const B = readState(prefix, lesson.id + "-T2");
        end.hidden = !(A && B);
        const note = $("#nsejs-completion");
        if (note) note.textContent = A && B ?
          "Task A and Task B are both committed through their changed-condition tests. Return to the exact source revision." :
          "Return to the source is enabled after independent Task A and B boundary attempts. Practice progress is browser-local and not certified mastery.";
      };
      buttonRoot.addEventListener("click", event => {
        const clicked = event.target.closest("button[data-action]");
        if (!clicked) return;
        /* Capture runs before the WPE stage transition. The probe is necessary
         * but insufficient: quota may allow a tiny probe while refusing the
         * real first-response or boundary payload.
         */
        if (!storageProbe()) {
          event.preventDefault(); event.stopImmediatePropagation();
          failClosed("STORAGE_DENIED_DURING_ATTEMPT"); return;
        }
        if (!precommitRevealAttempt(buttonRoot, prefix, lesson.id, clicked.dataset.action)) {
          event.preventDefault(); event.stopImmediatePropagation();
          failClosed("ACTUAL_ATTEMPT_NOT_DURABLY_SAVED"); return;
        }
      }, true);
      buttonRoot.addEventListener("click", event => {
        const clicked = event.target.closest("button[data-action]");
        if (!clicked) return;
        const action = clicked.dataset.action;
        queueMicrotask(() => {
          if (!storageProbe()) { failClosed("STORAGE_WRITE_FAILED"); return; }
          if (action === "attempt") {
            const variant = localStorage.getItem(prefix + "selected:" + lesson.id) === "T2"
              ? lesson.id + "-T2" : lesson.id;
            try {
              const record = JSON.parse(localStorage.getItem(prefix + variant) || "null");
              if (!record?.first?.answers?.reason || record.stage < 2) {
                failClosed("FIRST_RESPONSE_NOT_DURABLY_SAVED");
                return;
              }
            } catch (_) { failClosed("FIRST_RESPONSE_READBACK_FAILED"); return; }
          }
          updateReturn();
        });
      }, false);
      /* WPE is the only learner state engine; the adapter only prepares
       * data, visual model, source-identity checks and persistence guard.
       */
      const scenarios = {[lesson.id]: scenarioFor(data.value)};
      window.WPEGapJourneys(scenarios, {
        storagePrefix:prefix, coveragePath:"../data/learning-coverage-not-applicable.json"
      });
      updateReturn();
      return {status:"TECHNICAL_PREVIEW", source_uid:source.question_uid,
        revision:realRevision, lesson:lesson.id, engine:"WPEGapJourneys",
        academic_admission:"HOLD"};
    } catch (error) {
      failClosed(error instanceof ContractError ? error.message : "ADAPTER_UNEXPECTED_FAILURE");
      return {status:"HOLD", error:String(error)};
    }
  }

  window.NSEJSWPEAdapter = Object.freeze({mount, sourcePayload, validateContract, scenarioFor});
  function init() {
    if (document.body?.dataset?.nsejsMechanicsPilot === "true") {
      mount({contractUrl:"../data/mechanics-wpe-teaching-pilot.v1.json",
        bridgeUrl:"../data/source-learning-bridge-tech-preview.v1.json",
        sourceCollectionUrl:"../data/physics-authored-practice-r1.json"});
    }
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
