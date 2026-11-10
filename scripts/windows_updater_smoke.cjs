// Run with Playwright on a disposable Windows CI runner, never against company records.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
const {_electron}=require('playwright');
const executable=process.argv[2];
const reuse=process.argv.includes('--reuse');
const evidence=path.join(process.env.RUNNER_TEMP||require('node:os').tmpdir(),'employee-updater-smoke.json');
if(process.platform!=='win32'||!executable)throw Error('Supply the packaged Windows Employee executable on a disposable Windows test runner.');
const expectedData=path.join(process.env.APPDATA,'Backwoods Employees');
if(!reuse&&fs.existsSync(path.join(expectedData,'records','employees-data','employees.sqlite3')))throw Error('Refusing to run over existing employee records. Use a disposable runner.');
if(reuse&&!fs.existsSync(evidence))throw Error('A previous disposable test run is required before testing reinstall.');
const hash=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const api=(page,route,data)=>page.evaluate(async({route,data})=>{
 const response=await fetch(route,data===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
 const result=await response.json();if(!response.ok)throw Error(result.error||'Employee API request failed');return result;
},{route,data});
async function launch(){
 const app=await _electron.launch({executablePath:executable,timeout:90000});
 const page=await app.firstWindow({timeout:90000});
 await page.waitForURL('http://127.0.0.1:*/assets/windows-start.html',{timeout:90000});
 assert.equal(await app.evaluate(({app})=>app.getPath('userData')),expectedData);
 assert.equal(await app.evaluate(({app})=>app.getVersion()),'0.3.1');
 return {app,page};
}
(async()=>{
 let {app,page}=await launch();
 try{
  await api(page,reuse?'/api/login':'/api/desktop/initialize',{name:'Updater CI Owner',username:'updater.ci.owner',password:'updater-test-passphrase-490'});
  let state=await api(page,'/api/state');assert.equal(state.employees.length,1);
  const ownerId=state.me.id;
  const keyFile=path.join(expectedData,'employee-documents.dpapi');assert.ok(fs.existsSync(keyFile));const keyHash=hash(keyFile);
  if(reuse){const previous=JSON.parse(fs.readFileSync(evidence));assert.equal(ownerId,previous.ownerId);assert.equal(keyHash,previous.keyHash);}
  else fs.writeFileSync(evidence,JSON.stringify({ownerId,keyHash}));
  const wizardPromise=app.waitForEvent('window');
  await app.evaluate(({Menu})=>Menu.getApplicationMenu().items.find(i=>i.label==='App updates').submenu.items[0].click());
  const wizard=await wizardPromise;await wizard.waitForLoadState('domcontentloaded');
  assert.equal(await wizard.title(),'App updates');
  await wizard.locator('#current').filter({hasText:'0.3.1'}).waitFor();
  assert.equal(await wizard.locator('#feed').inputValue(),'https://github.com/zelmore219-lang/backwoods-brew-releases/releases/download/employee-updates/backwoods-employees-updates.json');
  await wizard.locator('#check').click();
  await wizard.locator('#phase').filter({hasText:/current|error|available/}).waitFor({timeout:90000});
  // Before first publication a clear 404 is expected; after publication current is expected.
  const message=await wizard.locator('#message').textContent();
  assert.match(message,/latest published version|not been published|new version is available/i);
  assert.equal(await wizard.locator('#install').isEnabled(),false);
  await app.close();
  ({app,page}=await launch());
  await api(page,'/api/login',{username:'updater.ci.owner',password:'updater-test-passphrase-490'});
  state=await api(page,'/api/state');assert.equal(state.me.id,ownerId);assert.equal(state.employees.length,1);
  assert.equal(hash(keyFile),keyHash,'The same encrypted document key must survive app restarts');
  console.log('PASS: packaged Windows app starts its bundled engine, uses the original data path, opens the updater, checks the feed, and preserves its employee record and DPAPI document key across restart.');
 }finally{await app.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
