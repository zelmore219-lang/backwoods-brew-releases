"""Publish the verified installer first, then update only the Driver feed."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import urllib.request
from assemble_driver import ROOT,assemble

REPO='zelmore219-lang/backwoods-brew-releases'
FEED_TAG='driver-updates'
FEED_NAME='backwoods-driver-updates.json'
PREFIX=f'https://github.com/{REPO}/releases/download/'


def api(path,method='GET',payload=None):
    arguments=['gh','api','--method',method,'-H','Cache-Control: no-cache',f'repos/{REPO}/{path}']
    if payload is not None:arguments+=['--input','-']
    return json.loads(subprocess.check_output(arguments,input=json.dumps(payload) if payload is not None else None,text=True))


def release(tag):
    result=subprocess.run(['gh','api',f'repos/{REPO}/releases/tags/{tag}'],capture_output=True,text=True)
    if result.returncode:
        # GitHub's tag endpoint can hide a draft until the tag is published.
        # Authenticated release listing includes our existing draft by ID.
        if '404' in result.stderr:
            existing=next((item for item in api('releases?per_page=100') if item['tag_name']==tag),None)
            if existing:return existing
            lookup=subprocess.run(['gh','release','view',tag,'--repo',REPO,'--json','apiUrl'],capture_output=True,text=True)
            if lookup.returncode==0:
                url=json.loads(lookup.stdout)['apiUrl'];prefix=f'https://api.github.com/repos/{REPO}/releases/'
                if not url.startswith(prefix) or not url[len(prefix):].isdigit():raise ValueError('Invalid draft release API identity')
                return api('releases/'+url[len(prefix):])
            return None
        raise RuntimeError('Cannot read the Driver release channel: '+result.stderr)
    return json.loads(result.stdout)


def gh(*args):
    subprocess.run(['gh',*args,'--repo',REPO],check=True)


def checksum(path):return hashlib.file_digest(path.open('rb'),'sha256').hexdigest()


def public_bytes(url,expected_size=None,expected_hash=None):
    request=urllib.request.Request(url,headers={'User-Agent':'Backwoods-Driver-Updater','Cache-Control':'no-cache'})
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


def verify_public_feed(url,expected):
    # GitHub's download edge can briefly serve the previous asset after an
    # atomic publisher upload, even with no-cache. Never accept different data.
    for attempt in range(8):
        if json.loads(public_bytes(url))==expected:return
        if attempt<7:time.sleep(5)
    raise ValueError('Published Driver feed could not be verified')


def publish():
    metadata,installer=assemble()
    android,apk=assemble('android') if (ROOT/'driver-updates/android-package.json').exists() else (None,None)
    version=metadata['version']
    if not re.fullmatch(r'\d+\.\d+\.\d+',version):raise ValueError('Invalid release version')
    if android and (android['version']!=version or android.get('packageName')!='com.backwoodsbrew.driver.next' or not isinstance(android.get('versionCode'),int) or android['versionCode']<1 or not re.fullmatch('[a-f0-9]{64}',android.get('certificateSha256',''))):raise ValueError('Invalid Android release identity')
    tag='driver-'+version
    current=release(tag)
    if not current:
        # Retain the creation response's numeric identity. A new draft is not
        # immediately visible through GitHub's tag/list endpoints.
        current=api('releases','POST',{'tag_name':tag,'target_commitish':os.environ['GITHUB_SHA'],'draft':True,'make_latest':'false','name':'Backwoods Driver '+version,'body':(ROOT/'DRIVER-RELEASE-NOTES.md').read_text()})
    release_id=current['id']
    packages=[(metadata,installer)]+([(android,apk)] if android else [])
    for details,file in packages:
        existing=asset(current,file.name)
        if existing:
            if existing.get('digest')!='sha256:'+details['sha256'] or existing['size']!=details['size']:
                raise ValueError('This version already contains different bytes. Use a new version.')
        else:
            if not current['draft']:raise ValueError('An already published version cannot gain replacement packages')
            gh('release','upload',tag,str(file))
        candidate=asset(api('releases/'+str(release_id)),file.name)
        if candidate.get('digest')!='sha256:'+details['sha256'] or candidate['size']!=details['size']:
            raise ValueError('Uploaded package checksum mismatch')
    if not asset(api('releases/'+str(release_id)),'SHA256SUMS.txt'):gh('release','upload',tag,str(installer.parent/'SHA256SUMS.txt'))
    if current['draft']:api('releases/'+str(release_id),'PATCH',{'draft':False,'make_latest':'false'})
    info={'version':version,'url':PREFIX+tag+'/'+installer.name,'sha256':metadata['sha256'],'size':metadata['size']}
    public_bytes(info['url'],info['size'],info['sha256'])
    android_info={key:android[key] for key in ['version','versionCode','packageName','certificateSha256','size','sha256','firstInstallOnly']} if android else None
    if android_info:
        android_info['url']=PREFIX+tag+'/'+apk.name
        android_info['minSdk']=android.get('minSdk',26)
        android_info['abis']=android.get('abis',['arm64-v8a','x86_64'])
        public_bytes(android_info['url'],android_info['size'],android_info['sha256'])
    channel=release(FEED_TAG)
    if not channel:
        channel=api('releases','POST',{'tag_name':FEED_TAG,'target_commitish':os.environ['GITHUB_SHA'],'draft':False,'make_latest':'false','name':'Backwoods Driver app update channel','body':'Verified Driver update feed. Install the bootstrap Windows update once, then use App updates in the Driver program.'})
    if channel['draft']:raise ValueError('The Driver feed channel must be publicly readable')
    before=asset(channel,FEED_NAME)
    old=None;previous=None
    if before:
        old=public_bytes(PREFIX+FEED_TAG+'/'+FEED_NAME)
        if hashlib.sha256(old).hexdigest()!=before.get('digest','').removeprefix('sha256:'):
            raise ValueError('The existing Driver feed changed. Retry after the current publisher completes.')
        previous=json.loads(old)
        prior=previous.get('apps',{}).get('driver',{}).get('windows',{})
        prior_version=prior.get('version','0.0.0')
        if not re.fullmatch(r'\d+\.\d+\.\d+',prior_version):raise ValueError('Invalid previous Driver version')
        if tuple(map(int,prior_version.split('.')))>tuple(map(int,version.split('.'))):raise ValueError('Refusing to downgrade the Driver feed')
        if prior_version==version and prior.get('sha256')!=info['sha256']:raise ValueError('An existing Driver version cannot be replaced')
    feed=previous or {'schemaVersion':1,'apps':{'driver':{}}}
    if feed.get('schemaVersion')!=1 or set(feed.get('apps',{}))!={'driver'}:
        raise ValueError('This publisher only supports the separate Driver feed')
    feed['apps']['driver']['windows']=info
    if android_info:
        old_android=feed['apps']['driver'].get('android',{})
        if old_android:
            if old_android.get('packageName')!=android_info['packageName'] or old_android.get('certificateSha256')!=android_info['certificateSha256']:raise ValueError('The Android signing identity cannot be replaced')
            if old_android.get('versionCode',0)>android_info['versionCode']:raise ValueError('Refusing to downgrade the Android feed')
            if old_android.get('versionCode')==android_info['versionCode'] and old_android.get('sha256')!=android_info['sha256']:raise ValueError('An existing Android version cannot be replaced')
        feed['apps']['driver']['android']=android_info
    feed['apps']['driver']['notes']=metadata.get('notes','Verified Driver update; preserves saved Driver deliveries, signatures and settings.')
    payload=ROOT/'output'/FEED_NAME;payload.write_text(json.dumps(feed,indent=2)+'\n')
    fresh=asset(api('releases/'+str(channel['id'])),FEED_NAME)
    if (before and (not fresh or fresh['id']!=before['id'] or fresh.get('digest')!=before.get('digest'))) or (not before and fresh):
        raise ValueError('The Driver feed changed while packages uploaded. Refusing to overwrite it.')
    try:
        gh('release','upload',FEED_TAG,str(payload),*(['--clobber'] if before else []))
    except Exception:
        latest=asset(api('releases/'+str(channel['id'])),FEED_NAME)
        if latest and latest.get('digest')=='sha256:'+checksum(payload):pass
        elif not latest and old is not None:
            rollback=ROOT/'output/rollback'/FEED_NAME;rollback.parent.mkdir(exist_ok=True);rollback.write_bytes(old)
            gh('release','upload',FEED_TAG,str(rollback));raise
        else:raise
    verify_public_feed(PREFIX+FEED_TAG+'/'+FEED_NAME,feed)
    print(json.dumps({'published':True,'windowsVersion':version,'androidVersion':android_info['version'] if android_info else None,'installerDownloadVerified':True,
        'feed':PREFIX+FEED_TAG+'/'+FEED_NAME,'release':f'https://github.com/{REPO}/releases/tag/{tag}',
        'otherAppsChanged':False},indent=2))


if __name__=='__main__':publish()
