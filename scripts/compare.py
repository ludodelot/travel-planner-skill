"""Compare trip options on effective cost per day.

The default weights are editable starting points, not truths: they only make the
trade-offs explicit (a vacation day, travel hours, a new country, refundability).
Always show the raw numbers next to the score.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Option:
    name: str
    total_cost: float
    days: int
    vacation_days: int = 0
    new_country: bool = False
    travel_hours: float = 0.0
    refundable: bool = False
    verified: bool = True


@dataclass(frozen=True)
class Weights:
    vacation_day_value: float = 80.0  # what one vacation day is worth to the traveler
    hour_value: float = 5.0  # cost of one hour spent in transit
    new_country_bonus: float = 40.0  # value of a country not yet visited
    refundable_bonus: float = 10.0  # value of free cancellation
    unverified_penalty: float = 15.0  # risk premium when the price is not verified


@dataclass(frozen=True)
class Ranked:
    option: Option
    effective_cost: float
    per_day: float
    notes: tuple[str, ...]


def cost_per_day(option: Option) -> float:
    if option.days <= 0:
        raise ValueError(f"{option.name}: days must be positive")
    return option.total_cost / option.days


def effective_cost(option: Option, weights: Weights = Weights()) -> tuple[float, tuple[str, ...]]:
    notes: list[str] = []
    value = option.total_cost
    if option.vacation_days:
        value += option.vacation_days * weights.vacation_day_value
        notes.append(f"+{option.vacation_days} vacation day(s)")
    if option.travel_hours:
        value += option.travel_hours * weights.hour_value
        notes.append(f"{option.travel_hours:g} h in transit")
    if option.new_country:
        value -= weights.new_country_bonus
        notes.append("new country")
    if option.refundable:
        value -= weights.refundable_bonus
        notes.append("refundable")
    if not option.verified:
        value += weights.unverified_penalty
        notes.append("price not verified")
    return value, tuple(notes)


def rank(options: list[Option], weights: Weights = Weights()) -> list[Ranked]:
    """Order options by effective cost per day (lowest first)."""
    if not options:
        raise ValueError("no options to rank")
    ranked = []
    for option in options:
        if option.days <= 0:
            raise ValueError(f"{option.name}: days must be positive")
        value, notes = effective_cost(option, weights)
        ranked.append(Ranked(option, value, value / option.days, notes))
    return sorted(ranked, key=lambda r: (r.per_day, r.option.name))


def markdown_table(ranked: list[Ranked]) -> str:
    """A table with raw numbers and the score, ready to paste into an answer."""
    lines = [
        "| # | Option | Total | Days | Cost/day | Vacation days | Score/day | Notes |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for index, item in enumerate(ranked, start=1):
        o = item.option
        lines.append(
            f"| {index} | {o.name} | {o.total_cost:g} | {o.days} | {cost_per_day(o):.1f} | "
            f"{o.vacation_days} | {item.per_day:.1f} | {', '.join(item.notes) or '-'} |"
        )
    return "\n".join(lines)
