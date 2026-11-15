import test from 'node:test';
import assert from 'node:assert/strict';
import {AssessmentHold, applyEvent, verifyRecord, initialRecord,
  AssessmentPhase, IndexedDbAttemptStore, fetchPinnedAsset} from './engine.mjs';
const uid='opaque-one', revision='a'.repeat(64), hash='b'.repeat(64);
const predict={hypothesis:'I expect the atom count to be conserved here.',conditions:'A fixed boundary with no unaccounted transport is assumed.'};
const attempt={claim:'The selected boundary can show a mass difference.',model:'I use conservation of atoms across a defined boundary.',reasoning:'I count material transfers before comparing both sides.',check:'The independent atomic ledger must balance overall.'};
const comparison={comparison:[{myStep:'I chose a solvent ledger for this reaction.',modelStep:'The reference ledger includes a moving species.',difference:'My approach ignored a transfer across the boundary.'}],uncertainty:'The larger-system assumption still needs explicit checking.'};
const diagnosis={attemptQuote:attempt.model,firstDivergence:'I incorrectly treated solvent and solute identically.',modelEvidence:'The reconstructed ledger distinguishes their transport.'};
const repair={correctedReasoning:'The revised ledger separately tracks each transferred species.',firstDivergenceAddressed:'The missing transfer across the chosen system is now counted.',independentCheck:'A larger closed-system atom count still balances correctly.'};
const boundary={changedCondition:'The wider system is now ventilated instead of sealed.',prediction:'The material ledger for the smaller system can decrease.',reasoning:'The new boundary permits flux across the control surface.',falsifier:'Measure outgoing mass flux and compare with lost inventory.'};
function event(record,type,evidence,overrides={}) {
  return applyEvent(record,{taskUid:uid,revision,expectedSequence:record?.sequence??0,type,evidence,...overrides});
}
function hold(code,fn){assert.throws(fn,e=>e instanceof AssessmentHold&&e.code===code);}
function attempted(){return event(event(null,'PREDICT',predict),'ATTEMPT',attempt);}
function completed(){
  let r=event(null,'PREDICT',predict);
  r=event(r,'HINT',{level:1});r=event(r,'HINT',{level:2});
  r=event(r,'ATTEMPT',attempt);r=event(r,'REVEAL_RECONSTRUCTION',{assetSha256:hash});
  r=event(r,'RECONSTRUCT',comparison);r=event(r,'DIAGNOSE',diagnosis);
  r=event(r,'REVEAL_DIAGNOSTIC',{assetSha256:hash});r=event(r,'REPAIR',repair);
  r=event(r,'REVEAL_BOUNDARY_TASK',{assetSha256:hash});r=event(r,'BOUNDARY',boundary);
  return event(r,'REVEAL_BOUNDARY_FEEDBACK',{assetSha256:hash});
}
test('complete feedback-driven journey, assistance and no academic promotion',()=>{
  const r=completed();assert.equal(r.phase,AssessmentPhase.DONE);
  assert.equal(r.events.length,12);assert.equal(r.firstAttemptAssistance,'ASSISTED');
  assert.equal(r.academicAssessment,'NOT_EVALUATED');assert.equal(verifyRecord(r).phase,'done');
});
test('unassisted attempt remains distinguished from hint-assisted attempt',()=>{
  assert.equal(attempted().firstAttemptAssistance,'UNASSISTED');
});
test('no model before attempt and no boundary feedback before its own attempt',()=>{
  hold('OUT_OF_ORDER:REVEAL_RECONSTRUCTION:predict',()=>event(null,'REVEAL_RECONSTRUCTION',{assetSha256:hash}));
  const r=event(null,'PREDICT',predict);
  hold('OUT_OF_ORDER:REVEAL_RECONSTRUCTION:attempt',()=>event(r,'REVEAL_RECONSTRUCTION',{assetSha256:hash}));
  hold('OUT_OF_ORDER:RECONSTRUCT:attempt',()=>event(r,'RECONSTRUCT',comparison));
  let s=attempted();s=event(s,'REVEAL_RECONSTRUCTION',{assetSha256:hash});
  s=event(s,'RECONSTRUCT',comparison);s=event(s,'DIAGNOSE',diagnosis);
  s=event(s,'REVEAL_DIAGNOSTIC',{assetSha256:hash});s=event(s,'REPAIR',repair);
  s=event(s,'REVEAL_BOUNDARY_TASK',{assetSha256:hash});
  hold('OUT_OF_ORDER:REVEAL_BOUNDARY_FEEDBACK:boundary',()=>event(s,'REVEAL_BOUNDARY_FEEDBACK',{assetSha256:hash}));
});
test('repair requires saved comparison, diagnosis and diagnostic feedback',()=>{
  let r=attempted();r=event(r,'REVEAL_RECONSTRUCTION',{assetSha256:hash});
  hold('OUT_OF_ORDER:DIAGNOSE:reconstruct',()=>event(r,'DIAGNOSE',diagnosis));
  r=event(r,'RECONSTRUCT',comparison);
  hold('OUT_OF_ORDER:REPAIR:diagnose',()=>event(r,'REPAIR',repair));
  r=event(r,'DIAGNOSE',diagnosis);
  hold('OUT_OF_ORDER:REPAIR:diagnostic-model',()=>event(r,'REPAIR',repair));
});
test('arbitrary free-text filler cannot pass structural attempt gate',()=>{
  const r=event(null,'PREDICT',predict);
  hold('ATTEMPT_SHAPE',()=>event(r,'ATTEMPT',{text:'done'}));
  hold('ATTEMPT_INCOMPLETE',()=>event(r,'ATTEMPT',{...attempt,reasoning:'ok'}));
});
test('diagnosis must quote actual protected first attempt',()=>{
  let r=attempted();r=event(r,'REVEAL_RECONSTRUCTION',{assetSha256:hash});
  r=event(r,'RECONSTRUCT',comparison);
  hold('DIAGNOSE_UNANCHORED',()=>event(r,'DIAGNOSE',{...diagnosis,attemptQuote:'Fabricated answer absent from original response.'}));
});
test('hint exposure cannot be skipped, repeated or revealed after attempt',()=>{
  let r=event(null,'PREDICT',predict);
  hold('HINT_NON_MONOTONIC',()=>event(r,'HINT',{level:2}));
  r=event(r,'HINT',{level:1});
  hold('HINT_NON_MONOTONIC',()=>event(r,'HINT',{level:1}));
  r=event(r,'ATTEMPT',attempt);
  hold('OUT_OF_ORDER:HINT:reconstruction-model',()=>event(r,'HINT',{level:2}));
});
test('simulated competing sequence and stale content revisions reject writes',()=>{
  const r=event(null,'PREDICT',predict);
  hold('CONCURRENT_UPDATE',()=>event(r,'ATTEMPT',attempt,{expectedSequence:0}));
  hold('STALE_REVISION',()=>event(r,'ATTEMPT',attempt,{revision:'c'.repeat(64)}));
});
test('first attempt cannot be overwritten or modified after commit',()=>{
  const r=attempted();
  hold('OUT_OF_ORDER:ATTEMPT:reconstruction-model',()=>event(r,'ATTEMPT',attempt));
  const corrupted=structuredClone(r);corrupted.responses.attempt.reasoning='tampered';
  hold('RECORD_REPLAY_MISMATCH',()=>verifyRecord(corrupted));
});
test('missing and reordered events cannot validate',()=>{
  const r=completed(),removed=structuredClone(r);
  removed.events.splice(4,1);
  hold('EVENT_SEQUENCE_INVALID',()=>verifyRecord(removed));
  const changed=structuredClone(r);changed.events[3].type='REVEAL_BOUNDARY_FEEDBACK';
  hold('OUT_OF_ORDER:REVEAL_BOUNDARY_FEEDBACK:attempt',()=>verifyRecord(changed));
});
test('missing expected revision or reveal digest is HOLD',()=>{
  hold('EXPECTED_DIGEST_REQUIRED',()=>initialRecord({taskUid:uid,revision:'bad'}));
  const r=attempted();
  hold('REVEAL_UNPINNED',()=>event(r,'REVEAL_RECONSTRUCTION',{assetSha256:'not-pinned'}));
});
test('storage-denied reads and writes fail without localStorage fallback',async()=>{
  const s=new IndexedDbAttemptStore({indexedDb:null});
  await assert.rejects(()=>s.read(uid),e=>e.code==='INDEXEDDB_UNAVAILABLE');
  await assert.rejects(()=>s.commit({taskUid:uid,revision,expectedSequence:0,type:'PREDICT',evidence:predict}),
    e=>e.code==='INDEXEDDB_UNAVAILABLE');
});
test('asset bytes must match an external expected digest',async()=>{
  await assert.rejects(()=>fetchPinnedAsset({url:'/answer',expectedSha256:'bad'}),e=>e.code==='EXPECTED_DIGEST_REQUIRED');
  const bytes=new TextEncoder().encode('untrusted response');
  const subtle=(await import('node:crypto')).webcrypto.subtle;
  await assert.rejects(()=>fetchPinnedAsset({url:'/answer',expectedSha256:hash,subtle,
    fetcher:async()=>({ok:true,arrayBuffer:async()=>bytes.buffer})}),e=>e.code==='ASSET_DIGEST_MISMATCH');
});
