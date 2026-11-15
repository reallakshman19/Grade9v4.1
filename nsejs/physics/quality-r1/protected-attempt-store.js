/* PH06-R2-derived shared browser-local attempt custody.
 * No server attestations. Web Locks + current-state check prevent cooperative
 * cross-tab overwrites; a user can still clear/modify localStorage manually.
 */
export const EXPOSURE_PREFIX="G9V41:PHYSICS:QUALITY-R2:STUDY:";
const storage=()=>{if(!globalThis.navigator?.locks?.request||!globalThis.crypto?.subtle)throw Error("Web Locks / crypto unavailable: fail closed");let x;try{x=localStorage}catch{throw Error("Storage denied: fail closed")}return x;};
const now=()=>new Date().toISOString();
const json=(v)=>JSON.stringify(v);
export function exposureKey(unit,revision){return EXPOSURE_PREFIX+unit+":"+revision;}
export function readExposure(unit,revision){
 try{
  const raw=storage().getItem(exposureKey(unit,revision));
  if(!raw)return {status:"UNKNOWN_NO_LOCAL_GUIDE_EVIDENCE",events:[]};
  const data=JSON.parse(raw);
  if(data.unit!==unit||data.revision!==revision||!Array.isArray(data.events)||data.events.length===0)throw Error("Invalid guide history");
  return {status:"LOCAL_GUIDE_VIEW_RECORDED",events:data.events.map(x=>({...x}))};
 }catch{return {status:"UNKNOWN_UNVERIFIED_EXPOSURE_HISTORY",events:[]};}
}
export async function recordStudyView(unit,revision){
 const key=exposureKey(unit,revision);
 try{
  const ls=storage();
  await navigator.locks.request(key,async()=>{
   const raw=ls.getItem(key);
   const old=raw?JSON.parse(raw):{unit,revision,events:[]};
   if(old.unit!==unit||old.revision!==revision||!Array.isArray(old.events))throw Error("Invalid exposure history");
   const next={...old,events:[...old.events,{kind:"DIRECT_OR_LINKED_STUDY_VIEW",at:now()}].slice(-100)};
   const encoded=json(next);ls.setItem(key,encoded);
   if(ls.getItem(key)!==encoded)throw Error("Exposure write/readback failed");
  });
  return "LOCAL_GUIDE_VIEW_RECORDED";
 }catch{return "UNKNOWN_UNVERIFIED_EXPOSURE_HISTORY";}
}
const valid=(r,uid,revision,hash)=>{
 if(!r||r.schema!==2||r.uid!==uid||r.revision!==revision||r.hash!==hash||
    !Number.isInteger(r.stage)||r.stage<1||r.stage>7||!Array.isArray(r.events)||
    !r.prediction||typeof r.prediction.value!=="string"||r.prediction.value.length<10)
  throw Error("Invalid revision-bound record");
 if(r.stage>=2&&(!r.first||typeof r.first.reasoning!=="string"||!r.first.fields||
     typeof r.first.fields!=="object"||r.first.reasoning.length<20))throw Error("Incomplete first record");
 if(r.stage>=3&&!r.revealed)throw Error("Reveal chronology corrupted");
 if(r.stage>=4&&(!r.diagnosis||!r.diagnosis.text))throw Error("Diagnosis missing");
 if(r.stage>=5&&(!r.repair||!r.repair.text))throw Error("Repair missing");
 if(r.stage>=6&&(!r.boundary||!r.boundary.fields))throw Error("Boundary missing");
 if(r.stage>=7&&!r.boundaryRevealed)throw Error("Boundary reveal missing");
 if(r.stage===1&&(r.first||r.revealed||r.boundary))throw Error("Precommit stage corrupted");
 if(r.stage<6&&r.boundary)throw Error("Premature boundary");
 return r;
};
export async function openProtectedStore({uid,revision,hash,onChange,onError}){
 const ls=storage(),key="G9V41:PHYSICS:R2:"+uid+":"+revision+":"+hash;
 const probe=key+":probe";ls.setItem(probe,"1");if(ls.getItem(probe)!=="1")throw Error("Storage write/readback denied");ls.removeItem(probe);
 const read=()=>{const raw=ls.getItem(key);return raw?valid(JSON.parse(raw),uid,revision,hash):null;};
 const dispatch=()=>{try{onChange(read())}catch(e){onError(e)}};
 const event=(kind)=>({kind,at:now()});
 const act=async(kind,payload={})=>{
  try{
   return await navigator.locks.request(key,async()=>{
    const old=read(); // latest state inside held Web Lock; never trust a stale UI snapshot
    const required=(stage)=>{if(!old||old.stage!==stage)throw Error("Attempt advanced in another tab or wrong stage; refusing stale write");};
    let next;
    if(kind==="prediction"){
     if(old)throw Error("Prediction already committed; original preserved");
     const value=String(payload.value||"").trim();if(value.length<10)throw Error("Prediction needs a reason");
     next={schema:2,uid,revision,hash,stage:1,prediction:{value,at:now()},
      first:null,revealed:false,hints:0,diagnosis:null,repair:null,boundary:null,boundaryRevealed:false,events:[event("prediction_commit")]};
    }else if(kind==="first"){
     required(1);
     const fields=payload.fields||{},reasoning=String(payload.reasoning||"").trim();
     if(reasoning.length<20||!fields.model)throw Error("Select a model and explain your first reasoning");
     if(old.first)throw Error("First answer already committed");
     const exposure=readExposure(unitFromUid(uid),revision);
     next={...old,stage:2,first:{fields:{...fields},reasoning,at:now(),exposure},events:[...old.events,event("first_commit")]};
    }else if(kind==="hint"){
     required(2);if(old.revealed||old.hints>=Number(payload.max))throw Error("Hint sequence exhausted or reconstruction already shown");
     next={...old,hints:old.hints+1,events:[...old.events,event("hint_"+(old.hints+1))]};
    }else if(kind==="reveal"){
     required(2);if(old.revealed)throw Error("Reconstruction already shown");
     next={...old,stage:3,revealed:true,events:[...old.events,event("reconstruction_revealed")]};
    }else if(kind==="diagnosis"){
     required(3);const why=String(payload.text||"").trim();
     if(why.length<20||!payload.field)throw Error("Name the first divergence and explain it");
     next={...old,stage:4,diagnosis:{field:payload.field,text:why,at:now()},events:[...old.events,event("diagnosis_commit")]};
    }else if(kind==="repair"){
     required(4);const why=String(payload.text||"").trim();
     if(why.length<30)throw Error("Repaired reasoning needs a scientific check");
     next={...old,stage:5,repair:{text:why,at:now()},events:[...old.events,event("repair_commit")]};
    }else if(kind==="boundary"){
     required(5);const reasoning=String(payload.reasoning||"").trim();
     if(reasoning.length<25||!payload.fields||Object.keys(payload.fields).length===0)throw Error("Boundary requires a new attempted model");
     next={...old,stage:6,boundary:{fields:{...payload.fields},reasoning,at:now()},events:[...old.events,event("boundary_commit")]};
    }else if(kind==="boundary_reveal"){
     required(6);next={...old,stage:7,boundaryRevealed:true,events:[...old.events,event("boundary_model_revealed")]};
    }else throw Error("Unknown state mutation");
    valid(next,uid,revision,hash);
    if(old){
     if(json(next.prediction)!==json(old.prediction))throw Error("Prediction mutation rejected");
     if(old.first&&json(next.first)!==json(old.first))throw Error("First commitment mutation rejected");
     if(next.stage<old.stage||next.events.length!==old.events.length+1)throw Error("Non-monotonic transition rejected");
    }
    const raw=json(next);ls.setItem(key,raw);
    if(ls.getItem(key)!==raw)throw Error("Write/readback mismatch");
    dispatch();
    return true;
   });
  }catch(err){onError(err);dispatch();return false}
 };
 function onStorage(ev){if(ev.key===key){if(ev.newValue===null){onError(Error("Saved first attempt deleted externally"));return}dispatch()}}
 window.addEventListener("storage",onStorage);
 dispatch();
 return {read,act,key,close:()=>window.removeEventListener("storage",onStorage)};
}
const unitFromUid=uid=>{const m=/AUTHORED-(PH(?:01-M05|02-F04|07-02|08-08))-/.exec(uid);return m?m[1]:"UNKNOWN";};
