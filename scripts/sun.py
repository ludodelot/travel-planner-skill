"""Sunrise, sunset and civil twilight without network access.

Uses the classic "Almanac for Computers" algorithm. Accuracy is typically within
two to three minutes, which is enough for planning photo sessions. Always confirm
exact times with an almanac for a shoot that depends on the minute.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

ZENITH_SUNRISE = 90.833  # standard refraction and solar radius
ZENITH_CIVIL = 96.0  # civil twilight (sun 6 degrees below the horizon)


@dataclass(frozen=True)
class SunTimes:
    civil_dawn: datetime | None
    sunrise: datetime | None
    sunset: datetime | None
    civil_dusk: datetime | None

    def daylight(self) -> timedelta | None:
        if self.sunrise and self.sunset:
            return self.sunset - self.sunrise
        return None


def _rad(deg: float) -> float:
    return math.radians(deg)


def _deg(rad: float) -> float:
    return math.degrees(rad)


def _event_ut_hours(lat: float, lon: float, day: date, zenith: float, rising: bool) -> float | None:
    """Universal time (hours, may be outside 0-24 before normalising) of a solar event, or None."""
    n = day.timetuple().tm_yday
    lng_hour = lon / 15.0
    t = n + ((6.0 if rising else 18.0) - lng_hour) / 24.0
    m = 0.9856 * t - 3.289
    l = (m + 1.916 * math.sin(_rad(m)) + 0.020 * math.sin(_rad(2 * m)) + 282.634) % 360.0
    ra = _deg(math.atan(0.91764 * math.tan(_rad(l)))) % 360.0
    ra += (math.floor(l / 90.0) * 90.0) - (math.floor(ra / 90.0) * 90.0)
    ra /= 15.0
    sin_dec = 0.39782 * math.sin(_rad(l))
    cos_dec = math.cos(math.asin(sin_dec))
    cos_h = (math.cos(_rad(zenith)) - sin_dec * math.sin(_rad(lat))) / (cos_dec * math.cos(_rad(lat)))
    if cos_h > 1 or cos_h < -1:
        return None  # sun never rises (or never sets) at this zenith on this date
    h = 360.0 - _deg(math.acos(cos_h)) if rising else _deg(math.acos(cos_h))
    h /= 15.0
    local_mean = h + ra - 0.06571 * t - 6.622
    return (local_mean - lng_hour) % 24.0


def _to_local(day: date, ut_hours: float | None, tz: ZoneInfo) -> datetime | None:
    if ut_hours is None:
        return None
    base = datetime(day.year, day.month, day.day, tzinfo=timezone.utc)
    return (base + timedelta(hours=ut_hours)).astimezone(tz)


def sun_times(lat: float, lon: float, day: date | str, tz_name: str = "UTC") -> SunTimes:
    """Civil dawn, sunrise, sunset and civil dusk in the given IANA time zone.

    Example: ``sun_times(55.9533, -3.1883, "2026-11-08", "Europe/London")``.
    """
    if isinstance(day, str):
        day = date.fromisoformat(day)
    tz = ZoneInfo(tz_name)
    return SunTimes(
        civil_dawn=_to_local(day, _event_ut_hours(lat, lon, day, ZENITH_CIVIL, True), tz),
        sunrise=_to_local(day, _event_ut_hours(lat, lon, day, ZENITH_SUNRISE, True), tz),
        sunset=_to_local(day, _event_ut_hours(lat, lon, day, ZENITH_SUNRISE, False), tz),
        civil_dusk=_to_local(day, _event_ut_hours(lat, lon, day, ZENITH_CIVIL, False), tz),
    )


def golden_windows(times: SunTimes, minutes: int = 60) -> dict[str, tuple[datetime, datetime]]:
    """Rough golden-hour windows: after sunrise and before sunset."""
    windows: dict[str, tuple[datetime, datetime]] = {}
    if times.sunrise:
        windows["morning"] = (times.sunrise, times.sunrise + timedelta(minutes=minutes))
    if times.sunset:
        windows["evening"] = (times.sunset - timedelta(minutes=minutes), times.sunset)
    return windows
