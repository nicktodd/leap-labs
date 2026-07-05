# Stakeholder Explanation: Why We Built the Dashboard This Way

We read the trade data from a daily file, not a live connection. For a book this size —
twenty trades, updated once a day — a file is simpler and more reliable than querying a live
system every time we run a report, and it doesn't depend on that system being available right
when we need it. A live connection only earns its extra complexity once the data changes many
times a day, or we only ever need a small slice of it rather than the whole book.

We're confident the underlying numbers are trustworthy because every figure in this dashboard
comes from data that's already been checked: missing or badly-formatted entries are caught and
either fixed or flagged before they ever reach a chart, rather than being discovered by accident
later. That checking runs automatically every time the data is refreshed, not just once by hand.

The three findings in this dashboard — which asset class makes up most of the book, which
advisor's clients trade in larger amounts on average, and how this week's activity compares to
last week's — are the kind of thing we'd expect a manager to ask about directly. Each one is
backed by a specific number from the data, not a general impression.
