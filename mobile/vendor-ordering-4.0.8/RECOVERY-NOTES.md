# Vendor Ordering 4.0.8 recovery

The split 7-Zip parts were reassembled and contained a ZIP with the Windows `app.asar`. Its package manifest identifies `backwoods-vendor-ordering`, version **4.0.8**. This is the newest version supplied in this conversation; it does not establish that no later version exists elsewhere.

Recovered from the packaged application:

- 48 original JavaScript/JSX source files from source-map `sourcesContent`, including the newer catalog, imports, sync log, settlements, scanner, offline authentication, and queued sync logic.
- The packaged production CSS, retained as src/styles.css. Original CSS formatting and comments were not present.
- Public icons, Brewfoot brand image, and Electron main/preload files.
- The packaged dependency manifest. Development/build scripts and Capacitor projects were reconstructed using the earlier tested mobile setup; the original 4.0.8 development configuration/lockfile was not included in the ASAR.

The recovered application source remains unchanged except six files adapted for native initialization, mobile navigation, GPS, native catalog exports/printing, and explicit test-only demo mode. Additional mobile helpers/styles are included. The newer scanner implementation and business/authentication/sync logic are retained.

The six required Firebase web-client settings match the archived production bundle. The local .env is excluded from the source download; use your original environment settings when rebuilding. No desktop user database, passwords, saved sessions, production order data, or signing keys are part of this recovery or download.

The Android APK uses the same application ID and debug signer as the prior 4.0 mobile test APK, with a higher version code. Install it as an update; do not uninstall the previous app to update. Back up business data before testing an upgrade.

The iOS project is prepared but still needs a Mac/Xcode build and Apple signing. Native hardware dialogs, camera/GPS, printer output and live account/cloud synchronization need real-device validation.

Original ASAR SHA-256: `5d9574211fb10f98381af03369eb084c95425c082ac5120ee6824dfbf2c9fd07`
