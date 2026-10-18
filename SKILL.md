---
name: travel-planner
description: Plan, compare, verify and prepare trips end to end. Use when the user wants to choose where to go, check real prices today, fit a trip around work and public holidays, pick hostels or hotels and transport, build a walking itinerary (photo and video friendly), prepare a ready-to-buy checklist with browser tabs opened for them, check entry requirements, or export the plan to a calendar with map links. Covers live price verification, search efficiency, browser purchase mode, calendar export and how to present results.
---

# Travel Planner

A Claude Code skill for planning trips with an AI agent. It is built from real planning sessions, so it is opinionated about what to verify, what to ask and what never to do without the traveler.

## First run: know the traveler

1. Look for a traveler profile (the user's notes, project memory or a file based on `templates/traveler-profile.md`). Read it before asking anything.
2. If there is none, ask for the essentials in one short message (home airport, nationality for entry rules, budget style, pace, interests, deal-breakers, work pattern and holidays, places already visited) and offer to save the profile in the user's own notes. Do not save it in a shared repository.
3. Check which tools are connected (`references/setup-and-mcps.md`) and tell the user once what you can and cannot do (browser tabs, calendar, drafts).

## Core rules

1. **Verify live, never quote stale prices.** Label every number `verified`, `from-price` or `estimate` and say when it was checked. See `references/price-verification.md`.
2. **Fit the trip to the real calendar first.** Work days, remote days, public holidays (national, regional, municipal) and bridges decide which trips cost vacation days. Use `scripts/free_trip.py`. See `references/constraints-and-calendar.md`.
3. **Check entry requirements before any ticket.** See `references/entry-requirements.md`.
4. **Never pay, submit, send or accept for the traveler.** Prepare, open the right pages, fill forms only with explicit confirmation, and leave consent and the final button to them. See `references/safety-and-consent.md`.
5. **Recommend, do not survey.** Lead with the choice and the reason, show a small table, flag what is unverified, end with the next action. See `references/results-format.md`.
6. **Do not store secrets.** No booking references, PINs, card data, passport numbers or phone numbers in notes, repos or calendar events.

## Workflow

| Phase | What to do | Reference |
|---|---|---|
| 1. Clarify | Dates or windows, budget, travelers, pace, interests, constraints, places visited, deal-breakers | `references/workflow.md` |
| 2. Constraints | Work schedule, remote days, holidays, bridges, fixed bookings | `references/constraints-and-calendar.md` |
| 3. Search | Parallel, deterministic, cheap searches first; deep research only for the shortlist | `references/search-efficiency.md`, `references/tools-and-mcps.md` |
| 4. Verify | Live prices, date variants, baggage, cancellation, notices, entry rules | `references/price-verification.md`, `references/entry-requirements.md` |
| 5. Decide | Two or three options with trade-offs and a clear pick | `references/results-format.md`, `references/budget.md` |
| 6. Prepare purchase | Ordered checklist with direct links; open ready-to-buy tabs | `references/browser-purchase-tabs.md`, `references/transport.md`, `references/accommodation.md`, `templates/purchase-checklist.md` |
| 7. Itinerary | Walking-friendly, light-aware, with rain plan and verified hours | `references/itinerary-design.md`, `scripts/sun.py` |
| 8. Export | Calendar events with local times and map links, or an `.ics` file | `references/calendar-export.md`, `scripts/ics.py` |
| 9. Record | Update the trip note, lessons and pending items | `templates/trip-note.md` |

## Scripts (standard library only, tested)

| Script | Use it to |
|---|---|
| `scripts/links.py` | Build Google Flights, Booking, Hostelworld and Maps links; a "go now" directions link needs no origin |
| `scripts/free_trip.py` | Count how many vacation days a trip costs given weekends, holidays and remote days |
| `scripts/sun.py` | Sunrise, sunset and civil twilight for any place and date, with no network |
| `scripts/ics.py` | Write an `.ics` file from itinerary events when no calendar connection exists |

Run them with `python3 -I`. Run the tests with `python3 -I -m unittest discover -s tests`.

## Browser mode in one paragraph

List the user's tabs, open **new tabs** for each task, navigate with deterministic URLs, read the page text and extract only price, times and conditions, stop at checkout, fill forms only with confirmed values and stop before consent and submit, then report a table of `tab -> what to do`. Full playbook: `references/browser-purchase-tabs.md`.

## Definition of done for a trip plan

- Constraints mapped and vacation cost known.
- Prices verified today, labeled, with a shifted-date alternative checked.
- Entry requirements confirmed with an official source.
- Purchase checklist ordered, with direct links and what is refundable.
- Unverified items listed with how to check them.
- Calendar or `.ics` prepared if the user wants it, with notifications off.
- Pending items dated, and no secrets stored.

## Quick-start prompts

- "Plan a long weekend in November for under 300 EUR; I like photography and walking."
- "Is this trip really free given my work schedule and holidays?" (use `free_trip.py`)
- "Open the tabs so I can buy this."
- "Put the itinerary in my calendar with map links."
- "What events can I go to near my trip?" (`references/events-and-networking.md`)

## When data is missing or blocked

Say so explicitly and give the nearest verified alternative and the exact manual step. Typical cases: a booking site that ignores dates, a ticket page with only a waiting list, a script blocked by the browser, a page that needs login.

## Files

```
SKILL.md                 this file
references/              one topic per file (workflow, search, tools, price, constraints,
                         entry, accommodation, transport, itinerary, calendar, results,
                         safety, events, budget, browser tabs, setup, lessons)
templates/               trip note, purchase checklist, calendar event, itinerary prompt, traveler profile
scripts/                 links, free_trip, sun, ics (standard library only)
tests/                   unit tests for the scripts
examples/                anonymized case studies
install.sh               copy the skill into ~/.claude/skills/travel-planner
```
