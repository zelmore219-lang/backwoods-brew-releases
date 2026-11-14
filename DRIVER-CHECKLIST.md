# Driver repair checklist

Status: **Driver 0.5.1 is released for Windows and Android. Automated acceptance, public download checks and the updater passed. The shared owner service is online. Business-device and physical printer acceptance remain.**
Checked entries mean the implementation has passed the verification described
below. They do not mean the repair is installed on a business device.

## Clock Out repair: 0.5.1

- [x] Reproduce the greyed-out Clock Out caused by an unconfirmed Clock In.
- [x] Close the existing local shift online while earlier punches are pending; retain the exact original times and signed-in account.
- [x] Stop GPS, retain punches through restart, recover setup failures, and reconcile server confirmations without duplicate events.
- [x] Pass Windows install/reinstall and the actual pending-clock UI regression.
- [x] Pass Android 35 native pending Clock Out/restart/synchronization, normal shifts, GPS, delivery, handwritten signature and printed PDFs.
- [x] Verify matching Android package/signing key with version code 2 for a compatible Driver (New) 0.5.0 update.
- [x] Verify the live owner service heartbeat and shared-clock readiness.
- [x] Publish 0.5.1 and verify public download hashes and the separate Driver updater.
- [ ] Install 0.5.1 on the business device and confirm its Clock Out button works.

## Implemented and verified

- [x] Work from the latest existing Driver source, retaining Firebase and authentication.
- [x] Completed Invoices retains saved versions independently of current routes/orders.
- [x] Completion dates use the delivery location's time zone; creation dates remain separate.
- [x] Daily groups retain both 11/10/2026 and 11/11/2026 in emulator browser tests.
- [x] Search completed invoices by invoice, customer, driver, and date.
- [x] Display saved quantities, totals, payment/delivery status, recipient, and signature status.
- [x] Explicit signature confirmation binds the saved invoice material and location snapshot.
- [x] Closing and reopening a draft restores quantities, check information, photos, and actual handwriting.
- [x] Editing quantities clears confirmation and requires the customer to sign again.
- [x] Device evidence survives offline restart and sync; signed deliveries cannot be discarded from the outbox.
- [x] Reprint the saved signed version from history in full-page and 80 mm formats.
- [x] Browser print-button tests invoke printing without opening a popup; generated PDFs contain actual saved text and the handwritten image.
- [x] Inspect the rendered receipt for readable content, a visible signature, and an unclipped version identifier.
- [x] Server time-clock rules reject duplicate active shifts, event replay, foreign identities, forged employee/company fields, driver payroll approval, and changes without a complete clock event transaction.
- [x] Server clock tests preserve an eight-hour offline shift with a 30-minute unpaid break as 450 paid minutes, marked for review.

- [x] App clock buttons, break/GPS pause and resume, offline restart, and reconnect have been verified against exact saved server timestamps and one immutable event per action.
- [x] The full local security/browser regression run passes for the combined repair.
- [x] Existing delivery/return/check exports pass the actual Accounting engine: balanced ledger, undeposited funds, and duplicate snapshot/payment protection.

Verification uses isolated Auth/Firestore emulators and fictitious business
records. Browser tests draw signatures on the real canvas; production invoice
generation contains no signature or transaction placeholders. Existing inventory,
returns, check custody, reconciliation, route alerts, SOS, inspections, and offline
delivery regression flows have passed. Unit tests, lint, and production build
have passed for this development work.

## In progress / still required

- [x] Connect shared timecards and permissions to the existing Employee/Main identity and payroll workflow; do not ship an isolated clock system.
- [x] Verify Employee administrator views, employee/date/location/pay-period filters, corrections, approvals, exports, and overtime using verified organization rules.
- [x] Native emulator tests verify granted location permission, screen-off GPS/route notifications, clock-out retaining authentication, and automatic tracking on the next shift. Native offline authorization is implemented; physical permission/recovery acceptance remains a device check.
- [x] Run the actual Android emulator workflow for clock, screen-off tracking/recovery, delivery, customer signature, completed history and native printing. Save and inspect both full-page and receipt-layout PDFs, containing the actual handwritten image and no blank pages.
- [x] Implement administrator-issued expiring, single-use, change-bound approval codes with server validation and attempt limits.
- [x] Preserve original/revised invoices and the approval audit; obtain a new signature after material edits.
- [x] Connect approved corrections to Wholesale and proper Accounting adjustments, preserving the independent wholesale division.
- [x] Run cross-application regression: 15 Auth/Firestore integration tests, the actual Driver/admin approval browser flow, protected payroll and the existing Accounting engine.
- [x] Build Windows and Android packages; Windows install/reinstall preserves actual IndexedDB records in the disposable acceptance fixture.
- [x] Publish Employee 0.4.2 and verify its Windows/Android downloads and compatible updater feed.
- [x] Compile and activate the composed Driver Firebase rules; verify live read-back while preserving Main, Wholesale, Accounting and Employee relay rules.
- [x] Publish tested Driver Windows/Android downloads and verify the separate Driver updater feed.
- [ ] Original-package Android update: blocked by the unavailable original signing key.
- [x] Produce a separately signed **Backwoods Driver (New)** APK, with its key backed up privately and the original installed app/data preserved.
- [x] Verify that the shared owner service is online with shared-clock readiness and a matching workspace.
- [ ] Review actual employee UID/job/workweek and existing Accounting-owner mappings on the business HR PC.
- [ ] Verify the customer's actual tablet and printer hardware.

## Release blockers and limits

The original Driver Android signing key has not been recovered. The published
APK contains its public certificate, not the private key needed for a compatible
update. The build report does not confirm an organization backup. No original-package signing-key replacement, uninstall, or device-data deletion has been performed.

A separate Android package has been registered in the existing Firebase project.
Its signing key has an owner-only recovery backup. Existing Driver records and the original installed Android package remain in place. The composed live Driver rules are deployed and verified as SHA-256 `0a8afc6718b2e0871ebc75f14133a2560792e92a6c0f040c73dfb7b6561a9f95`; Main, Wholesale, Accounting and Employee relay namespaces were preserved. Physical printer hardware and
actual payroll/job mappings still require owner review; the live service heartbeat and shared-clock readiness are verified.

## Latest verified integration checkpoint

- [x] Real Driver/admin browser flow: propose, compare original/revised, issue a secure code, validate it, draw a new signature, apply and reprint both versions.
- [x] Codes expire, are single-use, are bound to the proposal and lock after five wrong attempts; no plaintext code is stored on the device.
- [x] The existing Accounting engine posts an explicit reversal/revision and inventory adjustment in the same cloud commit as the Wholesale invoice. Closed periods preserve the original invoice and stock for Finance review.
- [x] A Driver shift appears under the same Employee UID, excludes an actual unpaid break, exports 7.5 paid hours, and prevents a second Employee clock-in.
- [x] Cross-app hours enter the existing timesheet/payroll engine: 40 regular plus 5 overtime hours under the verified test workweek; late changed hours block frozen payroll approval.
- [x] Reviewed missed clock-out retains the original and releases the shared active-shift state.
- [x] Windows updater verifies the correct app, trusted release URL, size and SHA-256; corrupted installers and foreign-frame calls are rejected (12 tests).

These checks used fictitious records in disposable emulators. The finished
Employee companion must be installed and its owner service started on the actual
Windows PC containing the company's existing HR records.

Final local integration: 15 Auth/Firestore emulator tests passed, including real Employee administrator filters/approval/export and the released Main clock helpers preventing a duplicate shift and closing the canonical Driver card.


## Previous 0.5.0 package verification

- Driver runtime build: `cf994c9f5f8239fa9f5b7319af05d524c7c89231`. Later native-test changes leave the production application files identical.
- Driver Windows 0.5.0 SHA-256: `53ccfafe356837e6bdde797ac10805b535d9fcc07414a186a422fc8eb87c75cc`.
- Driver separate Android 0.5.0 SHA-256: `81ef185f25d3e16340d6f597c001b3454c162b75bc5e6ba907254c0fc103a002`. Package `com.backwoodsbrew.driver.next`, version code 1.
- Employee companion build: `a51657575ad5f7d33dbe36754adb87c4d6696cd7`, version 0.4.2.
- Employee Windows SHA-256: `3885079b7ccb909aa85f3d4ea0e403679fb4bc27174f59a3ba19c42a695ae84b`.
- Employee Android SHA-256: `7ad6e502bbd0a2c26ed1f38b80076690b5299c3bfe1d3760f04d0560b2fe4d0f`. Its certificate matches Employee 0.4.1.

Install the Driver Windows setup once to add the updater. The original Driver 0.4.0 has no updater and cannot receive that bootstrap automatically. Synchronize pending original Android work before switching to the separate new package; keep the original app. Keep the actual Employee owner PC awake and online for shared administration. Onboarding document drafting remains deferred.

Final Android and browser acceptance passed: https://github.com/zelmore219-lang/driver_routeplanner/actions/runs/43345781788 . Windows/Android runtime build acceptance passed: https://github.com/zelmore219-lang/driver_routeplanner/actions/runs/43339467246 . Employee packaged acceptance passed: https://github.com/zelmore219-lang/backwoods-brew-android/actions/runs/43338403990 .

Android Save as PDF used the system-selected Letter media. The receipt layout remains narrow; the physical printer's paper size and Android print service must be selected and verified on the business device. No physical printer is claimed as tested.

Published Driver release: https://github.com/zelmore219-lang/backwoods-brew-releases/releases/tag/driver-0.5.0 . Publisher install/reinstall, public download hashes and updater feed passed: https://github.com/zelmore219-lang/backwoods-brew-releases/actions/runs/43447872823 . Employee 0.4.2 publication passed: https://github.com/zelmore219-lang/backwoods-brew-releases/actions/runs/43340092448 .

## Latest 0.5.1 package verification



- Lint, unit tests and the production web build pass locally.
- Actual browser buttons, GPS stop/resume, unpaid breaks, offline restart and
  exact-timestamp synchronization pass against isolated Auth/Firestore services.
- Regression covers the old attention-state Clock In, online Clock Out, restart,
  setup recovery and interrupted server acknowledgements.
- Windows install/reinstall, retained IndexedDB, pending-clock UI, updater and invoice PDF checks pass.
- Android 35 native clock, screen-off GPS, pending Clock Out/restart/reconnect, delivery, handwriting and actual printed PDFs pass.
- Installer build acceptance: https://github.com/zelmore219-lang/driver_routeplanner/actions/runs/43539094101 .
- Final full validation: https://github.com/zelmore219-lang/driver_routeplanner/actions/runs/43539248829 .
- Built source: `b4cd53644d8d1ea95da4a87cda7505bee43b3cc1`. Validated source: `07c95b8bdeee0664c8900f4adf0fa801a7a20b50`; their only difference is the native test fixture.

No live timecards or company records are created by these tests. Windows keeps
the same app identity and storage. Android uses the retained key and package
`com.backwoodsbrew.driver.next`, version code 2, to update Driver (New) 0.5.0.
The original Android package/key remains separate and its data is preserved.

The live owner service heartbeat, shared-clock readiness and matching workspace
were verified. The owner service must remain online for central synchronization.
Actual payroll/job mappings, business devices and printers require owner
acceptance. The repair must be installed on a business device before its
Clock Out behavior can be confirmed there.

Windows SHA-256: `384c27fe8dd6062e4ef558865c7ba9a1e8859c382c8048a4500a94225c4a3dd2`.
Android SHA-256: `3ecd527e2eac04d8317ad764dbbf80056a735c2992fe6c2dc695dc46c6fcacc5`.
Published release: https://github.com/zelmore219-lang/backwoods-brew-releases/releases/tag/driver-0.5.1 .
Public package hash/size checks and updater publication passed:
https://github.com/zelmore219-lang/backwoods-brew-releases/actions/runs/43540655228 .
The existing 0.5.0 updater accepts the published 0.5.1 Windows entry.
Android retains the package/certificate and increments its version code to 2.
The separate Employee feed is unchanged.
