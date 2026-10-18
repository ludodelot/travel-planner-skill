#!/usr/bin/env python3
"""Command-line entry point so an agent can use the tools without writing code.

Examples:
    python3 -I scripts/cli.py flights MAD EDI 2026-11-07 --return 2026-11-10
    python3 -I scripts/cli.py booking "San Sebastián" 2026-10-31 2026-11-02 --hostels --sort-price
    python3 -I scripts/cli.py maps "Edinburgh Airport" --mode transit
    python3 -I scripts/cli.py free-trip 2026-11-07 2026-11-10 --remote 1,4 --holiday 2026-11-09 --back-home-to-work
    python3 -I scripts/cli.py sun 55.9533 -3.1883 2026-11-08 --tz Europe/London
    python3 -I scripts/cli.py compare options.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import compare  # noqa: E402
import free_trip  # noqa: E402
import holidays  # noqa: E402
import links  # noqa: E402
import sun  # noqa: E402


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="travel-planner", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("flights", help="Google Flights search link")
    p.add_argument("origin")
    p.add_argument("destination")
    p.add_argument("depart")
    p.add_argument("--return", dest="return_date")
    p.add_argument("--currency", default="EUR")

    p = sub.add_parser("booking", help="Booking.com search link with dates")
    p.add_argument("destination")
    p.add_argument("checkin")
    p.add_argument("checkout")
    p.add_argument("--adults", type=int, default=1)
    p.add_argument("--hostels", action="store_true")
    p.add_argument("--sort-price", action="store_true")
    p.add_argument("--currency", default="EUR")

    p = sub.add_parser("maps", help="Google Maps directions; no --origin means from the user's location")
    p.add_argument("destination")
    p.add_argument("--origin")
    p.add_argument("--mode", default="walking", choices=["walking", "transit", "driving", "bicycling"])

    p = sub.add_parser("free-trip", help="Vacation days a trip costs")
    p.add_argument("start")
    p.add_argument("end")
    p.add_argument("--remote", default="", help="comma-separated weekday numbers, Monday=0 (for example 1,4)")
    p.add_argument("--holiday", action="append", default=[], help="ISO date, repeatable")
    p.add_argument("--region", help="holiday data file code, for example ES-MD-2026 (see data/holidays)")
    p.add_argument("--holidays-file", help="path to a holiday JSON file")
    p.add_argument("--levels", help="holiday levels to include: national,region,city (default all)")
    p.add_argument("--remote-abroad", action="store_true")
    p.add_argument("--leave-after-work", action="store_true")
    p.add_argument("--back-home-to-work", action="store_true")

    p = sub.add_parser("sun", help="Sunrise, sunset and civil twilight")
    p.add_argument("lat", type=float)
    p.add_argument("lon", type=float)
    p.add_argument("date")
    p.add_argument("--tz", default="UTC")

    p = sub.add_parser("compare", help="Rank options from a JSON file (list of objects with Option fields)")
    p.add_argument("file")
    return parser


def _fmt(value) -> str:
    return value.strftime("%H:%M") if value else "-"


def run(argv: list[str] | None = None) -> str:
    args = _build_parser().parse_args(argv)
    if args.command == "flights":
        return links.google_flights(args.origin, args.destination, args.depart, args.return_date, args.currency)
    if args.command == "booking":
        return links.booking_search(
            args.destination, args.checkin, args.checkout, adults=args.adults,
            currency=args.currency, hostels_only=args.hostels, order_by_price=args.sort_price,
        )
    if args.command == "maps":
        return links.maps_directions(args.destination, origin=args.origin, mode=args.mode)
    if args.command == "free-trip":
        remote = [int(x) for x in args.remote.split(",") if x.strip() != ""]
        holiday_dates = list(args.holiday)
        notes: list[str] = []
        calendar = None
        if args.region:
            calendar = holidays.load_region(args.region)
        elif args.holidays_file:
            calendar = holidays.load_file(args.holidays_file)
        if calendar:
            levels = holidays.parse_levels(args.levels)
            holiday_dates += [d.isoformat() for d in calendar.dates(levels)]
            notes.append(f"holidays: {calendar.region} {calendar.year}, levels {','.join(levels)}, checked {calendar.checked or 'unknown'}")
            if calendar.confidence:
                notes.append(f"confidence: {calendar.confidence}")
        cost = free_trip.trip_cost(
            args.start, args.end, remote, holiday_dates, args.remote_abroad,
            args.leave_after_work, args.back_home_to_work,
        )
        rows = [f"{d.day.isoformat()} {d.day.strftime('%a')}: {d.kind:<7} {'free' if d.free else 'COST'}  ({d.reason})" for d in cost.days]
        rows.append(f"vacation days needed: {cost.vacation_days}")
        return "\n".join(rows + notes)
    if args.command == "sun":
        t = sun.sun_times(args.lat, args.lon, args.date, args.tz)
        return (
            f"civil dawn {_fmt(t.civil_dawn)} | sunrise {_fmt(t.sunrise)} | "
            f"sunset {_fmt(t.sunset)} | civil dusk {_fmt(t.civil_dusk)}"
        )
    if args.command == "compare":
        data = json.loads(Path(args.file).read_text(encoding="utf-8"))
        options = [compare.Option(**item) for item in data]
        return compare.markdown_table(compare.rank(options))
    raise AssertionError(args.command)


def main(argv: list[str] | None = None) -> int:
    try:
        print(run(argv))
    except (ValueError, OSError, json.JSONDecodeError, TypeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
