import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import cli  # noqa: E402
import compare  # noqa: E402

Option = compare.Option


class CompareTest(unittest.TestCase):
    def test_train_beats_flight_when_cheaper_and_flexible(self):
        ranked = compare.rank([
            Option("train", 104, 4, travel_hours=10, refundable=True),
            Option("flight", 117, 4, travel_hours=7),
        ])
        self.assertEqual(ranked[0].option.name, "train")

    def test_vacation_day_flips_the_order(self):
        free = Option("free weekend", 300, 4)
        cheap_but_costs_a_day = Option("cheap", 240, 4, vacation_days=1)
        ranked = compare.rank([free, cheap_but_costs_a_day])
        self.assertEqual(ranked[0].option.name, "free weekend")
        # With a very low value for a vacation day the cheaper trip wins.
        low = compare.Weights(vacation_day_value=10)
        self.assertEqual(compare.rank([free, cheap_but_costs_a_day], low)[0].option.name, "cheap")

    def test_new_country_and_unverified_notes(self):
        item = compare.rank([Option("x", 100, 2, new_country=True, verified=False)])[0]
        self.assertIn("new country", item.notes)
        self.assertIn("price not verified", item.notes)
        self.assertAlmostEqual(item.effective_cost, 100 - 40 + 15)

    def test_markdown_table_shows_raw_numbers(self):
        table = compare.markdown_table(compare.rank([Option("a", 93, 3, vacation_days=0)]))
        self.assertIn("| 1 | a | 93 | 3 | 31.0 | 0 |", table)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            compare.rank([])
        with self.assertRaises(ValueError):
            compare.rank([Option("zero", 10, 0)])


class CliTest(unittest.TestCase):
    def test_flights(self):
        url = cli.run(["flights", "MAD", "EDI", "2026-11-07", "--return", "2026-11-10"])
        self.assertIn("Flights%20from%20MAD%20to%20EDI", url)

    def test_booking_hostels(self):
        url = cli.run(["booking", "Bilbao", "2026-10-30", "2026-10-31", "--hostels", "--sort-price"])
        self.assertIn("nflt=ht_id%3D203", url)
        self.assertIn("order=price", url)

    def test_maps_without_origin(self):
        url = cli.run(["maps", "Edinburgh Airport", "--mode", "transit"])
        self.assertNotIn("origin", url)

    def test_free_trip_report(self):
        out = cli.run([
            "free-trip", "2026-11-07", "2026-11-10", "--remote", "1,4",
            "--holiday", "2026-11-09", "--back-home-to-work",
        ])
        self.assertIn("vacation days needed: 0", out)

    def test_sun(self):
        out = cli.run(["sun", "55.9533", "-3.1883", "2026-11-08", "--tz", "Europe/London"])
        self.assertIn("sunrise 07:3", out)

    def test_compare_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "options.json"
            path.write_text(json.dumps([
                {"name": "A", "total_cost": 100, "days": 2},
                {"name": "B", "total_cost": 150, "days": 3},
            ]))
            out = cli.run(["compare", str(path)])
        self.assertIn("| 1 | A |", out)

    def test_main_returns_error_code_on_bad_input(self):
        self.assertEqual(cli.main(["flights", "MAD", "EDI", "not-a-date"]), 2)


if __name__ == "__main__":
    unittest.main()
