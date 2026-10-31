# Vendor Ordering 4.0.9 — device sync update

This update is for Vendor Ordering sharing data with its other Windows, Android, and iOS installations. The main Backwoods Brew accounting app was not changed.

## Install on every Vendor Ordering device

1. Export a business backup from the existing app before updating.
2. Android: install the 4.0.9 APK over the previous Vendor Ordering test APK. Do not uninstall the old app or clear app storage. Same application ID and signing certificate; version code increases from 2 to 3.
3. Windows: close the old Vendor Ordering app, download and run **Backwoods-Vendor-Ordering-4.0.9-Windows-Portable.exe**. This is a portable app, not a Windows installer. Use this new executable instead of the old desktop shortcut. It uses the same app name and standard Electron user-data directory; the old installation is left in place. Keep your exported backup.
4. Sign in online using your company’s assigned account on each device. Each account must have an active vendor user profile and role. Demo/local-only accounts do not share records.
5. Open **Device Sync** on each device. Wait for **Firebase connected** and **Pending records: 0**. Confirm the Firebase project matches on every device. The project settings are unchanged from the supplied 4.0.8 desktop app.
6. Make a small test change to a non-critical product/customer field on one device and verify it appears on the other. Test an offline edit, reconnect, and wait for pending records to reach zero. Test with spare records before operational use.

Older 4.0.8 clients can still upload stale full snapshots. Stop using the old version on every device while verifying the new version.

## Previous unsent data

The previous unscoped local cache and full-snapshot queue remain untouched. They are not replayed automatically over the cloud database. If older data is missing, an owner can open Device Sync and **Export previous device backup**. The export includes both preserved old snapshots as well as the preferred recovery dataset.

**Recover missing records** checks each original record in a Firebase transaction and creates it only if its ID is missing. It does not modify an existing cloud record, company settings, or replay old deletions. Review existing-record differences against the exported backup before editing them. A stopped recovery is safe to retry because existing records are skipped.

If local storage is full, export and check that previous-device backup first. The owner can then explicitly remove the old local copies in Device Sync to free storage. That action keeps cloud records and the new version’s outbox. Never clear all app storage to fix sync.

## What was fixed

- Replaced full-database uploads with durable, account- and Firebase-project-scoped per-record/per-field changes.
- Incoming snapshots continue to update untouched fields and collections while local edits wait to upload.
- Stale cached rows no longer overwrite newer cloud values or resurrect remotely deleted records.
- Edits made while a write is in flight retain their own acknowledgement and cannot be cleared by an older acknowledgement.
- Offline edits/deletions survive app restarts and retry on reconnect/resume. A failed write stays visible and queued. Independent records can still upload when another record is denied.
- Role-aware reads avoid unnecessary restricted collections, and customer reads are constrained to that customer.
- Confirmed server snapshots determine the connection indicator. “Online” alone is no longer reported as cloud sync success.
- Backups wait for initial cloud reads before running. Demo seed data and automatic catalog migrations are no longer uploaded just because the app started.
- New order/invoice numbers include an installation suffix to avoid collisions when two offline devices start from the same sequence. Existing invoice numbers are unchanged. Number allocation no longer writes owner-only company settings on each salesperson/customer order.

Different fields on the same record merge independently. Simultaneous edits to the same field are last-successful-write wins; this update does not introduce inventory/financial transactions or a conflict-resolution UI. If an existing record was deleted on another device, a pending edit will show an error for review rather than silently recreate it.

## Firebase access errors

If Device Sync reports permission-denied, its exact collection/path and error are shown. An authorized owner must review that account’s vendor role and the production Firestore rules. No production rules were deployed or weakened.

The supplied merge-only rule example previously named **vendorRoutePlans**, while the app has always used **vendorRoutes**. Its example is corrected to vendorRoutes and the read roles needed by route/delivery workflows. If your actual rules already cover these collections, no rules change is needed. Otherwise, merge the appropriate vendor sections into existing rules in Firebase Console; do not deploy the placeholder firestore.rules file or replace the main app’s rules wholesale. This build cannot grant permissions through client code.

## Verification and limits

Passed: 17 deterministic sync-engine tests plus 9 Playwright tests. Two independent React stores were tested against a shared simulated cloud for offline edits, another device’s edits/deletions, reconnect, and reload recovery. Tests also cover pending-write races, account separation, permissions/retry, local storage failure, cache-only status, numbering collisions, and mobile UI workflows.

Android APK and Windows portable packaging are verified separately. The Linux environment cannot launch the Windows executable or build/sign iOS. Native hardware and live production Firebase accounts/rules were not tested; the new Device Sync screen and the two-device check above provide the runtime evidence needed on your devices. The iOS project is prepared for Mac/Xcode building and Apple signing.
