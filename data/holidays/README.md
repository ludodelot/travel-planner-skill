# Holiday data

One JSON file per region and year, named `<REGION>-<YEAR>.json` (for example `ES-MD-2026.json`).

```json
{
  "region": "ES-MD",
  "year": 2026,
  "checked": "YYYY-MM-DD",
  "confidence": "what was read and where",
  "sources": ["official decree or calendar"],
  "holidays": [
    {"date": "YYYY-MM-DD", "name": "Holiday", "level": "national | region | city", "scope": "optional note"}
  ]
}
```

Rules:

1. Use the **observed** date, not the printed one: when a holiday falls on a Sunday and the region moves it, write the Monday and say so in the name.
2. `level: city` holidays apply only if the traveler's workplace is in that municipality: the loader lets you exclude them.
3. Always fill `checked`, `sources` and `confidence`. Holidays change every year; do not reuse a file for another year.
4. Prefer the official gazette or government calendar. Cross-check with a second source.
5. Only public facts here: no names, employers or addresses.

Use a file with the CLI:

```bash
python3 -I scripts/cli.py free-trip 2026-11-07 2026-11-10 --remote 1,4 --region ES-MD-2026 --back-home-to-work
python3 -I scripts/cli.py free-trip 2026-11-07 2026-11-10 --remote 1,4 --region ES-MD-2026 --levels national,region
```
