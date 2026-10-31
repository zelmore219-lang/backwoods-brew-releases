# Connected apps validation

- Main version 8.2.0, Android ID com.backwoodsbrew.mainapp, versionCode 2.
- Vendor version 4.1.0, Android ID com.backwoodsbrew.vendorordering, versionCode 4.
- Android debug APK builds passed with JDK 21 / Android SDK 35 / Gradle 8.11.1.
- Signing certificates compared with main 8.1.53 and vendor 4.0.9 APKs: match.
- Windows x64 Electron 34.5.8 payloads packaged with electron-builder 25.1.8.
- NSIS 3.0.4.1 installers compiled using the native Linux compiler. Installers create current-user shortcuts and uninstall entries. Uninstall deletes only packaged files and does not touch app data.
- 12 accounting tests: balanced journals, partial payments, payment deduplication, repeated projection, catalog/stock separation, returns/COGS, missing historical costs, conflicting/overpayments, locked invoice corrections, void review, fixed opening equity, cost-captured receipts, real patched main ledger/P&L totals, and stock adjustment posting.
- 3 vendor cost tests: durable delivery costs, partial receipt charge allocation and rounding, negative cost rejection.
- 17 existing device-sync tests passed.
- 7 main browser tests passed: navigation, Android/iOS bridge simulations, exports/printing/location, cash sale persistence, login failure, isolated REST accounting connection and acknowledgements, logout clearing, and denied permissions.
- 9 vendor browser tests passed: orders, product editing, role restrictions, mobile navigation, native bridge simulations, recovery functions, sync status, two-device replication, offline restart/reconnect, and preservation of older cached exports.
- Browser tests isolate Firebase with synthetic records and do not write production business data.

Not executed: Windows GUI install/uninstall, Android emulator/device launch, live Firebase owner-account connection, Apple/Xcode builds, App Store/Play Store submission.

See INSTALL-FIRST.md for the one-time connection setup and data-review cases. SHA256SUMS.txt contains artifact checksums.
