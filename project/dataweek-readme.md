# Data Week - Project Friday Guidance

## Context

This week's teaching covers data systems concepts, Postgres, SQL fundamentals through
subqueries and joins, data quality, RDBMS modelling, ER diagrams, choosing between relational and
NoSQL stores, and Snowflake as a cloud data warehouse.

This is the first week and one of the things you might want to explore is your projects's own data model. Go back to the business
requirements spec, this is where BR-06, BR-09, BR-14/15 and BR-16 stop being sentences on a page
and start being decisions about what you store and how.

## The trap to avoid

A week of RDBMS modelling and ER diagrams makes "one normalised Postgres schema for everything"
feel like the obvious answer. It's the freshest tool in your hand, so it's the one you'll reach
for. Before committing to that, look again at what the spec is actually asking for:

- BR-09 needs an order's fill, the cash movement and the position change to succeed or fail
  together, that's a strong argument for one transactional store.
- BR-14/15 and section 9.4 need a permanent, unalterable record that survives a restart or a bad
  deployment, at any point a regulator can ask to see it. Is that the same thing as "the current
  state," or a different property this store has to have?
- BR-16, and Priya's persona in section 6, need trading activity analysed by instrument, period
  and client segment, without competing with Joanna placing a live order. That's the same
  question Module 12 asked you to reflect on, does this genuinely want the OnLine Transaction Processing (OLTP) database, or
  something else?

You did Module 11 this week: classify your own platform's capabilities the way you classified
PaySprint's scenarios, by actual access pattern, not by instinct. The answer might genuinely be
"one store, well designed, is enough", that's a legitimate outcome if you can defend it against
the requirements above. What isn't legitimate is not asking the question, and documenting the decision.

This is also a good moment to hold your original candidate architecture up against what you now
know. If it said "a database" without saying which kind or how many, does it still hold up?

## Suggested Friday session

- Before drawing any ER diagram, list the platform's capabilities that need data (order
  processing, positions and cash, the audit trail, reporting) and for each one, its access
  pattern: read-heavy or write-heavy, current-state or historical, who queries it and how often.
- Decide, capability by capability, whether it belongs in the same store as the others or not,
  and write down the requirement that drove each decision.
- Design and review the schema for whatever you've decided is your transactional store, as a
  full team, every member should be able to defend it, not just whoever drew it.
- If you've decided any capability needs a different kind of store, don't build it this week,
  just capture the decision and what it implies for later weeks.
- If modelling this has left your team assuming something the spec doesn't actually say, how
  long history really needs to be kept, what "reporting" means to the business, anything like
  that, that's a fast question for your customer instructor rather than a guess baked into the
  schema. Module 10 taught you how to frame exactly this kind of check.

## What to present to the class

- Your capabilities-to-storage breakdown, and the requirement behind each decision.
- A walkthrough of your current thinking around any potential schemas or NoSQL database structures.
- Anywhere your original architecture pitch has changed now that you've actually modelled the
  data, and why.
- An updated backlog and risk list.
