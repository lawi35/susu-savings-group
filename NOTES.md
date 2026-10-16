# Assumptions and Design Notes

## Decisions and assumptions

1. **Member identity:** A member is identified by name/ID. Duplicate detection is case-insensitive and ignores leading/trailing spaces.
2. **Payout order:** Members receive the pot in the order they were added. The order repeats cyclically if the group continues beyond one round.
3. **When members may be added:** Members can be added only before any contribution has been recorded in week 1. This avoids changing the expected pot after the cycle has started.
4. **Partial payments:** A member may pay in multiple instalments during the current week. The total cannot exceed the weekly contribution.
5. **Week closure:** A week closes only when every member has paid the full contribution. An unsuccessful close leaves the week unchanged and returns each outstanding balance.
6. **Payout amount:** The pot is the fixed weekly contribution multiplied by the number of members. Payout is recorded only after all contributions are complete.
7. **Money precision:** Amounts are converted to integer pesewas; inputs with more than two decimal places are rejected.
8. **Persistence:** Data exists only while the program is running. Restarting the program starts a new group.
9. **Dates and audit trail:** Dates, timestamps, receipts, reversals, and authentication are outside the current scope.

## What I would improve with more time

- Add SQLite persistence and database migrations.
- Add member IDs separate from display names.
- Record timestamps and payment transaction IDs.
- Add a safe correction/reversal process with an audit log.
- Add a structured JSON report/export.
- Add role-based access, backups, and operational safeguards before real-world use.
