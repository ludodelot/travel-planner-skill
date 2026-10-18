import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import cli  # noqa: E402
import price_log as pl  # noqa: E402

NOW = datetime(2026, 10, 18, 12, 0, tzinfo=timezone.utc)


def obs(item, price, days_ago, label="verified"):
    return pl.make(item, price, "EUR", label, "test", NOW - timedelta(days=days_ago))


class PriceLogTest(unittest.TestCase):
    def test_drift_shows_the_price_climbing(self):
        series = [obs("flight", 67, 21), obs("flight", 93, 0), obs("flight", 169, 0.5)]
        drift = pl.drift(series, "flight")
        self.assertEqual(drift.first.price, 67)
        self.assertEqual(drift.last.price, 93)  # latest by time is the 0-days-ago observation
        self.assertAlmostEqual(drift.percent, 100 * 26 / 67)

    def test_stale_flags_old_latest_prices_only(self):
        series = [obs("a", 10, 10), obs("a", 11, 1), obs("b", 20, 5)]
        old = pl.stale(series, NOW, 3)
        self.assertEqual([o.item for o in old], ["b"])

    def test_roundtrip_through_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "prices.jsonl"
            pl.append(path, obs("x", 12.5, 0))
            pl.append(path, obs("y", 7, 2, "estimate"))
            loaded = pl.read(path)
        self.assertEqual([o.item for o in loaded], ["x", "y"])
        self.assertEqual(loaded[1].label, "estimate")

    def test_validation(self):
        with self.assertRaises(ValueError):
            pl.make("x", 1, label="rumor")
        with self.assertRaises(ValueError):
            pl.make("x", -1)

    def test_missing_file_is_empty(self):
        self.assertEqual(pl.read("/nonexistent/prices.jsonl"), [])


class CliPriceTest(unittest.TestCase):
    def test_add_show_and_stale(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "prices.jsonl")
            self.assertIn("logged", cli.run(["price", "add", "trip", "93", "--file", path]))
            self.assertIn("trip: 93 EUR [verified]", cli.run(["price", "show", "--file", path]))
            self.assertIn("nothing older", cli.run(["price", "stale", "--file", path]))

    def test_add_requires_item_and_amount(self):
        self.assertEqual(cli.main(["price", "add", "--file", "/tmp/never-written.jsonl"]), 2)


class CliIcsTest(unittest.TestCase):
    def test_json_to_ics(self):
        events = [
            {"summary": "Sunrise at the steps", "start": "2026-11-08T07:10", "end": "2026-11-08T07:35",
             "tz": "Europe/London", "location": "The Vennel Steps", "reminders_minutes": [15]},
            {"summary": "Holiday", "start": "2026-11-09", "end": "2026-11-10", "free": True},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "events.json"
            out = Path(tmp) / "trip.ics"
            src.write_text(json.dumps(events))
            message = cli.run(["ics", str(src), "--name", "Edinburgh", "--out", str(out)])
            text = out.read_bytes().decode()
        self.assertIn("wrote 2 events", message)
        self.assertIn("DTSTART:20261108T071000Z", text)
        self.assertIn("DTSTART;VALUE=DATE:20261109", text)
        self.assertIn("X-WR-CALNAME:Edinburgh", text)
        self.assertTrue(text.startswith("BEGIN:VCALENDAR\r\n"))


if __name__ == "__main__":
    unittest.main()
