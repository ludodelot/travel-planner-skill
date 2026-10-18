"""Minimal iCalendar (.ics) writer for itineraries.

Events are written in UTC so no VTIMEZONE block is needed; calendar apps convert
them to the viewer's time zone. All-day events use DATE values. Lines are folded
at 75 octets as required by RFC 5545.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import date, datetime, timezone

PRODID = "-//travel-planner-skill//EN"


@dataclass(frozen=True)
class Event:
    summary: str
    start: datetime | date
    end: datetime | date
    location: str = ""
    description: str = ""
    url: str = ""
    reminders_minutes: tuple[int, ...] = field(default_factory=tuple)
    free: bool = False  # True: transparent (does not block time)

    @property
    def all_day(self) -> bool:
        return not isinstance(self.start, datetime)


def escape_text(value: str) -> str:
    """Escape TEXT values: backslash, semicolon, comma and newlines."""
    return (
        value.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\r\n", "\\n")
        .replace("\n", "\\n")
    )


def fold(line: str) -> str:
    """Fold a content line to at most 75 octets per physical line (CRLF + space continuation)."""
    raw = line.encode("utf-8")
    if len(raw) <= 75:
        return line
    parts: list[str] = []
    current = b""
    limit = 75
    for char in line:
        encoded = char.encode("utf-8")
        if len(current) + len(encoded) > limit:
            parts.append(current.decode("utf-8"))
            current = b""
            limit = 74  # continuation lines start with one space
        current += encoded
    parts.append(current.decode("utf-8"))
    return "\r\n ".join(parts)


def _utc(value: datetime) -> str:
    if value.tzinfo is None:
        raise ValueError("datetimes must be timezone-aware")
    return value.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _uid(event: Event) -> str:
    seed = f"{event.summary}|{event.start}|{event.end}|{event.location}"
    return hashlib.sha1(seed.encode("utf-8")).hexdigest()[:20] + "@travel-planner-skill"


def build_ics(events: list[Event], calendar_name: str = "Trip", now: datetime | None = None) -> str:
    """Return the full iCalendar text (CRLF line endings)."""
    stamp = _utc(now or datetime.now(timezone.utc))
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        f"PRODID:{PRODID}",
        "CALSCALE:GREGORIAN",
        f"X-WR-CALNAME:{escape_text(calendar_name)}",
    ]
    for event in events:
        lines += ["BEGIN:VEVENT", f"UID:{_uid(event)}", f"DTSTAMP:{stamp}"]
        if event.all_day:
            lines += [f"DTSTART;VALUE=DATE:{event.start:%Y%m%d}", f"DTEND;VALUE=DATE:{event.end:%Y%m%d}"]
        else:
            lines += [f"DTSTART:{_utc(event.start)}", f"DTEND:{_utc(event.end)}"]
        lines.append(f"SUMMARY:{escape_text(event.summary)}")
        if event.location:
            lines.append(f"LOCATION:{escape_text(event.location)}")
        if event.description:
            lines.append(f"DESCRIPTION:{escape_text(event.description)}")
        if event.url:
            lines.append(f"URL:{event.url}")
        if event.free:
            lines.append("TRANSP:TRANSPARENT")
        for minutes in event.reminders_minutes:
            lines += [
                "BEGIN:VALARM",
                "ACTION:DISPLAY",
                f"DESCRIPTION:{escape_text(event.summary)}",
                f"TRIGGER:-PT{int(minutes)}M",
                "END:VALARM",
            ]
        lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")
    return "\r\n".join(fold(line) for line in lines) + "\r\n"
