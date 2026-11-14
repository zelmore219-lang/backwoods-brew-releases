# Backwoods Driver 0.5.1

Fixes the greyed-out **Clock Out** button when an earlier Clock In is still
awaiting synchronization or office review. Clock Out saves the end time on the
device, stops shift location sharing, and keeps the Backwoods account signed in.
Saved punches survive restart. Original capture times are retained for ordered
synchronization and review; payroll approval is not bypassed.

The update recovers the old missing-setup error once shared timekeeping is
activated and reconciles interrupted server acknowledgements without duplicating
time punches. A new shift requires activated shared timekeeping.

**Windows:** open **Backwoods Driver → App updates**, check for updates, then
download and install 0.5.1. The direct Windows setup also updates the existing
installation. Keep the same Windows user account and installation location.

**Android:** this APK updates **Backwoods Driver (New)** 0.5.0 using the same
package and signing key, preserving its saved data. Accept Android's standard
installation confirmation. For the older original Driver package, this remains
a separate app; keep its existing records and synchronize pending work before
switching. No uninstall or data clearing is required.

The free shared owner service must remain online for central administration and
payroll synchronization. Its live heartbeat and shared-clock readiness were
verified during this repair. Actual employee/job/payroll mappings still require
the business owner's review.

Verification includes isolated clock/security/browser regressions, actual
Windows install/reinstall and pending-clock UI checks, and Android native clock,
GPS, delivery/signature, completed history and printed PDF acceptance. Physical
business-device and printer checks remain. Tests use fictitious records only.
