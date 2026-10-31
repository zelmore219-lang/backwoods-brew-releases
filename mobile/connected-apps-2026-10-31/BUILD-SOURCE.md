# Rebuilding the connected apps

The source ZIP contains `main-app/` and `vendor-ordering/`, including Android/iOS projects, main preserved assets, integration code, and tests. User data, private live catalog exports, credentials, dependency caches, and build outputs are excluded. Vendor Firebase configuration must be supplied locally using `.env.example`; do not enable demo mode for a real build.

Use Node 22+, npm, JDK 21, Android SDK/build tools 35. Set JAVA_HOME and ANDROID_HOME/ANDROID_SDK_ROOT; create each android/local.properties with your SDK path. Keep the original APK signing key when rebuilding an installed app. The delivered APKs use the cloud build machine's existing debug key, which is intentionally excluded from this public source archive. A differently signed APK cannot replace them without uninstalling.

For each project:

```
npm ci
npm run mobile:sync
cd android
./gradlew :app:assembleDebug --no-daemon --max-workers=2
```

For main browser validation: `npm run build`, `node --test --test-isolation=none tests/vendor-accounting.test.js`, then `npx playwright test`.

For vendor validation: `npm run test:sync`, `node --test --test-isolation=none tests/accounting-costs.test.js`, then `npx playwright test`.

Chromium must be installed or available through Playwright. The tests use isolated synthetic records rather than live Firebase writes.

Windows desktop payloads were built with electron-builder 25.1.8 and Electron 34.5.8. For the vendor app, run `npm run mobile:sync` then `npx electron-builder --win dir --x64 --config.win.signAndEditExecutable=false --config.electronVersion=34.5.8`. For main, run `npm run build` and use the vendor project's electron-builder binary with main as its working directory and the same flags. Linux installer builds use a native makensis compiler; the accompanying `windows-installer-build.py` generates the current-user installer with a manifest of owned files for safe uninstall. Set its NSIS root to your local NSIS distribution and its output directory to a suitable location.

iOS sources are included for continuity but have not been compiled or signed. A Mac, Xcode, Capacitor iOS dependencies, and Apple signing are required. This delivery contains no installable iPhone build.
