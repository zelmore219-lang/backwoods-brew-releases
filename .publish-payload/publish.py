"""Publish checksum-pinned, natively accepted Windows packages and then their feeds.

Private source evidence is captured by the authorized source owner. The public
repository's workflow token can only access the destination repository.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent
REPO = 'zelmore219-lang/backwoods-brew-releases'
BASE = 'https://github.com/' + REPO + '/releases/download/'


def api(path, method='GET', payload=None):
    command = ['gh', 'api', '--method', method, 'repos/' + REPO + '/' + path]
    if payload is not None:
        command += ['--input', '-']
    result = subprocess.check_output(command, input=json.dumps(payload) if payload is not None else None, text=True)
    return json.loads(result) if result.strip() else None


def digest(file):
    with file.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read_public(url):
    with urllib.request.urlopen(url, timeout=90) as response:
        return response.read()


def verify_public(url, expected):
    for attempt in range(7):
        try:
            result = hashlib.sha256()
            size = 0
            with urllib.request.urlopen(url, timeout=120) as response:
                while chunk := response.read(1024 * 1024):
                    result.update(chunk)
                    size += len(chunk)
            if (result.hexdigest(), size) != expected:
                raise ValueError('Public package bytes differ from the accepted artifact')
            return
        except Exception:
            if attempt == 6:
                raise
            time.sleep(min(2 ** attempt, 30))


def upload(release, files):
    current = api('releases/' + str(release['id']))
    if not current['draft']:
        raise ValueError('Only an unpublished draft can receive package uploads')
    token = os.environ['GH_TOKEN']
    for file in files:
        expected = digest(file)
        existing = next((a for a in current['assets'] if a['name'] == file.name), None)
        if existing:
            if existing.get('digest') == 'sha256:' + expected and existing['size'] == file.stat().st_size:
                continue
            api('releases/assets/' + str(existing['id']), 'DELETE')
        url = 'https://uploads.github.com/repos/' + REPO + '/releases/' + str(current['id']) + '/assets?' + urllib.parse.urlencode({'name': file.name})
        with file.open('rb') as stream:
            request = urllib.request.Request(url, data=stream, method='POST', headers={
                'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json',
                'Content-Type': 'application/octet-stream', 'Content-Length': str(file.stat().st_size),
                'User-Agent': 'Backwoods-verified-Windows-release'})
            with urllib.request.urlopen(request, timeout=300) as response:
                asset = json.load(response)
        if asset.get('digest') != 'sha256:' + expected or asset['size'] != file.stat().st_size:
            raise ValueError('Upload did not preserve the accepted artifact')


def version(text):
    import re
    if not re.fullmatch(r'\d+\.\d+\.\d+', text):
        raise ValueError('Stable three-part version required')
    return tuple(map(int, text.split('.')))


def reconstruct(folder, manifest):
    files = []
    for item in manifest['files']:
        target = Path('/tmp') / item['name']
        if target.name != item['name'] or target.suffix != '.exe':
            raise ValueError('Invalid package filename')
        with target.open('wb') as stream:
            for index, part in enumerate(item['parts']):
                if part['name'] != item['name'] + '.part' + str(index).zfill(3):
                    raise ValueError('Unexpected chunk order')
                raw = (folder / part['name']).read_bytes()
                if len(raw) != part['size'] or hashlib.sha256(raw).hexdigest() != part['sha256']:
                    raise ValueError('Payload chunk checksum mismatch')
                stream.write(raw)
        if target.stat().st_size != item['size'] or digest(target) != item['sha256']:
            raise ValueError('Reconstructed package checksum mismatch')
        with target.open('rb') as stream:
            if stream.read(2) != b'MZ':
                raise ValueError('Not a Windows executable')
        files.append(target)
    return files


def publish(app, check_only=False):
    folder = ROOT / app
    manifest = json.loads((folder / 'manifest.json').read_text())
    evidence = json.loads((folder / 'accepted-build.json').read_text())
    run = evidence['run']
    if run['head_sha'] != manifest['sourceSha'] or run['id'] != manifest['acceptanceRun'] or run['status'] != 'completed' or run['conclusion'] != 'success':
        raise ValueError('The exact source workflow must pass before publication')
    windows = next((j for j in evidence['jobs']['jobs'] if j['name'] == 'windows'), None)
    if not windows or windows['status'] != 'completed' or windows['conclusion'] != 'success':
        raise ValueError('Actual Windows install/reinstall acceptance is required')
    if any(s['conclusion'] not in ('success', 'skipped') for s in windows.get('steps', [])):
        raise ValueError('A native acceptance step did not pass')
    private = evidence['release']
    prefix = 'pest-ci-' if app == 'pest' else 'employee-ci-'
    if private['tag_name'] != prefix + manifest['sourceSha'] or not private['draft']:
        raise ValueError('Use the privately staged exact build')
    for file in manifest['files']:
        asset = next((a for a in private['assets'] if a['name'] == file['name']), None)
        if not asset or asset.get('digest') != 'sha256:' + file['sha256'] or asset['size'] != file['size']:
            raise ValueError('Package must match accepted private release bytes')
    if app == 'pest':
        proof = evidence['nativeProof']
        if proof['sourceSha'] != manifest['sourceSha'] or proof['run'] != run['id'] or proof['windowsInstallReinstallPassed'] is not True or proof['version'] != manifest['version']:
            raise ValueError('Pest native proof does not match this exact build')
        if proof['files'] != [{k: f[k] for k in ('name', 'size', 'sha256')} for f in manifest['files']]:
            raise ValueError('Pest native proof package checksums differ')
    files = reconstruct(folder, manifest)
    setup = next(f for f in manifest['files'] if f['name'] == manifest['installer'])
    releases = api('releases?per_page=100')
    release = next(r for r in releases if r['tag_name'] == manifest['tag'])
    feed_release = next(r for r in releases if r['tag_name'] == manifest['feedTag'])
    feed_asset = next((a for a in feed_release['assets'] if a['name'] == manifest['feedName']), None)
    feed_url = BASE + manifest['feedTag'] + '/' + manifest['feedName']
    if feed_asset:
        original_bytes = read_public(feed_url)
        if feed_asset.get('digest') != 'sha256:' + hashlib.sha256(original_bytes).hexdigest():
            raise ValueError('Public feed is stale relative to its authoritative asset')
        original = json.loads(original_bytes)
    else:
        if not feed_release['draft'] or app != 'pest':
            raise ValueError('Refusing to invent or replace a missing existing feed')
        original = {'schemaVersion': 1, 'apps': {}}
    replacement = copy.deepcopy(original)
    entry = replacement['apps'].setdefault(app, {})
    expected = {'version': manifest['version'], 'url': BASE + manifest['tag'] + '/' + setup['name'], 'sha256': setup['sha256'], 'size': setup['size']}
    previous = entry.get('windows')
    if previous:
        if version(previous['version']) > version(manifest['version']):
            raise ValueError('Refusing to downgrade an update feed')
        if previous['version'] == manifest['version'] and any(previous.get(k) != v for k, v in expected.items()):
            raise ValueError('A published version is immutable')
    entry['windows'] = {**(previous or {}), **expected}
    entry['notes'] = manifest['notes']
    if app == 'employees' and entry.get('android') != original['apps']['employees'].get('android'):
        raise ValueError('Employee Android entry must be retained exactly')
    if check_only:
        print(json.dumps({'app': app, 'version': manifest['version'], 'source': manifest['sourceSha'], 'run': run['id'], 'checkOnly': True, 'feed': replacement}), flush=True)
        return
    with tempfile.TemporaryDirectory() as temp:
        temp = Path(temp)
        checksums = temp / 'SHA256SUMS.txt'
        checksums.write_text(''.join(f['sha256'] + '  ' + f['name'] + '\n' for f in manifest['files']))
        provenance = temp / 'release-source.json'
        provenance.write_text(json.dumps({k: manifest[k] for k in ('sourceRepository', 'sourceSha', 'version', 'acceptanceRun', 'files')}, indent=2) + '\n')
        acceptance = temp / 'accepted-build.json'
        acceptance.write_text(json.dumps(evidence, indent=2) + '\n')
        guide = temp / 'OWNER-GUIDE.md'
        guide.write_bytes((ROOT / 'OWNER-GUIDE.md').read_bytes())
        if release['draft']:
            upload(release, files + [checksums, provenance, acceptance, guide])
            api('releases/' + str(release['id']), 'PATCH', {'draft': False, 'make_latest': 'false'})
        else:
            for f in manifest['files']:
                asset = next(a for a in release['assets'] if a['name'] == f['name'])
                if asset.get('digest') != 'sha256:' + f['sha256'] or asset['size'] != f['size']:
                    raise ValueError('Refusing to replace a published package')
        for f in manifest['files']:
            verify_public(BASE + manifest['tag'] + '/' + f['name'], (f['sha256'], f['size']))
        current = api('releases/' + str(feed_release['id']))
        current_asset = next((a for a in current['assets'] if a['name'] == manifest['feedName']), None)
        if current_asset != feed_asset:
            # Download counts are mutable; compare immutable identity/digest/size.
            if not current_asset or not feed_asset or any(current_asset[k] != feed_asset[k] for k in ('id', 'digest', 'size')):
                raise ValueError('Updater feed changed concurrently; refusing to overwrite it')
        feed = temp / manifest['feedName']
        feed.write_text(json.dumps(replacement, indent=2) + '\n')
        if replacement != original:
            if current['draft']:
                upload(current, [feed])
                api('releases/' + str(current['id']), 'PATCH', {'draft': False, 'make_latest': 'false'})
            else:
                subprocess.run(['gh', 'release', 'upload', manifest['feedTag'], str(feed), '--repo', REPO, '--clobber'], check=True)
        for attempt in range(7):
            try:
                if json.loads(read_public(feed_url)) == replacement:
                    break
            except Exception:
                pass
            if attempt == 6:
                raise RuntimeError('Published feed could not be confirmed')
            time.sleep(min(2 ** attempt, 30))
        print(json.dumps({'app': app, 'version': manifest['version'], 'feed': feed_url, 'source': manifest['sourceSha'], 'run': run['id'], 'publicBytesVerified': True, 'retainedAndroid': app == 'employees'}), flush=True)


if __name__ == '__main__':
    import sys
    if len(sys.argv) not in (2, 3) or sys.argv[1] not in ('pest', 'employees') or (len(sys.argv) == 3 and sys.argv[2] != '--check-only'):
        raise SystemExit('Specify pest or employees [--check-only]')
    publish(sys.argv[1], '--check-only' in sys.argv)
