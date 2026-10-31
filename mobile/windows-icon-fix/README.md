# Windows app icon correction

- [Main Backwoods Brew — Windows installer with app icon](https://github.com/zelmore219-lang/backwoods-brew-releases/raw/refs/heads/vendor-ordering-mobile-4.0-downloads/mobile/windows-icon-fix/Backwoods-Brew-Main-8.2.0-Windows-Setup-Icons.exe)
- [Vendor Ordering — Windows installer with app icon](https://github.com/zelmore219-lang/backwoods-brew-releases/raw/refs/heads/vendor-ordering-mobile-4.0-downloads/mobile/windows-icon-fix/Backwoods-Vendor-Ordering-4.1.0-Windows-Setup-Icons.exe)

Close the app and run the corrected installer over the current installation. It recreates desktop and Start menu shortcuts with an explicit app icon. Keep the same installation folder; do not uninstall or clear app data. Android does not need another update for this fix.

If an old pinned taskbar shortcut still shows a generic icon, unpin it and pin the updated app shortcut again.

The correction embeds the existing multi-size app artwork into each Windows EXE, installer, uninstaller, and desktop/Start menu shortcut, and sets the Windows uninstall-list DisplayIcon. No business code or data changes are included. Application versions remain main 8.2.0 and vendor 4.1.0.

Validation: resource readback confirms the embedded icon images exactly match the supplied ICO at all sizes; existing non-icon executable resources (including Electron integrity metadata) are preserved. Installer icon resources and explicit shortcut icon paths are checked after compilation. Windows GUI display still needs checking on a Windows machine.

The packaging helpers and resource verification script are included for future builds and supersede the installer helper in the earlier source ZIP. They use the existing cloud workspace tool paths; adjust those paths if building elsewhere. The embed helper uses the vendor project's installed resedit and pe-library dependencies. No signing keys or user data are included.
