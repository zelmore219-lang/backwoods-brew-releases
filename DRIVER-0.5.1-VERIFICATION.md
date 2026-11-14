# Driver 0.5.1: pending Clock Out repair

When 0.5.0 retained an unconfirmed Clock In, its online queue disabled every
clock button, including Clock Out. Missing shared timekeeping setup could leave
that Clock In requiring attention indefinitely.

0.5.1 allows the signed-in driver to close the existing local shift while its
earlier punch is pending. It durably records Clock Out before stopping location
sharing, retains both original capture times, and keeps the account signed in.
A restart restores the closed local shift. Synchronization remains ordered;
disputed punches still need review, and payroll approval is not bypassed.

After shared timekeeping becomes available, the exact legacy setup error can
retry automatically. A server-confirmed event reconciles an interrupted local
acknowledgement without duplicating a punch. A new shift cannot start while
shared timekeeping has not been activated.

Verification before publication:

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
