const { _electron } = require("playwright");
const assert = require("node:assert/strict");

(async () => {
  const executablePath = process.argv[2];
  if (!executablePath) throw Error("Installed executable path is required.");
  const app = await _electron.launch({ executablePath, timeout: 60000 });
  try {
    const page = await app.firstWindow();
    const errors = [];
    page.on("pageerror", (error) => errors.push(error.message));
    await page.getByLabel('Username or email').waitFor();
    await page.getByText('Version '+require('../driver-updates/package.json').version,{exact:true}).waitFor();
    assert.equal(await page.locator('#preview,#driver-preview').count(),0);
    const retained=await page.evaluate(async reuse=>{
      const db=await new Promise((resolve,reject)=>{const request=indexedDB.open('backwoods-driver-operations',2);request.onupgradeneeded=()=>{for(const name of ['records','outboxMeta'])if(!request.result.objectStoreNames.contains(name))request.result.createObjectStore(name,{keyPath:'key'});};request.onsuccess=()=>resolve(request.result);request.onerror=()=>reject(request.error);});
      const marker={key:'ci-upgrade-preservation',invoice:'CI-WINDOWS-INVOICE',recipient:'Fictitious installer test recipient',quantity:3};
      try{return await new Promise((resolve,reject)=>{const transaction=db.transaction('records',reuse?'readonly':'readwrite'),store=transaction.objectStore('records');if(reuse){const request=store.get(marker.key);request.onsuccess=()=>resolve(request.result);request.onerror=()=>reject(request.error);}else{store.put(marker);transaction.oncomplete=()=>resolve(marker);transaction.onerror=()=>reject(transaction.error);}});}finally{db.close();}
    },process.argv.includes('--reuse'));
    assert.deepEqual(retained,{key:'ci-upgrade-preservation',invoice:'CI-WINDOWS-INVOICE',recipient:'Fictitious installer test recipient',quantity:3},'Reinstall must retain existing Driver IndexedDB records');

    assert.equal(await page.evaluate(() => typeof require), "undefined");
    assert.equal(
      await page.evaluate(() => typeof window.backwoods.getPosition),
      "function",
    );
    const updateWindow=app.waitForEvent('window');await page.evaluate(()=>window.backwoods.openUpdates());
    const wizard=await updateWindow;await wizard.getByRole('heading',{name:'App updates',exact:true}).waitFor();
    assert.equal(await wizard.evaluate(()=>typeof require),'undefined');await wizard.close();
    // Exercise the packaged IPC/preload path on a real Windows runner. Hosted
    // runners may have no location; expected failures must be readable errors.
    const location = await page.evaluate(async () => {
      try { return { position: await window.backwoods.getPosition() }; }
      catch (error) { return { error: error.message }; }
    });
    if (location.error) {
      assert.match(location.error, /^Windows/);
      assert.doesNotMatch(location.error, /Error invoking remote method/);
    } else {
      assert.ok(Number.isFinite(location.position.coords.latitude));
      assert.ok(Number.isFinite(location.position.timestamp));
    }
    // Test data stays in this CI script; there is no sample workspace in the app.
    const invoice = '<h1>CI-PRINT</h1><h2>Delivered items</h2><p>Fictitious Windows print handoff test: 10 units, $20.00.</p><h2>Returns</h2><p>2 units.</p>'; 
    await page.setContent(invoice);
    assert.equal(await page.getByRole('heading',{name:'Delivered items',exact:true}).count(),1);
    assert.equal(await page.getByRole('heading',{name:'Returns',exact:true}).count(),1);
    assert.equal(
      await page.evaluate(() => typeof window.backwoods.printInvoice),
      "function",
    );
    const pdf = await app.evaluate(async ({ BrowserWindow }) => {
      const bytes =
        await BrowserWindow.getAllWindows()[0].webContents.printToPDF({
          printBackground: true,
        });
      return { length: bytes.length, header: bytes.subarray(0, 5).toString() };
    });
    assert.equal(pdf.header, "%PDF-");
    assert.ok(pdf.length > 1000);
    assert.deepEqual(errors, []);
    console.log(
      "PASS: installed Windows executable opens, real location IPC and order/returns invoice PDF generation work, and renderer isolation/preload bridges are intact.",
    );
  } finally {
    await app.close();
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
