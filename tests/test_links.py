import sys
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import links  # noqa: E402


def params(url: str) -> dict[str, list[str]]:
    return parse_qs(urlparse(url).query)


class LinksTest(unittest.TestCase):
    def test_google_flights_round_trip(self):
        url = links.google_flights("MAD", "EDI", "2026-11-07", "2026-11-10")
        self.assertEqual(
            params(url)["q"],
            ["Flights from MAD to EDI on 2026-11-07 through 2026-11-10"],
        )
        self.assertEqual(params(url)["curr"], ["EUR"])

    def test_google_flights_one_way(self):
        url = links.google_flights("BIO", "MAD", "2026-11-02")
        self.assertNotIn("through", params(url)["q"][0])

    def test_booking_search_hostels_sorted(self):
        url = links.booking_search(
            "San Sebastián", "2026-10-31", "2026-11-02", hostels_only=True, order_by_price=True
        )
        p = params(url)
        self.assertEqual(p["ss"], ["San Sebastián"])
        self.assertEqual(p["nflt"], ["ht_id=203"])
        self.assertEqual(p["order"], ["price"])
        self.assertEqual(p["group_adults"], ["1"])

    def test_booking_rejects_inverted_dates(self):
        with self.assertRaises(ValueError):
            links.booking_search("Bilbao", "2026-10-31", "2026-10-30")
        with self.assertRaises(ValueError):
            links.booking_property("es", "x", "2026-10-31", "2026-10-31")

    def test_booking_property(self):
        url = links.booking_property("ES", "a-room-in-the-city", "2026-10-31", "2026-11-02")
        self.assertTrue(url.startswith("https://www.booking.com/hotel/es/a-room-in-the-city.en.html?"))
        self.assertEqual(params(url)["checkout"], ["2026-11-02"])

    def test_hostelworld_path(self):
        url = links.hostelworld_city("Europe", "Spain", "San Sebastian", "2026-10-31", "2026-11-02")
        self.assertIn("/hostels/europe/spain/san-sebastian/", url)
        self.assertEqual(params(url)["from"], ["2026-10-31"])

    def test_maps_directions_without_origin_uses_current_location(self):
        url = links.maps_directions("Edinburgh Airport", mode="transit")
        self.assertNotIn("origin", params(url))
        self.assertEqual(params(url)["travelmode"], ["transit"])

    def test_maps_directions_with_origin(self):
        url = links.maps_directions("Grassmarket Edinburgh", origin="The Vennel Steps Edinburgh")
        self.assertEqual(params(url)["origin"], ["The Vennel Steps Edinburgh"])

    def test_maps_directions_rejects_bad_mode(self):
        with self.assertRaises(ValueError):
            links.maps_directions("x", mode="teleport")

    def test_maps_search_encodes_spaces(self):
        self.assertIn("query=Royal%20Mile%20Edinburgh", links.maps_search("Royal Mile Edinburgh"))

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            links.google_flights("MAD", "EDI", "07-11-2026")


if __name__ == "__main__":
    unittest.main()
