import unittest
from susu import SusuGroup, SusuError


class SusuGroupTests(unittest.TestCase):
    def setUp(self):
        self.group = SusuGroup("50.00")
        for member in ("Ama", "Kofi", "Esi"):
            self.group.add_member(member)

    def test_partial_payment_then_full_payment(self):
        self.group.record_contribution("Ama", "50.00")
        self.group.record_contribution("Kofi", "50.00")
        self.group.record_contribution("Esi", "30.00")
        result = self.group.close_week()
        self.assertFalse(result["closed"])
        self.assertEqual(result["owes"], {"Esi": "20.00"})
        self.group.record_contribution("Esi", "20.00")
        result = self.group.close_week()
        self.assertTrue(result["closed"])
        self.assertEqual(result["recipient"], "Ama")
        self.assertEqual(result["payout"], "150.00")
        self.assertEqual(self.group.current_week, 2)

    def test_week_cannot_close_when_member_owes(self):
        self.group.record_contribution("Ama", "50.00")
        result = self.group.close_week()
        self.assertFalse(result["closed"])
        self.assertEqual(result["owes"], {"Kofi": "50.00", "Esi": "50.00"})
        self.assertEqual(self.group.current_week, 1)
        self.assertEqual(self.group.payout_history, [])

    def test_unknown_member_rejected(self):
        with self.assertRaises(SusuError):
            self.group.record_contribution("Yaw", "10.00")

    def test_duplicate_member_rejected_case_insensitive(self):
        with self.assertRaises(SusuError):
            self.group.add_member("ama")

    def test_zero_and_negative_payments_rejected(self):
        for amount in ("0", "-1.00"):
            with self.assertRaises(SusuError):
                self.group.record_contribution("Ama", amount)

    def test_overpayment_rejected(self):
        with self.assertRaises(SusuError):
            self.group.record_contribution("Ama", "50.01")

    def test_exact_decimal_money(self):
        group = SusuGroup("0.10")
        group.add_member("A")
        group.add_member("B")
        group.record_contribution("A", "0.10")
        group.record_contribution("B", "0.10")
        result = group.close_week()
        self.assertEqual(result["payout"], "0.20")

    def test_members_cannot_be_added_after_payments_start(self):
        self.group.record_contribution("Ama", "1.00")
        with self.assertRaises(SusuError):
            self.group.add_member("Yaw")

    def test_report_shows_current_week_and_payout_history(self):
        for member in self.group.members:
            self.group.record_contribution(member, "50.00")
        self.group.close_week()
        report = self.group.report()
        self.assertIn("Current week: 2", report)
        self.assertIn("Week 1: Ama received GHS 150.00", report)
        self.assertIn("Kofi: paid GHS 0.00; OWES GHS 50.00", report)


if __name__ == "__main__":
    unittest.main()
