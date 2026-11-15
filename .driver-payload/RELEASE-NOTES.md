# Backwoods Driver Windows 0.5.2

**Retry clock sync** now refreshes server timecards even when no clock actions remain on the device. It waits for an automatic send already in progress and reports completion, pending review, offline state, retained rejection or a bounded timeout. Original punch IDs/timestamps and server review requirements are preserved.

Windows updates the existing Driver installation. Save work and install over the existing program using the same Windows account. No uninstall or data reset is needed.

This release contains Windows only. The public Android 0.5.1 APK is retained and passed native installation, sign-in-screen, rotation and reinstall checks. The 0.5.2 Android source/build is prepared, but publication requires its existing private signing key; no incompatible replacement key is generated.

Unit, rules, actual browser/clock, native Android source and published Windows acceptance were rerun with fictitious records. This installer additionally must pass its own Windows install/reinstall, record preservation, clock, native location IPC and invoice-PDF checks before publication. Live Employee links and office reviews still require the owner to verify the exact person/UID, job, times and breaks.
