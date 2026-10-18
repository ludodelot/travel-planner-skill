# Changelog

## 0.4.0
- Holiday data: `data/holidays/ES-MD-2026.json` with sources, checked date and levels; `scripts/holidays.py` loader; `cli.py free-trip --region/--levels/--holidays-file`.
- `templates/pre-pay-review.md`: one-screen review after the purchase tabs are open.
- Installer now ships the `data` folder. 58 tests.

## 0.3.0
- `scripts/cli.py`: one command for links, free-trip cost, sun times and option comparison.
- `scripts/compare.py`: rank options by effective cost per day with editable weights and a raw-numbers table.
- Repository checks: valid skill metadata, no broken links, no personal data or secrets, installer test (48 tests).
- New references: destination research, post-trip. New `evals/scenarios.md` with ten behavior checks.

## 0.2.0
- Claude Code skill packaging: first-run profile, browser purchase mode, setup and MCP guidance, `install.sh`.
- New tested scripts: `free_trip.py` (vacation cost), `sun.py` (sunrise, sunset, twilight), `ics.py` (calendar export).
- New references: budget, browser purchase tabs, setup and MCPs. New template: traveler profile.
- CI workflow running the unit tests.

## 0.1.0
- Initial skill: workflow, verification rules, search efficiency, accommodation, transport, itinerary design, calendar export, safety and consent, templates, case studies and `links.py`.
