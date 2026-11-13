# Driver 0.5.0 setup

1. **Update the HR Windows PC.** Install Employee 0.4.2 using the same Windows
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
4. **Install Driver.** On Windows, run the Driver 0.5.0 setup once to gain the
   updater. On Android, synchronize pending work in the original Driver app,
   then install **Backwoods Driver (New)** alongside it. Keep the original app
   and its records. Sign in with the existing Backwoods username and password.
5. **Check the actual device.** Clock in, allow location and visible shift
   notifications, confirm the actual route, and select the intended printer.
   Android may require enabling the printer's own print service. Standard
   Android/Windows installation confirmations still apply to future updates.

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
