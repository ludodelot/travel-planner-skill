# Setup: tools and MCP connections for Claude Code

The skill works with only web search. It gets much better with the connections below. Check what is available before promising a capability.

## What each connection adds

| Connection | What it enables | Needed for |
|---|---|---|
| Web search and page fetch (built in) | Rules, official pages, event pages | Everything |
| Browser automation (Claude in Chrome extension) | Live prices, JS-heavy sites, opening purchase tabs, filling forms for the traveler to submit | Browser mode (`browser-purchase-tabs.md`) |
| Google Calendar | Reading real availability, creating itinerary and reminders | Constraint check and calendar export |
| Gmail | Drafting messages to hosts or organizers | Drafts only, never send for the traveler |
| Google Drive or local files | Saving checklists and itineraries | Deliverables |
| A notes folder (for example an Obsidian vault) | Preferences, visited places, constraints | Personal context |

## How to check

- In Claude Code, list connections with `claude mcp list` (or `/mcp` inside an interactive session). A server that "needs authentication" must be authorized by the user in the interactive UI; the agent cannot complete a login for them.
- Connectors such as Google Calendar, Gmail and Drive are enabled in the user's Claude account settings. The browser extension is installed from the browser's extension store and connected to Claude Code.
- If a tool is not connected, say so and use the fallback below.

## Fallbacks

| Missing | Fallback |
|---|---|
| Browser automation | Provide direct links and a checklist; the traveler opens them |
| Calendar | Produce an `.ics` file with `scripts/ics.py` that any calendar can import |
| Gmail | Show the draft text in the answer |
| Notes | Ask for the profile in `templates/traveler-profile.md` and keep it in the project memory |

## Install the skill

Copy or clone the folder into the personal skills directory:

```bash
./install.sh            # copies this folder to ~/.claude/skills/travel-planner
```

Then start a new Claude Code session and ask for a trip. The skill is picked up by its description.

## Permissions

The first time the agent opens pages, creates calendar events or writes files, Claude Code will ask for permission. Approve per action. Payments and form submission are never done by the agent regardless of permissions.

## Sharing privately

For friends: add them as collaborators on the GitHub repository (Settings, Collaborators), then they run `gh auth login` and `./install.sh` after cloning. Nothing in the repository is personal, so it can be made public later without cleaning.
