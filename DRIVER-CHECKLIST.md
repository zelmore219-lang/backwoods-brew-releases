# Driver repair checklist

Status: **Driver 0.5.0 and Employee 0.4.2 are released. Automated acceptance and public updater/download verification passed. Business-device activation and physical printer acceptance remain.**
Checked entries mean the implementation has passed the verification described
below. They do not mean the repair is installed on a business device.

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
- [ ] Activate Employee 0.4.2 Owner service on the actual HR Windows PC and review real employee UID/job/workweek and existing Accounting-owner mappings.
- [ ] Verify the customer's actual tablet and printer hardware.

## Release blockers and limits

The original Driver Android signing key has not been recovered. The published
APK contains its public certificate, not the private key needed for a compatible
update. The build report does not confirm an organization backup. No original-package signing-key replacement, uninstall, or device-data deletion has been performed.

A separate Android package has been registered in the existing Firebase project.
Its signing key has an owner-only recovery backup. Existing Driver records and the original installed Android package remain in place. The composed live Driver rules are deployed and verified as SHA-256 `0a8afc6718b2e0871ebc75f14133a2560792e92a6c0f040c73dfb7b6561a9f95`; Main, Wholesale, Accounting and Employee relay namespaces were preserved. Physical printer hardware and
the owner's running Employee service have not been verified here.

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


## Package verification

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
