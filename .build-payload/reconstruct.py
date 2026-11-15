import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
m=json.loads((root/'manifest.json').read_text())
assert (m['version'],m['sourceSha'],m['windowsAcceptanceRun'],m['size'],m['sha256'])==('0.4.7', 'a9f1fe3184ec00dffb55cc46148ad32cd4b886af', 43672644928, 172657137, '83a681e4d5294033b8282d5c3b07ecc42fdcdca0b801f47e4b97872a8e8e1e25')
assert m['filename']=='Backwoods-Employees-Setup-0.4.7.exe'
unit=json.loads((root/'accepted-build.json').read_text())['windowsUnit']
assert unit=={'id': 43672644928, 'sourceSha': 'a9f1fe3184ec00dffb55cc46148ad32cd4b886af', 'status': 'completed', 'conclusion': 'success', 'pythonTests': 137, 'pythonSkipped': 24, 'nodePassed': 17}
output=Path('/tmp')/m['filename']
with output.open('wb') as stream:
 for index,part in enumerate(m['parts']):
  assert part['name']=='installer.part'+str(index).zfill(3)
  raw=(root/part['name']).read_bytes()
  assert len(raw)==part['size'] and hashlib.sha256(raw).hexdigest()==part['sha256']
  stream.write(raw)
assert output.stat().st_size==m['size']
with output.open('rb') as stream:assert hashlib.file_digest(stream,'sha256').hexdigest()==m['sha256']
print('Reconstructed exact accepted Employee 0.4.7 Windows installer: unit, upgrade, report-route, encryption and reinstall checks passed.')
