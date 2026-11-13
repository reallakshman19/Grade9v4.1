/* B02 optics-only candidate route bridge. Does not alter Core2 answers, source
 * admission, shared QRT contracts, or other topics. Card UID + observed content
 * revision are checked against the exact reader data attributes before linking.
 * Unknown/stale revisions fail closed. No academic approval inferred. */
(function () {
  "use strict";
  const bank = document.getElementById("questions");
  if (!bank) return;
  const prefix = "nsejs/physics/";
  const routeUrl = "curriculum/topics/PH09/subtopics/core2-optics-routes.v1.json";
  const safePage = /^nsejs\/physics\/curriculum\/topics\/PH(?:09|10)\/subtopics\/(?:PH(?:09|10)-\d{2}\/)?[a-zA-Z0-9-]+\.html$/;
  function appendLink(box, path, label, hash) {
    if (!safePage.test(path)) return;
    const a = document.createElement("a");
    a.href = path.slice(prefix.length) + (hash || "");
    a.textContent = label;
    a.className = "ribbon-btn";
    box.appendChild(a);
  }
  function attach(card, route) {
    if (card.querySelector("[data-b02-core2-route]")) return;
    if (card.dataset.questionUid !== route.question_uid) return;
    const exact = (route.observed_revisions || []).find(
      item => item.revision === card.dataset.contentRevision
    );
    if (!exact) return; // fail closed: no stale link
    if (route.academic_admission !== "HOLD" || route.exact_source !== "HOLD") return;
    const box = document.createElement("section");
    box.dataset.b02Core2Route = route.source_id;
    box.setAttribute("aria-label", "B02 optics candidate learning links");
    box.className = "nsejs-topic-ribbon";
    const title = document.createElement("strong");
    title.textContent = "B02 · " + route.primary_subtopic + " · Core1A / Core1B candidate routes";
    box.appendChild(title);
    const note = document.createElement("p");
    note.textContent = "ACADEMIC HOLD · " + route.route_role + ". " + route.science_or_source_hold;
    box.appendChild(note);
    const topic = route.primary_subtopic.slice(0,4);
    const register = prefix + "curriculum/topics/" + topic + "/subtopics/core2-links.html";
    const blocked = route.route_role === "BLOCKED_EXAM_LOCATOR" ||
      exact.source_evidence_status === "OFFICIAL_ID_CONTRADICTED";
    if (!blocked) {
      appendLink(box, route.targeted_core1a || route.core1a, "Read " + route.primary_subtopic + " Core1A");
      appendLink(box, route.targeted_core1b || route.core1b, "Attempt fresh Core1B");
    }
    appendLink(box, register, blocked ? "Source contradiction audit (no learning-target admission)" : "Question-to-subtopic coverage and limitations", "#" + encodeURIComponent(route.source_id));
    card.appendChild(box);
  }
  fetch(routeUrl, {cache:"no-store",credentials:"same-origin"})
    .then(r => { if (!r.ok) throw Error("B02 route data unavailable"); return r.json(); })
    .then(data => {
      if (data.schema !== "g9v41-b02-core2-optics-routes/v1" ||
          data.status !== "CANDIDATE_LINKS_ONLY__ACADEMIC_HOLD" || !Array.isArray(data.routes)) return;
      const byId = new Map();
      for (const route of data.routes) {
        if (route.source_collection !== "nsejs/data/physics-core2-candidates.v1.json") continue;
        if (byId.has(route.source_id)) return;
        byId.set(route.source_id, route);
      }
      const scan = () => bank.querySelectorAll("[data-source-id][data-question-uid][data-content-revision]").forEach(card => {
        const route = byId.get(card.dataset.sourceId);
        if (route) attach(card, route);
      });
      const observer = new MutationObserver(scan);
      observer.observe(bank,{childList:true,subtree:true,attributes:true,attributeFilter:["data-question-uid","data-content-revision"]});
      scan();
    }).catch(() => { /* Unavailable or invalid route manifest: no links. */ });
})();
