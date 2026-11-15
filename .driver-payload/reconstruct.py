import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
m=json.loads((root/'manifest.json').read_text())
expected={'version': '0.5.2', 'filename': 'Backwoods-Driver-Setup-0.5.2.exe', 'sourceSha': '669b72d635ec002fadbe552bacac9599e268ffdc', 'windowsAcceptanceRun': 43675679450, 'sha256': '626606fe4e115c99455387c52d3a24887af61e9bc8b37974c02a06517fc01293', 'size': 115341669}
assert {key:m[key] for key in expected}==expected
output=Path('/tmp')/m['filename']
with output.open('wb') as stream:
 for index,part in enumerate(m['parts']):
  assert part['name']=='installer.part'+str(index).zfill(3)
  raw=(root/part['name']).read_bytes()
  assert len(raw)==part['size'] and hashlib.sha256(raw).hexdigest()==part['sha256']
  stream.write(raw)
assert output.stat().st_size==m['size'] and hashlib.file_digest(output.open('rb'),'sha256').hexdigest()==m['sha256']
print('Verified exact accepted Driver 0.5.2 Windows bytes.')
