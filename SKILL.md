---
name: travel-planner
description: Plan, compare, verify and prepare trips end to end. Use when the user wants to find where to go, check real prices, fit a trip around work and holidays, pick accommodation and transport, build a walking itinerary (photo/video friendly), prepare a purchase checklist, or export everything to a calendar. Covers search efficiency, live price verification, entry requirements, calendar export with map links, and how to present results.
---

# Travel Planner

A workflow skill for planning trips with an AI agent. It is built from real planning sessions, so it is opinionated about what to verify, what to ask, and what never to do without the traveler.

## Core rules (read first)

1. **Verify live, never quote stale prices.** Prices in notes, blogs or earlier searches expire within days. Re-check on the day, say when it was checked, and label every number as `verified`, `from-price` or `estimate`. See `references/price-verification.md`.
2. **Fit the trip to the traveler's real calendar first.** Work days, remote-work days, public holidays (national, regional and municipal) and bridges decide which trips cost vacation days. See `references/constraints-and-calendar.md`.
3. **Check entry requirements before any ticket.** Visa, ETA, ID validity, passport vs. ID card. See `references/entry-requirements.md`.
4. **Never pay, submit, send or accept on the traveler's behalf.** Prepare everything, open the right pages, fill forms only with explicit confirmation, and leave the consent checkbox and the final button to the traveler. See `references/safety-and-consent.md`.
5. **Give a recommendation, not a survey.** Lead with the choice and the reason, show a small table, flag what is unverified, and end with the next action. See `references/results-format.md`.
6. **Do not store secrets.** No booking references, PINs, card data or phone numbers in notes, repos or calendar events.

## Workflow

| Phase | What to do | Reference |
|---|---|---|
| 1. Clarify | Dates or windows, budget, travelers, pace, interests, constraints, places already visited, deal-breakers (for example hostel dorm size, free cancellation, no night arrivals) | `references/workflow.md` |
| 2. Constraints | Work schedule, remote days, holidays, bridges, flights or commitments already booked | `references/constraints-and-calendar.md` |
| 3. Search | Parallel, deterministic, cheap searches first; deep research only for the shortlist | `references/search-efficiency.md`, `references/tools-and-mcps.md` |
| 4. Verify | Live prices, date variants, baggage, cancellation, notices, entry requirements | `references/price-verification.md`, `references/entry-requirements.md` |
| 5. Decide | Shortlist of 2 to 3 options with trade-offs and a clear pick | `references/results-format.md` |
| 6. Prepare purchase | Ordered checklist with direct links, what is refundable, what to confirm before paying | `references/transport.md`, `references/accommodation.md`, `templates/purchase-checklist.md` |
| 7. Itinerary | Walking-friendly, light-aware, with rain plan, budget and verified opening hours | `references/itinerary-design.md` |
| 8. Export | Calendar events with local times, map links and a "go now" link; all-day plus timed events when needed | `references/calendar-export.md` |
| 9. Record | Update the trip note, lessons and pending items | `templates/trip-note.md` |

## Search and tooling at a glance

- Build search URLs deterministically with `scripts/links.py` (Google Flights, Booking, Hostelworld, Google Maps, directions without origin).
- Run independent searches in parallel. Fetch a result page once and extract only what matters.
- Prefer official sources for rules (holiday decrees, government entry pages, transport operators). Treat aggregator "from" prices as hints.
- With a browser tool, open **new tabs** for the traveler, leave payment pages ready, and never reuse their tabs.

## When data is missing or blocked

Say so explicitly. Typical cases: a booking site that ignores dates in a URL, a ticket page that shows no buy button (waiting list), a script blocked by the browser, a page that needs login. Offer the nearest verified alternative and the exact manual step.

## Files

```
SKILL.md                      this file
references/                   one topic per file
templates/                    trip note, purchase checklist, calendar event, itinerary prompt
scripts/links.py              URL builders (no network, no dependencies)
tests/                        unit tests for the URL builders
examples/                     anonymized case studies
```
