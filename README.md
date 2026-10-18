<p align="center">
  <img src="assets/banner.png" alt="Voxel airport at night with luggage, a laptop and a small orange voxel mascot" width="100%">
</p>

# Travel Planner Skill for Claude Code

A Claude Code skill that plans trips end to end: where to go, what it really costs today, how it fits your work and holiday calendar, where to sleep, how to get there, a walking itinerary, ready-to-buy browser tabs and a calendar full of map links.

Built from real planning sessions, so it encodes what actually goes wrong: stale prices, hostels with the wrong dorm, trips that cost a vacation day, entry rules found too late, and tools that fail.

> Idioma: [Español](README.es.md)

## What it does

- **Workflow** from clarifying questions to a purchase checklist and calendar export.
- **Verification rules**: every number is `verified`, `from-price` or `estimate`; live checks; date variants.
- **Calendar logic**: public holidays (national, regional, municipal), remote days, bridges and the "free trip" rule, with a calculator.
- **Browser mode**: opens new Chrome tabs ready to buy (rail, hostels, entry authorizations), fills forms only with your confirmation and stops before consent and submit.
- **MCP-aware**: uses Google Calendar, Gmail drafts, Drive and notes when connected, with fallbacks when not.
- **Search efficiency**: deterministic URLs, parallel searches, cheap first, compact extraction.
- **Itineraries** for photographers and videographers: light-aware, walking-friendly, with rain plans.
- **Safe by default**: the agent prepares; you pay, send and submit.

## Install

```bash
git clone https://github.com/ludodelot/travel-planner-skill
cd travel-planner-skill
./install.sh        # copies the skill to ~/.claude/skills/travel-planner
```

Start a new Claude Code session and ask, for example: "I have a long weekend in November, budget 300, I like photography and walking. Help me choose and prepare the purchases."

For browser mode and calendar export, connect the tools described in [references/setup-and-mcps.md](references/setup-and-mcps.md).

## Sharing with friends

The repository can stay private: add friends as collaborators on GitHub, they run `gh auth login`, clone and run `./install.sh`. The repository contains no personal data, so it can become public later without cleaning. Each person keeps their own traveler profile ([template](templates/traveler-profile.md)) in their own notes.

## Scripts (standard library only)

```python
import sys; sys.path.insert(0, "scripts")
import links, free_trip, sun, ics

links.google_flights("MAD", "EDI", "2026-11-07", "2026-11-10")
links.booking_search("San Sebastián", "2026-10-31", "2026-11-02", hostels_only=True, order_by_price=True)
links.maps_directions("Edinburgh Airport", mode="transit")       # starts from the user's location

free_trip.trip_cost("2026-11-07", "2026-11-10", remote_weekdays=(1, 4),
                    holidays=["2026-11-09"], back_home_to_work_last_day=True).vacation_days   # 0

sun.sun_times(55.9533, -3.1883, "2026-11-08", "Europe/London").sunset                          # about 16:18
```

```bash
python3 -I scripts/cli.py free-trip 2026-11-07 2026-11-10 --remote 1,4 --holiday 2026-11-09 --back-home-to-work
python3 -I scripts/cli.py sun 55.9533 -3.1883 2026-11-08 --tz Europe/London
python3 -I -m unittest discover -s tests -v     # 48 tests: scripts, privacy, links, installer
```

`scripts/compare.py` ranks options by effective cost per day; `evals/scenarios.md` lists ten scenarios to check that an agent follows the skill.

## Structure

```
SKILL.md                         entry point: first run, core rules, workflow, scripts
references/                      workflow, search efficiency, tools and MCPs, price verification,
                                 constraints and calendar, entry requirements, accommodation,
                                 transport, itinerary design, calendar export, results format,
                                 safety and consent, events, budget, browser purchase tabs,
                                 setup and MCPs, destination research, post-trip, lessons learned
templates/                       trip note, purchase checklist, calendar event, itinerary prompt,
                                 traveler profile
scripts/                         cli, links, free_trip, sun, ics, compare
tests/                           unit tests, privacy and link checks
evals/                           scenarios to evaluate agent behavior
examples/                        anonymized case studies
install.sh                       installer
```

## Principles

1. Verify before recommending. Dates and sources, always.
2. Fit the trip to the traveler's calendar, not the other way around.
3. Recommend one thing, show the trade-offs, flag what is unverified.
4. The traveler pays, sends and submits. The agent prepares.
5. No personal data in notes, calendars or this repository.

## Notes on data

Examples use real-world patterns from planning sessions, anonymized. Prices and rules change: verify against the operator or the official source on the day.

## License

MIT. See [LICENSE](LICENSE).
