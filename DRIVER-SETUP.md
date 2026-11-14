# Driver 0.5.1 setup

1. **Update the HR Windows PC.** Install Employee 0.4.3 using the same Windows
   account as the existing Employee program. Existing employee records and the
   encrypted document key remain in place.
2. **Start the free owner service.** Open Employee's **Owner service → Connect
   or manage owner service**. Connect the Google owner of the existing Backwoods
   Firebase project, review the existing HR owner/Main account association and
   start the service. Keep this PC awake, signed in and online during operations.
3. **Review actual employee records.** Link each Driver's existing Firebase UID
   to their actual HR record and grant the appropriate Driver/Employee access.
   Review each Driver's actual company, wholesale division, delivery job and
   workweek in **Time & attendance → Shared time cards** before approving payroll.
   The app does not create employee wages, retail stores or company books.
4. **Update Driver.** On Windows, open **Backwoods Driver → App updates** and
   install 0.5.1, or run the 0.5.1 Windows setup over the existing installation.
   The original 0.4.0 Windows app needs that direct setup once to gain the updater.
   On Android, update **Backwoods Driver (New)** 0.5.0 with the 0.5.1 APK; its
   package and signing key are unchanged. For the older original Driver app,
   synchronize pending work before switching to the separate new app. Keep
   existing apps and records. Use the existing Backwoods username and password.
5. **Check the actual device.** Clock in, allow location and visible shift
   notifications, confirm the actual route, and select the intended printer.
   Android may require enabling the printer's own print service. Select the
   printer's correct paper width in its print settings; Save as PDF may retain
   the system's Letter paper even with the narrow receipt layout. Standard
   Android/Windows installation confirmations still apply to future updates.

If Clock Out was greyed out, update to 0.5.1 and press **Clock Out**. The app
retains both punch times and stops location sharing while synchronization is
pending. Keep the app's saved data. Review any pending timecard warnings with
the office; do not create a second shift to replace the original punches.

Completed Invoices retains saved signed versions with delivery dates and supports
full-page or 80 mm reprints. For material corrections, a Wholesale administrator
reviews the proposed change and issues an expiring code in **Invoice corrections**.
The customer signs the revised invoice. The owner service preserves the original
and revised versions and updates the existing Wholesale inventory and company
Accounting ledger together. Closed periods or corrections requiring refunds stay
for Finance review. The service cannot validate approvals while the owner PC is
offline; pending requests and signatures remain saved for later synchronization.

Automated acceptance uses disposable Windows/Android devices, isolated Firebase
emulators and fictitious records. Actual company HR/job mappings, the owner PC
and physical tablet/printer acceptance require the business devices.
