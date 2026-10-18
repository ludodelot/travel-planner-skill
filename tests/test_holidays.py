import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import cli  # noqa: E402
import holidays  # noqa: E402


class HolidaysTest(unittest.TestCase):
    def test_bundled_region_loads_and_is_sorted(self):
        cal = holidays.load_region("ES-MD-2026")
        self.assertEqual(cal.year, 2026)
        days = [h.day for h in cal.holidays]
        self.assertEqual(days, sorted(days))
        self.assertIn(date(2026, 11, 2), cal.dates())  # moved from Sunday 1 Nov
        self.assertIn(date(2026, 12, 7), cal.dates())  # moved from Sunday 6 Dec
        self.assertTrue(cal.sources and cal.checked)

    def test_levels_filter_excludes_city_holidays(self):
        cal = holidays.load_region("ES-MD-2026")
        self.assertIn(date(2026, 11, 9), cal.dates())
        self.assertNotIn(date(2026, 11, 9), cal.dates(("national", "region")))

    def test_unknown_region_raises_with_choices(self):
        with self.assertRaisesRegex(ValueError, "ES-MD-2026"):
            holidays.load_region("XX-00-1999")

    def test_parse_levels(self):
        self.assertEqual(holidays.parse_levels("national, region"), ("national", "region"))
        with self.assertRaises(ValueError):
            holidays.parse_levels("galaxy")

    def test_observed_monday(self):
        self.assertEqual(holidays.observed_monday(date(2026, 11, 1)), date(2026, 11, 2))
        self.assertEqual(holidays.observed_monday(date(2026, 11, 3)), date(2026, 11, 3))

    def test_custom_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.json"
            path.write_text(json.dumps({
                "region": "XX", "year": 2030,
                "holidays": [{"date": "2030-01-02", "name": "Test", "level": "city"}],
            }))
            cal = holidays.load_file(path)
        self.assertEqual(cal.dates(), {date(2030, 1, 2)})

    def test_every_bundled_file_is_valid(self):
        for code in holidays.available_regions():
            cal = holidays.load_region(code)
            for holiday in cal.holidays:
                self.assertEqual(holiday.day.year, cal.year, f"{code}: {holiday}")


class CliRegionTest(unittest.TestCase):
    def test_bridge_is_free_with_region_data(self):
        out = cli.run([
            "free-trip", "2026-10-30", "2026-11-02", "--remote", "1,4",
            "--region", "ES-MD-2026", "--leave-after-work",
        ])
        self.assertIn("vacation days needed: 0", out)
        self.assertIn("ES-MD 2026", out)

    def test_city_holiday_matters(self):
        free = cli.run(["free-trip", "2026-11-07", "2026-11-10", "--remote", "1,4",
                        "--region", "ES-MD-2026", "--back-home-to-work"])
        self.assertIn("vacation days needed: 0", free)
        no_city = cli.run(["free-trip", "2026-11-07", "2026-11-10", "--remote", "1,4",
                           "--region", "ES-MD-2026", "--levels", "national,region", "--back-home-to-work"])
        self.assertIn("vacation days needed: 1", no_city)

    def test_unknown_region_is_an_error_code(self):
        self.assertEqual(cli.main(["free-trip", "2026-11-07", "2026-11-10", "--region", "nope"]), 2)


if __name__ == "__main__":
    unittest.main()
