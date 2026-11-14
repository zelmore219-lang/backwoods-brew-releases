# Backwoods Brew app downloads

- [Driver 0.5.1 — Windows and Android](https://github.com/zelmore219-lang/backwoods-brew-releases/releases/tag/driver-0.5.1)
- [Employee 0.4.3 — Windows and Android](https://github.com/zelmore219-lang/backwoods-brew-releases/releases/tag/employees-0.4.3)

Driver 0.5.1 fixes **Clock Out being greyed out when Clock In is pending**.
It saves the end time, stops shift GPS and retains the original punches for
synchronization and review. It keeps the Backwoods account signed in.

On Windows, use **Backwoods Driver → App updates** to install 0.5.1. The direct
Windows setup also updates the existing installation. The original Driver 0.4.0
needs that direct setup once to add its updater. Keep the same Windows account
and installation location. Install/reinstall data preservation is tested.

The Android APK updates **Backwoods Driver (New)** 0.5.0 using its retained key
and package, preserving its device records. The older original Driver app has a
different, unavailable key and remains separate; keep its records and synchronize
pending work before switching. Employee 0.4.3 Android updates 0.4.1/0.4.2 using
its retained key; legacy Employee 0.3.0-full has a different signing identity.

For shared accounts, timecards and approved Driver invoice revisions, keep the
actual HR PC's Employee **Owner service** online. Firebase stays on its free
plan. The live heartbeat and shared-clock readiness have been verified. Actual
employee/payroll mappings, business devices and physical printers require owner
acceptance. See [setup steps](DRIVER-SETUP.md) and the [updated checklist](DRIVER-CHECKLIST.md).

Driver and Employee have separate verified update feeds. The Main, Vendor and
Accounting feeds are preserved. Separate onboarding document drafting and
Production app work remain queued.
