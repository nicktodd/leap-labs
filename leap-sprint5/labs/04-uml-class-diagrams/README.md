# Module 4 Lab — UML Class Diagrams

## Objectives

By the end of this lab you will have:

- Expressed your Module 3 mission worksheet as a formal UML class diagram, in Mermaid
- Used association, dependency, inheritance, and interface-realization notation correctly
- Rendered the diagram to an image and committed both the source and the render

## Setup

- Node.js (for `npx`) — no separate install needed, `mmdc` runs via `npx --yes @mermaid-js/mermaid-cli`
- Your Module 3 worksheet (`labs/03-ooad-from-requirements-to-objects/worksheet-template.md`,
  filled in)

## Task

1. Create `mission-model.mmd` in this folder.
2. For every class on your Module 3 worksheet, add a `class Name { ... }` block. Include the
   key attributes and methods you identified — you don't need every field, just enough to show
   the shape of each class.
3. For every relationship you sketched, add the matching Mermaid edge:

   | Your Module 3 sketch said... | Use this notation |
   |---|---|
   | "X has a Y" (holds a reference) | `X --> Y` |
   | "X has many Y" | `X "1" --> "*" Y` |
   | "X has a Y, and Y can exist without X" (aggregation) | `X o-- Y` |
   | "X has a Y, and Y is meaningless without X" (composition) | `X *-- Y` |
   | "X uses Y, but doesn't hold onto it" | `X ..> Y` |
   | "X is a kind of Y" (inheritance) | `X --|> Y` |
   | "X implements the Y interface" | `Y` marked `<<interface>>`, edge `X ..|> Y` |

4. Render it:
   ```bash
   npx --yes @mermaid-js/mermaid-cli -i mission-model.mmd -o mission-model.png -b white
   ```
5. Open the PNG and check it against your Module 3 worksheet — does every class and relationship
   you listed actually appear? Anything you had to leave out or simplify to make the diagram
   readable is worth a one-line note (add it as a comment at the top of the `.mmd` file).

## A note on association vs. dependency, and aggregation vs. composition

These are the genuinely new ideas today (your Module 3 sketch didn't distinguish any of them).

- **Association vs. dependency**: does the class permanently hold a reference to the other
  (association, `-->`), or does it just use it briefly, e.g. as a method parameter (dependency,
  `..>`)?
- **Aggregation vs. composition**: for a "has a" relationship, ask "if I delete the whole, does
  the part still make sense on its own?" If yes, it's aggregation (`o--`) — e.g. a `Portfolio`
  references `Instrument`s that exist in the market regardless. If no, it's composition (`*--`) —
  e.g. a `Holding` has no meaning outside the `Portfolio` it belongs to.

Get any of these "wrong" and it's not a disaster — it's exactly the kind of thing Module 6's peer
review will surface and discuss.

## Deliverable

`mission-model.mmd` and `mission-model.png`, both committed. GitHub will render the `.mmd` source
directly if you view it in a markdown code fence — try embedding it in your own README to see this.

## Acceptance criteria

- Every class from your Module 3 worksheet appears in the diagram
- At least one association, one aggregation or composition, one dependency, one inheritance, and
  one interface-realization edge are used, each correctly (not all relationships lumped together
  as one arrow type)
- The diagram renders without errors via `mmdc`
- A model answer is available in `../../solutions/04-uml-class-diagrams/` once you've had a go
