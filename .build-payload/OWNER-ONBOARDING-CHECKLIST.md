# Employee Windows 0.4.7 — finish compatible Android release signing

The newer paper onboarding, automatic dates, Hours & pay, PTO and connected
Vendor/Accounting features are in the Android source, but the public signed
Android APK is still 0.4.3. A replacement signing key cannot update it.

Windows 0.4.7 adds a trusted owner-only setup for recovering the retained Android
key from its existing private Firebase backup. It verifies the actual PKCS12
password, alias, matching private/public key and installed certificate before
copying anything. Google authorization and employee data never enter the signing
setup. No replacement key or Firebase project is created.

## One-time owner action after installing Windows 0.4.7

1. **Owner service → Connect or manage owner service…**. Keep the existing
   connected, reviewed owner association and running service.
2. Scroll to **Android release signing** and select **Open private GitHub secret
   settings**. In the existing private `backwoods-brew-android` repository,
   create a secret named **EMPLOYEE_ANDROID_SIGNING_JSON**.
3. Return to Employee, check **I will store this signing setup only in the
   private GitHub repository secret**, and select **Copy verified Android
   signing setup**. Paste only into that private GitHub secret's value and
   choose **Add secret**. The clipboard clears after two minutes if unchanged.
   Do not paste the signing setup into chat, an issue or a public file.
4. The compatible Android release builder can then use the retained identity,
   test the embedded engine, sign the exact accepted APK and test upgrading the
   actual public 0.4.3 package plus reinstall/data preservation. Only accepted
   signed bytes may be published; this Windows update alone does not update the
   public Android feed.

If the owner connection cannot read the backup, or it does not match the
installed certificate, setup stops with a reason and copies no key. Existing
records, document encryption keys, Google connection and application grants are
preserved. Employee Android's old legacy 0.3.0-full signing identity remains a
separate unrecovered key; never uninstall that app to bypass a mismatch.

## Verification

Tests cover rejected wrong keys/passwords/aliases, missing backup, explicit
trusted-window confirmation, no key exposure to the renderer/state/configuration,
and retained owner-service behavior. Source Android login text now describes
hours/PTO and directs payroll processing to Business Accounting.
Installed Windows and Android acceptance are recorded by the release workflows;
the real owner must still perform the one-time private secret setup above.
