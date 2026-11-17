from pathlib import Path
import hashlib,json,zipfile,subprocess
root=Path(__file__).resolve().parent/'standalone'
out=Path('/tmp/clock-downloads');out.mkdir(exist_ok=True)
files=json.loads((root/'manifest.json').read_text())
for item in files:
 p=out/item['name']
 with p.open('wb') as f:
  for part in item['parts']:
   b=(root/part['name']).read_bytes()
   assert len(b)==part['size'] and hashlib.sha256(b).hexdigest()==part['sha256']
   f.write(b)
 assert p.stat().st_size==item['size'] and hashlib.file_digest(p.open('rb'),'sha256').hexdigest()==item['sha256']
 with zipfile.ZipFile(p) as z:assert z.testzip() is None
checks=out/'SHA256SUMS.txt';checks.write_text(''.join(i['sha256']+'  '+i['name']+'\n' for i in files))
subprocess.run(['gh','release','create','time-clock-0.1.0',*[str(out/i['name']) for i in files],str(checks),'--repo','zelmore219-lang/backwoods-brew-releases','--title','Backwoods Time Clock 0.1.0','--notes-file',str(root/'NOTES.md'),'--latest=false'],check=True)
