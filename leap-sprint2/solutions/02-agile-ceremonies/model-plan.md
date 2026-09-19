# Module 02 Lab — Model Sprint Plan (Instructor Reference)

There's no single correct breakdown, this is one reasonable example for calibrating what
"good" looks like.

## Example story breakdown

1. **View monthly spend by category** (5 points)
   As a customer, I want to see my total spend this month broken down by category, so that I
   can understand where my money is going.
   - Categories shown as a simple list or chart, ordered by spend, highest first
   - Uses existing transaction category data, no manual categorisation
   - Handles accounts with zero or very few transactions gracefully (shows an empty state, not
     an error)

2. **Compare spend to last month** (3 points)
   As a customer, I want to see how this month's category spend compares to last month, so
   that I can spot changes in my habits.
   - Each category shows a simple up/down indicator or percentage vs the prior month
   - If there's no data for last month (new account), the comparison is hidden, not shown as
     broken

3. **Drill into a category's transactions** (3 points)
   As a customer, I want to tap a category to see the transactions behind it, so that I can
   understand what makes up that total.
   - Tapping a category opens a filtered transaction list for that category and month
   - List reuses the existing transaction detail view from Module 01's PS-101

4. **Add an Insights tab to the home screen** (2 points)
   As a customer, I want an Insights tab alongside my existing home screen tabs, so that I can
   find this feature naturally.
   - New tab appears in the existing tab bar, doesn't require a design overhaul elsewhere

5. **Introduce a charting component** (5 points, technical enabler)
   As the development team, we want a reusable charting component in the app, so that Insights
   and future features can render simple charts consistently.
   - Not customer-facing on its own, a foundation the other stories depend on

6. **Handle new/low-activity accounts** (2 points)
   As a customer with a new account, I want the Insights tab to show a helpful empty state
   rather than a blank or broken screen, so that the feature still feels finished.

**Total: 20 points.** Given a rough 1 point ≈ 1-1.5 person-days rule of thumb, that's
consistent with the team's 30 person-day capacity, with some headroom for the ceremonies
themselves and normal task-switching, a realistic sprint rather than an optimistic one.

## Example sprint goal

"Give customers a clear, at-a-glance view of where their money went this month, without
needing a full accounting tool."

Notice this survives even if story 6 (empty states) slips to next sprint, it's about the
customer value, not a checklist of the stories above.

## What to watch for as an instructor

- Teams that write "Build the Insights dashboard" as a single story, that's PS-105 from Module
  01 all over again, not sized for a sprint.
- Teams that anchor on the first number said aloud instead of voting simultaneously, this
  undermines the whole point of Planning Poker.
- Sprint goals that just list the stories ("Ship stories 1-4"), rather than describing the
  value, ask them to rewrite it as a sentence a stakeholder would actually care about.
