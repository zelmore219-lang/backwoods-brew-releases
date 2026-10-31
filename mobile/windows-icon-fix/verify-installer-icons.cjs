const fs=require('fs'),dep=require('module').createRequire('/workspace/backwoods-builds/vendor-4.1.0/package.json'),PE=dep('pe-library'),RE=dep('resedit'),crypto=require('crypto');
for(const[slug,icon]of[['Backwoods-Brew-Main-8.2.0','/workspace/backwoods-builds/main-8.2.0/assets/icon.ico'],['Backwoods-Vendor-Ordering-4.1.0','/workspace/backwoods-builds/vendor-4.1.0/public/icons/app.ico']]){
 const file='/workspace/outputs/connected-apps-2026-10-31/'+slug+'-Windows-Setup-Icons.exe';const resources=PE.NtExecutableResource.from(PE.NtExecutable.from(fs.readFileSync(file)));
 const hash=value=>crypto.createHash('sha256').update(Buffer.from(value)).digest('hex');
 const expected=RE.Data.IconFile.from(fs.readFileSync(icon)).icons.map(x=>hash(x.data.isRaw()?x.data.bin:x.data.generate())).sort();
 const groups=RE.Resource.IconGroupEntry.fromEntries(resources.entries);if(!groups.length)throw Error('No installer icon group');
 for(const group of groups){const hashes=group.icons.map(x=>{const resource=resources.entries.find(e=>e.type===3&&e.id===x.iconID&&e.lang===group.lang);if(!resource)throw Error('Missing installer icon image');return hash(resource.bin);}).sort();if(JSON.stringify(hashes)!==JSON.stringify(expected))throw Error(slug+': installer icon does not match supplied artwork');}
 console.log(slug+': compiled installer artwork matches supplied ICO at '+expected.length+' sizes');
}
