# Fitting trips to the traveler's calendar

## Inputs

- Work pattern: office days, remote days, hours, commute, recurring tasks that cannot be skipped.
- Flexibility: can remote days be chosen? Can the traveler work from abroad? (Ask; do not assume.)
- Public holidays: national, regional and **municipal** ones. Observed days can differ from the printed date when a holiday falls on a weekend.
- Contract or term dates, fixed flights, exams, events.

## Holidays: where to verify

1. Regional or national holiday decree for the year (official gazette or the government calendar).
2. Municipal holidays set by the city council (two per year in many regions). They only apply if the workplace is in that municipality.
3. A cross-check source (a union bulletin or government portal) is fine as a second source, but the official text wins. Many aggregator guides are wrong.

Typical rule: when a holiday falls on a Sunday, the region may move it to Monday. Check the decree; do not assume.

## Bundled holiday data and the calculator

`data/holidays/` holds observed dates per region and year, each with sources, a checked date and a confidence note (see `data/holidays/README.md`). The calculator uses them:

```bash
python3 -I scripts/cli.py free-trip 2026-11-07 2026-11-10 --remote 1,4 --region ES-MD-2026 --back-home-to-work
```

If the region or year is missing, do not guess: search the official source, tell the traveler the confidence level, and offer to add a data file with sources and the checked date. Use `--levels national,region` when the workplace is outside a city whose local holidays are in the file.

## The "free trip" rule

A trip is free when every working day it touches is covered by a weekend, a holiday or a remote day. Coming back on a working Monday costs a day.

Example pattern:

- Friday remote + Saturday + Sunday + Monday holiday = four days, zero vacation.
- Weekend + a holiday Monday + a remote Tuesday = an arrival on Tuesday morning can still be worked from home.

## Quick method

1. List the dates the trip covers, one row per day.
2. Mark each day: weekend, holiday, remote, office.
3. Count the office days. Zero means free; otherwise decide between vacation, shifting dates or choosing remote days.
4. Check the day-of-return: arrival time vs. start of the workday.

## Weekly caps on remote days

If the traveler can choose remote days (for example two per week), allocate them across trips instead of promising the same day twice. Note weeks where a holiday and a trip compete for the same flexible days.

## Contract end and "last day"

Verify the last working day against the holiday calendar. A last day that falls on a holiday means the real last workday is the previous one. Put recurring work events up to that date.

## Scheduling daily tasks and commutes

Add commute and routine blocks (shower, breakfast, travel) only if the traveler asks; they help the agent avoid scheduling purchases or events on top of them. Exclude holidays with exception dates in recurring series.

## Conflicts to flag proactively

- Events that start before the workday ends.
- Returns on working days.
- Trips on days when the remote-work allowance is already used.
- Departures that need a long transfer after a long working day.
