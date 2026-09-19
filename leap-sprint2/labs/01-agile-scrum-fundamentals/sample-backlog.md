# PaySprint Mobile — Sample Product Backlog

A fictional mobile banking feature backlog, used only for this exercise. Items are listed in
the order the Product Owner currently has them, not necessarily the order you'd recommend.

## Backlog items

**PS-101 — View recent transactions**
As a customer, I want to see my 20 most recent transactions on the home screen, so that I can
quickly check my recent spending.
Acceptance criteria:
- Transactions are shown newest first
- Each row shows date, merchant name, and amount
- Tapping a transaction shows its full detail view

**PS-102 — Make the app better**
As a customer, I want the app to be more modern and easier to use, so that I enjoy using it.

**PS-103 — Export transactions to CSV**
As a customer, I want to export my transaction history to a CSV file, so that I can analyse my
spending in a spreadsheet.
Acceptance criteria:
- User can select a date range
- Export produces a valid CSV with date, merchant, amount, and category columns
- Export works for accounts with over 10,000 transactions

**PS-104 — Biometric login**
As a customer, I want to log in using fingerprint or face recognition, so that I don't have to
type my password every time.

**PS-105 — Rebuild the entire app in a new framework**
As the engineering team, we want to rewrite the mobile app in a different framework, so that
it's easier to maintain long-term.

**PS-106 — Set a spending alert**
As a customer, I want to set an alert that notifies me when my spending in a category exceeds a
limit I choose, so that I can stay within budget.
Acceptance criteria:
- User can pick a category and a monthly limit
- User receives a push notification when the limit is crossed
- User can view and edit active alerts from a settings screen

**PS-107 — Dark mode**
As a customer, I want the app to support dark mode, so that it's easier on my eyes at night.

**PS-108 — Freeze a lost or stolen card**
As a customer, I want to freeze my card instantly from the app, so that I can stop fraudulent
use immediately if it's lost or stolen.
Acceptance criteria:
- Freeze takes effect within 5 seconds of confirmation
- Frozen card is clearly shown as frozen in the app
- User can unfreeze the same way

**PS-109 — Improve performance**
As a customer, I want the app to be faster.

**PS-110 — Multi-currency support**
As a customer, I want to see balances and transactions in a currency other than GBP, so that I
can use the app while travelling or living abroad. This would need new backend services for
live exchange rates, a new settings UI, updated transaction display logic across every screen,
and legal review for each new market, we're not yet sure which markets to prioritise.
