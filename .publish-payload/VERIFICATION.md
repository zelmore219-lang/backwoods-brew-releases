# Pest Control / Employee / Business Accounting verification

Requested connection: **same legal company, separate Pest Control department**. No real employees, live timecards, production Firebase rules, company mappings, invoices, payments or bank records were changed by testing. Production app work remains deferred.

## Runtime sources and acceptance

| App | Version | Exact runtime source | Native acceptance |
| --- | --- | --- | --- |
| Pest Windows | 0.10.0 | `d32837e961bc1f99c844bbf831d678fbb3a78dc8` | [43718914009](https://github.com/zelmore219-lang/backwoods-brew-window-original1/actions/runs/43718914009), passed |
| Employee Windows | 0.4.9 | `58840434904a0a357077b81403a5e5967fb159cb` | [43720872093](https://github.com/zelmore219-lang/backwoods-brew-android/actions/runs/43720872093), passed |
| Accounting Windows / Android | 1.0.11 | `d88bcc30fe92fc75af6fe1d75b663c2e36f6962f` | [43718949652](https://github.com/zelmore219-lang/backwoods-accounting-/actions/runs/43718949652), passed |

Employee 0.4.9 supersedes the initially accepted 0.4.8. A final review found and reproduced an active Main-display cache entry surviving a completed Pest shift. The fix removes only the exact Pest projection; permanent clock records, retail originals, inventory and sales remain intact. The six Pest unit tests pass, and four Pest/Vendor integration cases passed again with Main-cache cleanup and actual Pest Hours & pay allocation checks.

Later source commits add owner documentation only. Package provenance identifies the exact tested runtime source rather than a later documentation commit.

## What changed

Pest keeps its existing `bugzapper-3397f` Firebase project and accounts. The new **Employee & Accounting** page verifies the currently signed-in Pest account and existing Employee identity separately, then requires the person to confirm the exact pair. The server checks the pinned project, Google account lookup/revocation state and active Pest staff profile. Customer accounts are denied. Unique mappings prevent either identity from being linked to two people; retries preserve one link.

The additive Employee migration provides Pest organizational defaults without activating anyone or assigning a rate. Authorized staff select their actual Pest job to clock in/out. Offline actions retain original timestamps and IDs; official processing requires fresh server verification. Pest is included in canonical Employee synchronization and reviewed corrections. Delayed time requires office review, including a fresh authoritative-source check. Device-captured timestamps remain evidence; official replayed clock entries initially use server receipt times. The owner must confirm actual offline work times and apply the audited UTC time correction/separate approval before finalizing payroll; the replay interval itself is not evidence of the full offline shift. Existing Main, Vendor, Driver and Employee time remain supported.

Pest billing requires both the existing Pest owner and Employee organization owner, plus explicit company confirmation. Only allowlisted issued/voided invoices and recorded payments enter the private finance projection. The Accounting owner then reviews the same company and source before the first import. Binding and first postings commit together. Stable source IDs, source snapshot hashes, missing-record checks and original accounting dates prevent duplicate or silently incomplete imports. Repeated invalid snapshots keep reporting the error even when the Employee roster did not change.

Pest service revenue posts to 4030, AR to 1100, and recorded sales tax to 2100. Cash receipts use 1010; checks and external card/ACH receipts use 1030 Undeposited Funds. No bank settlement, chemical cost, payroll payment or private service/personnel data is inferred.

Pest now has an NSIS Setup installer, its retained portable option and an official Windows updater with visible **App updates → Check for updates…**. App identity, user-data location, bundled origin and existing offline storage are preserved. Accounting's static version footer matches 1.0.11.

## Verification performed

* Pest root business/updater suite: **103 passed, zero failed**, plus syntax checks and an exact production Firebase asset build on Windows.
* Final Employee 0.4.9 Windows regression suite: **146 discovered; 121 passed, 25 explicitly skipped**, plus **17 Node owner-service/updater tests passed**. Optional emulator/physical/integration cases are not represented as Windows unit passes.
* Accounting regression suite, including six new Pest import/binding cases: **138 passed**. The dedicated local Pest/payroll subset passed **24 tests**.
* **10 integration cases actually ran and passed** against separate emulator services: Pest Auth/RTDB, Backwoods Auth/Firestore, three Vendor-clock cases, five Driver/Employee shared-clock cases and one protected Accounting identity/finance case. These are separate from the skipped Windows emulator tests.
* The new Pest integration uses real browser pages, Firebase SDK sign-in, the actual encrypted relay/owner worker and the existing private finance transport. One staff member links existing identities twice, clocks IN and OUT offline, reconnects/retries, and produces exactly one Pest card. A different authorized person sees and approves it in Employee; the staff status refresh shows approval. The owner then synchronizes a fictitious invoice/payment into the same Accounting ledger twice without duplicates. Project/lookup endpoints are directed to emulators only inside the explicit test harness.
* A separate Accounting browser test covers **App connections → Connect Pest Control → Connect and import**, company review, department/source trace and repeated import at desktop, tablet and mobile widths. Its private-feed input is a fixture; the protected feed transport is covered by the integration test above.
* Exact Pest Setup installed and reinstalled on Windows: login rendered, renderer isolated, native update-menu action opened the isolated wizard and a fictitious IndexedDB record survived. The registered accelerator was checked; physical keyboard input was not independently certified.
* Exact Employee installer upgraded the existing 0.3.1 fixture, started its bundled engine, opened/checked the updater, and retained the employee record and DPAPI document key across reinstallation.
* Exact Accounting/Main/Vendor Windows packages installed/reinstalled successfully. Accounting Android retained-signature upgrade and native WebView payroll calculation/export/save-picker tests passed. Existing Main 8.2.11 and Vendor 4.1.10 Windows/Android bytes were reused and their upgrade checks passed.

Raw logs, manifests, proof JSON and Accounting screenshots are retained in this directory. Native tests run on CI machines/emulators, not the owner's physical devices. No live sign-in or production database mutation is claimed.

## Owner action still required

Follow [OWNER-GUIDE.md](OWNER-GUIDE.md). Install the three updates; keep the existing Employee owner service online; review real employee identities, Pest grants and actual job/rate/effective dates; finish any genuine onboarding requirements; explicitly link each person's existing accounts; review real Pest shifts; and confirm the actual legal company in Pest and Accounting before importing real billing.

Paper W-4, Alabama A-4, I-9, handbook and emergency-contact acknowledgments remain supported without uploads. Actual paper review, I-9 examination, verified training and server account checks still apply. Packet approval dates update automatically; existing signatures/form dates are retained. Gusto is not required. Employee retains approvals, PTO, departmental hours and estimated pay; actual HR.my processing remains the owner's external workflow.

Pest Android 0.9.0 remains unchanged and has no newly published connection screen from this Windows release. Employee/Driver Android signing and physical-device acceptance remain separate outstanding work. This report does not claim every app/platform or live deployment is 100% complete.

## Reviewable source changes

* [Pest PR 1](https://github.com/zelmore219-lang/backwoods-brew-window-original1/pull/1)
* [Employee PR 8](https://github.com/zelmore219-lang/backwoods-brew-android/pull/8)
* [Accounting PR 7](https://github.com/zelmore219-lang/backwoods-accounting-/pull/7)

These branches build on the prior unmerged application-integration branches. The published packages use the pinned accepted source commits above; the PRs remain open for source review.

## Public delivery

**Pest 0.10.0, Employee 0.4.9 and Accounting 1.0.11 are published.** The initial 0.4.8 public feed confirmation exceeded one CI edge-cache propagation window; retry succeeded without replacing packages. The read-only `public-verification.json` independently confirms complete public package bytes, sizes and SHA-256 hashes. The final Employee 0.4.9 installer and public feed were independently verified before handoff. Its publisher [43721872541](https://github.com/zelmore219-lang/backwoods-brew-releases/actions/runs/43721872541) completed successfully.

Download the Windows installers: [Pest 0.10.0](https://github.com/zelmore219-lang/backwoods-brew-releases/releases/download/pest-0.10.0/Backwoods-Pest-Control-Setup-0.10.0.exe), [Employee 0.4.9](https://github.com/zelmore219-lang/backwoods-brew-releases/releases/download/employees-0.4.9/Backwoods-Employees-Setup-0.4.9.exe), [Accounting 1.0.11](https://github.com/zelmore219-lang/backwoods-accounting-/releases/download/apps-pest-integration-2026-11-15/Backwoods-Business-Accounting-Setup-1.0.11.exe).
