# Conversion validation

- Web/PWA production build: passed.
- Native web build and Android/iOS asset synchronization: passed. iOS CocoaPods installation and Xcode compilation were not run on this Linux machine.
- Four Playwright tests: passed. They cover phone order submission and inventory reservation, local persistence, product editing and role restrictions, tablet page navigation, and simulated native backup sharing/GPS permission grant and denial/printing.
- Android app compilation and debug APK packaging: passed (`:app:assembleDebug`).
- APK signature verification: passed (v1 and v2).
- APK identity: `com.backwoodsbrew.vendorordering`, version 4.0.0, minimum Android SDK 23, target SDK 35.
- Original uploaded Firebase web configuration used for the testing APK. No live company login, cloud synchronization, or production data edits were performed.
- Real-device camera, GPS, photo/signature, OS sharing and print dialogs remain untested. Native bridge tests used mocks.
- No compiled/signed iOS IPA is included. A Mac with Xcode and Apple signing is required to complete and validate that build.

See MOBILE-BUILD.md for rebuilding, installation, signing and real-device checks.
