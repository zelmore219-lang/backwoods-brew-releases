"""Reassemble a checksum-locked, data-free Employee installer for release."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def assemble(platform='windows'):
    if platform not in {'windows','android'}:raise ValueError('Unsupported Employee platform')
    manifest_path=ROOT/'employee-updates'/('package.json' if platform=='windows' else 'android-package.json')
    manifest=json.loads(manifest_path.read_text())
    if manifest['app']!='employees' or manifest['platform']!=platform:
        raise ValueError('The Employee package belongs to another application or platform')
    name=manifest['name']
    if Path(name).name!=name or '\\' in name or not name.endswith('.exe' if platform=='windows' else '.apk'):
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
    if target.open('rb').read(2)!=(b'MZ' if platform=='windows' else b'PK'):raise ValueError('The Employee package has an invalid file signature')
    with (output/'SHA256SUMS.txt').open('w' if platform=='windows' else 'a') as sums:sums.write(manifest['sha256']+'  '+name+'\n')
    print(json.dumps({'verified':True,'installer':str(target),'sha256':manifest['sha256']}))
    return manifest,target


if __name__=='__main__':
    assemble()
    if (ROOT/'employee-updates/android-package.json').exists():assemble('android')
