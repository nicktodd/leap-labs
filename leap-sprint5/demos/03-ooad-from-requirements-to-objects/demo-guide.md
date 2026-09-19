# Module 3 Demo Guide — OOAD: From Requirements to Objects

This is a live, instructor-led walkthrough. Do it on a whiteboard or shared
doc, not slides — the point is to show the *process*, not a finished answer.
Use a domain the mission doesn't use, so learners still have their own
discovery to make when they tackle the mission brief in the lab.

## Worked Example: Library Book Loans

Read this requirement out loud, one sentence at a time, and build the table
live as you go. Don't pre-empt it — let the group call out candidates and
argue about them.

> "A library member can borrow up to five books at a time. When a member
> borrows a book, a loan record is created with a due date 21 days later. If
> a book is returned after its due date, the member is charged a late fee of
> 20p per day. A member with more than £5 of unpaid fees cannot borrow
> further books until the fees are paid."

### Step 1 — Underline every noun

Nouns are **candidate classes** or **candidate attributes**. Write them all
up, don't filter yet: *library, member, book, loan record, due date, late
fee, unpaid fees*.

### Step 2 — Underline every verb

Verbs are **candidate responsibilities** (methods). *borrow, create, return,
charge, pay*.

### Step 3 — Sort nouns into "thing with identity and behaviour" vs. "just a value"

This is the step learners usually skip, and it's the one worth slowing down
on.

| Noun | Class, or just an attribute? |
|---|---|
| Member | Class — has identity, has behaviour (borrows, pays fees) |
| Book | Class — has identity (a library owns many copies) |
| Loan | Class — this is the easy one to miss. It's not just "a member has a book" — it has its own data (due date) and its own behaviour (is this overdue?) |
| Due date | Attribute of Loan, not its own class |
| Late fee | This is interesting — is it an attribute of Loan, or a responsibility of Member (they accumulate across loans)? Let the group debate; there's a defensible answer either way. |

### Step 4 — Assign responsibilities (verbs) to classes

For each verb, ask: **whose job is this, really?** This is where "God
classes" get created if you're not careful — resist putting everything on
`Member`.

| Responsibility | Best owner | Why |
|---|---|---|
| Create a loan when a book is borrowed | `Library` or a `LoanService` — not `Member` and not `Book` alone, because it needs both plus a rule check | 
| Check if a member can borrow (< 5 active loans, < £5 fees) | `Member` — it's the member's own state being checked |
| Calculate a late fee for a returned loan | `Loan` — it has the due date and return date, everything it needs |
| Track total unpaid fees | `Member` — accumulates across loans |

### Step 5 — Draw the relationships (informally, no UML notation yet)

- A `Member` **has many** `Loan`s
- A `Loan` **refers to** exactly one `Book` and exactly one `Member`
- `Library` **coordinates** — it's often the "verb-heavy" class that doesn't
  map to a single noun in the requirements at all. That's normal: not every
  useful class is a noun in the original text.

### The Point to Land

Nobody gets this right on the first pass, and that's fine — that's what
Module 6 (peer review) and Modules 7-8 (SOLID) are for. The goal of Module 3
is a **defensible first draft**, not a correct final answer. Move fast,
argue about the genuinely ambiguous calls (like the late-fee ownership
question above), and don't get stuck polishing.

## Transition to the Lab

Now hand off to `shared/mission-brief.md`. Learners repeat this exact
process — nouns, verbs, sort, assign, relate — against the Order Processing
& Settlement Engine requirements, in pairs, without writing any UML yet.
UML comes in Modules 4-5, once there's a design worth diagramming.
