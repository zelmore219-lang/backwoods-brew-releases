"""Publish verified documentation assets without changing apps or update feeds."""
from pathlib import Path
import hashlib,json,subprocess,urllib.request,time,zipfile
ROOT=Path(__file__).resolve().parents[1];REPO='zelmore219-lang/backwoods-brew-releases';TAG='driver-0.5.1'
manifest=json.loads((ROOT/'documentation-downloads/driver-0.5.1/manifest.json').read_text())
assert manifest['app']=='driver' and manifest['version']=='0.5.1' and manifest['tag']==TAG
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
release=api('releases/tags/'+TAG);assert not release['draft']
baseline={a['name']:(a['id'],a.get('digest'),a['size']) for a in release['assets'] if a['name'] in {'Backwoods-Driver-0.5.1.apk','Backwoods-Driver-Setup-0.5.1.exe','SHA256SUMS.txt'}}
assert len(baseline)==3
feed_url='https://github.com/'+REPO+'/releases/download/driver-updates/backwoods-driver-updates.json';feed_before=public(feed_url)
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
  assert Path(item['name']).name==item['name'] and item['name'].startswith('Backwoods-Driver-0.5.1-')
  source=('Guides/' if item['name'].endswith(('.pdf','.docx')) else 'Verification/')+item['name']
  path=out/item['name'];path.write_bytes(z.read(source));assert path.stat().st_size==item['size'] and sha(path)==item['sha256']
checksum=out/'Backwoods-Driver-0.5.1-Documentation-SHA256SUMS.txt';checksum.write_text(''.join(item['sha256']+'  '+item['name']+'\n' for item in manifest['files']))
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
current=api('releases/'+str(release['id']));after={a['name']:(a['id'],a.get('digest'),a['size']) for a in current['assets'] if a['name'] in baseline}
assert baseline==after,'Application assets changed'
assert public(feed_url)==feed_before,'Driver updater feed changed'
print(json.dumps({'documentationPublished':True,'allPublicDownloadsVerified':True,'applicationAssetsUnchanged':True,'updaterFeedUnchanged':True,'release':release['html_url']}),flush=True)
