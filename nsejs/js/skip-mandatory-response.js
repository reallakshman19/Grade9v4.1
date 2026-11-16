/* Grade9 learner text-response Skip R2.
 * A Skip is navigation only, NOT an answer/attempt, grade, B1–B7 result,
 * or permission to reveal model feedback. The control lives outside assessment
 * form DOM so it cannot alter existing save selectors or keyboard Tab sequence. */
(() => {
  'use strict';
  if (window.Grade9Skip?.version === 'r2') return;
  const script = document.currentScript;
  const root = script?.src ? new URL('../', script.src) : new URL('./nsejs/', location.href);
  const mounted = new WeakSet();
  const ignored = /(?:search|filter|find|username|email|password|login|feedback|comment)/i;
  const types = new Set(['text', 'number']);
  const style = document.createElement('style');
  style.setAttribute('data-g9-skip-style','r2');
  style.textContent = [
    '.g9-skip-dock{position:fixed;z-index:600;right:14px;bottom:14px;',
    'max-width:min(360px,calc(100vw - 28px));box-sizing:border-box;',
    'border:2px solid #51657b;border-radius:12px;padding:10px 12px;',
    'background:#fff;color:#213547;box-shadow:0 4px 16px #0002;',
    'font:500 15px/1.5 system-ui,sans-serif}',
    '.g9-skip-dock[hidden]{display:none!important}',
    '.g9-skip-label{font-weight:650;font-size:14px;margin:0 0 6px}',
    '.g9-skip-button{box-sizing:border-box;min-height:56px;min-width:112px;',
    'padding:9px 16px;border:2px solid #51657b;border-radius:10px;',
    'background:#fff;color:#213547;font:700 16px/1.4 system-ui,sans-serif;',
    'cursor:pointer}',
    '.g9-skip-button:focus-visible,.g9-skip-continue:focus-visible{outline:3px solid #ad6417;outline-offset:3px}',
    '.g9-skip-status{display:none;font-size:14px;margin:8px 0}',
    '.g9-skip-dock[data-skipped="true"] .g9-skip-status{display:block}',
    '.g9-skip-continue{display:none;min-height:44px;align-items:center;',
    'padding:7px 9px;text-decoration:underline;font-weight:650}',
    '.g9-skip-dock[data-skipped="true"] .g9-skip-continue{display:inline-flex}',
    '@media(max-width:600px){.g9-skip-dock{left:12px;right:12px;max-width:none}}'
  ].join('');
  document.head.append(style);
  let dock,button,status,next,label,active;
  function subject() {
    const path = location.pathname;
    if (/(^|\/)biology(\/|$)/i.test(path)) return 'biology';
    if (/(^|\/)chemistry(\/|$)/i.test(path)) return 'chemistry';
    if (/(^|\/)mathematics(\/|$)/i.test(path)) return 'mathematics';
    return 'physics';
  }
  function fallback() {
    const s=subject();
    return s==='mathematics'
      ? new URL('../../mathematics/index.html',root).href
      : new URL(s+'/index.html',root).href;
  }
  function safeNext(field) {
    const container=field.closest('article,section,main')||document;
    const candidates=[
      ...container.querySelectorAll(
        'a[rel="next"],a.g9-next,a.chem-next,a[data-next-question],a[data-next-task]'),
      ...document.querySelectorAll(
        'nav.g9-study-nav a.g9-next,nav.chem-journey-nav a.chem-next')
    ];
    for (const candidate of candidates) {
      if (candidate.closest('[hidden],[aria-hidden="true"]')) continue;
      try {
        const url=new URL(candidate.href,location.href);
        if (url.origin===location.origin && url.href!==location.href &&
            !url.username && !url.password)
          return {href:url.href,label:'Next lesson or question'};
      } catch (_) {}
    }
    return {href:fallback(),label:'Continue to '+subject()+' topics'};
  }
  function eligible(field) {
    if (!(field instanceof HTMLElement)||field.disabled||field.readOnly) return false;
    const tag=field.tagName.toLowerCase();
    if (tag!=='textarea'&&!(tag==='input'&&types.has(field.type)))return false;
    if (field.closest('header,nav,footer,[data-g9-skip-ignore],.g9-skip-dock'))return false;
    if (tag==='input'&&!field.required&&
      !/(?:answer|attempt|predict|reason|diagnos|repair|transfer|boundary|response|revision|calculation|value|number)/i.test(
        [field.id,field.name,field.placeholder,field.getAttribute('aria-label')||''].join(' ')
      ))return false;
    if (ignored.test([field.id,field.name,field.placeholder].join(' ')))return false;
    return true;
  }
  function setActive(field) {
    if (!eligible(field) || !dock) return;
    active=field;
    dock.hidden=false;
    const title=field.labels?.[0]?.textContent?.trim()||
      field.getAttribute('aria-label')||field.id||'this response';
    label.textContent='Optional Skip: '+title.slice(0,85);
    const skipped=field.dataset.g9SkipStatus==='SKIPPED_UNASSESSED';
    dock.dataset.skipped=skipped?'true':'false';
    button.textContent=skipped?'Skipped — try again':'Skip for now';
    const link=safeNext(field);
    next.href=link.href;next.textContent=link.label+' →';
    status.textContent='Skipped for now — no answer submitted or scored. '+
      'Your response is still available to attempt later; protected feedback stays locked.';
  }
  function enhance(field) {
    if (mounted.has(field)||!eligible(field))return;
    mounted.add(field);
    field.dataset.g9SkipEligible='r2';
    field.addEventListener('focus',()=>setActive(field));
    field.addEventListener('input',()=>{
      if (field.dataset.g9SkipStatus!=='SKIPPED_UNASSESSED')return;
      field.removeAttribute('data-g9-skip-status');
      if (active===field)setActive(field);
    });
  }
  function createDock(){
    dock=document.createElement('aside');
    dock.id='g9-skip-dock';
    dock.className='g9-skip-dock';
    dock.setAttribute('aria-label','Skip the focused learner response');
    dock.dataset.skipped='false';
    dock.hidden=true;
    label=document.createElement('p');
    label.className='g9-skip-label';
    button=document.createElement('button');
    button.type='button';
    button.className='g9-skip-button';
    button.textContent='Skip for now';
    status=document.createElement('p');
    status.className='g9-skip-status';
    status.setAttribute('role','status');
    status.setAttribute('aria-live','polite');
    next=document.createElement('a');
    next.className='g9-skip-continue';
    button.addEventListener('click',()=>{
      if (!active||!eligible(active)) {dock.hidden=true;return;}
      // Do not set field.value, click Save/Submit, or grant access to a model.
      active.dataset.g9SkipStatus='SKIPPED_UNASSESSED';
      setActive(active);
      if (active.value.trim())
        status.textContent='Skipped for now; typed text was NOT submitted or scored. '+
          'Use the original Save button if you later choose to attempt it.';
      active.dispatchEvent(new CustomEvent('g9:skip-response',{
        bubbles:true,detail:{kind:'SKIPPED_UNASSESSED',fieldId:active.id||active.name||'response'}
      }));
    });
    dock.append(label,button,status,next);
    document.body.append(dock);
    document.addEventListener('focusin',e=>{
      if (eligible(e.target))setActive(e.target);
      else if (dock&&!dock.contains(e.target))dock.hidden=true;
    });
  }
  let pending=false;
  function scan(){
    pending=false;
    document.querySelectorAll(
      'main textarea,main input,article textarea,article input,form textarea,form input,'+
      '[data-agent-b-core1b] textarea,[data-agent2-core1b] textarea'
    ).forEach(enhance);
  }
  function queue(){if(pending)return;pending=true;Promise.resolve().then(scan);}
  function start(){
    createDock();
    scan();
    const observer=new MutationObserver(changes=>{
      if (changes.some(m=>m.type==='attributes'
        ? m.target.matches?.('textarea,input')
        : Array.from(m.addedNodes).some(n=>
          n.nodeType===1&&(n.matches?.('textarea,input')||n.querySelector?.('textarea,input'))
        )))queue();
    });
    observer.observe(document.body,{
      childList:true,subtree:true,attributes:true,attributeFilter:['disabled','readonly']
    });
  }
  if(document.readyState==='loading')
    document.addEventListener('DOMContentLoaded',start,{once:true});
  else start();
  window.Grade9Skip=Object.freeze({version:'r2',refresh:queue});
})();
