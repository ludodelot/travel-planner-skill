import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import free_trip as ft  # noqa: E402

REMOTE = (ft.TUESDAY, ft.FRIDAY)


class FreeTripTest(unittest.TestCase):
    def test_weekend_abroad_with_holiday_monday_and_remote_tuesday(self):
        cost = ft.trip_cost(
            "2026-11-07", "2026-11-10", REMOTE, holidays=["2026-11-09"],
            back_home_to_work_last_day=True,
        )
        self.assertTrue(cost.is_free)
        self.assertEqual([d.kind for d in cost.days], ["weekend", "weekend", "holiday", "remote"])

    def test_bridge_with_remote_friday_leaving_after_work(self):
        cost = ft.trip_cost(
            "2026-10-30", "2026-11-02", REMOTE, holidays=["2026-11-02"],
            leave_after_work_first_day=True,
        )
        self.assertTrue(cost.is_free)

    def test_return_on_working_monday_costs_a_day(self):
        cost = ft.trip_cost("2026-11-27", "2026-11-30", REMOTE, leave_after_work_first_day=True)
        self.assertEqual(cost.vacation_days, 1)
        self.assertEqual(cost.days[-1].kind, "office")

    def test_remote_abroad_not_allowed_costs_the_remote_day(self):
        cost = ft.trip_cost("2026-11-13", "2026-11-15", REMOTE, remote_abroad=False)
        self.assertEqual(cost.vacation_days, 1)
        self.assertIn("not allowed", cost.days[0].reason)

    def test_remote_abroad_allowed_is_free(self):
        cost = ft.trip_cost("2026-11-13", "2026-11-15", REMOTE, remote_abroad=True)
        self.assertTrue(cost.is_free)

    def test_thursday_to_sunday_needs_two_days_without_flexibility(self):
        cost = ft.trip_cost("2026-11-12", "2026-11-15", REMOTE)
        self.assertEqual(cost.vacation_days, 2)

    def test_invalid_range(self):
        with self.assertRaises(ValueError):
            ft.trip_cost("2026-11-10", "2026-11-09")


if __name__ == "__main__":
    unittest.main()
