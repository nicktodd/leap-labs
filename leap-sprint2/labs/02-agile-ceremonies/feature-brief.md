# PaySprint Mobile — Feature Brief: Spending Insights Dashboard

*Continues the fictional PaySprint Mobile backlog from Module 01.*

## Feature description

Customers have asked for a way to understand their spending patterns at a glance, rather than
scrolling through a raw transaction list. The Product Owner wants a new "Insights" tab on the
home screen that gives customers a simple visual breakdown of where their money is going.

## What the Product Owner wants, in their own words

"I want customers to open the app and immediately see: how much they've spent this month
broken down by category (groceries, eating out, bills, etc), how that compares to last month,
and a simple way to drill into any one category to see the transactions behind it. It should
feel lightweight, not like a full accounting tool. Categories should use whatever category data
already exists on each transaction, we're not asking customers to categorise things manually
for version one."

## Known constraints

- Category data already exists on transactions (from an earlier, unrelated backlog item), no
  new categorisation logic is needed for v1
- The mobile team has no existing charting library in the app yet
- The Insights tab needs to work for accounts with very few transactions (new customers) as
  well as accounts with thousands
- No requirement yet to export or share the insights view, that's explicitly out of scope for
  this feature

## Team capacity for this exercise

Treat this as a **one-week sprint** for a team of **5 developers**, each with roughly **6
productive days** available (accounting for the ceremonies themselves, meetings, and normal
task-switching overhead), giving a total team capacity of **30 person-days** for the sprint.
