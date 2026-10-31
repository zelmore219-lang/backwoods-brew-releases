# Backwoods Brew main app 8.1.53 — Android and iOS build project

This is the main Backwoods Brew app supplied in the uploaded app.asar, **version 8.1.53**, separate from Vendor Ordering. The user chose this supplied version for conversion. It does not include features added in later Windows builds such as 8.1.61.

The original React/JSX source maps were absent. This project retains the packaged web interface and business logic exactly and adds editable mobile adapters plus native Android/iOS projects. It is a mobile build project, not a reconstruction of the missing original React source repository.

## Prepared behavior

- Separate mobile application ID: `com.backwoodsbrew.mainapp`; display name: Backwoods Brew. Installs alongside Vendor Ordering.
- Collapsible phone navigation, tablet sidebar, safe-area spacing, and touch-sized controls.
- Original login, business logic, POS, data storage, permissions, and sync logic retained.
- Native backup/document share sheets replace browser downloads.
- App-created receipt/report popup documents become mobile print previews with native system printing. Embedded popup scripts are not executed. PDF attachments use native save/share to open.
- Native foreground location permissions support the existing store weather location action.
- External HTTPS links open in the system browser. Android Back closes previews/menus or minimizes the app.
- Original employee clock entry page retained at clock.html.

## Build Android

Install Node 22+, Java **JDK 21**, Android Studio/SDK Platform 35 and Build Tools 34.0.0/35.0.0. Configure ANDROID_HOME or create android/local.properties through Android Studio.

```sh
npm ci
npm run android:apk
```

Output: `android/app/build/outputs/apk/debug/app-debug.apk`. On Windows use `npm run mobile:sync`, then `cd android` and `gradlew.bat :app:assembleDebug`. `npm run mobile:android` opens Android Studio.

The provided APK is an installable **testing build**, minimum Android 6, target SDK 35. Transfer to Android, open it, and permit installation from that source when prompted. It does not replace the Vendor Ordering app. A store-distribution build needs your own release signing key and review against the current store target-SDK requirements. Preserve that key for future updates.

## Build iPhone/iPad

The iOS project is prepared; Linux cannot build or sign an IPA. On a Mac with Xcode 16+, Node, and CocoaPods:

```sh
npm ci
npm run mobile:ios
```

Open `ios/App/App.xcworkspace`, select the App target, choose your Apple development team under Signing & Capabilities, confirm the bundle identifier, and select a device. Run on a device, or Archive and Distribute through TestFlight/App Store using your Apple Developer membership. iOS 14+ is configured. No compiled or signed iOS IPA is included.

## Accounts, data, and platform limits

The provided app uses its existing embedded Firebase web-client configuration and original account/login logic. No company account, saved password, desktop database, or session was imported from your PC. Sign in with your company account. Data stored only on the Windows PC will not appear automatically; use the original cloud sync or backup/restore workflow as appropriate. Back up before restoring or using real business data.

No live company login or cloud synchronization was tested. Tests intercept all HTTPS requests and use a synthetic local account in a disposable browser context; they do not create production accounts or write company records. This app has its original local-login fallback rules; test your real login on a device before relying on offline access.

Windows auto-update, Windows printer drivers, direct USB/serial receipt-printer control, and cash-drawer hardware are not mobile integrations. Use system printing/share/PDF and separately configured supported printers. Mobile updates use a new signed APK or Apple's distribution system; a Windows .exe cannot update this mobile app. Existing payroll, accounting, Square and QuickBooks screens retain their original behavior; this conversion does not supply a new native payment-terminal or OAuth backend integration.

Before operational use, validate on real devices: login, cloud updates, exports/restores, receipts/report print layout, location grant/deny, attachment pickers, external integrations, offline/reconnect behavior, and your selected printer. OS dialogs, hardware, and live services were not exercised by simulated bridge tests. Review Apple privacy declarations against your actual deployment before store submission.

## Validation

```sh
npx playwright install chromium
npm run test:mobile
```

Five browser tests exercise the actual packaged app: local login/business navigation; Android and iOS mock-native backup export contents, document preview/print, browser links and location grant/deny; a cash sale/receipt and persistence across reload; wrong-password rejection and tablet navigation. The mobile adapters are bundled with esbuild; the packaged application assets are copied without rewriting the compiled application logic.

See VALIDATION.md and PACKAGED-ASSETS-SHA256.json for the executed checks and input provenance.
