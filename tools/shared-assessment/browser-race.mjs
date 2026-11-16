/** Real Chromium HTTP and two-tab IndexedDB regression. No external JS packages.
 * Requires Node 22+ and CHROME_BINARY (or google-chrome). This tests storage
 * conflicts only; it does NOT certify DOM/asset secrecy in actual learner pages. */
import {spawn} from 'node:child_process';
import {mkdtemp,readFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createServer} from 'node:http';
import {once} from 'node:events';
import assert from 'node:assert/strict';

const root=dirname(fileURLToPath(import.meta.url));
const profile=await mkdtemp(join(tmpdir(),'g9-shared-idb-'));
const server=createServer(async(req,res)=>{
  if(req.url==='/engine.mjs'){
    res.setHeader('Content-Type','text/javascript; charset=UTF-8');
    res.end(await readFile(join(root,'engine.mjs')));
  }else{res.setHeader('Content-Type','text/html; charset=UTF-8');
    res.end('<!doctype html><title>G9 transactional attempt browser test</title>');}
});
server.listen(0,'127.0.0.1');
await once(server,'listening');
const base='http://127.0.0.1:'+server.address().port;
const binary=process.env.CHROME_BINARY||'google-chrome';
const chrome=spawn(binary,['--headless=new','--no-sandbox','--disable-dev-shm-usage',
  '--disable-background-networking','--no-proxy-server','--remote-allow-origins=*',
  '--remote-debugging-port=0','--user-data-dir='+profile,base],{stdio:'ignore'});
function sleep(ms){return new Promise(resolve=>setTimeout(resolve,ms));}
async function remotePort(){
  for(let i=0;i<160;i++){
    try{const file=await readFile(join(profile,'DevToolsActivePort'),'utf8');
      return Number(file.split('\n')[0]);}
    catch(e){await sleep(50);}
  }
  throw Error('CHROME_START_FAILED');
}
class Cdp {
  constructor(ws){this.ws=ws;this.pending=new Map();this.sequence=0;
    ws.addEventListener('message',event=>{
      const v=JSON.parse(event.data);
      if(this.pending.has(v.id)){
        const handlers=this.pending.get(v.id);this.pending.delete(v.id);
        if(v.error)handlers.reject(Error(v.error.message));else handlers.resolve(v.result);
      }
    });
  }
  send(method,params={}){
    const id=++this.sequence;
    return new Promise((resolve,reject)=>{
      this.pending.set(id,{resolve,reject});
      this.ws.send(JSON.stringify({id,method,params}));
    });
  }
  async evaluate(expression){
    const result=await this.send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});
    if(result.exceptionDetails)throw Error(JSON.stringify(result.exceptionDetails));
    return result.result.value;
  }
  close(){this.ws.close();}
}
async function connect(url){
  assert.equal(typeof WebSocket,'function','Node global WebSocket required');
  const ws=new WebSocket(url);
  await new Promise((resolve,reject)=>{
    ws.addEventListener('open',resolve,{once:true});
    ws.addEventListener('error',reject,{once:true});
  });
  return new Cdp(ws);
}
async function tab(port){
  const result=await fetch('http://127.0.0.1:'+port+'/json/new?about:blank',{method:'PUT'});
  assert.equal(result.ok,true,'CDP new tab');
  const target=await result.json();
  const c=await connect(target.webSocketDebuggerUrl);
  await c.send('Page.enable');await c.send('Runtime.enable');
  const nav=await c.send('Page.navigate',{url:base});
  if(nav.errorText)throw Error('BROWSER_NAVIGATION_BLOCKED:'+nav.errorText);
  for(let i=0;i<100;i++){
    try{
      if(await c.evaluate('document.readyState')==='complete'){
        if((await c.evaluate('location.href')).startsWith(base))return c;
      }
    }catch(e){}
    await sleep(40);
  }
  throw Error('BROWSER_TAB_NOT_LOADED');
}
const rev='a'.repeat(64);
const predict={hypothesis:'The conserved atomic inventory remains constant here.',
  conditions:'No matter crosses the explicitly chosen outer boundary.'};
const attempt={claim:'The tracked system can exhibit a measured mass change.',
  model:'I use a system-boundary and component-transport ledger.',
  reasoning:'I identify transfers before interpreting a change in reading.',
  check:'The larger atomic inventory is independently accounted for.'};
function statement(type,evidence,expectedSequence){
  return '(async()=>{const m=await import("/engine.mjs");'+
    'const s=new m.IndexedDbAttemptStore({dbName:"g9-real-browser-idb-r0"});'+
    'try{const r=await s.commit({taskUid:"two-tabs",revision:"'+rev+
    '",expectedSequence:'+expectedSequence+',type:'+JSON.stringify(type)+
    ',evidence:'+JSON.stringify(evidence)+'});'+
    'return {ok:true,sequence:r.sequence,phase:r.phase};}'+
    'catch(e){return {ok:false,code:e.code||String(e)};}})()';
}
try{
  const port=await remotePort();
  const left=await tab(port),right=await tab(port);
  const [a,b]=await Promise.all([
    left.evaluate(statement('PREDICT',predict,0)),
    right.evaluate(statement('PREDICT',predict,0)),
  ]);
  assert.equal([a,b].filter(x=>x.ok).length,1,JSON.stringify([a,b]));
  assert.equal([a,b].filter(x=>!x.ok)[0].code,'CONCURRENT_UPDATE');
  const [c,d]=await Promise.all([
    left.evaluate(statement('HINT',{level:1},1)),
    right.evaluate(statement('ATTEMPT',attempt,1)),
  ]);
  assert.equal([c,d].filter(x=>x.ok).length,1,JSON.stringify([c,d]));
  assert.equal([c,d].filter(x=>!x.ok)[0].code,'CONCURRENT_UPDATE');
  const state=await left.evaluate('(async()=>{const m=await import("/engine.mjs");'+
    'const s=new m.IndexedDbAttemptStore({dbName:"g9-real-browser-idb-r0"});'+
    'const r=await s.read("two-tabs","'+rev+'");'+
    'return {sequence:r.sequence,events:r.events.map(e=>e.type),phase:r.phase,'+
    'assistance:r.firstAttemptAssistance,academic:r.academicAssessment};})()');
  assert.equal(state.sequence,2);
  assert.equal(state.events.length,2);
  assert.equal(state.academic,'NOT_EVALUATED');
  const failure=await right.evaluate('(async()=>{const m=await import("/engine.mjs");'+
    'try{await new m.IndexedDbAttemptStore({indexedDb:null}).read("two-tabs");'+
    'return "UNSAFE";}catch(e){return e.code;}})()');
  assert.equal(failure,'INDEXEDDB_UNAVAILABLE');
  const tamper=await left.evaluate('(async()=>{const m=await import("/engine.mjs");'+
    'const s=new m.IndexedDbAttemptStore({dbName:"g9-real-browser-idb-r0"});'+
    'const r=await s.read("two-tabs","'+rev+'");r.events[0].evidence.hypothesis="A long but forged replacement hypothesis to test replay mismatch.";'+
    'try{m.verifyRecord(r);return "UNSAFE";}catch(e){return e.code;}})()');
  assert.equal(tamper,'RECORD_REPLAY_MISMATCH');
  left.close();right.close();
  console.log('CHROME_IDB_TWO_TAB_PASS: 1 writer and 1 CONCURRENT_UPDATE per race;'+
    ' readback, blocked storage, and replay-tamper checks passed.');
  console.log(JSON.stringify({firstRace:[a,b],secondRace:[c,d],state,failure,tamper}));
}finally{
  chrome.kill('SIGKILL');server.close();
  await rm(profile,{recursive:true,force:true,maxRetries:5,retryDelay:100}).catch(()=>{});
}
