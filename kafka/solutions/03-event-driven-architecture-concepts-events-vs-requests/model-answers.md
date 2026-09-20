# Module 3 - Model Answers

## Scenario A - End-of-Day Settlement: Request-Driven (Mostly)

The settlement job itself needs definite answers - did this trade reconcile, did that account
balance correctly - before it can mark the day as settled. It genuinely can't proceed to "day is
closed" without confirmed responses. (In practice, the batch job's individual steps might
internally use events for logging/audit trail, but the core "is settlement complete" question is
a request-driven check, because there's a real answer needed before moving on.)

## Scenario B - A Live Price Feed: Event-Driven

Nothing waits for a "response" to a price change - a price change is announced, and every
interested consumer (risk calculations, the dashboard, order pricing) reacts independently,
whenever it happens. No consumer needs to ask "what's the price?" and block for an answer in this
scenario - they're told the moment it changes. (A component that DOES need to ask "what's the
current price right now?" on demand - see Discussion Question 3 - is a different, request-driven
need layered on top of the same event stream.)

## Scenario C - Monthly Client Statements: Request-Driven, Triggered on a Schedule

Generating a statement needs a definite answer to "what happened in this client's account this
month" - it's a lookup, not a reaction to something happening. It could be *triggered* by an
event (a "month-end" signal), but the actual work of assembling the statement is request-driven:
query the data, get a definite answer, build the document.

## Discussion Question 1 - Do the Two Axes Diverge?

**Scenario C is the clearest example of divergence.** Batch vs real-time (Module 2) answered
"batch" - bounded, scheduled, no reason to process incrementally. Event vs request (today)
answers "request-driven" - because generating one statement is a lookup with a definite answer,
not an announcement. The two axes are genuinely independent: "how often does this run" (batch vs
real-time) is a different question from "does the caller need an answer" (event vs request). A
batch job can be built entirely from request-driven calls (as this one is); a real-time system can
be built from either events or a rapid sequence of requests.

## Discussion Question 2 - What Breaks With the Wrong Choice?

**A live price feed built as request-driven** (every consumer polling "what's the price now?")
means every consumer has to guess how often to ask. Poll too rarely and risk calculations use
stale prices; poll too often and you've built a self-inflicted denial-of-service against your own
pricing service, with most requests getting the same unchanged answer. An event-driven feed
sidesteps the whole problem - consumers are told exactly when something changes, no guessing.

## Discussion Question 3 - an Event-Driven System With a Real Answer

Yes - this is a genuinely common pattern, usually called **request-reply over events** (or CQRS's
"read model" approach). Two ways it's normally done:

1. **A materialised view**: a listener continuously consumes the price-change events and keeps an
   up-to-date, queryable store (a simple in-memory cache, or a database table) of "current price
   per ticker." A consumer that needs an answer *right now* queries that store directly - a
   request-driven read against data that was populated by events, not a live request to the
   original price source.
2. **A correlation ID reply pattern**: the requester publishes its own "give me the current price"
   event carrying a unique ID and a "reply to" address; a listener responds by publishing a
   correlated reply event the original requester is specifically listening for. More complex, and
   usually only worth it when the request-driven fallback (option 1) genuinely isn't available.

Most real systems reach for option 1 - it keeps the event stream the single source of truth while
still giving any consumer a fast, definite "what's true right now" answer when it needs one.
