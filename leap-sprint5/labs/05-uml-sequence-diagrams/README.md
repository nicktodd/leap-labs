# Module 5 Lab — UML Sequence Diagrams

## Objectives

By the end of this lab you will have:

- Expressed the mission's "client submits an order" workflow as a UML sequence diagram, in Mermaid
- Used synchronous calls, return messages, and activation bars correctly
- Modelled a genuinely conditional path (valid vs. invalid order) using the `alt` fragment

## Setup

- Node.js (for `npx`), same as Module 4
- Your Module 4 `mission-model.mmd` (class diagram) — every participant in today's diagram should
  be a class that already exists there
- `shared/mission-brief.md`, requirements 3-6 (validation, rejection, execution, reporting)

## Task

1. Create `mission-order-sequence.mmd` in this folder. Start it with
   `%%{init: {'sequence': {'mirrorActors': false}}}%%` on its own line before `sequenceDiagram` —
   this stops Mermaid repeating every participant box at the bottom of the diagram, which just adds
   noise once the lifelines are long.
2. Add one `participant` per object involved in processing an order. At minimum: `Client`,
   `Order`, `OrderValidator`, `OrderExecutor`, `Portfolio`, `Instrument`, `SettlementReport` — use
   your own Module 4 class names if they differ.
3. Sequence the **happy path** first: client submits an order, it gets validated, executed, and
   reported on. Use `->>` for each call and `-->>` for its return.
4. Add activation bars (`+` / `-`) so it's visible which object is doing work at each step.
5. Wrap the validation outcome in an `alt` fragment:
   ```
   alt order is valid
       ... execute, update the holding, report as accepted ...
   else order is invalid
       ... report as rejected, with a reason ...
   end
   ```
6. Render it:
   ```bash
   npx --yes @mermaid-js/mermaid-cli -i mission-order-sequence.mmd -o mission-order-sequence.png -b white -w 1200
   ```

## A note on what belongs in the diagram

Don't try to show every possible validation rule from the mission brief as a separate branch —
one `alt` with a valid/invalid split is enough to demonstrate the technique. The point isn't
exhaustive coverage, it's showing that you can express a genuinely conditional workflow, not just
a straight line of calls.

## Deliverable

`mission-order-sequence.mmd` and `mission-order-sequence.png`, both committed.

## Acceptance criteria

- Every participant in the diagram corresponds to a class in your Module 4 `mission-model.mmd`
- At least one synchronous call and its matching return are shown correctly
- At least one activation bar is used, with matching `+`/`-` (an unmatched activation will fail to
  render — `mmdc` will error out, which is itself useful feedback)
- An `alt` fragment models the valid/invalid order split, with a distinct sequence of messages in
  each branch
- The diagram renders without errors via `mmdc`
- A model answer is available in `../../solutions/05-uml-sequence-diagrams/` once you've had a go
