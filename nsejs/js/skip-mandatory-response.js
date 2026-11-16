/* Grade9 — optional learner-response SKIP control.
 * No response is fabricated; no first attempt, grade, model/hint or
 * B1–B7 decision is unlocked. Skipping is navigation, not completion.
 * Authored learner pages only; not a secure assessment engine. */
(() => {
  'use strict';
  if (window.Grade9Skip?.version === 'r1') return;
  const script = document.currentScript;
  const root = script?.src ? new URL('../', script.src) : new URL('./nsejs/', location.href);
  const mounted = new WeakSet();
  const state = new WeakMap();
  const ignored = /(?:search|filter|find|username|email|password|login|feedback|comment)/i;
  const types = new Set(['text', 'number']);
  const style = document.createElement('style');
  style.setAttribute('data-g9-skip-style', 'r1');
  style.textContent = [
    '.g9-skip-control{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:8px 0 16px}',
    '.g9-skip-button{box-sizing:border-box;display:inline-flex;align-items:center;justify-content:center;',
    'min-height:56px;min-width:112px;padding:9px 16px;border:2px solid #51657b;border-radius:10px;',
    'background:transparent;color:inherit;font:600 16px/1.4 system-ui,sans-serif;cursor:pointer}',
    '.g9-skip-button:disabled{opacity:.6;cursor:not-allowed}',
    '.g9-skip-button:focus-visible,.g9-skip-continue:focus-visible{outline:3px solid #ad6417;outline-offset:3px}',
    '.g9-skip-status{display:none;width:100%;font:500 14px/1.5 system-ui,sans-serif;color:inherit}',
    '.g9-skip-control[data-skipped="true"] .g9-skip-status{display:block}',
    '.g9-skip-continue{display:none;min-height:44px;align-items:center;padding:7px 9px;',
    'font:600 15px/1.4 system-ui,sans-serif;text-decoration:underline}',
    '.g9-skip-control[data-skipped="true"] .g9-skip-continue{display:inline-flex}',
    '[hidden] .g9-skip-control{display:none!important}'
  ].join('');
  document.head.append(style);

  function subject() {
    const path = location.pathname;
    if (/(^|\/)biology(\/|$)/i.test(path)) return 'biology';
    if (/(^|\/)chemistry(\/|$)/i.test(path)) return 'chemistry';
    if (/(^|\/)mathematics(\/|$)/i.test(path)) return 'mathematics';
    return 'physics';
  }
  function fallback() {
    const s = subject();
    return s === 'mathematics'
      ? new URL('../../mathematics/index.html', root).href
      : new URL(s + '/index.html', root).href;
  }
  function safeNext(field) {
    const container = field.closest('article,section,main') || document;
    const candidates = [
      ...container.querySelectorAll(
        'a[rel="next"],a.g9-next,a.chem-next,a[data-next-question],a[data-next-task]'
      ),
      ...document.querySelectorAll(
        'nav.g9-study-nav a.g9-next,nav.chem-journey-nav a.chem-next'
      )
    ];
    for (const candidate of candidates) {
      if (candidate.closest('[hidden],[aria-hidden="true"]')) continue;
      try {
        const url = new URL(candidate.href, location.href);
        if (url.origin === location.origin && url.href !== location.href &&
            !url.username && !url.password) return {href:url.href,label:'Next lesson or question'};
      } catch (_) {}
    }
    return {href:fallback(),label:'Continue to ' + subject() + ' topics'};
  }
  function eligible(field) {
    if (!(field instanceof HTMLElement) || field.disabled || field.readOnly) return false;
    const tag = field.tagName.toLowerCase();
    if (tag !== 'textarea' && !(tag === 'input' && types.has(field.type))) return false;
    if (field.closest('header,nav,footer,[data-g9-skip-ignore],.g9-skip-control')) return false;
    if (tag === 'input' && !field.required &&
        !/(?:answer|attempt|predict|reason|diagnos|repair|transfer|boundary|response|revision|calculation|value|number)/i.test(
          [field.id,field.name,field.placeholder,field.getAttribute('aria-label')||''].join(' ')
        )) return false;
    if (ignored.test([field.id,field.name,field.placeholder].join(' '))) return false;
    return true;
  }
  function enhance(field) {
    if (mounted.has(field) || !eligible(field)) return;
    mounted.add(field);
    const controls = document.createElement('div');
    controls.className = 'g9-skip-control';
    controls.dataset.g9SkipControl = 'r1';
    controls.dataset.skipped = 'false';
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'g9-skip-button';
    button.textContent = 'Skip for now';
    button.setAttribute('aria-label',
      'Skip this response without submitting an answer or earning credit');
    const message = document.createElement('span');
    message.className = 'g9-skip-status';
    message.setAttribute('role','status');
    message.setAttribute('aria-live','polite');
    message.textContent = 'Skipped for now — no answer submitted or scored. ' +
      'You can return and try it later; protected model feedback stays locked.';
    const next = document.createElement('a');
    next.className = 'g9-skip-continue';
    const id = field.id || field.name ||
      'response-' + Array.from(document.querySelectorAll('textarea,input')).indexOf(field);
    controls.dataset.field = id;
    button.addEventListener('click', () => {
      if (!eligible(field)) return;
      // Do not call the page's original save, submit, next-stage or reveal handlers.
      // A skipped response is never a first attempt or a grade.
      state.set(field, 'SKIPPED_UNASSESSED');
      controls.dataset.skipped = 'true';
      const destination = safeNext(field);
      next.href = destination.href;
      next.textContent = destination.label + ' →';
      button.textContent = 'Skipped — try again';
      field.dispatchEvent(new CustomEvent('g9:skip-response', {
        bubbles:true, detail:{kind:'SKIPPED_UNASSESSED',fieldId:id}
      }));
      message.textContent = field.value.trim()
        ? 'Skipped for now. Your typed text was not submitted or scored. ' +
          'Use the normal Save button if you decide to attempt this later.'
        : 'Skipped for now — no answer submitted or scored. ' +
          'You can return to attempt it; protected feedback stays locked.';
    });
    field.addEventListener('input', () => {
      if (state.get(field) !== 'SKIPPED_UNASSESSED') return;
      state.delete(field);
      controls.dataset.skipped = 'false';
      button.textContent = 'Skip for now';
    });
    controls.append(button,message,next);
    field.insertAdjacentElement('afterend', controls);
  }
  let pending = false;
  function scan() {
    pending = false;
    document.querySelectorAll('main textarea,main input,article textarea,article input,form textarea,form input,'+
      '[data-agent-b-core1b] textarea,[data-agent2-core1b] textarea')
      .forEach(enhance);
  }
  function queue() {
    if (pending) return;
    pending = true;
    Promise.resolve().then(scan);
  }
  const observer = new MutationObserver(mutations => {
    // Skip UI itself creates DOM mutations: ignore controls to avoid churn.
    if (mutations.some(m => {
      if (m.type === 'attributes') return m.target.matches?.('textarea,input');
      return Array.from(m.addedNodes).some(n =>
        n.nodeType === 1 && !n.closest?.('.g9-skip-control') &&
        (n.matches?.('textarea,input') || n.querySelector?.('textarea,input'))
      );
    })) queue();
  });
  function start() {
    scan();
    observer.observe(document.body, {
      childList:true,subtree:true,attributes:true,
      attributeFilter:['disabled','readonly']
    });
  }
  if (document.readyState === 'loading')
    document.addEventListener('DOMContentLoaded', start, {once:true});
  else start();
  window.Grade9Skip = Object.freeze({version:'r1',refresh:queue});
})();
