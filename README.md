<p align="center">
  <img src="assets/banner.png" alt="Voxel airport at night with luggage, a laptop and a small orange voxel mascot" width="100%">
</p>

# Travel Planner Skill

A skill for AI agents that plans trips end to end: where to go, what it really costs today, how it fits the traveler's work and holiday calendar, where to sleep, how to get there, a walking itinerary, and a calendar full of map links.

It was built from real planning sessions, so it encodes what actually goes wrong: stale prices, hostels with the wrong dorm, trips that cost a vacation day, entry rules found too late, and tools that fail.

> Idioma: [Español](README.es.md)

## What you get

- **A workflow** from clarifying questions to a ready-to-buy checklist and calendar export.
- **Verification rules**: label every number `verified`, `from-price` or `estimate`; check live; try date variants.
- **Calendar logic**: public holidays (national, regional, municipal), remote days, bridges and the "free trip" rule.
- **Search efficiency**: deterministic URLs, parallel searches, cheap-first, compact extraction.
- **Tools and MCP guidance**: what to use for rules, prices, calendar and drafts, and how to handle failures.
- **Itinerary design** for photographers and videographers, with a prompt for other assistants.
- **Safe-by-default behavior**: prepare and open pages, never pay, send or submit for the traveler.
- **A tested URL builder**: Google Flights, Booking, Hostelworld, Google Maps directions (with a "go now" link that needs no origin).

## Install

Copy the folder into your agent's skills directory, for example:

```bash
git clone https://github.com/ludodelot/travel-planner-skill ~/.claude/skills/travel-planner
```

Then ask your agent to plan a trip, for example: "I have a long weekend in November, budget 300, I like photography and walking, help me choose and prepare the purchases".

## Structure

```
SKILL.md                         entry point: core rules and workflow table
references/
  workflow.md                    clarify, constrain, search, verify, decide, prepare
  search-efficiency.md           how to search with fewer calls and less context
  tools-and-mcps.md              tools, MCP servers, failure modes
  price-verification.md          labels, checklist, booking order
  constraints-and-calendar.md    work calendar, holidays, bridges, free-trip rule
  entry-requirements.md          visas, electronic authorizations, documents
  accommodation.md               hostel criteria, traps, message templates
  transport.md                   train vs. flight, low-cost, night transfers
  itinerary-design.md            light-aware walking itineraries
  calendar-export.md             event format, links, time zones, series
  results-format.md              how to present answers
  safety-and-consent.md          what the agent never does alone
  events-and-networking.md       triage of local events
  lessons-learned.md             twenty concrete lessons
templates/                       trip note, purchase checklist, calendar event, itinerary prompt
scripts/links.py                 URL builders (stdlib only)
tests/test_links.py              unit tests
examples/                        anonymized case studies
```

## URL builder

```python
from scripts import links  # or: sys.path.insert(0, "scripts"); import links

links.google_flights("MAD", "EDI", "2026-11-07", "2026-11-10")
links.booking_search("San Sebastián", "2026-10-31", "2026-11-02", hostels_only=True, order_by_price=True)
links.maps_directions("Edinburgh Airport", mode="transit")      # starts from the user's location
links.maps_directions("Grassmarket", origin="The Vennel Steps") # starts from a given stop
```

Run the tests:

```bash
python3 -I -m unittest discover -s tests -v
```

## Principles

1. Verify before recommending. Dates and sources, always.
2. Fit the trip to the traveler's calendar, not the other way around.
3. Recommend one thing, show the trade-offs, flag what is unverified.
4. The traveler pays, sends and submits. The agent prepares.
5. No personal data in notes, calendars or this repository.

## Notes on data

Examples use real-world patterns from planning sessions, anonymized. Prices and rules change: always verify against the operator or the official source on the day.

## License

MIT. See [LICENSE](LICENSE).
