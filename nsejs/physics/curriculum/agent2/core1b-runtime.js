/* Agent 2 Core1B: source-neutral candidate practice, not an examination reader.
   Browser-only attempt custody. Local storage is not tamper resistant or server-backed.
   No academic approval inferred from software validation. */
(function () {
  'use strict';
  const root = document.querySelector('[data-agent2-core1b]');
  if (!root) return;
  const $ = id => document.getElementById(id);
  const state = { package: null, tasks: [], current: null, ready: false, record: null };
  function say(message, kind) {
    const el = $('status');
    el.textContent = message;
    el.dataset.kind = kind || 'info';
  }
  function safeStorage() {
    try {
      const key = '__g9_physics_probe__';
      localStorage.setItem(key, '1');
      if (localStorage.getItem(key) !== '1') return false;
      localStorage.removeItem(key);
      return true;
    } catch (_err) { return false; }
  }
  function key() { return 'g9-physics-agent2-core1b-v1:' + state.current.id; }
  function read() {
    try {
      const raw = localStorage.getItem(key());
      if (!raw) return { id: state.current.id, version: state.package.version,
        first: null, revisions: [], exposures: [] };
      const data = JSON.parse(raw);
      if (data.id !== state.current.id || data.version !== state.package.version ||
          !Array.isArray(data.revisions) || !Array.isArray(data.exposures))
        throw new Error('stale or invalid attempt');
      return data;
    } catch (_err) { return null; }
  }
  function store(data) {
    try {
      const payload = JSON.stringify(data);
      localStorage.setItem(key(), payload);
      return localStorage.getItem(key()) === payload;
    } catch (_err) { return false; }
  }
  function unlock(record) {
    $('lesson').hidden = false;
    $('first-save').disabled = Boolean(record.first);
    $('first-attempt').disabled = Boolean(record.first);
    $('first-predict').disabled = Boolean(record.first);
    $('revision-save').disabled = !record.first;
    $('revision').disabled = !record.first;
    $('help').disabled = !state.ready;
    $('reveal').disabled = !record.first;
    $('attempt-receipt').textContent = record.first ?
      'First attempt retained at ' + record.first.at + '. Earlier answer stays unchanged on revisions.' :
      'No first attempt recorded. Reconstruction locked.';
    if (record.first) {
      $('first-predict').value = record.first.predict;
      $('first-attempt').value = record.first.attempt;
    } else { $('first-predict').value = ''; $('first-attempt').value = ''; }
    $('history').textContent = 'Saved revisions: ' + record.revisions.length +
      ' · Help/reconstruction exposures: ' + record.exposures.length;
  }
  function lockdown(why) {
    state.ready = false;
    root.querySelectorAll('textarea,button,select').forEach(el => { el.disabled = true; });
    $('lesson').hidden = true;
    say(why + ' This is a read-only preview until a writable record is available.', 'blocked');
  }
  function choose(id) {
    state.current = state.tasks.find(x => x.id === id);
    if (!state.current) { lockdown('Unknown task identity.'); return; }
    $('task-title').textContent = state.current.qrt_target_id + ' · ' + state.current.kind;
    $('task').textContent = state.current.fresh_task;
    $('predict-prompt').textContent = state.current.stages.predict;
    $('attempt-prompt').textContent = state.current.stages.attempt;
    $('help-text').hidden = true;
    $('revealed').hidden = true;
    $('revision').value = '';
    state.record = read();
    if (!state.record) { lockdown('Stored attempt is corrupt or not compatible with this revision.'); return; }
    unlock(state.record);
    say(state.record.first ? 'Saved first attempt restored. Later stages may be inspected.' :
      'Predict and attempt independently, then save the original answer.', 'info');
  }
  function exposure(type) {
    if (!state.ready || !state.record) return false;
    const item = { type, at: new Date().toISOString() };
    const next = { ...state.record, exposures: [...state.record.exposures, item] };
    if (!store(next)) { lockdown('Exposure could not be recorded.'); return false; }
    state.record = next;
    // Pre-attempt orientation must not erase unsaved learner text.
    if (next.first) unlock(next);
    else $('history').textContent = 'Saved revisions: 0 · Help/reconstruction exposures: ' + next.exposures.length;
    return true;
  }
  function saveFirst() {
    const predict = $('first-predict').value.trim();
    const attempt = $('first-attempt').value.trim();
    if (!predict || !attempt) { say('Both a prediction and an independent attempt are required.', 'blocked'); return; }
    if (!state.ready || state.record.first) return;
    const next = { ...state.record, first: { predict, attempt, at: new Date().toISOString() } };
    if (!store(next)) { lockdown('First answer could not be saved.'); return; }
    state.record = next;
    unlock(next);
    say('Original response saved. Reconstruction is now available.', 'success');
  }
  function saveRevision() {
    if (!state.ready || !state.record.first) return;
    const answer = $('revision').value.trim();
    if (!answer) { say('Write a revision before saving.', 'blocked'); return; }
    const next = { ...state.record, revisions: [...state.record.revisions,
      { answer, at: new Date().toISOString() }] };
    if (!store(next)) { lockdown('Revision could not be saved.'); return; }
    state.record = next;
    unlock(next);
    $('revision').value = '';
    say('Revision saved separately. Original response remains unchanged.', 'success');
  }
  function reveal() {
    if (!state.record || !state.record.first) { say('Submit an independent first attempt before reconstruction.', 'blocked'); return; }
    if (!exposure('POST_ATTEMPT_RECONSTRUCTION')) return;
    const stages = state.current.stages;
    $('revealed').hidden = false;
    ['reconstruct', 'diagnose', 'repair', 'boundary_test'].forEach(name => {
      $(name.replace('_test', '') + '-text').textContent = stages[name];
    });
    say('Reconstruction revealed after the persisted first attempt.', 'info');
  }
  async function init() {
    if (!safeStorage()) { lockdown('Browser storage is unavailable.'); return; }
    const path = root.dataset.package;
    if (!path || !/^\.\.?\/?[\w./-]+\.json$/.test(path)) {
      lockdown('Invalid relative candidate package path.'); return;
    }
    try {
      const response = await fetch(path, { cache: 'no-store', credentials: 'same-origin' });
      if (!response.ok) throw new Error('HTTP ' + response.status);
      state.package = await response.json();
      if (state.package.status !== 'DRAFT_AUTHOR_EXPOSED' ||
          state.package.owner_agent !== 'AGENT_2' ||
          state.package.topic_id !== root.dataset.topic ||
          state.package.acceptance?.release !== 'HOLD' ||
          !Array.isArray(state.package.core1b))
        throw new Error('package authority/shape mismatch');
      state.tasks = state.package.core1b;
      const select = $('task-select');
      for (const task of state.tasks) {
        const option = document.createElement('option');
        option.value = task.id;
        option.textContent = task.kind + ' · ' + task.qrt_target_id.split('-').slice(-2).join(' ');
        select.appendChild(option);
      }
      if (!state.tasks.length) throw new Error('empty task set');
      state.ready = true;
      select.disabled = false;
      $('first-save').disabled = false;
      $('help').disabled = false;
      select.addEventListener('change', () => choose(select.value));
      $('first-save').addEventListener('click', saveFirst);
      $('revision-save').addEventListener('click', saveRevision);
      $('reveal').addEventListener('click', reveal);
      $('help').addEventListener('click', () => {
        if (exposure('NONDECISIVE_ORIENTATION')) {
          $('help-text').hidden = false;
          say('Orientation help exposure logged. The decisive step remains withheld.', 'info');
        }
      });
      choose(state.tasks[0].id);
    } catch (err) { lockdown('The candidate package could not be loaded: ' + err.message + '.'); }
  }
  init();
})();
