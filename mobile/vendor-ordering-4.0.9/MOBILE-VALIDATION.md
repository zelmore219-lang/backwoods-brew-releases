# Vendor Ordering 4.0.9 validation

Passed: 17 sync-engine tests and 9 Playwright tests (26 total), web/native build, Android APK compilation/packaging/signature validation, Windows portable packaging and PE validation, Android/iOS configuration syntax and dependency lockfile checks. Android uses the 4.0.8 test build’s signer with higher version code 3.

Replication tests use a shared simulated cloud and two independent React stores. Production Firebase access, real user accounts/rules, hardware, and running the Windows executable were not tested in this Linux environment. No production rules or company data were modified. The iOS project was synced but was not compiled/signed without Mac/Xcode.

See SYNC-UPDATE-4.0.9.md for mandatory upgrade steps, preserved-data recovery, Firebase permissions, and same-field conflict limits. Both Android and Windows need updating; the main accounting app is outside this change.
