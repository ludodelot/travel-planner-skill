"""Deterministic URL builders for trip planning.

No network access and no third-party dependencies. Every function returns a plain
string URL. Dates are ISO strings (``YYYY-MM-DD``).

Notes learned in practice:
- Booking accepts dates and the hostel filter in the URL.
- Hostelworld city pages may ignore the dates, so their prices are minimums, not
  date-specific quotes. Never compare them with Booking prices.
- Google Directions without an ``origin`` starts from the user's current location.
"""

from __future__ import annotations

from datetime import date
from urllib.parse import quote, urlencode

BOOKING_HOSTEL_FILTER = "ht_id=203"


def _iso(value: str) -> str:
    """Validate and normalise an ISO date string."""
    return date.fromisoformat(value).isoformat()


def _q(text: str) -> str:
    """Percent-encode a free-text query (spaces as %20, no '+')."""
    return quote(text, safe="")


def google_flights(
    origin: str,
    destination: str,
    depart: str,
    return_date: str | None = None,
    currency: str = "EUR",
    language: str = "en",
) -> str:
    """Google Flights natural-language search. Also lists a recommended train when one exists."""
    depart = _iso(depart)
    query = f"Flights from {origin} to {destination} on {depart}"
    if return_date:
        query += f" through {_iso(return_date)}"
    params = {"q": query, "curr": currency, "hl": language}
    return "https://www.google.com/travel/flights?" + urlencode(params, quote_via=quote)


def booking_search(
    destination: str,
    checkin: str,
    checkout: str,
    adults: int = 1,
    rooms: int = 1,
    currency: str = "EUR",
    hostels_only: bool = False,
    order_by_price: bool = False,
    language: str = "en",
) -> str:
    """Booking.com search results with dates. ``hostels_only`` applies the hostel filter."""
    checkin, checkout = _iso(checkin), _iso(checkout)
    if checkout <= checkin:
        raise ValueError("checkout must be after checkin")
    params = {
        "ss": destination,
        "checkin": checkin,
        "checkout": checkout,
        "group_adults": adults,
        "no_rooms": rooms,
        "group_children": 0,
        "selected_currency": currency,
    }
    url = f"https://www.booking.com/searchresults.{language}.html?" + urlencode(params, quote_via=quote)
    if hostels_only:
        url += "&nflt=" + quote(BOOKING_HOSTEL_FILTER, safe="")
    if order_by_price:
        url += "&order=price"
    return url


def booking_property(
    country_code: str,
    slug: str,
    checkin: str,
    checkout: str,
    adults: int = 1,
    rooms: int = 1,
    currency: str = "EUR",
    language: str = "en",
) -> str:
    """Direct link to one Booking property with dates (slug comes from the property URL)."""
    checkin, checkout = _iso(checkin), _iso(checkout)
    if checkout <= checkin:
        raise ValueError("checkout must be after checkin")
    params = {
        "checkin": checkin,
        "checkout": checkout,
        "group_adults": adults,
        "no_rooms": rooms,
        "group_children": 0,
        "selected_currency": currency,
    }
    base = f"https://www.booking.com/hotel/{country_code.lower()}/{slug}.{language}.html?"
    return base + urlencode(params, quote_via=quote)


def hostelworld_city(
    continent: str,
    country: str,
    city: str,
    checkin: str,
    checkout: str,
    guests: int = 1,
    currency: str = "EUR",
) -> str:
    """Hostelworld city page. Dates may be ignored by the site: treat prices as minimums."""
    params = {
        "from": _iso(checkin),
        "to": _iso(checkout),
        "guests": guests,
        "currency": currency,
    }
    path = "/".join(part.strip().lower().replace(" ", "-") for part in (continent, country, city))
    return f"https://www.hostelworld.com/hostels/{path}/?" + urlencode(params, quote_via=quote)


def maps_search(query: str) -> str:
    """Google Maps search for a place name or address."""
    return f"https://www.google.com/maps/search/?api=1&query={_q(query)}"


def maps_directions(destination: str, origin: str | None = None, mode: str = "walking") -> str:
    """Google Maps directions.

    Without ``origin`` the route starts from the user's current location: use this
    for a "go now" link. ``mode`` is one of walking, transit, driving, bicycling.
    """
    if mode not in {"walking", "transit", "driving", "bicycling"}:
        raise ValueError(f"unsupported travel mode: {mode}")
    url = "https://www.google.com/maps/dir/?api=1"
    if origin:
        url += f"&origin={_q(origin)}"
    url += f"&destination={_q(destination)}&travelmode={mode}"
    return url
