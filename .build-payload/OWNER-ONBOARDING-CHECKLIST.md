# Backwoods Employees 0.4.5

Employee is the workforce app: onboarding, shared timecards, time approval and
denial, hours and estimated gross pay by department, and PTO. Payroll processing,
taxes, deductions, payroll results and payments belong in Business Accounting.
The Employee screens and command API no longer offer payroll processing or a
Gusto connection. Historical payroll records remain in the existing database
and backups. Existing Backwoods identities, documents and time punches stay in
place.

## Owner setup and onboarding

1. Install the Windows update using the same Windows account and existing data.
   Open Owner service → Connect or manage owner service… and keep Start service
   running. No new Firebase project, sign-in or billing plan is needed for an
   already connected owner PC.
2. People → View the actual employee. In Connected Backwoods accounts, link the
   existing Driver login to that person's matching Employee profile and exact
   verified UID. Use the existing employee record and password. A timecard's
   username may differ from another employee you checked earlier; confirm the
   actual worker before linking hours.
3. People → View → Prepare paper onboarding packet. The Packet approval date
   fills itself using the organization timezone; the server records the actual
   approval date. Handbook version or reference is optional. Enter the actual
   paper-file storage location and approve the checklist, then Approve and
   assign paper packet. An Activate employee dialog with draft blockers also
   opens this setup directly. All five required paper acknowledgments are
   assigned and unfinished starter drafts are replaced. The previous handbook
   reference and storage location are remembered. Repeating this on another
   day does not redate or replace unchanged signed paperwork.
4. The employee completes the W-4, Alabama A-4, I-9, handbook acknowledgment
   and emergency contact paper originals. In My workspace → View → Acknowledge
   paper completion, enter the employee's full name, confirm completion and
   signature consent, then Sign acknowledgment for each assignment.
5. A different authorized owner / HR reviewer uses Documents → Review → Approve
   document to confirm each actual paper original and storage reference. I-9
   also requires its actual verifier examination and retention details. No
   document upload is required. Finish any required password change, actual job
   assignment and training completion/verification, then Activate employee.

## Hours, gross pay and PTO

- Time & attendance → Shared time cards collects connected Main, Driver and
  Employee clocks. Department and work-location labels come from the reviewed
  payroll job, never from a guessed home department or retail store. Owner
  service now refreshes old unchanged records after a verified identity link.
  Driver-only workspaces can open shared timecards without a saved Main record.
- Use Review to confirm offline clock times, actual unpaid breaks and the
  employee's actual job. Owner / managers can approve or deny shared timecards
  and submitted timesheets. Denying a timesheet preserves its original clock
  history and lets the employee correct and resubmit it.
- Hours & pay → choose company, period, employee and department → Calculate
  hours & pay. See regular/OT hours and estimated hourly gross wages before
  taxes/deductions. Open or disputed records show their reason rather than a
  guessed wage. Salary arrangements remain identified for Accounting review.
- Time & attendance / Hours & pay → PTO balances. Owner / HR uses Adjust PTO
  balance for actual earned/opening hours or documented corrections. No accrual
  policy is assumed. Employee: Scheduling → Request time off. Manager: Review
  the request, approve/deny it, enter actual paid hours and the actual job.
  Approved usage reduces the balance once. Denials do not consume PTO. Paid
  leave remains separate from worked hours and does not increase overtime.

## Accounting handoff

After timecards and the complete timesheets are approved, open Hours & pay,
choose the company and a period containing complete approved timesheets, then
Download approved time & PTO. This download includes all departments for that
company/period; employee and department filters only narrow the preview.

Extract the ZIP. It contains business-accounting-time.json, department totals,
approved hours / estimated gross wages, approved time off and supporting
timecards. Money fields ending in Cents are integer cents. In Business Accounting
1.0.7 or later, open Connect apps → Source app: Employee Employer app, choose
business-accounting-time.json, Preview import, then Import into company ledger.
Payroll & employees shows the approved Employee hours & PTO for payroll review.
Importing hours does not post wages, pay staff or file taxes. Reimporting the same
records does not duplicate them. Complete payroll and HR.my result entry in
Business Accounting, not in Employee.

## Verification before Windows packaging

126 ordinary Python tests: 107 passed, 19 explicit emulator skips. The new
browser workflow covers actual draft recovery, automatic dates, department pay
progress, employee PTO request / owner approval, original Employee timecards in
the ZIP, and actual Accounting UI import / duplicate retry. The existing
17-check browser workflow also passes, including five paper signatures,
separate original review, I-9 evidence and activation without uploads. No live
company records or payments were changed. Windows install/reinstall verification
and owner-device acceptance are separate from these local checks.

Windows acceptance passed: https://github.com/zelmore219-lang/backwoods-brew-android/actions/runs/43617489601 .
Source: b15fe1a91c75753d1e17c624cc3f9949ce799951. Installer SHA-256: cf02f994401b238eb5212ccc654f42ea04c5a7e2eb4af9a9dc7b1b1db53075c1.
