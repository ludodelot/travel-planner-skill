# Exporting the plan to a calendar

## Read before writing

List existing events in the date range and search by trip name. Avoid duplicates; update instead of creating when the event exists. Respect events created by other apps.

## One event per decision point

| Event type | Examples | Notes |
|---|---|---|
| Transport | Flight, airport bus, walking transfer | Flights: show departure in the origin time zone and the duration; state the arrival local time in the description |
| Stay | Check-in night, check-out and luggage storage | One block per night is enough |
| Stops | Each photo spot or visit | Short events (10 to 30 min) with directions |
| Meals and rest | Lunch, dinner, warm-up waits | Mark as free time |
| Tasks | Register, buy, write to the hotel, check weather | Dated reminders, with the links needed |
| Optional | Concerts, side events | Mark `OPTIONAL` and set availability to free |

## Title and description pattern

Title: emoji, then the point of the event, then a short qualifier. Status words go in the description: `PLAN`, `BOOKED`, `OPTIONAL`, `CONDITIONAL`, `UNVERIFIED`.

Description layout:

```
GO NOW (from my location): <directions link without origin>

LOCAL TIME: <time zone and sun times if relevant>
TYPE: PLAN

<photo ideas / video ideas / what to do>
LOGISTICS: distance, minutes, cost, rules, warnings

MAP: <maps search link>
ROUTE FROM PREVIOUS STOP: <directions link with origin>
Approximate times: adapt to reality.
```

Put the "go now" link on the first line so it can be tapped without scrolling.

## Links

- Maps search: `scripts/links.py` `maps_search`.
- Directions from the previous stop: `maps_directions(destination, origin=...)`.
- Directions from where the traveler is: `maps_directions(destination)` with no origin.
- Do not invent URLs. If you only have a name, use a search link.

## Time zones

- Create the event in the destination's local time zone.
- The calendar will display it in the traveler's calendar time zone until the device switches. Tell the traveler to enable "use device time zone".
- Write the local time in the description so it is unambiguous.

## All-day plus timed events

For events that require leaving work early or that are holidays, create an all-day event with the note, and a separate timed event with the real hours, location and links. Invite another address only when the traveler asks; invitations send email.

## Recurring series

Use a weekly rule with an end date (the last working day) and exception dates for holidays. Exception dates must use the same start time as the series. Do not create a recurrence over days already covered by single events.

## Reminders

Popup reminders only, short for transitions (5 to 10 minutes), longer for flights (hours before) and for registrations.

## Notifications

Create and update with notifications off unless an attendee should be emailed on purpose.

## Check afterwards

List the range, verify counts and gaps, and fix wrong descriptions (for example saying something is bought when it is not).
