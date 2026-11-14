import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
m=json.loads((root/'manifest.json').read_text())
assert (m['version'],m['sourceSha'],m['windowsAcceptanceRun'],m['size'],m['sha256'])==('0.4.6', 'f00c69b810f864e9d799fe955de76164d9518c2b', 43635778527, 172638312, 'aa10ef7455e59c84264add88f1ec42c7d7780c483b98ade15c7f30ac7d88ee5a')
assert m['filename']=='Backwoods-Employees-Setup-0.4.6.exe'
unit=json.loads((root/'accepted-build.json').read_text())['windowsUnit']
assert unit=={'id': 43635778527, 'sourceSha': 'f00c69b810f864e9d799fe955de76164d9518c2b', 'status': 'completed', 'conclusion': 'success', 'pythonTests': 135, 'pythonSkipped': 24, 'nodePassed': 16}
output=Path('/tmp')/m['filename']
with output.open('wb') as stream:
 for index,part in enumerate(m['parts']):
  assert part['name']=='installer.part'+str(index).zfill(3)
  raw=(root/part['name']).read_bytes()
  assert len(raw)==part['size'] and hashlib.sha256(raw).hexdigest()==part['sha256']
  stream.write(raw)
assert output.stat().st_size==m['size']
with output.open('rb') as stream:assert hashlib.file_digest(stream,'sha256').hexdigest()==m['sha256']
print('Reconstructed exact accepted Employee 0.4.6 Windows installer: unit, upgrade, report-route, encryption and reinstall checks passed.')
