# Browser mode: open ready-to-buy tabs (Claude in Chrome)

Goal: the traveler clicks "pay" on pages that are already open on the right dates. The agent researches, opens, reads and fills only what the traveler confirms.

## Requirements

- A browser-automation tool (for example the Claude in Chrome extension and its MCP tools). Without one, fall back to a markdown checklist with direct links.
- Tool names vary by setup. The pattern below uses generic names: list tabs, create tab, navigate, read page text, screenshot, find element, click, type, run script.

## Session start

1. **List the existing tabs first** and note which belong to the traveler. Never reuse their tabs unless asked.
2. Create **one new tab per task** (flights, accommodation, rail, authorization) and keep a map: `tab -> purpose`.
3. Tell the traveler which tab holds what, in a short table.

## Opening a purchase page

1. Navigate with a **deterministic URL** (`scripts/links.py`): dates, travelers and filters in the URL when the site supports it.
2. Read the page text, extract only price, times, conditions and cancellation. Do not paste whole pages into the answer.
3. If the site ignores the URL parameters (some operator checkouts and hostel city pages do), open the search form and tell the traveler which fields to enter: origin, destination, dates, fare.
4. Take a screenshot when the layout matters (calendars, consent dialogs).
5. Stop at the checkout page. Do not enter card or bank data, passwords or passport numbers.

## Filling forms (registrations, waiting lists)

- Ask once for missing values (phone, entity, gender field) and offer a default.
- Fill the fields, then **stop before consent and submit**. The traveler ticks the box and presses send.
- After filling, list exactly what you typed so they can check it.
- If a form needs account credentials or a payment method, stop and explain.

## Cookie banners and consent

Do not accept legal terms or marketing consent for the traveler. A cookie banner that blocks the page: choose the least permissive option if asked to proceed, otherwise leave it and tell the traveler.

## Reading data from pages

- Prefer reading the page text. Use element search to find a button or link target, and a small script only to extract link URLs.
- Some pages block scripts that touch cookies or query strings: switch to reading text instead of retrying.
- A guessed URL that returns an error: search the site's navigation for the right page, do not retry guesses.

## Tab hygiene

- Close tabs you opened for lookups when done; leave purchase tabs open.
- If the traveler changed or closed a tab, refresh the tab list before acting.
- Do not trigger browser dialogs (alerts, confirms) that block the tool.

## Stop conditions

Report instead of looping when a page fails three times, the extension does not respond, or an element does not react. Say what you tried and the manual step.

## Report format after opening tabs

| Tab | What it is | What to do | Dates |
|---|---|---|---|
| 1 | Rail search | Enter origin, destination, date; pick the flexible fare | Fri, Mon |
| 2 | Hostel A (dates set) | Book with free cancellation | 2 nights |
| 3 | Entry authorization (official) | Apply; check nationality exemption first | urgent |

Use `templates/pre-pay-review.md` for a one-screen review before the traveler pays.

Never claim a purchase is done. The traveler pays.
