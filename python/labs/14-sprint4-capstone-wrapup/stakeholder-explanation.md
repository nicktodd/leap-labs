# Stakeholder Explanation - PaySprint February Card Payments Dashboard

> Team task. Write this in PLAIN LANGUAGE for PaySprint's head of card payments, who does not
> write code. No unexplained acronyms or jargon ("ETL", "DataFrame", "NaT", "dtype" all need
> rewording). Every claim should be specific to this dataset and this team's choices, not a
> generic statement. Delete these instructions once you have written your answers.

## Why we read the data the way we did

<!-- TODO: Explain why the dashboard reads the monthly export file rather than the payments
     API from Module 11 (or the reverse, if your team chose the API). Give a SPECIFIC reason
     grounded in this data: how many transactions there are, whether February can still
     change now that the month has closed, how many requests and rate-limit waits a full
     download takes, and whether the dashboard should give the same numbers every time it
     is run. Say when the other option would be the better choice. -->

## Why we are confident the numbers are trustworthy

<!-- TODO: Name the problems your cleaning found in the export and what each would have done
     to the dashboard if nobody had caught it. Use the real counts from your data-quality
     line. For example: what would a duplicate payment have done to total spend? What would
     adding euros and dollars to pounds without converting them have done? Why did you
     reject the payment dated 29 February instead of choosing a date for it? -->

<!-- TODO: Explain, in one or two sentences, what your validation step checks and what
     happens if a check fails (the dashboard is not produced). -->

## What we left out, and why

<!-- TODO: Name the payment you held for review instead of deleting or correcting, and why.
     Say which transactions your "customer spend" figure excludes (for example declined
     payments and confirmed fraud) so the reader knows exactly what the headline number
     means. -->
