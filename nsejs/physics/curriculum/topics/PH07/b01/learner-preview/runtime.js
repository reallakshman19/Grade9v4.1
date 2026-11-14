/* B01 takeover R1 — candidate protected-sequence preview.
   Revision-bound localStorage is pedagogic sequencing only, NOT tamper-proof custody.
   Public JSON includes author solutions. No canonical MAIN, exam admission or mastery.
*/
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const HOME = '../../../../../../../';  // repo root relative to b01/learner-preview/
  const ROOT = new URL(HOME, location.href);
  const PREVIEW = 'g9-b01-r1:';
  const state = { tasks: [], current: null, record: null, digest: null, ready: false, source: null, storageOK: false };
  function status(text, kind) { $('status').textContent = text; $('status').dataset.kind = kind || 'info'; }
  function bool(id, show) { $(id).hidden = !show; }
  function lock(reason) {
    state.ready = false; $('task-select').disabled = true;
    bool('learner', false); bool('after-first', false);
    status('Fail closed: ' + reason + '. Reader is unavailable for this attempt.', 'blocked');
  }
  function hex(bytes) { return [...new Uint8Array(bytes)].map(b => b.toString(16).padStart(2, '0')).join(''); }
  function bytes(text) { return new TextEncoder().encode(text); }
  async function hash(text, kind) { return hex(await crypto.subtle.digest(kind, bytes(text))); }
  async function gitBlob(text) {
    const data = bytes(text);
    const head = bytes('blob ' + data.length + '\0');
    const body = new Uint8Array(head.length + data.length);
    body.set(head); body.set(data, head.length);
    return hex(await crypto.subtle.digest('SHA-1', body));
  }
  async function request(path, expectedBlob) {
    if (!/^[\w./-]+\.json$/.test(path) || path.includes('..')) throw Error('Invalid source path');
    const url = new URL(path, ROOT);
    if (url.origin !== location.origin) throw Error('Untrusted source origin');
    const res = await fetch(url.href, {cache:'no-store', credentials:'same-origin'});
    if (!res.ok) throw Error('Missing pinned package: ' + path);
    const raw = await res.text();
    if (expectedBlob && await gitBlob(raw) !== expectedBlob)
      throw Error('Pinned Git blob mismatch: ' + path);
    return { json: JSON.parse(raw), raw };
  }
  function storageProbe() {
    try { const k=PREVIEW+'probe'; localStorage.setItem(k,'ok');
      const ok=localStorage.getItem(k)==='ok'; localStorage.removeItem(k); return ok;
    } catch (_) { return false; }
  }
  function key() { return PREVIEW + state.digest + ':' + state.current.id; }
  function blank() {
    return {schema:'g9-b01-attempt-r1',task_id:state.current.id,content_revision:state.digest,
      first_answer:null,help_exposure:[],diagnosis_notes:[],repairs:[],boundary_attempts:[],
      mastery_status:'UNASSESSED'};
  }
  function valid(r) {
    return r && r.schema==='g9-b01-attempt-r1' && r.task_id===state.current.id &&
      r.content_revision===state.digest && (r.first_answer===null ||
        (typeof r.first_answer.prediction==='string' && typeof r.first_answer.answer==='string')) &&
      ['help_exposure','diagnosis_notes','repairs','boundary_attempts'].every(k=>Array.isArray(r[k])) &&
      r.mastery_status==='UNASSESSED';
  }
  function read() {
    try { const x=localStorage.getItem(key()); if(!x) return blank();
      const r=JSON.parse(x); return valid(r)?r:null;
    } catch (_) { return null; }
  }
  function write(r) {
    if (!valid(r)) return false;
    try {
      const raw=JSON.stringify(r);localStorage.setItem(key(),raw);
      if (localStorage.getItem(key())!==raw) return false;
      state.record=r;return true;
    } catch (_) {return false;}
  }
  function logExposure(kind) {
    if(!state.ready || !state.record) return false;
    const next=structuredClone(state.record);
    next.help_exposure.push({kind,at:new Date().toISOString()});
    if(!write(next)){lock('Could not save help exposure');return false;}
    return true;
  }
  function resetSection() {
    for (const id of ['predict-input','attempt-input','diagnose-input','repair-input','boundary-input']) $(id).value='';
    for (const id of ['help-text','saved-first','completion','reconstruct-model','boundary-model']) $(id).textContent='';
    for (const id of ['reconstruct-model','diagnosis-stage','repair-stage','boundary-stage','boundary-model']) bool(id,false);
    $('h1').focus?.();
  }
  function restore() {
    const r=state.record;
    bool('learner',true);
    const first=Boolean(r.first_answer);
    bool('after-first',first);
    $('predict-input').disabled=first;
    $('attempt-input').disabled=first;
    $('save-first').disabled=first;
    if(first) {
      $('predict-input').value=r.first_answer.prediction;
      $('attempt-input').value=r.first_answer.answer;
      $('saved-first').textContent='Original answer saved at '+r.first_answer.saved_at+' (later edits are separate).';
    }
    const kinds=r.help_exposure.map(x=>x.kind);
    $('h2').disabled=false;
    $('h1').disabled=kinds.indexOf('H1')!==-1;
    $('h2').disabled=kinds.indexOf('H1')===-1 || kinds.indexOf('H2')!==-1;
    $('h3').disabled=kinds.indexOf('H2')===-1 || kinds.indexOf('H3')!==-1;
    if(kinds.includes('H3')) $('help-text').textContent='H1–H3 were opened and recorded.';
    else if(kinds.includes('H2')) $('help-text').textContent='H1 and H2 were opened and recorded.';
    else if(kinds.includes('H1')) $('help-text').textContent='H1 was opened and recorded.';
    const reconstruct=kinds.includes('RECONSTRUCT');
    bool('reconstruct-model',reconstruct);
    if(reconstruct)$('reconstruct-model').textContent=state.current.stages.reconstruct;
    $('reveal').disabled=reconstruct;
    bool('diagnosis-stage',reconstruct);
    bool('repair-stage',r.diagnosis_notes.length>0);
    bool('boundary-stage',r.repairs.length>0);
    $('save-diagnosis').disabled=r.diagnosis_notes.length>0;
    $('diagnose-input').disabled=r.diagnosis_notes.length>0;
    $('save-repair').disabled=r.repairs.length>0;
    $('repair-input').disabled=r.repairs.length>0;
    $('save-boundary').disabled=r.boundary_attempts.length>0;
    $('boundary-input').disabled=r.boundary_attempts.length>0;
    $('show-boundary').disabled=r.boundary_attempts.length===0 || kinds.includes('BOUNDARY_MODEL');
    if(r.diagnosis_notes.length)$('diagnose-input').value=r.diagnosis_notes[0].text;
    if(r.repairs.length)$('repair-input').value=r.repairs[0].text;
    if(r.boundary_attempts.length)$('boundary-input').value=r.boundary_attempts[0].text;
    const shown=kinds.includes('BOUNDARY_MODEL');
    bool('boundary-model',shown);
    if(shown) $('boundary-model').textContent=state.current.boundary_response_criterion||
      'No independently approved model response exists in this original package. Keep this attempt for R01 review.';
    if(r.boundary_attempts.length)
      $('completion').textContent='Boundary answer saved separately from first answer; no automatic grading or learner mastery inferred.';
  }
  function choose(id) {
    const task=state.tasks.find(x=>x.id===id);
    if (!task) {lock('Unknown candidate identity');return;}
    state.current=task;
    state.record=read();
    if (!state.record) {lock('Stored attempt is malformed/stale. No silent reset allowed');return;}
    resetSection();
    $('task-meta').textContent=task.kind+' · '+task.subtopic_id+' · '+task.cell+' · '+task.source_kind;
    $('task-heading').textContent=task.id;
    $('task-source-role').textContent=task.source_kind==='SUPPLEMENTAL'?
      'Authored source-related transfer; its locator is not an authenticated exam item.':
      'Original primary transfer from the version-pinned B01 subtopic package.';
    $('predict-prompt').textContent=task.stages.predict;
    $('attempt-prompt').textContent=task.stages.attempt;
    $('diagnose-prompt').textContent=task.stages.diagnose;
    $('repair-prompt').textContent=task.stages.repair;
    $('boundary-prompt').textContent=task.stages.boundary_test;
    $('core1a-link').href=new URL(task.core1a,ROOT).href;
    $('original-core1b-link').href=new URL(task.core1b,ROOT).href;
    bool('task-info',true);
    restore();
    status(state.record.first_answer?'Previous first answer restored; later stages remain separately recorded.':
      'Exact-version author candidate loaded; record prediction and reasoning before reconstruction.','info');
  }
  function attempt() {
    if(!state.ready || state.record.first_answer)return;
    const prediction=$('predict-input').value.trim(),answer=$('attempt-input').value.trim();
    if(!prediction || !answer){status('Prediction and reasoned attempt are both required.','blocked');return;}
    const next=structuredClone(state.record);
    next.first_answer={prediction,answer,saved_at:new Date().toISOString()};
    if(!write(next)){lock('Cannot persist immutable first answer');return;}
    restore();status('First answer saved; reconstruction now unlockable.','success');
  }
  function onceSave(field,input,id,nextStep) {
    if(!state.ready || !state.record.first_answer || state.record[field].length)return;
    const value=$(input).value.trim();
    if(!value){status('Write your own reasoning for this stage.','blocked');return;}
    const next=structuredClone(state.record);
    next[field].push({text:value,at:new Date().toISOString(),
      exposed_before_attempt:state.record.help_exposure.map(x=>x.kind),
      kind:field==='diagnosis_notes'?'LEARNER_SELF_REPORT_NOT_AUTOMATIC_DIAGNOSIS':'LEARNER_REVISION_NOT_SCORED'});
    if(!write(next)){lock('Failed to persist '+id);return;}
    restore();status(nextStep+' saved separately; original answer unchanged.','success');
  }
  async function init() {
    if(!globalThis.crypto?.subtle){lock('WebCrypto unavailable');return;}
    if(!storageProbe()){lock('Writable localStorage unavailable');return;}
    state.storageOK=true;
    try {
      const registryPath='nsejs/physics/curriculum/topics/PH07/b01/B01_INTEGRATED_CURRICULUM_PROPOSAL.v1.json';
      const registry=await request(registryPath);
      const x=registry.json;
      if(x.status!=='AUTHOR_PROPOSAL_ONLY__INTEGRATION_HOLD'||
         x.academic_status!=='HOLD'||x.runtime_status!=='NOT_IMPLEMENTED' ||
         x.counts.selected_canonical_adapters!==0||x.counts.selected_canonical_mains!==0||
         x.counts.primary_instances!==75||x.counts.supplemental_instances!==14||
         x.counts.total_instances!==89||x.groups.length!==16)
        throw Error('Unexpected author proposal authority or inventory');
      const pkgMap=new Map();
      const manifest=[];
      for(const g of x.groups) {
        if(g.canonical_main!==null ||g.qualification!=='HOLD')throw Error('Unexpected approved mixed MAIN');
        for(const e of g.base_instances) {
          if(pkgMap.has(e.package_path)&&pkgMap.get(e.package_path).blob!==e.package_blob)
            throw Error('Conflicting package pin');
          pkgMap.set(e.package_path,{blob:e.package_blob,version:e.package_version,subtopic:e.subtopic_id});
          manifest.push({...e,cell:g.cell,source_kind:'BASE'});
        }
      }
      const supplementMap=new Map(x.supplements.map(x=>[x.proposal_path,x]));
      if(manifest.length!==75 ||pkgMap.size!==25||supplementMap.size!==14)
        throw Error('Incorrect source inventory');
      const urls=[...pkgMap.entries()].map(([path,pin])=>({path,blob:pin.blob,...pin}));
      const results=await Promise.all(urls.map(async item=>({item,resource:await request(item.path,item.blob)})));
      for(const {item,resource} of results) {
        const pkg=resource.json;
        if(pkg.status!=='DRAFT_AUTHOR_EXPOSED'||pkg.owner_agent!=='AGENT_2'||
          pkg.acceptance?.release!=='HOLD'||pkg.version!==item.version||
          pkg.subtopics.length!==1||pkg.subtopics[0].id!==item.subtopic)
          throw Error('Package revision/status mismatch for '+item.path);
        for(const e of manifest.filter(x=>x.package_path===item.path)) {
          const cycle=pkg.core1b.find(t=>t.id===e.instance_cycle);
          if(!cycle ||cycle.kind!=='INSTANCE'||cycle.qrt_target_id!==e.target_id)
            throw Error('Missing proposed INSTANCE '+e.target_id);
          state.tasks.push({id:cycle.id,kind:'INSTANCE',subtopic_id:e.subtopic_id,
            cell:e.cell,source_kind:'PRIMARY',stages:cycle.stages,
            core1a:item.path.replace('physics-topic-package.v1.json','core1a.html'),
            core1b:item.path.replace('physics-topic-package.v1.json','core1b.html'),
            boundary_response_criterion:null});
        }
      }
      for(const e of supplementMap.values()) {
        const resource=await request(e.proposal_path,e.proposal_blob);
        const pkg=resource.json;
        if(pkg.status!=='AUTHOR_EXPOSED_NOT_INDEPENDENTLY_QUALIFIED' ||
           pkg.acceptance?.release!=='HOLD'||pkg.acceptance?.canonical_integration!=='NOT_SELECTED' ||
           pkg.existing_package_pin?.blob!==e.base_package_blob||
           pkg.existing_package_pin?.version!==e.base_package_version ||
           pkg.target?.id!==e.target_id ||pkg.subtopic_id!==e.subtopic_id)
          throw Error('Supplement authority or source pin mismatch '+e.proposal_path);
        const cycle=pkg.core1b.find(t=>t.id===e.instance_cycle);
        if(!cycle||cycle.kind!=='INSTANCE')throw Error('Missing authored supplement INSTANCE');
        const group=x.groups.find(g=>g.supplemental_instances.some(s=>s.target_id===e.target_id));
        if(!group)throw Error('Orphan supplemental task');
        state.tasks.push({id:cycle.id,kind:'INSTANCE',subtopic_id:e.subtopic_id,
          cell:group.cell,source_kind:'SUPPLEMENTAL',stages:cycle.stages,
          core1a:e.core1a,core1b:e.core1b,
          boundary_response_criterion:cycle.boundary_response_criterion||null});
      }
      if(state.tasks.length!==89||new Set(state.tasks.map(t=>t.id)).size!==89)
        throw Error('Duplicate or missing reasoning tasks');
      const revisionMaterial=registry.raw+'\n'+
        urls.map(x=>x.path+':'+x.blob).sort().join('\n')+'\n'+
        x.supplements.map(y=>y.proposal_path+':'+y.proposal_blob).sort().join('\n');
      state.digest=await hash(revisionMaterial,'SHA-256');
      $('revision').textContent='Verified author-proposal digest SHA-256 '+state.digest.slice(0,24)+
        '…; every package checked against its pinned Git blob. 89 INSTANCE tasks · 0 selected MAINs.';
      state.tasks.sort((a,b)=>a.subtopic_id.localeCompare(b.subtopic_id)||a.id.localeCompare(b.id));
      const select=$('task-select');select.replaceChildren();
      for(const task of state.tasks) {
        const op=document.createElement('option');op.value=task.id;
        op.textContent=task.subtopic_id+' · '+task.cell+' · '+(task.source_kind==='SUPPLEMENTAL'?'source transfer':'primary')+' · '+task.id;
        select.appendChild(op);
      }
      select.disabled=false;state.ready=true;
      const wanted=new URL(location.href).searchParams.get('task');
      if(wanted&&state.tasks.some(t=>t.id===wanted))select.value=wanted;
      select.addEventListener('change',()=>choose(select.value));
      choose(select.value);
    }catch(err){lock('Package/revision verification failed: '+String(err.message));}
  }
  $('h1').addEventListener('click',()=>{
    if(state.record.help_exposure.some(x=>x.kind==='H1'))return;
    if(logExposure('H1')) { $('help-text').textContent='H1: State the physical quantities and units; separate observed data from assumptions.';restore(); }
  });
  $('h2').addEventListener('click',()=>{
    if(state.record.help_exposure.some(x=>x.kind==='H2'))return;
    if(logExposure('H2')) { $('help-text').textContent='H2: Check conservation, symmetry, direction or a comparison control before using a formula.';restore(); }
  });
  $('h3').addEventListener('click',()=>{
    if(state.record.help_exposure.some(x=>x.kind==='H3'))return;
    if(logExposure('H3')) { $('help-text').textContent='H3: Test the assumptions with an extreme or changed-condition case; do not infer uniqueness too early.';restore(); }
  });
  $('save-first').addEventListener('click',attempt);
  $('reveal').addEventListener('click',()=>{
    if(!state.record?.first_answer)return;
    if(logExposure('RECONSTRUCT')) {restore();status('Candidate reconstruction exposed; write a learner self-diagnosis.','info');}
  });
  $('save-diagnosis').addEventListener('click',()=>onceSave('diagnosis_notes','diagnose-input','diagnosis','Diagnosis'));
  $('save-repair').addEventListener('click',()=>onceSave('repairs','repair-input','repair','Repair'));
  $('save-boundary').addEventListener('click',()=>onceSave('boundary_attempts','boundary-input','boundary','Boundary'));
  $('show-boundary').addEventListener('click',()=>{
    if(!state.record?.boundary_attempts.length)return;
    if(logExposure('BOUNDARY_MODEL'))restore();
  });
  init();
})();
