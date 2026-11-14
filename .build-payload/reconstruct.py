import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
m=json.loads((root/'manifest.json').read_text())
assert (m['version'],m['sourceSha'],m['windowsAcceptanceRun'],m['size'],m['sha256'])==('0.4.5', 'b15fe1a91c75753d1e17c624cc3f9949ce799951', 43617489601, 172758185, 'cf02f994401b238eb5212ccc654f42ea04c5a7e2eb4af9a9dc7b1b1db53075c1')
assert m['filename']=='Backwoods-Employees-Setup-0.4.5.exe'
unit=json.loads((root/'accepted-build.json').read_text())['windowsUnit']
assert unit=={'id': 43617489601, 'sourceSha': 'b15fe1a91c75753d1e17c624cc3f9949ce799951', 'status': 'completed', 'conclusion': 'success', 'pythonTests': 126, 'pythonSkipped': 20, 'nodePassed': 16}
output=Path('/tmp')/m['filename']
with output.open('wb') as stream:
 for index,part in enumerate(m['parts']):
  assert part['name']=='installer.part'+str(index).zfill(3)
  raw=(root/part['name']).read_bytes()
  assert len(raw)==part['size'] and hashlib.sha256(raw).hexdigest()==part['sha256']
  stream.write(raw)
assert output.stat().st_size==m['size']
with output.open('rb') as stream:assert hashlib.file_digest(stream,'sha256').hexdigest()==m['sha256']
print('Reconstructed exact accepted Employee 0.4.5 Windows installer: unit, upgrade, report-route, encryption and reinstall checks passed.')
