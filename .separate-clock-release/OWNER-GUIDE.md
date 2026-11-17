# Shared PIN time clock

This change adds one registered-device PIN clock to Employee, Main, Vendor,
Driver, Pest Control and the separate **Backwoods Time Clock** app. **Every
login-screen Time Clock and the separate app support both Clock In and Clock
Out.** A punch is recorded only after the employee confirms the next action.

## Source and existing records

The Employee source is in `zelmore219-lang/backwoods-brew-android/employee-app`.
The existing Windows 0.4.12 release identifies source
`8cbb47690b73f863e2dbc39e25a4ffbebf012a79`; its Production connection and owner
startup/request-context fixes are retained. Main and Vendor's connected build
inputs live in `backwoods-accounting-/source-app-updates` and `android-apps`.
Driver uses `driver_routeplanner`; Pest uses `backwoods-brew-window-original1`.

The authoritative records remain `employeeTimecards`, `employeeClockStates` and
`employeeTimeEvents` in the existing Backwoods Firestore project. The existing
Employee SQLite database retains its employee IDs, job assignments, reviews,
original versions, approved timesheets and payroll/export logic. Main's original
timecard arrays and Employee's original SQL punches remain accessible. New Main
clock controls submit to the owner operation instead of editing local arrays.

Migration 015 adds protected PIN history, device registrations, attempt counters,
short-lived confirmation tickets and immutable request receipts. PIN issuance
uses strings and a keyed verifier; retired codes are not reassigned. Five failed
attempts on a registered device block further PIN checks for five minutes. A PIN
reset also invalidates pending confirmations. No PIN is retained in browser
storage, analytics, request logs or plaintext relay records.

The owner operation checks the current employment status, account grants, device
revocation and exact existing UID mappings. Pest uses the existing verified
Pest/Employee link; it does not infer a link from a name or email. A device Auth
identity has no ordinary app or personnel access. It can submit only encrypted
clock requests. A PIN never creates a regular app session.

## Rollout

1. Back up the existing Employee data and retain its document encryption key.
   Build/install the updated Employee edition using the existing Windows build
   workflow. Android's bundled program is refreshed by `scripts/prepare_android.py`.
   Keep the existing owner workspace and Google connection.
2. Export and review the **current live Firestore rules**, including Production,
   Driver and Accounting permissions. Run:

   ```sh
   python scripts/upgrade_clock_rules.py live.rules reviewed.rules --expected-sha256 SHA256_OF_LIVE_RULES
   ```

   The helper changes the known Employee relay namespace and clock-write guards;
   it refuses an unknown namespace/permission shape. Review, emulator-test and
   deploy the result to the existing Backwoods project. The two checked-in
   `deploy/pin-clock*.merged.rules` files are compiled reference snapshots, not a
   substitute for reviewing the actual live rules. No live rules were deployed
   during implementation.
3. Install the updated Main, Vendor, Driver and Pest builds. Main/Vendor's Android
   web inputs are updated as well. Rebuild those APKs/installers through their
   existing release workflows; the implementation does not replace update feeds.
   For future source edits, run `scripts/sync_shared_clock.py` with the three
   checkout paths before rebuilding consuming apps.
4. Start Employee's **Owner service** and wait for it to be online. The service
   advertises `pinClockVersion: 1`. New punches require connectivity and the
   running owner service. The source apps keep their normal account sign-in.
5. In **People → employee profile → Time clock PIN**, use **Generate PIN** or
   **Reset PIN** and give the displayed code to the employee. Verify the actual
   job, business and work location in the existing employee record.
6. In **People → Time-clock devices**, register and name each shared device at its
   actual business/location. Paste the issued device pairing code into the app
   on that device. Pair each app installation that will expose a login clock.
   Revoke retired/lost installations from this screen.
7. For Pest signed-in punches, retain/complete **Employee & Accounting → Connect
   Employee → Link verified accounts** for the same real staff member. Owner-
   approved Pest application access and the actual Pest job are required. The
   customer portal has no clock controls.
8. Deploy the separate app's prepared `clock-app/web` at an HTTPS origin/path for
   tablet installation, or use its independent Windows package. It opens directly
   to the keypad after registration and returns there after either punch.

Old unsent Driver/Pest/Vendor offline requests are retained for recovery/review;
new shared-clock buttons do not claim to record time offline. Resolve earlier
queued work before relying on a new device. Original records are not discarded.

## Review, corrections and payroll

**My Timecard** is on Employee's home screen. **Time & attendance → Shared time
cards** displays all authorized sources and filters by business and department.
Times use the assigned business location's configured timezone. Clock-out keeps
the business/job recorded at clock-in, including when it comes from another app.

Employees use **Request correction** or the existing missed-punch request form.
Authorized reviewers approve, reject or correct using the existing audited
workflow. The original version, request, reason and reviewer remain available.
Approved corrected hours flow into the existing timesheet/payroll exports; the
existing second-person review and completed-workweek requirements still apply.

## Verification

Executed on disposable Auth/Firestore emulators and fictitious employee records:

- Separate-app/warehouse PIN clock-in and authenticated Driver clock-out produce
  one card, two source-labelled events, and one payroll job/business.
- Every registered Main, Vendor, Driver, Pest and separate-app login clock can
  clock out a shift started in the separate app.
- Pest-office PIN clock-in and signed-staff clock-out keep one Pest Control card;
  another app sees that open shift and cannot create an overlapping one. This
  new-path test supplies an already verified Pest profile; live cross-project
  credentials and the full deployed Pest flow remain commissioning checks.
- Leading-zero PINs, reset tickets, inactive employees, revoked devices, attempt
  limits, duplicate requests, concurrent confirmations, status changes and a
  process failure after Firestore commit are covered.
- The actual WebCrypto relay recovers a deliberately lost reply without saving
  a PIN or creating a second shift. Device credentials cannot read Main data.
- An employee-requested correction retains the original version, is reviewed by
  another person, and produces the expected eight approved payroll hours/export.
- Actual Vendor username sign-in, punches and Employee visibility are tested at
  desktop, tablet and phone widths. Shared UI browser checks cover all login
  entries plus the separate app's direct keypad, masking, Clear/Backspace, both
  punch actions, privacy timeout and recovery.

The full ordinary Employee suite, desktop Node checks, Driver tests/build, Pest
checks/build and Main source verification are also run. Emulator-only suites are
reported separately from skipped tests in ordinary discovery. Physical tablet
acceptance, Windows installation, live owner-service/account commissioning, APK
signing and production deployment are not established by these tests.
