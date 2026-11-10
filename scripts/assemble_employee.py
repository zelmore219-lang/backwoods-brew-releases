"""Reassemble a checksum-locked, data-free Employee installer for release."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def assemble():
    manifest=json.loads((ROOT/'employee-updates/package.json').read_text())
    if manifest['app']!='employees' or manifest['platform']!='windows':
        raise ValueError('Only an Employee Windows package is supported')
    name=manifest['name']
    if Path(name).name!=name or not name.endswith('.exe'):
        raise ValueError('Invalid installer filename')
    output=ROOT/'output';output.mkdir(exist_ok=True)
    target=output/name
    with target.open('wb') as result:
        for info in manifest['parts']:
            part=(ROOT/info['path']).resolve()
            if not part.is_relative_to((ROOT/'employee-updates').resolve()):
                raise ValueError('Invalid package part path')
            raw=part.read_bytes()
            if len(raw)!=info['size'] or hashlib.sha256(raw).hexdigest()!=info['sha256']:
                raise ValueError('Installer part checksum mismatch')
            result.write(raw)
    if target.stat().st_size!=manifest['size'] or hashlib.file_digest(target.open('rb'),'sha256').hexdigest()!=manifest['sha256']:
        raise ValueError('Reconstructed installer checksum mismatch')
    if target.open('rb').read(2)!=b'MZ':raise ValueError('Installer is not a Windows executable')
    (output/'SHA256SUMS.txt').write_text(manifest['sha256']+'  '+name+'\n')
    print(json.dumps({'verified':True,'installer':str(target),'sha256':manifest['sha256']}))
    return manifest,target


if __name__=='__main__':assemble()
