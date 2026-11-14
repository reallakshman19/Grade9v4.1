/* Node-only deterministic smoke harness for draft Core1B browser-local state.
   Emulates DOM/storage interactions, NOT a Chromium or academic review. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const ROOT = path.resolve(__dirname, '../../../../../');
const JS = fs.readFileSync(path.join(__dirname, '..', 'core1b-runtime.js'), 'utf8');
const PACKAGE = JSON.parse(fs.readFileSync(
  path.join(ROOT, 'nsejs/physics/curriculum/topics/PH11/physics-topic-package.v1.json'), 'utf8'
));
class MockEl {
  constructor(id) { this.id = id; this.disabled = false; this.hidden = true; this.value = '';
    this.textContent = ''; this.dataset = {}; this.events = {}; this.children = []; }
  addEventListener(k, fn) { this.events[k] = fn; }
  appendChild(x) { this.children.push(x); }
  click() { if (!this.disabled) this.events.click?.(); }
}
function boot({ map = new Map(), storageBlocked = false, corrupt = false, packageOverride = PACKAGE } = {}) {
  const names = ['status','lesson','task-select','task-title','task','predict-prompt',
    'attempt-prompt','help-text','revealed','revision','first-save','first-attempt',
    'first-predict','revision-save','help','reveal','attempt-receipt','history',
    'reconstruct-text','diagnose-text','repair-text','boundary-text'];
  const elements = Object.fromEntries(names.map(x => [x, new MockEl(x)]));
  for (const id of ['task-select','first-save','help','reveal','revision-save']) elements[id].disabled = true;
  const root = { dataset: { topic: 'PH11', package: './physics-topic-package.v1.json' },
    querySelectorAll: () => Object.values(elements) };
  const document = { querySelector: () => root, getElementById: id => {
      assert.ok(elements[id], 'Missing DOM element ' + id);
      return elements[id];
    },
    createElement: () => new MockEl('option') };
  const storage = {setItem(k,v) { if (storageBlocked) throw new Error('Storage denied'); map.set(k,v); },
    getItem(k) {if (storageBlocked) throw new Error('Storage denied'); return map.get(k)??null; },
    removeItem(k) { if (storageBlocked) throw new Error('Storage denied'); map.delete(k); }};
  if (corrupt) map.set('g9-physics-agent2-core1b-v1:' + PACKAGE.core1b[0].id, '{{BAD-JSON');
  const context = { document, localStorage: storage, Date, console,
    fetch: async()=>({ok:true,json:async()=>packageOverride}) };
  vm.runInNewContext(JS, context, {timeout:1000, filename:'core1b-runtime.js'});
  return {elements, map, storage};
}
async function settle() { for (let n=0; n<5; n++) await new Promise(setImmediate); }
async function main() {
  const learner = boot(); await settle(); const e = learner.elements;
  assert.equal(e['task-select'].children.length, 12);
  assert.equal(e.reveal.disabled, true, 'Reconstruction must start locked');
  assert.equal(e.lesson.hidden, false);
  e['first-predict'].value='Prediction: the current splits';
  e['first-attempt'].value='Attempt: compare branch endpoint nodes';
  e.help.click();
  assert.equal(e['first-attempt'].value,'Attempt: compare branch endpoint nodes',
    'Nondecisive help must preserve unsaved work');
  assert.equal(e['help-text'].hidden,false);
  e['first-save'].click();
  assert.equal(e.reveal.disabled,false,'First answer must unlock reconstruction');
  const task=PACKAGE.core1b[0], key='g9-physics-agent2-core1b-v1:' + task.id;
  const saved=JSON.parse(learner.map.get(key));
  assert.equal(saved.first.attempt,'Attempt: compare branch endpoint nodes');
  assert.equal(saved.exposures.length,1);
  const reloaded=boot({map:learner.map});await settle(); const r=reloaded.elements;
  assert.equal(r.reveal.disabled,false,'Refresh should preserve first attempt');
  r.reveal.click();
  assert.equal(r.revealed.hidden,false);
  r.revision.value='Revised node graph after reconstruction';
  r['revision-save'].click();
  const updated=JSON.parse(learner.map.get(key));
  assert.deepEqual(updated.first,saved.first,'Revisions must not rewrite first response');
  assert.equal(updated.revisions.length,1);
  assert.equal(updated.exposures.length,2);
  const blocked=boot({storageBlocked:true});await settle();
  assert.equal(blocked.elements.lesson.hidden,true);
  assert.equal(blocked.elements['first-save'].disabled,true);
  assert.equal(blocked.elements.reveal.disabled,true);
  const corrupt=boot({map:new Map(),corrupt:true});await settle();
  assert.equal(corrupt.elements.lesson.hidden,true,'Corrupted saved attempts must fail closed');
  const unauthorized=boot({packageOverride:{...PACKAGE,status:'APPROVED'}});await settle();
  assert.equal(unauthorized.elements.lesson.hidden,true,'Unauthorized status must be rejected');
  console.log('AGENT2_NODE_RUNTIME_PASS: first-attempt-lock, help-exposure, refresh, immutable-original, revisions, reveal, storage-disabled, stale/corrupt, authority');
}
main().catch(err=>{console.error(err);process.exitCode=1;});
