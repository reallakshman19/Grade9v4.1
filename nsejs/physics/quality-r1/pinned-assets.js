/* Candidate-only exact-byte integrity; NOT an independently signed R3 manifest.
 * Prevents benign/stale static assets from silently changing learner state.
 */
const PIN_MANIFEST_BLOB="4422464136fac69dd67a0573be5906b909b4a69f";
const base=new URL("./",import.meta.url);
let pinsPromise=null;
const bhex=bytes=>[...new Uint8Array(bytes)].map(x=>x.toString(16).padStart(2,"0")).join("");
export async function gitBlobSha(raw){
 if(!crypto?.subtle||!globalThis.TextEncoder)throw Error("Integrity digest unavailable");
 const data=new TextEncoder().encode(raw);
 const head=new TextEncoder().encode("blob "+data.length+String.fromCharCode(0));
 const all=new Uint8Array(head.length+data.length);all.set(head);all.set(data,head.length);
 return bhex(await crypto.subtle.digest("SHA-1",all));
}
export async function sha256(text){return bhex(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(text)));}
async function fetchNoCache(filename){
 if(!/^[\w-]+\.v2\.json$/.test(filename))throw Error("Unexpected learner asset path");
 const url=new URL(filename,base);
 if(url.origin!==location.origin||!url.pathname.startsWith(base.pathname))throw Error("External or traversing asset");
 const response=await fetch(url,{cache:"no-store",credentials:"same-origin"});
 if(!response.ok)throw Error("Pinned asset missing: "+filename);
 return response.text();
}
export async function assetPins(){
 if(!pinsPromise)pinsPromise=(async()=>{
  const raw=await fetchNoCache("asset-pins.v2.json");
  if(await gitBlobSha(raw)!==PIN_MANIFEST_BLOB)throw Error("Candidate pin manifest does not match audited bytes");
  const data=JSON.parse(raw);
  if(data.schema!=="g9v41-physics-author-pins/v2"||data.status!=="AUTHOR_ONLY__NOT_INDEPENDENTLY_SIGNED__ACADEMIC_HOLD"||data.items?.length!==7)throw Error("Candidate pin manifest invalid");
  const entries=new Map();
  for(const r of data.items){
   if(!/^[\w-]+\.v2\.json$/.test(r.path)||!/^[0-9a-f]{40}$/.test(r.git_blob_sha)||entries.has(r.path))throw Error("Pin entry invalid");
   entries.set(r.path,r.git_blob_sha);
  }
  if(entries.get("cases.v2.json")!==data.source_v2_git_blob)throw Error("Author case revision unpinned");
  return {entries,source_sha:data.source_v2_git_blob,pin_blob:PIN_MANIFEST_BLOB};
 })();
 return pinsPromise;
}
export async function pinnedJson(filename,expectedSchema){
 const pins=await assetPins();
 const expected=pins.entries.get(filename);if(!expected)throw Error("Asset missing from revision pins");
 const raw=await fetchNoCache(filename);
 if(await gitBlobSha(raw)!==expected)throw Error("Pinned bytes mismatch: "+filename);
 const body=JSON.parse(raw);
 if(body.schema!==expectedSchema||body.status!==undefined&&body.status!=="AUTHOR_EXPOSED_CANDIDATE__ACADEMIC_HOLD"&&body.status!=="CANDIDATE_UNQUALIFIED__NO_ORIGINAL_QUESTIONS_ADMITTED")throw Error("Asset schema or HOLD status invalid");
 if(body.source_v2_git_blob&&body.source_v2_git_blob!==pins.source_sha)throw Error("Stale or fabricated author source pin");
 return {body,pins};
}
