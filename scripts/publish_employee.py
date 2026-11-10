"""Publish the verified installer first, then update only the Employee feed."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.request
from assemble_employee import ROOT,assemble

REPO='zelmore219-lang/backwoods-brew-releases'
FEED_TAG='employee-updates'
FEED_NAME='backwoods-employees-updates.json'
PREFIX=f'https://github.com/{REPO}/releases/download/'


def api(path):
    return json.loads(subprocess.check_output(['gh','api',f'repos/{REPO}/{path}'],text=True))


def release(tag):
    result=subprocess.run(['gh','api',f'repos/{REPO}/releases/tags/{tag}'],capture_output=True,text=True)
    if result.returncode:
        # GitHub's tag endpoint can hide a draft until the tag is published.
        # Authenticated release listing includes our existing draft by ID.
        if '404' in result.stderr:
            return next((item for item in api('releases?per_page=100') if item['tag_name']==tag),None)
        raise RuntimeError('Cannot read the Employee release channel: '+result.stderr)
    return json.loads(result.stdout)


def gh(*args):
    subprocess.run(['gh',*args,'--repo',REPO],check=True)


def checksum(path):return hashlib.file_digest(path.open('rb'),'sha256').hexdigest()


def public_bytes(url,expected_size=None,expected_hash=None):
    request=urllib.request.Request(url,headers={'User-Agent':'Backwoods-Employee-Updater','Cache-Control':'no-cache'})
    digest=hashlib.sha256();size=0;small=bytearray()
    with urllib.request.urlopen(request,timeout=120) as response:
        while block:=response.read(1024*1024):
            size+=len(block)
            if expected_size is not None and size>expected_size:raise ValueError('Public download exceeds declared size')
            digest.update(block)
            if expected_size is None:
                if size>1024*1024:raise ValueError('Feed is too large')
                small.extend(block)
    if expected_size is not None and (size!=expected_size or digest.hexdigest()!=expected_hash):
        raise ValueError('Public installer failed size/checksum verification')
    return bytes(small)


def asset(channel,name):return next((a for a in channel['assets'] if a['name']==name),None)


def publish():
    metadata,installer=assemble()
    version=metadata['version']
    if not re.fullmatch(r'\d+\.\d+\.\d+',version):raise ValueError('Invalid release version')
    tag='employees-'+version
    current=release(tag)
    if not current:
        gh('release','create',tag,'--target',os.environ['GITHUB_SHA'],'--draft','--latest=false',
           '--title','Backwoods Employees '+version+' — Windows updater','--notes-file',str(ROOT/'EMPLOYEE-RELEASE-NOTES.md'))
        current=release(tag)
    existing=asset(current,installer.name)
    if existing:
        if existing.get('digest')!='sha256:'+metadata['sha256'] or existing['size']!=metadata['size']:
            raise ValueError('This version already contains different bytes. Use a new version.')
    else:
        if not current['draft']:raise ValueError('An already published version cannot gain replacement packages')
        gh('release','upload',tag,str(installer),str(installer.parent/'SHA256SUMS.txt'))
    candidate=asset(release(tag),installer.name)
    if candidate.get('digest')!='sha256:'+metadata['sha256'] or candidate['size']!=metadata['size']:
        raise ValueError('Uploaded installer checksum mismatch')
    if current['draft']:gh('release','edit',tag,'--draft=false','--latest=false')
    info={'version':version,'url':PREFIX+tag+'/'+installer.name,'sha256':metadata['sha256'],'size':metadata['size']}
    public_bytes(info['url'],info['size'],info['sha256'])
    channel=release(FEED_TAG)
    if not channel:
        gh('release','create',FEED_TAG,'--target',os.environ['GITHUB_SHA'],'--latest=false',
           '--title','Backwoods Employee app update channel','--notes','Verified Employee update feed. Install the bootstrap Windows update once, then use App updates in the Employee program.')
        channel=release(FEED_TAG)
    if channel['draft']:raise ValueError('The Employee feed channel must be publicly readable')
    before=asset(channel,FEED_NAME)
    old=None;previous=None
    if before:
        old=public_bytes(PREFIX+FEED_TAG+'/'+FEED_NAME)
        if hashlib.sha256(old).hexdigest()!=before.get('digest','').removeprefix('sha256:'):
            raise ValueError('The existing Employee feed changed. Retry after the current publisher completes.')
        previous=json.loads(old)
        prior=previous.get('apps',{}).get('employees',{}).get('windows',{})
        prior_version=prior.get('version','0.0.0')
        if not re.fullmatch(r'\d+\.\d+\.\d+',prior_version):raise ValueError('Invalid previous Employee version')
        if tuple(map(int,prior_version.split('.')))>tuple(map(int,version.split('.'))):raise ValueError('Refusing to downgrade the Employee feed')
        if prior_version==version and prior.get('sha256')!=info['sha256']:raise ValueError('An existing Employee version cannot be replaced')
    feed=previous or {'schemaVersion':1,'apps':{'employees':{}}}
    if feed.get('schemaVersion')!=1 or set(feed.get('apps',{}))!={'employees'}:
        raise ValueError('This publisher only supports the separate Employee feed')
    feed['apps']['employees']['windows']=info
    feed['apps']['employees']['notes']='Adds automatic update checks, optional automatic downloads, and verified installation from the Employee app. Keeps the existing Windows records and document key. Central HR repairs are separate work.'
    payload=ROOT/'output'/FEED_NAME;payload.write_text(json.dumps(feed,indent=2)+'\n')
    fresh=asset(release(FEED_TAG),FEED_NAME)
    if (before and (not fresh or fresh['id']!=before['id'] or fresh.get('digest')!=before.get('digest'))) or (not before and fresh):
        raise ValueError('The Employee feed changed while packages uploaded. Refusing to overwrite it.')
    try:
        gh('release','upload',FEED_TAG,str(payload),*(['--clobber'] if before else []))
    except Exception:
        latest=asset(release(FEED_TAG),FEED_NAME)
        if latest and latest.get('digest')=='sha256:'+checksum(payload):pass
        elif not latest and old is not None:
            rollback=ROOT/'output/rollback'/FEED_NAME;rollback.parent.mkdir(exist_ok=True);rollback.write_bytes(old)
            gh('release','upload',FEED_TAG,str(rollback));raise
        else:raise
    final=public_bytes(PREFIX+FEED_TAG+'/'+FEED_NAME)
    if json.loads(final)!=feed:raise ValueError('Published Employee feed could not be verified')
    print(json.dumps({'published':True,'windowsVersion':version,'installerDownloadVerified':True,
        'feed':PREFIX+FEED_TAG+'/'+FEED_NAME,'release':f'https://github.com/{REPO}/releases/tag/{tag}',
        'otherAppsChanged':False},indent=2))


if __name__=='__main__':publish()
