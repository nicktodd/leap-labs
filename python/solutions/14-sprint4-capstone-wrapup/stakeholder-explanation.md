# Stakeholder Explanation - PaySprint February Card Payments Dashboard

## Why we read the data the way we did

The dashboard reads the monthly export file for February, not the live payments system. February
is closed: no new payments will be added to it, so a live connection would give us nothing the
file does not already contain. The file holds 143 rows, a small amount of data that is quick to
read. The live system only hands out payments in batches and limits how many requests we can
make in a short period, so collecting the whole month that way means several requests and
sometimes a pause of up to ten seconds. Most importantly, a file gives the same numbers every
time the dashboard is run, so anyone who questions a figure can check it against the same
source. The live system is the better choice for questions about today, such as the fraud team
checking this morning's declined payments, and our dashboard is built so that only the first
step would change if we switched.

## Why we are confident the numbers are trustworthy

The export arrived with problems, and the dashboard fixes or removes each one before any figure
is calculated:

- **Duplicates.** Two payments appeared twice. One copy differed only in spacing and capital
  letters, so it only showed up as a duplicate after we had tidied the text. Left in, each
  would have counted the same payment twice.
- **Unusable amounts.** One payment had a blank amount and one said "TBC". We removed both
  rather than guess a value, because a guessed amount would feed into every total.
- **An impossible date.** One payment was dated 29 February 2026, a day that does not exist.
  It could have been the 28th or 1 March, so we set it aside instead of choosing for it.
- **Different currencies.** Payments are in pounds, euros and dollars. We convert everything
  to pounds before adding it up. Adding the raw amounts together would have overstated the
  month's total by GBP 2,562.63.
- **Inconsistent spelling.** On 15 rows the payment type was written in a non-standard way
  (for example "online", "ONLINE" or "instore"), and the United Kingdom appeared as "UK" on 7 rows
  instead of the standard "GB". Left alone, these would have split one group into several and
  made every breakdown wrong.

In total, 143 rows were received, 5 were removed for the reasons above, and 138 were used. After
cleaning, the dashboard runs a set of checks: every payment has an identifier that appears only
once, every value comes from the expected list, every currency has a conversion rate, every
amount is above zero and every date falls inside February's reporting period. If any check
fails, the dashboard is not produced at all, and the message says which check failed. We
tested this by deliberately removing the dollar conversion rate: the run stopped and named the
8 dollar payments it could not convert.

## What we left out, and why

One payment of GBP 1,850.00 at Pret A Manger was made by contactless card, which is limited to
GBP 100. It is almost certainly GBP 18.50 typed without the decimal point. We have not deleted
or corrected it, because only the card processor's records can confirm the true amount. It is
kept in the data but left out of the spend figures until it is confirmed; including it would
have added GBP 1,850.00 to a customer-spend total of GBP 7,295.33.

"Customer spend" on the dashboard means payments that were approved and were not confirmed as
fraud. Declined payments are excluded because no money changed hands, and confirmed fraud is
shown separately so that it does not inflate what customers chose to spend.
