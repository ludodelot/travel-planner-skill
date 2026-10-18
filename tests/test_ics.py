import sys
import unittest
from datetime import date, datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import ics  # noqa: E402

NOW = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)
LONDON = ZoneInfo("Europe/London")


class IcsTest(unittest.TestCase):
    def test_timed_event_is_utc_and_has_alarm(self):
        event = ics.Event(
            "Sunrise at The Vennel",
            datetime(2026, 11, 8, 7, 10, tzinfo=LONDON),
            datetime(2026, 11, 8, 7, 35, tzinfo=LONDON),
            location="The Vennel Steps, Edinburgh",
            reminders_minutes=(15,),
        )
        text = ics.build_ics([event], "Edinburgh", now=NOW)
        self.assertIn("DTSTART:20261108T071000Z", text)  # GMT in November: same clock time
        self.assertIn("TRIGGER:-PT15M", text)
        self.assertTrue(text.startswith("BEGIN:VCALENDAR\r\n"))
        self.assertTrue(text.endswith("END:VCALENDAR\r\n"))

    def test_summer_time_conversion(self):
        event = ics.Event("x", datetime(2026, 7, 1, 9, 0, tzinfo=LONDON), datetime(2026, 7, 1, 10, 0, tzinfo=LONDON))
        self.assertIn("DTSTART:20260701T080000Z", ics.build_ics([event], now=NOW))

    def test_all_day_event_uses_date_values(self):
        event = ics.Event("Holiday", date(2026, 11, 9), date(2026, 11, 10), free=True)
        text = ics.build_ics([event], now=NOW)
        self.assertIn("DTSTART;VALUE=DATE:20261109", text)
        self.assertIn("DTEND;VALUE=DATE:20261110", text)
        self.assertIn("TRANSP:TRANSPARENT", text)

    def test_escaping(self):
        self.assertEqual(ics.escape_text("a,b;c\\d\ne"), "a\\,b\\;c\\\\d\\ne")

    def test_folding_keeps_lines_within_75_octets(self):
        event = ics.Event(
            "x",
            datetime(2026, 11, 8, 7, 10, tzinfo=LONDON),
            datetime(2026, 11, 8, 8, 0, tzinfo=LONDON),
            description="Photo ideas: " + "castle over the roofs, ñandú ✓ " * 20,
        )
        text = ics.build_ics([event], now=NOW)
        for physical in text.split("\r\n"):
            self.assertLessEqual(len(physical.encode("utf-8")), 75)
        unfolded = text.replace("\r\n ", "")
        self.assertIn("castle over the roofs", unfolded)

    def test_naive_datetime_rejected(self):
        event = ics.Event("x", datetime(2026, 11, 8, 7), datetime(2026, 11, 8, 8))
        with self.assertRaises(ValueError):
            ics.build_ics([event], now=NOW)

    def test_uid_is_stable(self):
        event = ics.Event("x", date(2026, 11, 9), date(2026, 11, 10))
        self.assertEqual(ics.build_ics([event], now=NOW), ics.build_ics([event], now=NOW))


if __name__ == "__main__":
    unittest.main()
