"""Core business logic for a rotating susu savings group."""
from decimal import Decimal, InvalidOperation


class SusuError(ValueError):
    """Raised when a susu group operation violates a rule."""


def to_pesewas(value) -> int:
    """Convert a GHS amount to exact integer pesewas."""
    try:
        amount = Decimal(str(value).strip())
    except (InvalidOperation, AttributeError) as exc:
        raise SusuError("Enter a valid money amount, e.g. 50.00.") from exc
    if not amount.is_finite():
        raise SusuError("Amount must be a finite number.")
    if amount <= 0:
        raise SusuError("Amount must be greater than zero.")
    if amount.as_tuple().exponent < -2:
        raise SusuError("Amounts may have at most two decimal places.")
    return int(amount * 100)


def format_money(pesewas: int) -> str:
    return f"{pesewas // 100}.{pesewas % 100:02d}"


class SusuGroup:
    """One rotating savings group with a fixed weekly contribution."""

    def __init__(self, weekly_contribution):
        self.weekly_contribution = to_pesewas(weekly_contribution)
        self.members: list[str] = []
        self.current_week = 1
        self._payments: dict[int, dict[str, int]] = {1: {}}
        self.payout_history: list[dict] = []

    def add_member(self, name: str) -> None:
        if not isinstance(name, str) or not name.strip():
            raise SusuError("Member name/ID cannot be blank.")
        name = name.strip()
        if any(existing.casefold() == name.casefold() for existing in self.members):
            raise SusuError(f"Duplicate member: {name}.")
        if self.current_week != 1 or self._payments[1]:
            raise SusuError("Members can only be added before any contribution is recorded in week 1.")
        self.members.append(name)

    def record_contribution(self, member: str, amount) -> None:
        if member not in self.members:
            raise SusuError(f"Unknown member: {member}.")
        payment = to_pesewas(amount)
        week_payments = self._payments[self.current_week]
        already_paid = week_payments.get(member, 0)
        remaining = self.weekly_contribution - already_paid
        if payment > remaining:
            raise SusuError(f"{member} owes only GHS {format_money(remaining)} for week {self.current_week}.")
        week_payments[member] = already_paid + payment

    def close_week(self) -> dict:
        if not self.members:
            raise SusuError("Add at least one member before closing a week.")
        payments = self._payments[self.current_week]
        owes = {
            member: self.weekly_contribution - payments.get(member, 0)
            for member in self.members
            if payments.get(member, 0) < self.weekly_contribution
        }
        if owes:
            return {"closed": False, "week": self.current_week,
                    "owes": {member: format_money(amount) for member, amount in owes.items()}}

        recipient = self.members[(self.current_week - 1) % len(self.members)]
        pot = self.weekly_contribution * len(self.members)
        self.payout_history.append({"week": self.current_week, "recipient": recipient, "amount_pesewas": pot})
        closed_week = self.current_week
        self.current_week += 1
        self._payments[self.current_week] = {}
        return {"closed": True, "week": closed_week, "recipient": recipient, "payout": format_money(pot)}

    def report(self) -> str:
        lines = ["SUSU GROUP REPORT", f"Weekly contribution: GHS {format_money(self.weekly_contribution)}",
                 f"Current week: {self.current_week}",
                 f"Members (payout order): {', '.join(self.members) if self.members else '(none)'}", "",
                 f"Week {self.current_week} contributions:"]
        payments = self._payments[self.current_week]
        for member in self.members:
            paid = payments.get(member, 0)
            remaining = self.weekly_contribution - paid
            status = "PAID IN FULL" if remaining == 0 else f"OWES GHS {format_money(remaining)}"
            lines.append(f"- {member}: paid GHS {format_money(paid)}; {status}")
        lines.extend(["", "PAYOUT HISTORY:"])
        if not self.payout_history:
            lines.append("- No payouts yet.")
        else:
            for item in self.payout_history:
                lines.append(f"- Week {item['week']}: {item['recipient']} received GHS {format_money(item['amount_pesewas'])}")
        return "\n".join(lines)
