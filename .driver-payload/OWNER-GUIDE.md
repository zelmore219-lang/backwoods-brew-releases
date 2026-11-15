# Driver clock retry and Employee import

Retry clock sync previously had no completion result, did not reload a shift
when its local upload queue was empty, and could silently return while an
automatic send was in progress. A server snapshot also cleared the visible
error even when the original attention row remained on the device.

The retry now waits for the current send, retries retained attention rows in
their original order, reloads the server even with an empty queue, and reports
completion, offline state, a retained rejection, or a bounded connection
timeout. The original request IDs, shift IDs and captured timestamps remain
unchanged. Retained errors survive a fresh snapshot. An expanded My time cards
list stays expanded during refresh. Current server-published office review and
verified Employee linkage are shown without rewriting the original timecard.
An approval for an older event cannot hide a newer event's required review.

Local verification: unit suite, lint and production build; browser regression
for inactive-to-active retry, simultaneous automatic send, empty queue refresh,
offline/error/timeout feedback, current versus stale office approval, original
timestamps and duplicate prevention; actual Driver clock service/rules and
clock/restart/setup-recovery browser workflows against loopback emulators.

The complementary Employee repair refreshes unchanged cached timecards after
an owner verifies the exact Firebase UID. Windows 0.5.2 packages the retry feedback repair after exact installer acceptance. Android publication still requires the retained signing key. No live personnel, clock or payroll data was
changed by verification.

For an existing installation, on the owner PC open Owner service → Connect or
manage owner service… → Service controls → Stop service → Start service and
wait for the service to be online. This starts a full import. Open Employee →
Time & attendance → Shared time cards → Refresh with filters cleared. If the
shift appears, use Review, select the employee's actual existing payroll job,
verify the original timestamps and actual unpaid breaks, enter the review
reason, then Save review. Retry sync does not approve payroll hours.
