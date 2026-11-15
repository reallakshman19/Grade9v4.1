/**
 * Shared assessment R0 candidate: workflow integrity, NOT scientific grading.
 * Static public study assets remain inspectable. Secure exams need server authority.
 * No academic approval inferred from software validation.
 */
const STORE = 'attempts';
const SHA = /^[a-f0-9]{64}$/;
const PHASE = Object.freeze({
  PREDICT: 'predict', ATTEMPT: 'attempt', RECONSTRUCTION_MODEL: 'reconstruction-model',
  RECONSTRUCT: 'reconstruct', DIAGNOSE: 'diagnose', DIAGNOSTIC_MODEL: 'diagnostic-model',
  REPAIR: 'repair', BOUNDARY_TASK: 'boundary-task', BOUNDARY: 'boundary',
  BOUNDARY_MODEL: 'boundary-model', DONE: 'done',
});
export const AssessmentPhase = PHASE;
export class AssessmentHold extends Error {
  constructor(code) { super(code); this.name = 'AssessmentHold'; this.code = code; }
}
function requireThat(ok, code) { if (!ok) throw new AssessmentHold(code); }
function text(value, min = 16, max = 10000) {
  return typeof value === 'string' && value.trim().length >= min && value.length <= max;
}
function object(value) { return !!value && typeof value === 'object' && !Array.isArray(value); }
function exact(value, fields) {
  return object(value) && Object.keys(value).length === fields.length &&
    fields.every(k => Object.prototype.hasOwnProperty.call(value, k));
}
function copy(value) { return JSON.parse(JSON.stringify(value)); }
function validateEvidence(type, evidence, previous) {
  if (type === 'PREDICT') {
    requireThat(exact(evidence, ['hypothesis','conditions']), 'PREDICT_SHAPE');
    requireThat(text(evidence.hypothesis) && text(evidence.conditions), 'PREDICT_EMPTY');
  } else if (type === 'ATTEMPT') {
    requireThat(exact(evidence,['claim','model','reasoning','check']), 'ATTEMPT_SHAPE');
    requireThat(['claim','model','reasoning','check'].every(k => text(evidence[k])), 'ATTEMPT_INCOMPLETE');
  } else if (type === 'RECONSTRUCT') {
    requireThat(exact(evidence,['comparison','uncertainty']), 'RECONSTRUCT_SHAPE');
    requireThat(Array.isArray(evidence.comparison) && evidence.comparison.length > 0 &&
      evidence.comparison.length <= 20, 'RECONSTRUCT_COMPARISON');
    for (const c of evidence.comparison) {
      requireThat(exact(c,['myStep','modelStep','difference']) &&
        text(c.myStep) && text(c.modelStep) && text(c.difference), 'RECONSTRUCT_STEP');
    }
    requireThat(text(evidence.uncertainty), 'RECONSTRUCT_UNCERTAINTY');
  } else if (type === 'DIAGNOSE') {
    requireThat(exact(evidence,['attemptQuote','firstDivergence','modelEvidence']), 'DIAGNOSE_SHAPE');
    requireThat(Object.values(evidence).every(v => text(v)), 'DIAGNOSE_INCOMPLETE');
    const original = Object.values(previous.attempt).join(' ');
    requireThat(original.includes(evidence.attemptQuote.trim()), 'DIAGNOSE_UNANCHORED');
  } else if (type === 'REPAIR') {
    requireThat(exact(evidence,['correctedReasoning','firstDivergenceAddressed','independentCheck']), 'REPAIR_SHAPE');
    requireThat(Object.values(evidence).every(v => text(v)), 'REPAIR_INCOMPLETE');
  } else if (type === 'BOUNDARY') {
    requireThat(exact(evidence,['changedCondition','prediction','reasoning','falsifier']), 'BOUNDARY_SHAPE');
    requireThat(Object.values(evidence).every(v => text(v)), 'BOUNDARY_INCOMPLETE');
  } else if (type === 'HINT') {
    requireThat(exact(evidence,['level']), 'HINT_SHAPE');
    requireThat(Number.isInteger(evidence.level) && evidence.level >= 1 && evidence.level <= 3,
      'HINT_LEVEL_INVALID');
  } else if (['REVEAL_RECONSTRUCTION','REVEAL_DIAGNOSTIC','REVEAL_BOUNDARY_TASK',
               'REVEAL_BOUNDARY_FEEDBACK'].includes(type)) {
    requireThat(exact(evidence,['assetSha256']), 'REVEAL_SHAPE');
    requireThat(SHA.test(evidence.assetSha256), 'REVEAL_UNPINNED');
  } else throw new AssessmentHold('UNKNOWN_EVENT');
}
const PERMITTED = Object.freeze({
  PREDICT: [PHASE.PREDICT], HINT: [PHASE.ATTEMPT], ATTEMPT: [PHASE.ATTEMPT],
  REVEAL_RECONSTRUCTION: [PHASE.RECONSTRUCTION_MODEL],
  RECONSTRUCT: [PHASE.RECONSTRUCT], DIAGNOSE: [PHASE.DIAGNOSE],
  REVEAL_DIAGNOSTIC: [PHASE.DIAGNOSTIC_MODEL], REPAIR: [PHASE.REPAIR],
  REVEAL_BOUNDARY_TASK: [PHASE.BOUNDARY_TASK], BOUNDARY: [PHASE.BOUNDARY],
  REVEAL_BOUNDARY_FEEDBACK: [PHASE.BOUNDARY_MODEL],
});
const NEXT = Object.freeze({
  PREDICT: PHASE.ATTEMPT, ATTEMPT: PHASE.RECONSTRUCTION_MODEL,
  REVEAL_RECONSTRUCTION: PHASE.RECONSTRUCT, RECONSTRUCT: PHASE.DIAGNOSE,
  DIAGNOSE: PHASE.DIAGNOSTIC_MODEL, REVEAL_DIAGNOSTIC: PHASE.REPAIR,
  REPAIR: PHASE.BOUNDARY_TASK, REVEAL_BOUNDARY_TASK: PHASE.BOUNDARY,
  BOUNDARY: PHASE.BOUNDARY_MODEL, REVEAL_BOUNDARY_FEEDBACK: PHASE.DONE,
});
export function initialRecord({taskUid,revision}) {
  requireThat(text(taskUid, 2, 256) && !/[\s\\/]/.test(taskUid), 'INVALID_UID');
  requireThat(typeof revision === 'string' && SHA.test(revision), 'EXPECTED_DIGEST_REQUIRED');
  return {schema:'g9-shared-assessment/r0',taskUid,revision,sequence:0,
    phase:PHASE.PREDICT,events:[],responses:{},hintDepth:0,
    firstAttemptAssistance:null,academicAssessment:'NOT_EVALUATED'};
}
function advance(record, type, evidence) {
  requireThat(Array.isArray(PERMITTED[type]) && PERMITTED[type].includes(record.phase),
    'OUT_OF_ORDER:'+type+':'+record.phase);
  validateEvidence(type,evidence,record.responses);
  if(type==='HINT') requireThat(evidence.level===record.hintDepth+1, 'HINT_NON_MONOTONIC');
  if(type==='PREDICT') record.responses.predict=copy(evidence);
  if(type==='ATTEMPT') {
    record.responses.attempt=copy(evidence);
    record.firstAttemptAssistance=record.hintDepth>0?'ASSISTED':'UNASSISTED';
  }
  if(type==='RECONSTRUCT') record.responses.reconstruct=copy(evidence);
  if(type==='DIAGNOSE') record.responses.diagnose=copy(evidence);
  if(type==='REPAIR') record.responses.repair=copy(evidence);
  if(type==='BOUNDARY') record.responses.boundary=copy(evidence);
  if(type==='HINT') record.hintDepth=evidence.level;
  if(type!=='HINT')record.phase=NEXT[type];
  record.sequence++;
  record.events.push({sequence:record.sequence,type,evidence:copy(evidence)});
  return record;
}
/** Replays event history before every write. This is corruption detection,
 * not proof against a malicious client editing all local records. */
export function verifyRecord(record) {
  requireThat(object(record) && record.schema==='g9-shared-assessment/r0', 'INVALID_RECORD');
  let projected=initialRecord({taskUid:record.taskUid,revision:record.revision});
  requireThat(Array.isArray(record.events) && record.events.length <= 200, 'EVENT_HISTORY_INVALID');
  for(const item of record.events){
    requireThat(exact(item,['sequence','type','evidence']) &&
      item.sequence===projected.sequence+1,'EVENT_SEQUENCE_INVALID');
    projected=advance(projected,item.type,item.evidence);
  }
  requireThat(JSON.stringify(projected)===JSON.stringify(record),'RECORD_REPLAY_MISMATCH');
  return copy(record);
}
/** Pure transition. expectedSequence must be checked INSIDE a readwrite transaction. */
export function applyEvent(current, {taskUid,revision,expectedSequence,type,evidence}) {
  let record=current===undefined || current===null
    ?initialRecord({taskUid,revision}):verifyRecord(current);
  requireThat(record.taskUid===taskUid && record.revision===revision, 'STALE_REVISION');
  requireThat(Number.isInteger(expectedSequence) && expectedSequence===record.sequence,
    'CONCURRENT_UPDATE');
  requireThat(object(evidence), 'EVIDENCE_OBJECT_REQUIRED');
  return advance(record,type,evidence);
}
function idbOpen(indexedDb, dbName) {
  requireThat(indexedDb && typeof indexedDb.open==='function', 'INDEXEDDB_UNAVAILABLE');
  return new Promise((resolve,reject)=>{
    let done=false;
    let req;
    try{req=indexedDb.open(dbName,1);}catch(e){reject(new AssessmentHold('INDEXEDDB_OPEN_FAILED'));return;}
    function fail(code){if(!done){done=true;reject(new AssessmentHold(code));}}
    req.onupgradeneeded=()=>{
      try{if(!req.result.objectStoreNames.contains(STORE))req.result.createObjectStore(STORE);}
      catch(e){fail('INDEXEDDB_SCHEMA_FAILED');}
    };
    req.onblocked=()=>fail('INDEXEDDB_UPGRADE_BLOCKED');
    req.onerror=()=>fail('INDEXEDDB_OPEN_FAILED');
    req.onsuccess=()=>{if(done){req.result.close();return;}done=true;
      req.result.onversionchange=()=>req.result.close();resolve(req.result);};
  });
}
/** A single IndexedDB readwrite transaction serializes competing browser tabs.
 * Storage failure means HOLD; no localStorage fallback. */
export class IndexedDbAttemptStore {
  constructor({indexedDb=globalThis.indexedDB,dbName='g9-shared-assessment-r0'}={}) {
    this.indexedDb=indexedDb;this.dbName=dbName;
  }
  async read(taskUid){
    const db=await idbOpen(this.indexedDb,this.dbName);
    return new Promise((resolve,reject)=>{
      let tx,req,failed=false;
      try {tx=db.transaction(STORE,'readonly');req=tx.objectStore(STORE).get(taskUid);}
      catch(e){db.close();reject(new AssessmentHold('STORAGE_READ_FAILED'));return;}
      function fail(){if(!failed){failed=true;db.close();reject(new AssessmentHold('STORAGE_READ_FAILED'));}}
      req.onerror=fail;tx.onabort=fail;tx.onerror=fail;
      tx.oncomplete=()=>{if(failed)return;db.close();
        try{resolve(req.result===undefined?null:verifyRecord(req.result));}
        catch(e){reject(e);}
      };
    });
  }
  async commit(input){
    const db=await idbOpen(this.indexedDb,this.dbName);
    return new Promise((resolve,reject)=>{
      let tx,req,next,reason=null,settled=false;
      function fail(err){if(!settled){settled=true;db.close();reject(err);}}
      try{
        tx=db.transaction(STORE,'readwrite');
        const table=tx.objectStore(STORE);
        req=table.get(input.taskUid);
        req.onsuccess=()=>{
          try {next=applyEvent(req.result,input);table.put(next,input.taskUid);}
          catch(e){reason=e;try{tx.abort();}catch(_){} }
        };
        req.onerror=()=>{reason=new AssessmentHold('STORAGE_READ_FAILED');};
        tx.oncomplete=()=>{if(settled)return;settled=true;db.close();resolve(copy(next));};
        tx.onerror=()=>{reason ||=new AssessmentHold('STORAGE_TRANSACTION_FAILED');};
        tx.onabort=()=>fail(reason||new AssessmentHold('STORAGE_TRANSACTION_ABORTED'));
      }catch(e){fail(new AssessmentHold('STORAGE_TRANSACTION_FAILED'));}
    });
  }
}
/** Hash must be pinned in a separately checked manifest, never derived from an
 * untrusted response. Call only after committing the corresponding REVEAL event.
 * A public URL is not answer confidentiality. */
export async function fetchPinnedAsset({url,expectedSha256,fetcher=globalThis.fetch,subtle=globalThis.crypto?.subtle}) {
  requireThat(typeof expectedSha256==='string'&&SHA.test(expectedSha256),'EXPECTED_DIGEST_REQUIRED');
  requireThat(typeof url==='string'&&url.length>0,'ASSET_URL_REQUIRED');
  requireThat(typeof fetcher==='function'&&subtle,'ASSET_VERIFICATION_UNAVAILABLE');
  let response;
  try{response=await fetcher(url,{cache:'no-store',credentials:'same-origin'});}
  catch(e){throw new AssessmentHold('ASSET_NETWORK_FAILED');}
  requireThat(response && response.ok,'ASSET_HTTP_FAILED');
  const bytes=await response.arrayBuffer();
  const hash=Array.from(new Uint8Array(await subtle.digest('SHA-256',bytes)),
    b=>b.toString(16).padStart(2,'0')).join('');
  requireThat(hash===expectedSha256,'ASSET_DIGEST_MISMATCH');
  return bytes;
}
