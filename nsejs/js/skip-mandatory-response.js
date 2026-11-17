/* Grade9 learner per-question Skip R3.
 * A Skip is navigation only, NOT an answer/attempt, grade, B1–B7 result,
 * or permission to reveal model feedback. The control lives outside assessment
 * form DOM so it cannot alter existing save selectors or keyboard Tab sequence. */
(() => {
  'use strict';
  if (window.Grade9Skip) return;
  const script = document.currentScript;
  const root = script?.src ? new URL('../', script.src) : new URL('./nsejs/', location.href);
  const mounted = new WeakSet();
  const inlineByField = new WeakMap();
  const ignored = /(?:search|filter|find|username|email|password|login|feedback|comment)/i;
  const types = new Set(['text', 'number']);
  const questionSelectors = 'main textarea,main input,main select,main fieldset,article textarea,article input,article select,article fieldset,form textarea,form input,form select,form fieldset,[data-agent-b-core1b] textarea,[data-agent2-core1b] textarea';
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
    '.g9-skip-inline{display:flex;align-items:center;flex-wrap:wrap;gap:8px 12px;',
    'margin:8px 0 16px;padding:10px 12px;border:1px solid #a6bac8;',
    'border-radius:10px;background:#f4f9fb;font:500 14px/1.4 system-ui,sans-serif}',
    '.g9-skip-inline [hidden]{display:none!important}',
    '.g9-skip-inline-button,.g9-skip-inline-advance{min-height:48px;',
    'padding:9px 14px;border:2px solid #51738a;border-radius:9px;background:#fff;',
    'color:#173b55;font:700 15px/1.4 system-ui,sans-serif;cursor:pointer}',
    '.g9-skip-inline-next{min-height:44px;display:inline-flex;align-items:center;',
    'font-weight:700;color:#175779;text-underline-offset:3px}',
    '.g9-skip-inline-status{flex-basis:100%;color:#375567;font-weight:600;margin:0}',
    '.g9-skip-inline button:focus-visible,.g9-skip-inline a:focus-visible{',
    'outline:3px solid #ad6417;outline-offset:2px}',
    '@media(max-width:600px){.g9-skip-dock{left:12px;right:12px;max-width:none}',
    '.g9-skip-inline{align-items:stretch}.g9-skip-inline-button{width:100%}}'
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
    const radioGroup=tag==='fieldset'&&!!field.querySelector('input[type="radio"]')&&
      !!field.querySelector('legend');
    const questionSelect=tag==='select'&&(field.required||field.hasAttribute('data-question-select'));
    if (tag!=='textarea'&&!(tag==='input'&&types.has(field.type))&&
      !radioGroup&&!questionSelect)return false;
    if (questionSelect&&/(?:unit|topic|task|filter|sort|difficulty|exam|mode|chapter)/i.test(
      [field.id,field.name].join(' ')))return false;
    if (field.closest('header,nav,footer,[data-g9-skip-ignore],.g9-skip-dock,.g9-skip-inline'))return false;
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
    // The inline question control is visible without focusing the response.
    // Retain the old dock only for unusual DOMs where inline mounting failed.
    if (inlineByField.has(field)) {dock.hidden=true;return;}
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
  function visible(field){
    return field.getClientRects().length>0 && !field.closest('[hidden],[aria-hidden="true"]');
  }
  function nextResponse(field){
    const candidates=[...document.querySelectorAll(questionSelectors)]
      .filter(f=>eligible(f)&&visible(f)&&inlineByField.has(f));
    const i=candidates.indexOf(field);
    return i<0?null:candidates.slice(i+1).find(f=>f!==field)||null;
  }
  function nextTaskSelector(){
    const selector=document.querySelector('#task-select,select[data-task-select]');
    if (!selector||selector.disabled)return null;
    const current=selector.selectedIndex;
    const options=[...selector.options];
    const index=options.findIndex((option,i)=>i>current&&!option.disabled&&option.value);
    return index<0?null:{selector,index};
  }
  function advanceWithoutAnswer(field){
    const following=nextResponse(field);
    if(following){following.scrollIntoView({block:'center'});following.focus();return;}
    const task=nextTaskSelector();
    if(task){
      task.selector.selectedIndex=task.index;
      task.selector.dispatchEvent(new Event('change',{bubbles:true}));
      return;
    }
    const destination=safeNext(field);
    if(destination.href)location.assign(destination.href);
  }
  function fieldLabel(field){
    return field.labels?.[0]?.textContent?.trim()||
      field.querySelector?.('legend')?.textContent?.trim()||
      field.getAttribute('aria-label')||field.id||field.name||'this question';
  }
  function createInline(field){
    const wrap=document.createElement('div');
    wrap.className='g9-skip-inline';
    wrap.dataset.skipped='false';
    wrap.setAttribute('role','group');
    wrap.setAttribute('aria-label','Optional question controls: '+fieldLabel(field).slice(0,90));
    const skip=document.createElement('button');
    skip.type='button';
    skip.className='g9-skip-inline-button';
    skip.textContent='Skip this question · no credit';
    const advance=document.createElement('button');
    advance.type='button';
    advance.className='g9-skip-inline-advance';
    advance.textContent='Next question →';
    advance.hidden=true;
    const link=document.createElement('a');
    link.className='g9-skip-inline-next';
    link.hidden=true;
    const statusText=document.createElement('p');
    statusText.className='g9-skip-inline-status';
    statusText.setAttribute('role','status');
    statusText.setAttribute('aria-live','polite');
    statusText.hidden=true;
    wrap.append(skip,advance,link,statusText);
    field.insertAdjacentElement('afterend',wrap);
    inlineByField.set(field,{wrap,skip,advance,link,statusText});
    field.dataset.g9SkipInline='r3';
    function refresh(){
      const skipped=field.dataset.g9SkipStatus==='SKIPPED_UNASSESSED';
      wrap.dataset.skipped=skipped?'true':'false';
      skip.textContent=skipped?'Undo skip · try this question':'Skip this question · no credit';
      const following=nextResponse(field);
      const task=nextTaskSelector();
      advance.hidden=!skipped||(!following&&!task);
      advance.textContent=following?'Next response →':'Next question →';
      const destination=safeNext(field);
      link.href=destination.href;
      link.textContent=destination.label+' →';
      link.hidden=!skipped;
      statusText.hidden=!skipped;
      if(skipped)statusText.textContent='Skipped · not submitted, scored, or counted as mastery. '+
        (field.value?.trim()?'Your draft is unchanged and unsaved. ':'')+
        'Protected model feedback remains locked; try again at any time.';
    }
    skip.addEventListener('click',()=>{
      const wasSkipped=field.dataset.g9SkipStatus==='SKIPPED_UNASSESSED';
      if(wasSkipped){
        field.removeAttribute('data-g9-skip-status');
        refresh();field.focus();return;
      }
      // Never fabricate answers, trigger form validation, commit an attempt,
      // advance the protected stage, or unlock a model.
      field.dataset.g9SkipStatus='SKIPPED_UNASSESSED';
      refresh();
      field.dispatchEvent(new CustomEvent('g9:skip-response',{
        bubbles:true,detail:{kind:'SKIPPED_UNASSESSED',fieldId:field.id||field.name||'response'}
      }));
    });
    advance.addEventListener('click',()=>advanceWithoutAnswer(field));
    const undoOnInput=()=>{
      if(field.dataset.g9SkipStatus!=='SKIPPED_UNASSESSED')return;
      field.removeAttribute('data-g9-skip-status');refresh();
    };
    field.addEventListener('input',undoOnInput);
    field.addEventListener('change',undoOnInput);
    refresh();
  }
  function enhance(field) {
    if (mounted.has(field)||!eligible(field))return;
    mounted.add(field);
    field.dataset.g9SkipEligible='r3';
    field.addEventListener('focusin',()=>setActive(field));
    createInline(field);
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
    document.querySelectorAll(questionSelectors).forEach(enhance);
  }
  function queue(){if(pending)return;pending=true;Promise.resolve().then(scan);}
  function start(){
    createDock();
    scan();
    const observer=new MutationObserver(changes=>{
      if (changes.some(m=>m.type==='attributes'
        ? m.target.matches?.('textarea,input')
        : Array.from(m.addedNodes).some(n=>
          n.nodeType===1&&(n.matches?.('textarea,input,select,fieldset')||n.querySelector?.('textarea,input,select,fieldset'))
        )))queue();
    });
    observer.observe(document.body,{
      childList:true,subtree:true,attributes:true,attributeFilter:['disabled','readonly']
    });
  }
  if(document.readyState==='loading')
    document.addEventListener('DOMContentLoaded',start,{once:true});
  else start();
  window.Grade9Skip=Object.freeze({version:'r3',refresh:queue});
})();
