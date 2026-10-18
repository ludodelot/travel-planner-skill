# Searching efficiently

The goal is the fewest calls and the least context for a trustworthy answer.

## Principles

1. **Deterministic first.** Build URLs with `scripts/links.py` instead of typing queries each time. Same inputs, same pages, easy to cache and compare.
2. **Parallel when independent.** Flights for three date variants, hostels for two cities and a holiday lookup do not depend on each other: issue them together.
3. **Cheap before deep.** One round-trip price per candidate and date variant. Go deep (hostels, timings, opening hours) only for the shortlist.
4. **Extract, do not hoard.** After loading a results page, pull the few lines you need (price, times, carrier, cancellation) and drop the rest. Result pages can be tens of thousands of characters.
5. **One source of truth per fact.** Rules from the official body, prices from the live page, opening hours from the venue. Aggregators are hints.
6. **Cache what does not change** (holiday dates, venue addresses, direct property URLs); never cache prices beyond the day.

## Date-variant matrix

For a weekend or bridge, check the base window and its neighbors. Example pattern that paid off: moving the return from Monday to Tuesday lowered a round trip from about 170 to about 90 because the cheap flight pattern was different.

| Variant | Why |
|---|---|
| Base window | Reference |
| Return +1 day | Often cheaper if the extra day is a free day |
| Depart -1 day | Useful when the first day is a remote-work day |
| Different weekday pair | Mid-week fares are usually lower |

## Price pages: what each source gives

| Source | Reliable for | Watch out |
|---|---|---|
| Google Flights (natural-language URL) | Cheapest direct and connecting flights, price level (low/normal/high), a recommended train "from" price | The train price is a "from" price, not the operator's checkout price |
| Operator site (rail, airline) | Final fares, fare conditions, notices | Needs a manual form; deep links with dates are not always possible |
| Booking.com (search URL with dates) | Date-specific hostel prices, free cancellation flag, dorm size in the room name | Rankings can be sponsored; availability notes ("only 1 left") are real signals |
| Hostelworld city page | Reviews, vibe | May ignore dates and show minimum "from" prices |
| Maps (directions) | Walking times, transit options | Times are estimates |

## Efficient hostel selection

1. Search with dates, hostel filter, sorted by price.
2. Extract per property: total for the stay, bed type and dorm size, rating, distance to center, free cancellation, breakfast.
3. Filter by the traveler's rules (for example dorm of 8 beds or fewer).
4. Get the direct property URL for the winner and add the dates to it.

## Stop conditions

Stop and report instead of retrying when: a page returns an error three times, a form needs credentials, a site blocks scripts, or a ticket page shows only a waiting list. Say what you tried and give the manual step.

## Token budget habits

- Summarize results into a table before reasoning about them.
- Keep a running "verified facts" list with source and time.
- Do not re-fetch a page already read in the session unless the data is time-sensitive.
