"""A small price log that makes "verify live" operational.

Each observation is one JSON line: item, price, currency, label, source and the
time it was checked. The log tells you which prices are stale and how much a price
moved since the first time you saw it (for example 67 then 93 then 169).

The log file belongs to the traveler, not to this repository: keep it in your own
notes. ``prices*.jsonl`` is git-ignored here.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

LABELS = ("verified", "from-price", "estimate")


@dataclass(frozen=True)
class Observation:
    item: str
    price: float
    currency: str
    label: str
    source: str
    checked_at: datetime

    def to_json(self) -> str:
        return json.dumps(
            {
                "item": self.item,
                "price": self.price,
                "currency": self.currency,
                "label": self.label,
                "source": self.source,
                "checked_at": self.checked_at.astimezone(timezone.utc).isoformat(),
            },
            ensure_ascii=False,
        )

    @staticmethod
    def from_json(line: str) -> "Observation":
        data = json.loads(line)
        return Observation(
            item=data["item"],
            price=float(data["price"]),
            currency=data["currency"],
            label=data["label"],
            source=data["source"],
            checked_at=datetime.fromisoformat(data["checked_at"]),
        )


@dataclass(frozen=True)
class Drift:
    item: str
    first: Observation
    last: Observation

    @property
    def absolute(self) -> float:
        return self.last.price - self.first.price

    @property
    def percent(self) -> float:
        return 0.0 if self.first.price == 0 else 100.0 * self.absolute / self.first.price


def make(
    item: str,
    price: float,
    currency: str = "EUR",
    label: str = "verified",
    source: str = "",
    checked_at: datetime | None = None,
) -> Observation:
    if label not in LABELS:
        raise ValueError(f"label must be one of {', '.join(LABELS)}")
    if price < 0:
        raise ValueError("price must not be negative")
    return Observation(item, float(price), currency.upper(), label, source, checked_at or datetime.now(timezone.utc))


def append(path: str | Path, observation: Observation) -> None:
    with Path(path).open("a", encoding="utf-8") as handle:
        handle.write(observation.to_json() + "\n")


def read(path: str | Path) -> list[Observation]:
    file = Path(path)
    if not file.is_file():
        return []
    return [Observation.from_json(line) for line in file.read_text(encoding="utf-8").splitlines() if line.strip()]


def latest(observations: list[Observation]) -> dict[str, Observation]:
    result: dict[str, Observation] = {}
    for obs in sorted(observations, key=lambda o: o.checked_at):
        result[obs.item] = obs
    return result


def stale(observations: list[Observation], now: datetime | None = None, max_age_days: float = 3) -> list[Observation]:
    """Latest observation per item that is older than ``max_age_days`` (or not verified)."""
    now = now or datetime.now(timezone.utc)
    limit = timedelta(days=max_age_days)
    return [o for o in latest(observations).values() if now - o.checked_at > limit]


def drift(observations: list[Observation], item: str) -> Drift | None:
    series = sorted((o for o in observations if o.item == item), key=lambda o: o.checked_at)
    if len(series) < 2:
        return None
    return Drift(item, series[0], series[-1])


def age_label(observation: Observation, now: datetime | None = None) -> str:
    delta = (now or datetime.now(timezone.utc)) - observation.checked_at
    days = delta.total_seconds() / 86400
    if days < 1:
        return f"{int(delta.total_seconds() // 3600)} h ago"
    return f"{int(days)} d ago"
