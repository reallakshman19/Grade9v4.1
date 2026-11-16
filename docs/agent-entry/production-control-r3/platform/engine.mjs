/* G9 common assessment platform. No subject answers, no HTML, no academic authority.
 * Protects cooperating browser sessions; local storage and static files are not examination custody.
 */
export const ENGINE_VERSION="g9-assessment/1.0.0";
const HASH=/^[a-f0-9]{64}$/, ID=/^[a-zA-Z0-9_-]{1,80}$/;
const ROLES=["source_prompt","study","challenge","hint1","hint2","hint3","feedback","boundary","boundary_feedback","source_feedback"];
const REQUIRED=ROLES.filter(r=>!r.startsWith("hint"));
const MAX_TEXT=12000, MAX_BYTES=2_000_000, MAX_EVENTS=250;
const assert=(ok,msg)=>{if(!ok)throw Error(msg)};
const obj=x=>x!==null&&typeof x==="object"&&!Array.isArray(x)&&Object.getPrototypeOf(x)===Object.prototype;
const exact=(x,keys)=>obj(x)&&Object.keys(x).length===keys.length&&keys.every(k=>Object.hasOwn(x,k));
const str=(x,min=1)=>typeof x==="string"&&x.trim().length>=min&&x.length<=MAX_TEXT;
const id=x=>typeof x==="string"&&ID.test(x)&&!Object.hasOwn(Object.prototype,x)&&x!=="prototype";
const deepFreeze=x=>{if(x&&typeof x==="object"&&!Object.isFrozen(x)){Object.values(x).forEach(deepFreeze);Object.freeze(x)}return x};
const finite=x=>typeof x==="number"&&Number.isFinite(x);
const copy=x=>JSON.parse(JSON.stringify(x));
const unique=x=>new Set(x).size===x.length;
const fail=(s)=>{throw Error(s)};
// Native window.fetch requires the Window receiver in Chromium. Calling it as
// assessment.fetcher(url) otherwise binds this to Assessment (Illegal invocation).
const browserFetch=(...args)=>globalThis.fetch(...args);
export async function digest(bytes,crypto=globalThis.crypto){
 assert(crypto?.subtle,"CRYPTO_UNAVAILABLE");
 return Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",bytes)),x=>x.toString(16).padStart(2,"0")).join("");
}
function fields(xs){
 assert(Array.isArray(xs)&&xs.length>0&&xs.length<=40,"FIELD_COUNT");
 for(const f of xs){
  assert(obj(f)&&id(f.id)&&str(f.label)&&["number","choice","text"].includes(f.type),"FIELD_SHAPE");
  if(f.type==="choice")assert(exact(f,["id","label","type","options"])&&Array.isArray(f.options)&&f.options.length>=2&&f.options.length<=20&&f.options.every(o=>exact(o,["id","label"])&&id(o.id)&&str(o.label))&&unique(f.options.map(o=>o.id)),"CHOICE_SHAPE");
  else assert(exact(f,["id","label","type"]),"FIELD_UNKNOWN_KEYS");
 }
 assert(unique(xs.map(f=>f.id))&&xs.some(f=>f.type!=="text"),"FIELD_IDS_OR_NO_CHECKABLE_FIELD");
}
function answerShape(x){
 assert(obj(x)&&Object.keys(x).length>0&&Object.keys(x).length<=40,"ANSWER_SHAPE");
 for(const [k,v] of Object.entries(x))assert(id(k)&&(str(v)||finite(v)),"ANSWER_VALUE:"+k);
}
export function validateAnswer(def,x){
 answerShape(x);assert(exact(x,def.map(f=>f.id)),"ANSWER_FIELD_SET");
 for(const f of def){
  const v=x[f.id];
  if(f.type==="number")assert(finite(v),"NUMBER_REQUIRED:"+f.id);
  else if(f.type==="choice")assert(f.options.some(o=>o.id===v),"CHOICE_REQUIRED:"+f.id);
  else assert(str(v),"TEXT_REQUIRED:"+f.id);
 }
 return copy(x);
}
function checks(xs){
 assert(Array.isArray(xs)&&xs.length>0&&xs.length<=40,"CHECK_COUNT");
 for(const c of xs){
  assert(obj(c)&&id(c.field)&&str(c.feedback)&&["number","choice"].includes(c.type),"CHECK_SHAPE");
  if(c.type==="number")assert(exact(c,["field","type","expected","abs_tolerance","rel_tolerance","feedback"])&&finite(c.expected)&&finite(c.abs_tolerance)&&finite(c.rel_tolerance)&&c.abs_tolerance>=0&&c.rel_tolerance>=0&&c.rel_tolerance<=0.1,"NUMERIC_CHECK");
  else assert(exact(c,["field","type","expected","feedback"])&&id(c.expected),"CHOICE_CHECK");
 }
 assert(unique(xs.map(c=>c.field)),"DUPLICATE_CHECK");
}
export function compare(def,rubric,answer){
 validateAnswer(def,answer);checks(rubric);
 const graded=def.filter(f=>f.type!=="text");
 assert(rubric.length===graded.length&&graded.every(f=>rubric.some(c=>c.field===f.id&&c.type===f.type)),"RUBRIC_COVERAGE");
 const results=rubric.map(c=>{
  const f=def.find(f=>f.id===c.field);
  if(c.type==="choice")assert(f.options.some(o=>o.id===c.expected),"RUBRIC_CHOICE_UNKNOWN");
  const actual=answer[c.field];
  const pass=c.type==="choice"?actual===c.expected:Math.abs(actual-c.expected)<=Math.max(c.abs_tolerance,c.rel_tolerance*Math.abs(c.expected));
  return {field:c.field,pass,feedback:pass?null:c.feedback};
 });
 return {allMatched:results.every(x=>x.pass),firstDivergence:results.find(x=>!x.pass)?.field??null,results,ungradedText: def.filter(f=>f.type==="text").map(f=>f.id)};
}
export function validateManifest(m){
 assert(exact(m,["schema","engine","uid","revision","status","assets"])&&m.schema==="g9-assessment-manifest/v1"&&m.engine===ENGINE_VERSION&&id(m.uid)&&id(m.revision)&&m.status==="TECHNICAL_CANDIDATE_HOLD"&&obj(m.assets),"MANIFEST_SHAPE");
 const roles=Object.keys(m.assets);
 assert(REQUIRED.every(r=>roles.includes(r))&&roles.every(r=>ROLES.includes(r)),"ASSET_ROLES");
 assert(!m.assets.hint2||m.assets.hint1,"HINT_GAP");assert(!m.assets.hint3||m.assets.hint2,"HINT_GAP");
 const paths=[];
 for(const r of roles){const a=m.assets[r];
  assert((exact(a,["path","sha256"])||exact(a,["path","sha256","media"]))&&typeof a.path==="string"&&/^[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)*\.json$/.test(a.path)&&HASH.test(a.sha256),"ASSET_PIN:"+r);
  paths.push(a.path);
  if(a.media){assert(Array.isArray(a.media)&&a.media.length<=8,"MEDIA_COUNT");for(const image of a.media){assert(exact(image,["path","sha256","alt"])&&/^[a-zA-Z0-9_-]+\.(?:png|webp)$/.test(image.path)&&HASH.test(image.sha256)&&str(image.alt),"MEDIA_PIN");paths.push(image.path)}}
 }
 assert(unique(paths),"ASSET_ROLE_REUSE");return m;
}
export function validateAsset(m,role,a){
 assert(exact(a,["schema","uid","revision","role","payload"])&&a.schema==="g9-assessment-asset/v1"&&a.uid===m.uid&&a.revision===m.revision&&a.role===role,"ASSET_IDENTITY:"+role);
 const p=a.payload;
 if(["source_prompt","challenge","boundary"].includes(role)){
  const keys=role==="challenge"?["stem","prediction","fields"]:["stem","fields"];
  assert(exact(p,keys)&&str(p.stem)&&(role!=="challenge"||str(p.prediction)),"PROMPT_SHAPE:"+role);fields(p.fields);
 }else if(role==="study"){
  assert(exact(p,["title","sections"])&&str(p.title)&&Array.isArray(p.sections)&&p.sections.length>=2&&p.sections.length<=40&&p.sections.every(s=>exact(s,["heading","body"])&&str(s.heading)&&Array.isArray(s.body)&&s.body.length&&s.body.every(t=>str(t))),"STUDY_SHAPE");
 }else if(role.startsWith("hint")){
  assert(exact(p,["text"])&&str(p.text),"HINT_SHAPE");
 }else if(role==="feedback"){
  assert(exact(p,["reconstruction","checks","repair_prompt"])&&Array.isArray(p.reconstruction)&&p.reconstruction.length>=2&&p.reconstruction.every(s=>str(s))&&str(p.repair_prompt),"FEEDBACK_SHAPE");checks(p.checks);
 }else{
  assert(exact(p,["model","checks"])&&str(p.model),"CLOSURE_SHAPE:"+role);checks(p.checks);
 }
 return p;
}
const initial=()=>({opened:{},source:null,prediction:null,first:null,reconstruction:null,diagnosis:null,repairs:[],boundary:null,boundaryRepairs:[],sourceReturn:null,events:[]});
const matched=(xs)=>xs.length>0&&xs[xs.length-1].matched===true;
const mark=(s,r)=>Boolean(s.opened[r]);
export function canOpen(s,r,m){
 if(mark(s,r)||!m.assets[r])return false;
 switch(r){
  case "source_prompt":return !s.source;
  case "study":return !!s.source;
  case "challenge":return mark(s,"study");
  case "hint1":case "hint2":case "hint3":return !!s.prediction&&!s.first&&(r==="hint1"||mark(s,"hint"+(Number(r.slice(-1))-1)));
  case "feedback":return !!s.first;
  case "boundary":return matched(s.repairs);
  case "boundary_feedback":return !!s.boundary;
  case "source_feedback":return !!s.sourceReturn;
  default:return false;
 }
}
const resultShape=x=>exact(x,["answer","matched"])&&typeof x.matched==="boolean";
function reduce(s,e,m){
 const {kind,data}=e;
 if(kind.startsWith("open:")){
  const r=kind.slice(5);assert(data===null&&canOpen(s,r,m),"ILLEGAL_EXPOSURE:"+r);s.opened[r]=e.seq;return;
 }
 switch(kind){
  case "source":assert(mark(s,"source_prompt")&&!s.source,"SOURCE_LOCKED");answerShape(data);s.source=data;break;
  case "prediction":assert(mark(s,"challenge")&&!s.prediction&&str(data),"PREDICTION_LOCKED");s.prediction=data;break;
  case "first":assert(s.prediction&&!s.first,"FIRST_LOCKED");answerShape(data);s.first={answer:data,assisted:Object.keys(s.opened).filter(r=>r.startsWith("hint"))};break;
  case "reconstruct":assert(mark(s,"feedback")&&!s.reconstruction&&str(data),"RECONSTRUCTION_LOCKED");s.reconstruction=data;break;
  case "diagnose":assert(s.reconstruction&&!s.diagnosis&&exact(data,["field","explanation"])&&(data.field===null||id(data.field))&&str(data.explanation),"DIAGNOSIS_LOCKED");s.diagnosis=data;break;
  case "repair":assert(s.diagnosis&&!matched(s.repairs)&&resultShape(data),"REPAIR_LOCKED");answerShape(data.answer);s.repairs.push(data);break;
  case "boundary":assert(mark(s,"boundary")&&!s.boundary,"BOUNDARY_LOCKED");answerShape(data);s.boundary=data;break;
  case "boundary_repair":assert(mark(s,"boundary_feedback")&&!s.sourceReturn&&!matched(s.boundaryRepairs)&&resultShape(data),"BOUNDARY_REPAIR_LOCKED");answerShape(data.answer);s.boundaryRepairs.push(data);break;
  case "source_return":assert(mark(s,"boundary_feedback")&&!s.sourceReturn,"SOURCE_RETURN_LOCKED");answerShape(data);s.sourceReturn=data;break;
  default:fail("UNKNOWN_EVENT:"+kind);
 }
}
export function replay(record,m,manifestHash){
 assert(exact(record,["schema","uid","revision","manifest","engine","events"])&&record.schema==="g9-assessment-record/v1"&&record.uid===m.uid&&record.revision===m.revision&&record.manifest===manifestHash&&record.engine===ENGINE_VERSION&&Array.isArray(record.events)&&record.events.length<=MAX_EVENTS,"RECORD_IDENTITY");
 const s=initial();let last=0;
 for(let i=0;i<record.events.length;i++){
  const e=record.events[i];
  assert(exact(e,["seq","at","kind","data"])&&e.seq===i+1&&typeof e.kind==="string"&&Number.isSafeInteger(e.at)&&e.at>=last&&e.at>0,"EVENT_ORDER");
  last=e.at;reduce(s,e,m);
 }
 s.events=record.events;return s;
}
export class Assessment{
 constructor({manifest,manifestHash,baseURL,storage,locks,fetcher=browserFetch,crypto=globalThis.crypto,clock=Date.now}){
  this.m=deepFreeze(validateManifest(copy(manifest)));assert(HASH.test(manifestHash),"MANIFEST_HASH");this.hash=manifestHash;
  this.base=new URL(baseURL);assert(["http:","https:"].includes(this.base.protocol)&&this.base.pathname.endsWith("/")&&!this.base.search&&!this.base.hash,"BASE_URL");
  this.storage=storage;this.locks=locks;this.fetcher=fetcher;this.crypto=crypto;this.clock=clock;
  this.key="g9:assessment:v1:"+this.m.uid+":"+manifestHash;this.cache=new Map();this.mediaCache=new Map();this.seen=[];this.blocked=false;
 }
 blank(){return {schema:"g9-assessment-record/v1",uid:this.m.uid,revision:this.m.revision,manifest:this.hash,engine:ENGINE_VERSION,events:[]}}
 read(){
  const raw=this.storage.getItem(this.key);if(raw===null){assert(this.seen.length===0,"RECORD_DISAPPEARED");return this.blank()}
  assert(typeof raw==="string"&&raw.length<=MAX_BYTES,"STORAGE_SIZE");const r=JSON.parse(raw);replay(r,this.m,this.hash);assert(r.events.length>=this.seen.length&&this.seen.every((x,i)=>x===JSON.stringify(r.events[i])),"RECORD_ROLLBACK");this.seen=r.events.map(x=>JSON.stringify(x));return r;
 }
 async locked(fn){
  assert(!this.blocked,"SESSION_BLOCKED");
  try{
   assert(this.locks?.request&&this.storage&&this.crypto?.subtle,"PROTECTION_UNAVAILABLE");
   return await this.locks.request(this.key,{mode:"exclusive"},fn);
  }catch(e){this.blocked=true;throw e}
 }
 append(r,kind,data){
  assert(r.events.length<MAX_EVENTS,"EVENT_LIMIT");
  const at=Math.max(this.clock(),r.events.at(-1)?.at??0);
  const next={...r,events:[...r.events,{seq:r.events.length+1,at,kind,data:copy(data)}]};
  replay(next,this.m,this.hash);
  const raw=JSON.stringify(next);assert(raw.length<=MAX_BYTES,"STORAGE_SIZE");
  this.storage.setItem(this.key,raw);assert(this.storage.getItem(this.key)===raw,"SAVE_READBACK");
  this.seen=next.events.map(x=>JSON.stringify(x));return next;
 }
 async getAsset(r,role){
  const s=replay(r,this.m,this.hash);assert(mark(s,role),"ASSET_NOT_OPEN:"+role);
  if(this.cache.has(role))return this.cache.get(role);
  const pin=this.m.assets[role],u=new URL(pin.path,this.base);
  assert(u.origin===this.base.origin&&u.pathname.startsWith(this.base.pathname),"ASSET_ORIGIN");
  const response=await this.fetcher(u.href,{cache:"no-store",credentials:"same-origin",redirect:"error"});
  assert(response.ok,"ASSET_HTTP:"+role);
  const bytes=new Uint8Array(await response.arrayBuffer());assert(bytes.length<=MAX_BYTES&&await digest(bytes,this.crypto)===pin.sha256,"ASSET_HASH:"+role);
  const value=validateAsset(this.m,role,JSON.parse(new TextDecoder("utf-8",{fatal:true}).decode(bytes)));
  this.cache.set(role,deepFreeze(value));return value;
 }
 async getMedia(r,role){
  const s=replay(r,this.m,this.hash);assert(mark(s,role),"MEDIA_NOT_OPEN");
  if(this.mediaCache.has(role))return this.mediaCache.get(role);
  const result=[];
  for(const p of this.m.assets[role].media??[]){
   const u=new URL(p.path,this.base);
   const resp=await this.fetcher(u.href,{cache:"no-store",credentials:"same-origin",redirect:"error"});assert(resp.ok,"MEDIA_HTTP");
   const b=new Uint8Array(await resp.arrayBuffer());assert(b.length<=MAX_BYTES&&await digest(b,this.crypto)===p.sha256,"MEDIA_HASH");
   const png=p.path.endsWith(".png"),magic=png?b.length>=8&&[137,80,78,71,13,10,26,10].every((x,i)=>b[i]===x):b.length>=12&&String.fromCharCode(...b.slice(0,4))==="RIFF"&&String.fromCharCode(...b.slice(8,12))==="WEBP";
   assert(magic,"MEDIA_FORMAT");
   result.push(Object.freeze({alt:p.alt,blob:new Blob([b],{type:png?"image/png":"image/webp"})}));
  }
  const frozen=Object.freeze(result);this.mediaCache.set(role,frozen);return frozen;
 }
 async verify(r){
  const s=replay(r,this.m,this.hash),assets={},media={};
  for(const role of ROLES)if(mark(s,role)){assets[role]=await this.getAsset(r,role);media[role]=await this.getMedia(r,role)}
  if(s.source)validateAnswer(assets.source_prompt.fields,s.source);
  if(s.first)validateAnswer(assets.challenge.fields,s.first.answer);
  let diagnostic=null,boundaryResult=null;
  if(assets.feedback){
   diagnostic=compare(assets.challenge.fields,assets.feedback.checks,s.first.answer);
   if(s.diagnosis)assert(s.diagnosis.field===diagnostic.firstDivergence,"STALE_DIAGNOSIS");
   for(const x of s.repairs)assert(compare(assets.challenge.fields,assets.feedback.checks,x.answer).allMatched===x.matched,"STALE_REPAIR");
  }
  if(s.boundary)validateAnswer(assets.boundary.fields,s.boundary);
  if(assets.boundary_feedback){
   boundaryResult=compare(assets.boundary.fields,assets.boundary_feedback.checks,s.boundary);
   if(boundaryResult.allMatched)assert(!s.boundaryRepairs.length,"UNNEEDED_BOUNDARY_REPAIR");
   for(const x of s.boundaryRepairs)assert(compare(assets.boundary.fields,assets.boundary_feedback.checks,x.answer).allMatched===x.matched,"STALE_BOUNDARY_REPAIR");
   if(s.sourceReturn)assert(boundaryResult.allMatched||matched(s.boundaryRepairs),"BOUNDARY_NOT_REPAIRED");
  }
  if(s.sourceReturn)validateAnswer(assets.source_prompt.fields,s.sourceReturn);
  const sourceResult=assets.source_feedback?compare(assets.source_prompt.fields,assets.source_feedback.checks,s.sourceReturn):null;
  return {state:deepFreeze(s),assets:Object.freeze(assets),media:Object.freeze(media),diagnostic,boundaryResult,sourceResult,sourceFirstResult:assets.source_feedback?compare(assets.source_prompt.fields,assets.source_feedback.checks,s.source):null,academicStatus:"HOLD"};
 }
 async snapshot(){return this.locked(async()=>this.verify(this.read()))}
 async open(role){
  return this.locked(async()=>{
   let r=this.read();const s=replay(r,this.m,this.hash);
   if(!mark(s,role)){
    if(!canOpen(s,role,this.m))return {accepted:false,reason:"EXPOSURE_NOT_ALLOWED",...await this.verify(r)};
    r=this.append(r,"open:"+role,null); // persist exposure permission BEFORE any fetch
   }
   return {accepted:true,...await this.verify(r)};
  })
 }
 async submit(kind,data){
  return this.locked(async()=>{
   let r=this.read(),v=await this.verify(r),s=v.state,a=v.assets;
   try{
    switch(kind){
     case "source":data=validateAnswer(a.source_prompt.fields,data);break;
     case "prediction":assert(str(data),"PREDICTION_REQUIRED");break;
     case "first":data=validateAnswer(a.challenge.fields,data);break;
     case "reconstruct":assert(str(data),"COMPARISON_REQUIRED");break;
     case "diagnose":assert(v.diagnostic&&exact(data,["field","explanation"])&&data.field===v.diagnostic.firstDivergence&&str(data.explanation),"FIRST_DIVERGENCE_REQUIRED");break;
     case "repair":data={answer:validateAnswer(a.challenge.fields,data),matched:compare(a.challenge.fields,a.feedback.checks,data).allMatched};break;
     case "boundary":data=validateAnswer(a.boundary.fields,data);break;
     case "boundary_repair":assert(v.boundaryResult&&!v.boundaryResult.allMatched,"BOUNDARY_REPAIR_NOT_REQUIRED");data={answer:validateAnswer(a.boundary.fields,data),matched:compare(a.boundary.fields,a.boundary_feedback.checks,data).allMatched};break;
     case "source_return":assert(v.boundaryResult&&(v.boundaryResult.allMatched||matched(s.boundaryRepairs)),"BOUNDARY_NOT_REPAIRED");data=validateAnswer(a.source_prompt.fields,data);break;
     default:fail("UNKNOWN_SUBMISSION");
    }
    const test={seq:r.events.length+1,at:Math.max(this.clock(),r.events.at(-1)?.at??0),kind,data};
    reduce(replay(r,this.m,this.hash),test,this.m); // reject invalid/duplicate transition without mutating persisted record
   }catch(e){return {accepted:false,reason:String(e.message),...await this.verify(r)}}
   r=this.append(r,kind,data);return {accepted:true,...await this.verify(r)};
  })
 }
}
export async function loadAssessment({manifestURL,expectedHash,baseURL=undefined,fetcher=browserFetch,crypto=globalThis.crypto,storage=globalThis.localStorage,locks=globalThis.navigator?.locks,clock}){
 assert(HASH.test(expectedHash),"EXPECTED_MANIFEST_HASH_REQUIRED");
 const u=new URL(manifestURL);assert(["http:","https:"].includes(u.protocol)&&!u.search&&!u.hash,"MANIFEST_URL");
 const resp=await fetcher(u.href,{cache:"no-store",credentials:"same-origin",redirect:"error"});assert(resp.ok,"MANIFEST_HTTP");
 const bytes=new Uint8Array(await resp.arrayBuffer());assert(bytes.length<=MAX_BYTES&&await digest(bytes,crypto)===expectedHash,"MANIFEST_HASH_MISMATCH");
 const m=JSON.parse(new TextDecoder("utf-8",{fatal:true}).decode(bytes));
 const base=baseURL??new URL("./",u).href;assert(new URL(base).href===new URL("./",u).href,"MANIFEST_BASE_MISMATCH");
 return new Assessment({manifest:m,manifestHash:expectedHash,baseURL:base,fetcher,crypto,storage,locks,clock});
}
