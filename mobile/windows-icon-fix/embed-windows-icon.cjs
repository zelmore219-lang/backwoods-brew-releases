const fs=require('fs');
const {createRequire}=require('module');
const dependency=createRequire('/workspace/backwoods-builds/vendor-4.1.0/package.json');
const PE=dependency('pe-library'),RE=dependency('resedit');
const [file,icon]=process.argv.slice(2);
const exe=PE.NtExecutable.from(fs.readFileSync(file));
const resources=PE.NtExecutableResource.from(exe);
const original=resources.entries.filter(e=>![3,14].includes(e.type)).map(e=>({...e,bin:Buffer.from(e.bin)}));
const image=RE.Data.IconFile.from(fs.readFileSync(icon));
const groups=resources.entries.filter(e=>e.type===14);
for(const group of groups.length?groups:[{id:101,lang:1033}])RE.Resource.IconGroupEntry.replaceIconsForResource(resources.entries,group.id,group.lang,image.icons.map(i=>i.data));
resources.outputResource(exe);
const output=Buffer.from(exe.generate());
const verify=PE.NtExecutableResource.from(PE.NtExecutable.from(output));
for(const entry of original){const found=verify.entries.find(e=>e.type===entry.type&&e.id===entry.id&&e.lang===entry.lang);if(!found||!Buffer.from(found.bin).equals(entry.bin))throw Error('Unrelated PE resource changed');}
for(const entry of verify.entries.filter(e=>e.type===14)){
 const group=RE.Resource.IconGroupEntry.fromEntries([entry])[0];const icons=group.getIconItemsFromEntries(verify.entries);
 if(icons.length!==image.icons.length||icons.some((v,i)=>!Buffer.from(v.isRaw()?v.bin:v.generate()).equals(Buffer.from(image.icons[i].data.isRaw()?image.icons[i].data.bin:image.icons[i].data.generate()))))throw Error('Icon verification failed');
}
fs.writeFileSync(file+'.icon-fixed',output);fs.renameSync(file+'.icon-fixed',file);
console.log('Embedded and verified '+image.icons.length+' icon sizes: '+file);
