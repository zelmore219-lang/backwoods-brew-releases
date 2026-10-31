from pathlib import Path
import sys,subprocess,shutil
project=Path(sys.argv[1]).resolve();name=sys.argv[2];version=sys.argv[3];slug=sys.argv[4]
payload=project/'release/win-unpacked';out=Path('/workspace/outputs/connected-apps-2026-10-31');out.mkdir(parents=True,exist_ok=True)
icon=project/('assets/icon.ico' if name=='Backwoods Brew' else 'public/icons/app.ico')
shutil.copy(icon,payload/'app.ico')
subprocess.run(['node',str(Path(__file__).with_name('embed-windows-icon.cjs')),str(payload/(name+'.exe')),str(icon)],check=True)
exe=out/f'{slug}-{version}-Windows-Setup-Icons.exe';script=project/'release/installer.nsi'
nsisroot=Path('/home/agent/.cache/electron-builder/nsis/nsis-3.0.4.1')
files=sorted(p for p in payload.rglob('*') if p.is_file());dirs=sorted((p for p in payload.rglob('*')if p.is_dir()),key=lambda p:len(p.parts),reverse=True)
def win(path):return str(path).replace('/','\\')
text=f'''Unicode true
!include "MUI2.nsh"
!include "LogicLib.nsh"
Name "{name} {version}"
Icon "{icon}"
UninstallIcon "{icon}"
OutFile "{exe}"
InstallDir "$LOCALAPPDATA\\Programs\\{name}"
InstallDirRegKey HKCU "Software\\BackwoodsBrew\\{slug}" "InstallLocation"
RequestExecutionLevel user
SetCompressor /SOLID lzma
VIProductVersion "{version}.0"
VIAddVersionKey /LANG=1033 "ProductName" "{name}"
VIAddVersionKey /LANG=1033 "FileDescription" "{name} Installer"
VIAddVersionKey /LANG=1033 "FileVersion" "{version}"
VIAddVersionKey /LANG=1033 "LegalCopyright" "Backwoods Brew"
!define MUI_ICON "{icon}"
!define MUI_UNICON "{icon}"
!define MUI_ABORTWARNING
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"
Function .onVerifyInstDir
  GetFileName $0 "$INSTDIR"
  ${{If}} $0 != "{name}"
    Abort
  ${{EndIf}}
FunctionEnd
Section "Install"
  SetShellVarContext current
  SetOutPath "$INSTDIR"
  File /r "{payload}/*"
  WriteUninstaller "$INSTDIR\\Uninstall.exe"
  CreateDirectory "$SMPROGRAMS\\{name}"
  CreateShortcut "$SMPROGRAMS\\{name}\\{name}.lnk" "$INSTDIR\\{name}.exe" "" "$INSTDIR\\app.ico" 0
  CreateShortcut "$DESKTOP\\{name}.lnk" "$INSTDIR\\{name}.exe" "" "$INSTDIR\\app.ico" 0
  WriteRegStr HKCU "Software\\BackwoodsBrew\\{slug}" "InstallLocation" "$INSTDIR"
  WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{slug}" "DisplayName" "{name}"
  WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{slug}" "DisplayVersion" "{version}"
  WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{slug}" "DisplayIcon" "$INSTDIR\\app.ico"
  WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{slug}" "Publisher" "Backwoods Brew"
  WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{slug}" "InstallLocation" "$INSTDIR"
  WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{slug}" "UninstallString" '$\\"$INSTDIR\\Uninstall.exe$\\"'
SectionEnd
Section "Uninstall"
  SetShellVarContext current
  Delete "$DESKTOP\\{name}.lnk"
  Delete "$SMPROGRAMS\\{name}\\{name}.lnk"
  RMDir "$SMPROGRAMS\\{name}"
'''
for file in files:text+=f'  Delete "$INSTDIR\\{win(file.relative_to(payload))}"\n'
for folder in dirs:text+=f'  RMDir "$INSTDIR\\{win(folder.relative_to(payload))}"\n'
text+=f'''  Delete "$INSTDIR\\Uninstall.exe"
  RMDir "$INSTDIR"
  DeleteRegKey HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{slug}"
  DeleteRegKey HKCU "Software\\BackwoodsBrew\\{slug}"
SectionEnd
'''
# GetFileName is FileFunc macro, ensure install only targets the dedicated application folder.
text=text.replace('!include "LogicLib.nsh"','!include "LogicLib.nsh"\n!include "FileFunc.nsh"').replace('GetFileName $0 "$INSTDIR"','${GetFileName} "$INSTDIR" $0')
script.write_text(text)
subprocess.run([str(nsisroot/'linux/makensis'),'-V2',str(script)],check=True,env=__import__('os').environ|{'NSISDIR':str(nsisroot)})
print(exe)
