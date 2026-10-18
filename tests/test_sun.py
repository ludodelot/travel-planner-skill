import sys
import unittest
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import sun  # noqa: E402


def minutes(dt: datetime) -> int:
    return dt.hour * 60 + dt.minute


class SunTest(unittest.TestCase):
    def assert_close(self, dt, hhmm, tolerance=4):
        h, m = map(int, hhmm.split(":"))
        self.assertLessEqual(abs(minutes(dt) - (h * 60 + m)), tolerance, f"{dt} vs {hhmm}")

    def test_edinburgh_november(self):
        # Published values for 8 Nov 2026 (almanac): about 07:34 / 16:17.
        t = sun.sun_times(55.9533, -3.1883, "2026-11-08", "Europe/London")
        self.assert_close(t.sunrise, "07:34")
        self.assert_close(t.sunset, "16:17")
        self.assert_close(t.civil_dawn, "06:53")
        self.assert_close(t.civil_dusk, "16:58")

    def test_order_of_events(self):
        t = sun.sun_times(40.4168, -3.7038, "2026-11-02", "Europe/Madrid")
        self.assertLess(t.civil_dawn, t.sunrise)
        self.assertLess(t.sunrise, t.sunset)
        self.assertLess(t.sunset, t.civil_dusk)
        self.assertGreater(t.daylight().total_seconds(), 9 * 3600)

    def test_timezone_is_applied(self):
        t = sun.sun_times(40.4168, -3.7038, "2026-07-01", "Europe/Madrid")
        self.assertEqual(t.sunrise.utcoffset().total_seconds(), 2 * 3600)

    def test_polar_summer_has_no_sunset(self):
        t = sun.sun_times(78.2232, 15.6267, "2026-06-21", "Arctic/Longyearbyen")
        self.assertIsNone(t.sunrise)
        self.assertIsNone(t.sunset)

    def test_golden_windows(self):
        t = sun.sun_times(55.9533, -3.1883, "2026-11-08", "Europe/London")
        w = sun.golden_windows(t, 45)
        self.assertEqual((w["evening"][1] - w["evening"][0]).seconds, 45 * 60)
        self.assertEqual(w["evening"][1], t.sunset)


if __name__ == "__main__":
    unittest.main()
