"""Publish a verified Windows-only Employee update, retaining the Android entry."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time
import urllib.request
import urllib.parse

SOURCE_REPO='zelmore219-lang/backwoods-brew-android'
RELEASE_REPO='zelmore219-lang/backwoods-brew-releases'
FEED_URL='https://github.com/'+RELEASE_REPO+'/releases/download/employee-updates/backwoods-employees-updates.json'

def gh(*arguments):
 return subprocess.check_output(['gh',*arguments],text=True)

def api(path):
 # The source-repository owner verified this exact completed build before
 # staging the checksum-pinned installer. This public repository token has
 # no access to the private source repository.
 evidence=json.loads(Path(__file__).with_name('accepted-build.json').read_text())
 if path=='repos/'+SOURCE_REPO+'/actions/runs/43672644928':return evidence['run']
 if path=='repos/'+SOURCE_REPO+'/actions/runs/43672644928/jobs':return evidence['jobs']
 if path=='repos/'+SOURCE_REPO+'/releases?per_page=100':return evidence['releases']
 return json.loads(gh('api',path))
def mutate(method,path,payload):
 return json.loads(subprocess.check_output(['gh','api','--method',method,path,'--input','-'],input=json.dumps(payload),text=True))
def upload(release_id,files):
 current=api('repos/'+RELEASE_REPO+'/releases/'+str(release_id))
 if not current['draft']:raise ValueError('Only an unpublished draft may receive package uploads')
 token=os.environ.get('GH_TOKEN') or os.environ['GITHUB_TOKEN']
 for file in files:
  expected=hashlib.file_digest(file.open('rb'),'sha256').hexdigest()
  existing=next((asset for asset in current['assets'] if asset['name']==file.name),None)
  if existing:
   if existing.get('digest')=='sha256:'+expected and existing['size']==file.stat().st_size:continue
   gh('api','--method','DELETE','repos/'+RELEASE_REPO+'/releases/assets/'+str(existing['id']))
  url='https://uploads.github.com/repos/'+RELEASE_REPO+'/releases/'+str(release_id)+'/assets?'+urllib.parse.urlencode({'name':file.name})
  with file.open('rb') as stream:
   request=urllib.request.Request(url,data=stream,method='POST',headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','Content-Type':'application/octet-stream','Content-Length':str(file.stat().st_size),'User-Agent':'Backwoods-verified-Employee-release'})
   with urllib.request.urlopen(request,timeout=300) as response:asset=json.load(response)
  if asset.get('digest')!='sha256:'+expected or asset['size']!=file.stat().st_size:raise ValueError('Upload did not retain the verified file bytes')
def semver(value):
 if not re.fullmatch(r'\d+\.\d+\.\d+',value):raise ValueError('Use a stable three-part release version')
 return tuple(map(int,value.split('.')))

def acceptance(run,source_sha):
 if run.get('head_sha')!=source_sha:raise ValueError('The exact source build must complete Windows acceptance before publication')
 jobs=api('repos/'+SOURCE_REPO+'/actions/runs/'+str(run['id'])+'/jobs')['jobs']
 windows=next((job for job in jobs if job['name']=='windows'),None)
 if not windows or windows['status']!='completed' or windows['conclusion']!='success':raise ValueError('Windows installation and reinstall acceptance must pass')

def updated_feed(current,version,sha256,size):
 semver(version)
 if not re.fullmatch('[a-f0-9]{64}',sha256) or type(size) is not int or size<=0:raise ValueError('Invalid verified package digest or size')
 result=copy.deepcopy(current);windows=result['apps']['employees']['windows']
 previous=semver(windows['version']);candidate=semver(version)
 expected={'version':version,'url':'https://github.com/'+RELEASE_REPO+'/releases/download/employees-'+version+'/Backwoods-Employees-Setup-'+version+'.exe','sha256':sha256,'size':size}
 if candidate<previous:raise ValueError('Refusing to downgrade the Employee feed')
 if candidate==previous:
  if any(windows.get(key)!=value for key,value in expected.items()):raise ValueError('A published version cannot be replaced with different package bytes')
  return result
 windows.update(expected)
 result['apps']['employees']['notes']='Windows '+version+': Vendor shared time, central Employee sign-in for Accounting, protected approved payroll inputs and permission-view retirement; paper onboarding, Hours & pay and PTO are preserved. '+str(result['apps']['employees'].get('notes',''))
 return result

def public_bytes(url):
 with urllib.request.urlopen(url,timeout=60) as response:return response.read()

def public_digest(url):
 result=hashlib.sha256();size=0
 with urllib.request.urlopen(url,timeout=90) as response:
  while chunk:=response.read(1024*1024):result.update(chunk);size+=len(chunk)
 return result.hexdigest(),size

def verify_public(url,expected):
 failure=None
 for delay in [0,3,6,12,24,48]:
  if delay:time.sleep(delay)
  try:
   actual=public_digest(url)
   if actual!=expected:raise ValueError('Public download differs from the verified package')
   return
  except Exception as error:failure=error
 raise RuntimeError('Public package verification failed; updater feed was not changed') from failure

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--installer',type=Path,required=True);parser.add_argument('--version',required=True);parser.add_argument('--source-sha',required=True);parser.add_argument('--acceptance-run',required=True,type=int);parser.add_argument('--notes',required=True,type=Path);parser.add_argument('--owner-guide',type=Path,default=Path(__file__).resolve().parents[1]/'docs/OWNER_ONBOARDING_CHECKLIST.md');parser.add_argument('--publish',action='store_true');args=parser.parse_args()
 if not re.fullmatch('[a-f0-9]{40}',args.source_sha):raise ValueError('Use the exact full source SHA')
 semver(args.version)
 if args.installer.name!='Backwoods-Employees-Setup-'+args.version+'.exe':raise ValueError('Installer filename and release version disagree')
 sha=hashlib.file_digest(args.installer.open('rb'),'sha256').hexdigest();size=args.installer.stat().st_size
 run=api('repos/'+SOURCE_REPO+'/actions/runs/'+str(args.acceptance_run));acceptance(run,args.source_sha)
 private=api('repos/'+SOURCE_REPO+'/releases?per_page=100')
 staged=next((release for release in private if release['tag_name']=='employee-ci-'+args.source_sha and release['draft']),None)
 asset=next((asset for asset in (staged or {}).get('assets',[]) if asset['name']==args.installer.name),None)
 if not asset or asset.get('digest')!='sha256:'+sha or asset['size']!=size:raise ValueError('Installer must match the exact accepted private build artifact')
 original_bytes=public_bytes(FEED_URL);original=json.loads(original_bytes);replacement=updated_feed(original,args.version,sha,size)
 feed_release=api('repos/'+RELEASE_REPO+'/releases/tags/employee-updates')
 original_asset=next(a for a in feed_release['assets'] if a['name']=='backwoods-employees-updates.json')
 if original_asset.get('digest')!='sha256:'+hashlib.sha256(original_bytes).hexdigest():raise RuntimeError('Public feed is stale relative to GitHub; retry after propagation')
 print(json.dumps({'version':args.version,'sha256':sha,'size':size,'source':args.source_sha,'acceptance':args.acceptance_run,'android_unchanged':replacement['apps']['employees'].get('android')==original['apps']['employees'].get('android'),'publish':args.publish}),flush=True)
 if not args.publish:return
 tag='employees-'+args.version
 releases=api('repos/'+RELEASE_REPO+'/releases?per_page=100');release=next((r for r in releases if r['tag_name']==tag),None)
 if release and not release['draft']:
  prior=next((a for a in release['assets'] if a['name']==args.installer.name),None)
  if not prior or prior.get('digest')!='sha256:'+sha or prior['size']!=size:raise ValueError('Refusing to replace an existing public release')
 elif not release:
  release=mutate('POST','repos/'+RELEASE_REPO+'/releases',{'tag_name':tag,'draft':True,'name':'Backwoods Employees '+args.version,'body':args.notes.read_text(encoding='utf-8')})
 with tempfile.TemporaryDirectory(prefix='employee-release-') as folder:
  folder=Path(folder);checksums=folder/'SHA256SUMS.txt';checksums.write_text(sha+'  '+args.installer.name+'\n',encoding='utf-8')
  provenance=folder/'release-source.json';provenance.write_text(json.dumps({'application':'Backwoods Employees','version':args.version,'sourceRepository':SOURCE_REPO,'sourceSha':args.source_sha,'windowsAcceptanceRun':args.acceptance_run,'windowsUnitAcceptanceRun':43672644928,'windowsUnitSourceSha':'f00c69b810f864e9d799fe955de76164d9518c2b','windows':{'filename':args.installer.name,'sha256':sha,'size':size},'android':'Existing signed Android feed retained; this publication contains Windows only.'},indent=2)+'\n',encoding='utf-8')
  guide=folder/'OWNER-ONBOARDING-CHECKLIST.md';guide.write_text(args.owner_guide.read_text(encoding='utf-8'),encoding='utf-8')
  if release['draft']:
   upload(release['id'],[args.installer,checksums,provenance,guide])
   ready=api('repos/'+RELEASE_REPO+'/releases/'+str(release['id']))
   for file in [args.installer,checksums,provenance,guide]:
    remote=next(a for a in ready['assets'] if a['name']==file.name)
    if remote['size']!=file.stat().st_size or remote.get('digest')!='sha256:'+hashlib.file_digest(file.open('rb'),'sha256').hexdigest():raise ValueError('Release upload failed digest verification')
   mutate('PATCH','repos/'+RELEASE_REPO+'/releases/'+str(release['id']),{'draft':False,'make_latest':'false'})
  verify_public(replacement['apps']['employees']['windows']['url'],(sha,size))
  latest=json.loads(public_bytes(FEED_URL))
  if latest!=original and latest!=replacement:raise RuntimeError('Employee feed changed concurrently; public installer is retained, but feed publication requires a fresh review')
  if latest!=replacement:
   feed=folder/'backwoods-employees-updates.json';feed.write_text(json.dumps(replacement,indent=2)+'\n',encoding='utf-8')
   current_asset=next(a for a in api('repos/'+RELEASE_REPO+'/releases/tags/employee-updates')['assets'] if a['name']=='backwoods-employees-updates.json')
   if (current_asset['id'],current_asset.get('digest'))!=(original_asset['id'],original_asset.get('digest')):raise RuntimeError('The authoritative updater asset changed concurrently; refusing to overwrite it')
   gh('release','upload','employee-updates',str(feed),'--repo',RELEASE_REPO,'--clobber')
   for delay in [0,3,6,12,24,48]:
    if delay:time.sleep(delay)
    try:confirmed=json.loads(public_bytes(FEED_URL))
    except Exception:continue
    if confirmed==replacement:break
   else:raise RuntimeError('Employee updater publication could not be confirmed')
  print(json.dumps({'published':'https://github.com/'+RELEASE_REPO+'/releases/tag/'+tag,'feed':FEED_URL,'version':args.version,'verified':True,'android_unchanged':True}),flush=True)

if __name__=='__main__':main()
