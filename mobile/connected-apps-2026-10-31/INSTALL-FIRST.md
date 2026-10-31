# Backwoods connected apps — October 31, 2026

Install BOTH updated apps on the Windows computer and Android device.

| App | Windows computer | Android phone/tablet |
|---|---|---|
| Main Backwoods Brew 8.2.0 | Backwoods-Brew-Main-8.2.0-Windows-Setup.exe | Backwoods-Brew-Main-8.2.0-Android.apk |
| Vendor Ordering 4.1.0 | Backwoods-Vendor-Ordering-4.1.0-Windows-Setup.exe | Backwoods-Vendor-Ordering-4.1.0-Android.apk |

1. Export a backup from each existing app before updating. Close the Windows apps.
2. Run the Windows Setup EXEs and use the dedicated app folders shown by the installer. These create desktop and Start menu shortcuts and a Windows uninstall entry.
3. On Android, open the APK downloads and choose Update/Install. Permit installation from your browser if Android asks. These use the same package IDs and signing certificates as the prior APK downloads. Do not uninstall the previous apps or clear their storage.
4. Sign in using your existing accounts and let Vendor Ordering finish Device Sync.
5. In the MAIN app, open the menu and choose **Vendor Connection**. Select the store where vendor accounting belongs and choose **Enable accounting connection**. Repeat the sign-in on the other devices; the connection setting is saved with the main app's normal cloud data.
6. Both apps must point to the same Firebase project. The signed-in Firebase user needs an active main-app profile and an active vendor profile with accounting/management access. An account that can sign in to only one app may need its profile assigned by the owner. This build does not change your Firestore rules.
7. Resolve any items under **Needs review**. Enter documented historical unit costs for older invoices if requested. Where costs differ by invoice, edit the vendor invoice's saved unit cost in source before including it. Review and approve the opening inventory reconciliation only after source invoices and costs are correct. This posts an opening inventory/equity journal; the apps do not zero any stock.
8. Verify one delivered vendor invoice and one payment in the main app's Invoices / A/R and ledger/P&L. Check the remaining balance after a partial payment. Vendor Ordering's Main App Sync Log receives the main app acknowledgement.

## What is connected

- Delivered/completed vendor invoices, tax, payments, embedded approved credits/returns, recorded COGS, new cost-captured purchase receipts, and new cost-captured manual stock adjustments feed the main app's accounting view.
- Repeat refreshes use stable source IDs instead of inserting another invoice. Payments duplicated in the order and payments collection count once.
- Vendor inventory is visible as its own stock list in Vendor Connection. Main-app coffee-shop products, supplies, sales, and stock stay separate. Main sales do not appear in Vendor Ordering or reduce vendor stock.
- Vendor rows are read-only in main reports. Enter source corrections/payments in Vendor Ordering. Native coffee-shop data is saved through the existing main app sync.
- Vendor source data is read while the main app is running, about every 30 seconds, plus Refresh now and reconnect. This is not a background server process. Previously fetched records have a per-account offline cache. A connection failure is shown; offline totals may be stale.
- Imported accounting is derived from source records rather than copied into the main app's native data arrays. Every connected main installation needs this update to show the combined reports. Disabling the connection excludes vendor rows from that view; it does not erase vendor records.

## Review cases and limits

Older invoices with no cost record, conflicting payment records, customer overpayments/refunds, previously posted invoice voids, and changes to locked invoice periods need review. The previous acknowledged invoice snapshot is retained when a correction is blocked. Do not assume an error means the source transaction was erased.

Older purchase receipts with uncertain landed costs need review. A supplier invoice merely marked Paid has no dated supplier payment transaction in the recovered app; this build flags it for a bank/payment journal review rather than inventing a bank withdrawal. Stock value differences are flagged for reconciliation instead of silently changing owner equity. The historical-cost approval applies to earlier invoices for the selected product; it is not an assertion that today's catalog cost was the cost on every past invoice.

This main build is based on the recovered 8.1.53 app, with the new connection and mobile adapters. It does not restore unavailable 8.1.61 source changes. Desktop updates for this connected main build use these installers; the legacy automatic updater is disabled to prevent installation of an unrelated older release.

The EXEs are unsigned Windows x64 installers; Windows may show an unknown-publisher prompt. The APKs are sideload/debug-signed updates, not Play Store releases. No iOS IPA is included; the source projects require a Mac/Xcode and Apple signing for iOS.

## Validation

Both Android APKs compiled successfully, have increasing version codes, and match their previous signing certificates. Both Windows payloads and NSIS installers compiled. Accounting, device-sync, and browser tests passed (see VALIDATION.md). Actual Windows GUI installation and live Firebase financial-account testing were not available in this Linux build environment. Verify the first live invoice/payment before relying on combined totals.
