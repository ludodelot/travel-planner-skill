"""How many vacation days does a trip cost?

Classifies each day of a trip as weekend, holiday, remote or office and counts the
office days that would need vacation. Pure functions, no network.

Remote days only count as free when ``remote_abroad`` is true (the traveler is
allowed to work from the destination) or when the traveler is back home that day.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Iterable

MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(7)


@dataclass(frozen=True)
class DayCost:
    day: date
    kind: str  # weekend | holiday | remote | office
    free: bool
    reason: str


@dataclass(frozen=True)
class TripCost:
    days: tuple[DayCost, ...]

    @property
    def vacation_days(self) -> int:
        return sum(1 for d in self.days if not d.free)

    @property
    def is_free(self) -> bool:
        return self.vacation_days == 0


def _as_date(value: date | str) -> date:
    return value if isinstance(value, date) else date.fromisoformat(value)


def trip_cost(
    start: date | str,
    end: date | str,
    remote_weekdays: Iterable[int] = (),
    holidays: Iterable[date | str] = (),
    remote_abroad: bool = False,
    leave_after_work_first_day: bool = False,
    back_home_to_work_last_day: bool = False,
) -> TripCost:
    """Cost of a trip from ``start`` to ``end`` (both inclusive, the days away from home).

    Parameters
    ----------
    remote_weekdays:
        Weekday numbers (Monday=0) when the traveler works remotely.
    holidays:
        Dates that are public holidays for the traveler's workplace.
    remote_abroad:
        True when working remotely from the destination is allowed.
    leave_after_work_first_day:
        The first day is worked normally and the traveler leaves afterwards.
    back_home_to_work_last_day:
        The return lands early enough to work the last day from home.
    """
    first, last = _as_date(start), _as_date(end)
    if last < first:
        raise ValueError("end must not be before start")
    remote = set(remote_weekdays)
    holiday_set = {_as_date(h) for h in holidays}

    rows: list[DayCost] = []
    current = first
    while current <= last:
        weekday = current.weekday()
        if weekday >= SATURDAY:
            row = DayCost(current, "weekend", True, "weekend")
        elif current in holiday_set:
            row = DayCost(current, "holiday", True, "public holiday")
        elif weekday in remote:
            if current == first and leave_after_work_first_day:
                row = DayCost(current, "remote", True, "remote day, leave after work")
            elif current == last and back_home_to_work_last_day:
                row = DayCost(current, "remote", True, "remote day, back home to work")
            elif remote_abroad:
                row = DayCost(current, "remote", True, "remote day, allowed abroad")
            else:
                row = DayCost(current, "remote", False, "remote day but not allowed from the destination")
        else:
            if current == first and leave_after_work_first_day:
                row = DayCost(current, "office", True, "office day, leave after work")
            else:
                row = DayCost(current, "office", False, "office day: needs vacation")
        rows.append(row)
        current += timedelta(days=1)
    return TripCost(tuple(rows))
