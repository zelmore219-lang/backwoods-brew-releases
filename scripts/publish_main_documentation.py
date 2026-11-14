"""Publish verified documentation assets without changing apps or update feeds."""
from pathlib import Path
import hashlib,json,subprocess,urllib.request,time,zipfile
ROOT=Path(__file__).resolve().parents[1];REPO='zelmore219-lang/backwoods-brew-releases';TAG='main-manual-8.2.9'
manifest=json.loads((ROOT/'documentation-downloads/main-8.2.9/manifest.json').read_text())
assert manifest['app']=='main' and manifest['version']=='8.2.9' and manifest['tag']==TAG
out=ROOT/'documentation-output';out.mkdir(exist_ok=True)
def sha(path):return hashlib.file_digest(path.open('rb'),'sha256').hexdigest()
def api(path):return json.loads(subprocess.check_output(['gh','api','repos/'+REPO+'/'+path],text=True))
def public(url,size=None,digest=None):
 request=urllib.request.Request(url,headers={'User-Agent':'Backwoods-documentation-download-check','Cache-Control':'no-cache'})
 h=hashlib.sha256();length=0;small=bytearray()
 with urllib.request.urlopen(request,timeout=120) as response:
  while data:=response.read(1024*1024):
   length+=len(data);h.update(data)
   if size is None:small.extend(data);assert length<1024*1024
   else:assert length<=size
 if size is not None:assert length==size and h.hexdigest()==digest,'Public download checksum mismatch'
 return bytes(small)
# Documentation has its own non-latest release; application releases and updater feeds are never written.
feed_urls=[
 'https://github.com/'+REPO+'/releases/download/driver-updates/backwoods-driver-updates.json',
 'https://github.com/'+REPO+'/releases/download/employee-updates/backwoods-employees-updates.json',
 'https://github.com/zelmore219-lang/backwoods-accounting-/releases/download/app-updates/backwoods-updates.json']
feeds_before={url:public(url) for url in feed_urls}
existing=subprocess.run(['gh','release','view',TAG,'--repo',REPO],capture_output=True)
if existing.returncode:
 notes=ROOT/'documentation-downloads/main-8.2.9/RELEASE-NOTES.md'
 subprocess.run(['gh','release','create',TAG,'--repo',REPO,'--target',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'--title','Backwoods Brew Main 8.2.9 — Manuals and training guides','--notes-file',str(notes),'--latest=false'],check=True)
release=api('releases/tags/'+TAG);assert not release['draft']
archive=out/manifest['archive']['name']
with archive.open('wb') as target:
 for part in manifest['archive']['parts']:
  path=(ROOT/part['path']).resolve();assert path.is_relative_to((ROOT/'documentation-downloads').resolve())
  assert path.stat().st_size==part['size'] and sha(path)==part['sha256'];target.write(path.read_bytes())
assert archive.stat().st_size==manifest['archive']['size'] and sha(archive)==manifest['archive']['sha256']
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for item in manifest['files']:
  if item['name']==archive.name:continue
  assert Path(item['name']).name==item['name'] and item['name'].startswith('Backwoods-Main-8.2.9-')
  source=('Guides/' if item['name'].endswith(('.pdf','.docx')) else 'Verification/')+item['name']
  path=out/item['name'];path.write_bytes(z.read(source));assert path.stat().st_size==item['size'] and sha(path)==item['sha256']
checksum=out/'Backwoods-Main-8.2.9-Documentation-SHA256SUMS.txt';checksum.write_text(''.join(item['sha256']+'  '+item['name']+'\n' for item in manifest['files']))
files=[out/item['name'] for item in manifest['files']]+[checksum]
for path in files:
 current=api('releases/'+str(release['id']));existing=next((a for a in current['assets'] if a['name']==path.name),None)
 if existing:assert existing.get('digest')=='sha256:'+sha(path) and existing['size']==path.stat().st_size,'Existing documentation cannot be silently replaced'
 else:subprocess.run(['gh','release','upload',TAG,str(path),'--repo',REPO],check=True)
 current=api('releases/'+str(release['id']));asset=next(a for a in current['assets'] if a['name']==path.name);assert asset.get('digest')=='sha256:'+sha(path)
 url='https://github.com/'+REPO+'/releases/download/'+TAG+'/'+path.name
 for attempt in range(3):
  try:public(url,path.stat().st_size,sha(path));break
  except Exception:
   if attempt==2:raise
   time.sleep(2)
 print(json.dumps({'publicDownloadVerified':path.name,'size':path.stat().st_size,'sha256':sha(path)}),flush=True)
assert all(public(url)==before for url,before in feeds_before.items()),'An updater feed changed'
print(json.dumps({'documentationPublished':True,'allPublicDownloadsVerified':True,'appUpdateFeedsUnchanged':True,'release':release['html_url']}),flush=True)
