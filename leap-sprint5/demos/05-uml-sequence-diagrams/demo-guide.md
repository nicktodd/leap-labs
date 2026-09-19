# Module 5 Demo Guide — UML Sequence Diagrams

Continues the Library Book Loans example. Module 4 diagrammed *structure* — what classes exist
and how they relate. Today's demo diagrams *behaviour* — the actual sequence of calls for one
specific scenario: a member borrowing a book.

## Why a Second Diagram Type

A class diagram alone hides all the interesting questions: what order do things happen in? Who
calls whom? What happens when something goes wrong? A sequence diagram answers those, for one
scenario at a time — it's not a replacement for the class diagram, it's a complementary view.

## Live Walkthrough

Introduce the three concepts in order, each with its own small example before the full picture:

1. **Participants and messages** (`concepts/messages.mmd`) — `participant Name as Alias`, then
   `A->>B: message` for a call, `B-->>A: message` for its return. Time flows top to bottom.

2. **Activation** (`concepts/activation.mmd`) — add `+` to a call and `-` to its matching return
   to show the vertical activation bar. Point out: `OrderExecutor`'s bar stays active for its
   entire nested call to `Portfolio` — that's normal. If a bar stays active for almost the whole
   diagram regardless of who it's calling, that's a "doing too much" smell worth flagging.

3. **The `alt` fragment** (`concepts/alt-fragment.mmd`) — real workflows branch. `alt condition
   ... else condition ... end` shows two genuinely different message sequences, not a comment
   saying "or maybe this happens instead."

## Building the Full Diagram

Open `library-borrow-sequence.mmd` and build it up live, narrating each line back to Module 4's
class diagram: every participant here (`Member`, `Library`, `Book`, `Loan`) is a class from that
diagram; every message here is a responsibility assigned back in Module 3.

```bash
npx --yes @mermaid-js/mermaid-cli -i library-borrow-sequence.mmd -o library-borrow-sequence.png -b white -w 1200
```

## Points to Make Explicitly

- **This diagram has no `alt` branch, and that's a gap worth noticing out loud.** What should
  happen if the book isn't available, or the member already has 5 loans? The requirements (Module
  3's worked example) imply a rejection path this diagram doesn't show. Ask the group to sketch
  what an `alt` branch here would look like — it's good rehearsal for the lab.
- **A sequence diagram is a hypothesis, not a fact.** It says "this is the order I think things
  happen in" — Module 6's peer review is where that hypothesis gets checked against someone else's
  reading of the same requirements.

## Transition to the Lab

Learners now sequence-diagram the mission's "client submits an order" scenario, including the
`alt` branch this demo deliberately left out — valid vs. invalid order, straight from Module 3's
requirement 4 ("if an order fails validation, it is rejected... and does not affect the client's
portfolio").
