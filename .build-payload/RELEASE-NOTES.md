# Employee Windows 0.4.6 — Vendor time and Accounting connection

- Vendor Clock In / Clock Out uses the existing shared Employee UID, active
  Wholesale access and actual Wholesale job. Owner service performs the punch
  with server timestamps in the existing shared active-shift transaction.
- Employee administrators can review Vendor records with Main, Driver and
  Employee time, including original source, division/job, correction history and
  approval status. Delayed/offline clock actions require office review. Retry
  IDs prevent duplicate punches, cards and financial sources.
- Accounting application access can be granted as owner/accountant/viewer from
  the existing Employee profile. Accounting 1.0.8 can use that same password and
  UID; staff do not need a second personnel login.
- Authorized owner/payroll views publish a private read-only roster and complete
  current approved hours/paid leave for Accounting. Stale approvals are withheld
  with a reason. Personnel forms, SSNs, bank details, emergency contacts and
  employee passwords are never in that feed.
- Obsolete private view chunks are retired when permissions change, so a lower
  role cannot fetch an earlier privileged payroll projection. Original records
  remain in the private Employee database.
- Paper onboarding, automatic approval dates, activation verification, PTO,
  Hours & pay and the existing manual approved-time download remain intact.
  Employee does not process payroll or require Gusto enrollment.

## Owner steps

1. Update the existing Windows installation using the same account and data.
2. Open **Owner service → Connect or manage owner service… → Start service**.
   Keep that PC running. Reuse the existing Firebase configuration; no new
   project, billing upgrade or rule deployment is required for this extension.
3. In **People → View**, confirm the actual person's shared login/verified UID,
   active employment, changed temporary password and actual Wholesale job.
   **Application access → Assign access → wholesale** grants Vendor access.
   Assign **accounting** separately for authorized financial staff.
4. Vendor 4.1.9: same username/password → **Clock In / Clock Out**. Employee:
   **Time & attendance → Shared time cards → Refresh → Review**. Complete
   approved workweeks/timesheets before Accounting **Sync approved Employee
   hours**. Do not link the reported jboozer/jcopeland shift to zstyles by name.
5. Accounting 1.0.8: **Payroll Management → Connect Employee**, review workspace
   and select the actual legal company. HR.my/provider preparation, receipt,
   final-result accounting and bank reconciliation happen in Accounting and the
   actual external service, not Employee.

## Validation / limits

Disposable real Auth/Firestore integration covers Vendor username login,
P-256 encrypted owner relay, cross-device active state, lost responses, offline
retry, review permissions, original timestamp protection and department display
on desktop/tablet/phone. Real approved Employee hours reach the same Accounting
ledger; staff use the same UID/password, revoked grants are denied, stale or
withdrawn approvals are not eligible. Permission downgrades retire obsolete
private payroll projections and their chunks. No live personnel, source timecards,
activations, provider submissions or bank payments were altered by testing.

The existing public Employee Android package is retained; a new unsigned CI
Android build is not a compatible published update without its original signing
identity. Main/Vendor/Accounting Android builds use their retained signing key.
Production's unshipped source remains missing, so manufacturing integration is
not claimed. See Accounting's `docs/COORDINATED-OWNER-GUIDE.md` for the full owner
workflow and provider-dependent configuration.

Windows acceptance passed: https://github.com/zelmore219-lang/backwoods-brew-android/actions/runs/43635778527 .
Source: f00c69b810f864e9d799fe955de76164d9518c2b. Installer SHA-256: aa10ef7455e59c84264add88f1ec42c7d7780c483b98ade15c7f30ac7d88ee5a.

[Open the complete owner setup and payroll guide](https://github.com/zelmore219-lang/backwoods-accounting-/releases/tag/apps-coordinated-2026-11-14).
