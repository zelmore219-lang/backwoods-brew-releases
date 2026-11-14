import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
m=json.loads((root/'manifest.json').read_text())
assert (m['version'],m['sourceSha'],m['windowsAcceptanceRun'],m['size'],m['sha256'])==('0.4.4', '8eb347afa633cb88187b703cd04f5a8234c409ff', 43543976858, 172688278, '159089da0780a4ffd54559c60e60b4f29a01000640b1ebf5fd33a0852d7b2a6a')
assert m['filename']=='Backwoods-Employees-Setup-0.4.4.exe'
unit=json.loads((root/'accepted-build.json').read_text())['windowsUnit']
assert unit=={'id': 43545263061, 'sourceSha': '8eb347afa633cb88187b703cd04f5a8234c409ff', 'status': 'completed', 'conclusion': 'success', 'pythonTests': 114, 'pythonSkipped': 18, 'nodePassed': 16}
output=Path('/tmp/Backwoods-Employees-Setup-0.4.4.exe')
with output.open('wb') as stream:
 for index,part in enumerate(m['parts']):
  assert part['name']=='installer.part'+str(index).zfill(3)
  raw=(root/part['name']).read_bytes()
  assert len(raw)==part['size'] and hashlib.sha256(raw).hexdigest()==part['sha256']
  stream.write(raw)
assert output.stat().st_size==m['size'] and hashlib.file_digest(output.open('rb'),'sha256').hexdigest()==m['sha256']
print('Reconstructed the exact Windows installer that passed upgrade, clipboard and reinstall acceptance.')
