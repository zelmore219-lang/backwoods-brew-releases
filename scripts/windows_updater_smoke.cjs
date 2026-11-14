// Run with Playwright on a disposable Windows CI runner, never against company records.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
const {_electron}=require('playwright');
const executable=process.argv[2];
const publicMetadata=path.join(__dirname,'../employee-updates/package.json');
const versionArgument=process.argv.find(argument=>argument.startsWith('--expected-version='));
const expectedVersion=versionArgument?versionArgument.split('=')[1]:JSON.parse(fs.readFileSync(fs.existsSync(publicMetadata)?publicMetadata:path.join(__dirname,'../desktop-local/package.json'))).version;
assert.match(expectedVersion,/^\d+\.\d+\.\d+$/);
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
 assert.equal(await app.evaluate(({app})=>app.getVersion()),expectedVersion);
 return {app,page};
}
(async()=>{
 let {app,page}=await launch();
 try{
  await api(page,reuse?'/api/login':'/api/desktop/initialize',{name:'Updater CI Owner',username:'updater.ci.owner',password:'updater-test-passphrase-490'});
  let state=await api(page,'/api/state');assert.equal(state.employees.length,1);
  const ownerId=state.me.id;
  const keyFile=path.join(expectedData,'employee-documents.dpapi');assert.ok(fs.existsSync(keyFile));const keyHash=hash(keyFile);
  if(expectedVersion!=='0.3.1'){
   const ownerRuntime=await app.evaluate(({app})=>{
    const require=process.mainModule?.require?process.mainModule.require.bind(process.mainModule):process.getBuiltinModule('node:module').createRequire(app.getAppPath()+'/package.json');
    const path=require('node:path'),fs=require('node:fs'),{spawnSync}=require('node:child_process');
    const resources=path.dirname(app.getAppPath());
    const archive=path.join(app.getAppPath(),'owner-auth.asar');
    const auth=require(path.join(fs.existsSync(archive)?archive:path.join(app.getAppPath(),'owner-auth'),'node_modules/firebase-tools/lib/auth.js'));
    const child=spawnSync(path.join(resources,'python/python.exe'),['-c','import firebase_admin; from google.oauth2.credentials import Credentials; from app.owner_runtime import Runtime; print("owner-runtime-ready")'],{cwd:path.join(resources,'program'),encoding:'utf8',windowsHide:true,timeout:30000});
    return {start:typeof auth.loginRemotelyStart,complete:typeof auth.loginRemotelyComplete,status:child.status,output:child.stdout,error:child.stderr};
   });
   assert.equal(ownerRuntime.start,'function');assert.equal(ownerRuntime.complete,'function');
   assert.equal(ownerRuntime.status,0,ownerRuntime.error);assert.match(ownerRuntime.output,/owner-runtime-ready/);
   assert.equal(await page.evaluate(()=>typeof window.employeeOwner),'undefined','The Employee renderer must not expose the owner credential bridge');
   assert.equal(fs.existsSync(path.join(expectedData,'owner-google.dpapi')),false,'No customer Google administrator credential may ship in an installer');
   const ownerPromise=app.waitForEvent('window');
   await app.evaluate(({Menu})=>Menu.getApplicationMenu().items.find(item=>item.label==='Owner service').submenu.items[0].click());
   const ownerWindow=await ownerPromise;await ownerWindow.waitForLoadState('domcontentloaded');
   await ownerWindow.getByRole('heading',{name:'Employee owner service',exact:true}).waitFor();
   const ownerState=await ownerWindow.evaluate(()=>window.employeeOwner.action('state'));
   assert.equal(ownerState.connected,false);assert.equal(ownerState.running,false);
   assert.deepEqual(Object.keys(ownerState).sort(),['configured','connected','email','message','running']);
   await ownerWindow.getByRole('button',{name:'Load owner records',exact:true}).click();
   await ownerWindow.locator('#error').filter({hasText:'Connect the Google owner account first'}).waitFor();
   await ownerWindow.close();
  }
  if(reuse){const previous=JSON.parse(fs.readFileSync(evidence));assert.equal(ownerId,previous.ownerId);assert.equal(keyHash,previous.keyHash);}
  else fs.writeFileSync(evidence,JSON.stringify({ownerId,keyHash}));
  const wizardPromise=app.waitForEvent('window');
  await app.evaluate(({Menu})=>Menu.getApplicationMenu().items.find(i=>i.label==='App updates').submenu.items[0].click());
  const wizard=await wizardPromise;await wizard.waitForLoadState('domcontentloaded');
  assert.equal(await wizard.title(),'App updates');
  await wizard.locator('#current').filter({hasText:expectedVersion}).waitFor();
  assert.equal(await wizard.locator('#feed').inputValue(),'https://github.com/zelmore219-lang/backwoods-brew-releases/releases/download/employee-updates/backwoods-employees-updates.json');
  const feedResponse=await fetch('https://github.com/zelmore219-lang/backwoods-brew-releases/releases/download/employee-updates/backwoods-employees-updates.json');
  assert.ok(feedResponse.ok||feedResponse.status===404);
  await wizard.locator('#check').click();
  await wizard.locator('#phase').filter({hasText:/current|error|available/}).waitFor({timeout:90000});
  // Before first publication a clear 404 is expected; after publication current is expected.
  const message=await wizard.locator('#message').textContent();
  assert.match(message,feedResponse.ok?/latest published version|new version is available/i:/not been published/i);
  console.log('Verified Windows updater response: '+message);
  assert.equal(await wizard.locator('#install').isEnabled(),false);
  await app.close();
  ({app,page}=await launch());
  await api(page,'/api/login',{username:'updater.ci.owner',password:'updater-test-passphrase-490'});
  state=await api(page,'/api/state');assert.equal(state.me.id,ownerId);assert.equal(state.employees.length,1);
  assert.equal(hash(keyFile),keyHash,'The same encrypted document key must survive app restarts');
  console.log('PASS: packaged Windows app starts its bundled engine, uses the original data path, opens the updater, checks the feed, and preserves its employee record and DPAPI document key across restart.');
 }finally{await app.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
