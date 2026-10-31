# Backwoods Vendor Ordering 4.0.8 — Android and iOS

This is Backwoods Vendor Ordering **4.0.8**, recovered from the uploaded Windows `app.asar`. It is separate from the Backwoods Brew main app. See RECOVERY-NOTES.md for exactly what was recovered.

## What changed

- Added Capacitor 7 Android and iOS projects (same React/Firebase app, app ID `com.backwoodsbrew.vendorordering`).
- Added a collapsible phone menu, safe-area spacing, larger touch controls, and scrolling tablet navigation.
- Added native foreground GPS permission handling for delivery proof.
- Camera barcode scanning now uses ZXing, including browsers without BarcodeDetector. Manual/USB/Bluetooth barcode entry remains available.
- JSON/CSV exports use the device's native share/save sheet. Existing browser downloads still work on the web.
- Native print dialogs handle invoices, labels and packing slips. Android's print dialog offers Save as PDF; iOS offers AirPrint and PDF sharing through the system dialog.
- External web links open through the native browser. Android back goes through page history or minimizes at the root.
- Native builds bundle web assets and disable the PWA service worker; web/PWA and Windows scripts remain present.

## Install dependencies

Use Node 22 or newer (tested here with Node 24). Run commands in this folder.

```sh
npm ci
```

For a mobile-only install, skip the optional Windows/desktop Electron binary download:

```sh
ELECTRON_SKIP_BINARY_DOWNLOAD=1 npm ci
```

For PowerShell: `$env:ELECTRON_SKIP_BINARY_DOWNLOAD='1'; npm ci`.

Keep your Firebase settings in `.env` as in the original app. The downloadable source excludes that local file; copy it from your original ZIP before rebuilding against your company data. Never put service-account credentials in Vite variables. Only Firebase web-client settings belong in this app.

## Android APK

Install Android Studio, Java **JDK 21**, Android SDK Platform 35 and Build Tools 34.0.0/35.0.0. Configure `ANDROID_HOME` or let Android Studio create `android/local.properties`. Android 6+ is supported by the generated project.

```sh
npm run android:apk
```

On Windows, run `npm run mobile:sync`, then `cd android` and `gradlew.bat assembleDebug`.

The installable testing APK is `android/app/build/outputs/apk/debug/app-debug.apk`. Transfer it to the Android device, open it, and permit installation from that source when Android asks. The debug APK is for testing and is not signed for Play Store distribution. Debug builds use a development signing key. A later production build signed with another key cannot replace it in place; export a backup before uninstalling a test build. Keep your release signing key under your control; use Android Studio's Generate Signed Bundle / APK for a production release. Store distribution requires checking the current Play target SDK and policy requirements.

Use `npm run mobile:android` to open Android Studio. `npm run android:bundle` creates an unsigned release bundle until you configure signing.

## iPhone and iPad

The `ios/` project is prepared, but this Linux environment cannot run Xcode, compile iOS, or sign an IPA.

On a Mac, install Xcode 16+ with its command-line tools, Node, and CocoaPods. Then:

```sh
npm ci
npm run mobile:ios
```

This builds the web assets, runs Capacitor sync/pod installation, and opens `ios/App/App.xcworkspace`. In Xcode, choose the App target, select your Apple development team under Signing & Capabilities, confirm the bundle identifier, and select your connected device. Run for personal device testing, or Product > Archive and Distribute App for TestFlight/App Store distribution using your Apple Developer membership. iOS 14+ is configured.

No installable iOS app is included until those Mac build/signing steps are completed. Verify privacy declarations against your actual Firebase use and data collection before store submission.

## Shared data and account setup

The native builds use the original uploaded Firebase web configuration, not a new database. Sign in with your existing company account. Cross-device business data requires the same Firebase project and appropriate vendor Firestore rules/user roles. Local demo data is device-local and does not sync. This conversion does not deploy Firestore rules or modify live company records. Use the original rules merge guidance; do not replace production rules blindly.

No live login or cloud sync was tested here because no company login was supplied. Back up existing data and test using a non-production account before operational use. Installing a new mobile app does not automatically copy data stored only inside the Windows app; use the original backup/restore or cloud sync workflow where appropriate.

## Validation

```sh
npx playwright install chromium
npm run test:mobile
npm run build
npm run mobile:sync
```

Browser tests explicitly force demo mode and do not touch live Firebase data. They exercise phone ordering and inventory reservation, local persistence, product editing, role access, tablet navigation, and native adapter calls using a simulated bridge. Use `CHROMIUM_PATH` to select an existing Chromium binary.

Before operational use, check on real Android/iOS devices: sign-in and cross-device updates; camera permission grant/deny, scan and close; GPS permission grant/deny; delivery photos/signatures; backup export and restore; invoice/label/packing print layout; external maps/payment links; offline/reconnect behavior. Simulated bridge tests do not validate OS dialogs, printer output, hardware or Apple compilation.
