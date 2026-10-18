"""Load public-holiday data files for the free-trip calculator.

Files live in ``data/holidays/<REGION>-<YEAR>.json``. See ``data/holidays/README.md``
for the format. The loader never guesses: an unknown region raises an error so the
agent has to ask or search instead of assuming.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "holidays"
LEVELS = ("national", "region", "city")


@dataclass(frozen=True)
class Holiday:
    day: date
    name: str
    level: str
    scope: str = ""


@dataclass(frozen=True)
class HolidayCalendar:
    region: str
    year: int
    checked: str
    confidence: str
    sources: tuple[str, ...]
    holidays: tuple[Holiday, ...]

    def dates(self, levels: tuple[str, ...] = LEVELS) -> set[date]:
        return {h.day for h in self.holidays if h.level in levels}

    def between(self, start: date, end: date, levels: tuple[str, ...] = LEVELS) -> list[Holiday]:
        return [h for h in self.holidays if start <= h.day <= end and h.level in levels]


def parse(data: dict) -> HolidayCalendar:
    holidays = []
    for item in data["holidays"]:
        level = item.get("level", "national")
        if level not in LEVELS:
            raise ValueError(f"unknown holiday level: {level}")
        holidays.append(Holiday(date.fromisoformat(item["date"]), item["name"], level, item.get("scope", "")))
    return HolidayCalendar(
        region=data["region"],
        year=int(data["year"]),
        checked=data.get("checked", ""),
        confidence=data.get("confidence", ""),
        sources=tuple(data.get("sources", ())),
        holidays=tuple(sorted(holidays, key=lambda h: h.day)),
    )


def load_file(path: str | Path) -> HolidayCalendar:
    return parse(json.loads(Path(path).read_text(encoding="utf-8")))


def available_regions() -> list[str]:
    return sorted(p.stem for p in DATA_DIR.glob("*.json"))


def load_region(code: str) -> HolidayCalendar:
    """Load ``data/holidays/<code>.json`` (for example ``ES-MD-2026``)."""
    path = DATA_DIR / f"{code}.json"
    if not path.is_file():
        raise ValueError(f"no holiday data for {code!r}; available: {', '.join(available_regions()) or 'none'}")
    return load_file(path)


def parse_levels(text: str | None) -> tuple[str, ...]:
    if not text:
        return LEVELS
    levels = tuple(part.strip() for part in text.split(",") if part.strip())
    unknown = [level for level in levels if level not in LEVELS]
    if unknown:
        raise ValueError(f"unknown holiday level(s): {', '.join(unknown)}")
    return levels


def observed_monday(day: date) -> date:
    """If ``day`` is a Sunday, return the following Monday (a common observance rule); otherwise ``day``.

    Rules differ by region and year: confirm against the official decree before relying on it.
    """
    return day + timedelta(days=1) if day.weekday() == 6 else day
