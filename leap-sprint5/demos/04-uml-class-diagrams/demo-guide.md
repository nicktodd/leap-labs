# Module 4 Demo Guide — UML Class Diagrams

Continues the Library Book Loans example from Module 3. Learners already have the entities,
responsibilities, and relationships on paper — today's demo shows how to express that same
model formally, in UML class diagram notation, using Mermaid.

## Why Mermaid

- Diagrams live as **text**, in the git repo, next to the code they describe — they diff and
  review like code, and never go stale in a slide deck nobody re-opens.
- GitHub renders `.mmd`-embedded fences natively — no separate viewer needed to review a PR.
- The same source renders to an image (via `mmdc`, the Mermaid CLI) for embedding in slides.

## Live Walkthrough

Open `library-model.mmd` and build it up line by line, mapping directly back to Module 3's
worksheet:

1. **Classes first** — one `class Name { ... }` block per class identified in Module 3.
   Attributes use `-` (private) or `+` (public); methods look like `+name() returnType`.

2. **Relationships next** — this is where UML notation adds precision that the informal
   Module 3 sketch didn't have:
   - `-->` = association ("has a reference to")
   - `o--` = aggregation ("has a", but the part can outlive the whole)
   - `*--` = composition ("has a", and the part cannot exist without the whole)
   - `..>` = dependency (uses it, but doesn't hold a permanent reference)
   - `--|>` = inheritance ("is a")
   - `..|>` = interface realization ("implements")
   - Multiplicities in quotes: `"1"`, `"*"`, `"0..1"` — read the Member/Loan line as "one Member
     has many Loans"

3. **Render it**:
   ```bash
   npx --yes @mermaid-js/mermaid-cli -i library-model.mmd -o library-model.png -b white -w 1400
   ```
   `direction LR` at the top of the diagram lays classes out left-to-right instead of top-to-bottom
   — for a linear chain like this one it renders far more legibly on a 16:9 slide (wide and short,
   instead of tall and narrow). `-w 1400` renders at a higher base resolution so text stays sharp
   once scaled into a slide.

### Before the class diagram: five relationships, five slides

Before touching the library model, the slide deck walks through the five relationship types one
at a time, each as its own concrete example rendered from `relationships/*.mmd` — every example
uses a class name straight out of Modules 1-2, so the notation lands as "notation for OO ideas you
already know", not as new content to memorise:

| Relationship | Example | File |
|---|---|---|
| Association | `Order --> Client` | `relationships/association.mmd` |
| Aggregation | `Portfolio o-- Instrument` | `relationships/aggregation.mmd` |
| Composition | `Portfolio *-- Holding` | `relationships/composition.mmd` |
| Inheritance | `BondInstrument --|> Instrument` | `relationships/inheritance.mmd` |
| Implements | `Instrument ..|> Feeable` | `relationships/implements.mmd` |

Spend the most time on **aggregation vs. composition**, since it's the pair everyone mixes up:
ask "if the whole is deleted, does the part still make sense on its own?" — an `Instrument` still
exists in the market with no `Portfolio` pointing at it (aggregation, open diamond); a `Holding`
means nothing without the `Portfolio` it belongs to (composition, filled diamond). The two example
diagrams are deliberately near-identical in layout, differing only in the diamond — that's the
whole point: the shape of the diamond is doing all the semantic work.

## Points to Make Explicitly

- **Association vs. dependency is a real design decision, not decoration.** `Library ..> Member`
  (dependency) rather than `Library --> Member` (association) says: Library doesn't *hold* a
  permanent list of members, it just uses one when asked. Compare to `Member --> Loan`, which is
  a genuine "has many" association — Member really does hold its loans.
- **The diagram should match the worksheet, not replace the thinking.** If a class or
  relationship shows up in the diagram that wasn't in the Module 3 worksheet, that's worth
  noticing — either the worksheet missed something, or the diagram is inventing structure that
  isn't justified yet.
- **This is still a first draft.** Nothing here is final until Module 6's peer review.

## Transition to the Lab

Learners now do the same thing to their own Module 3 mission worksheet: turn
`Client`/`Portfolio`/`Holding`/`Order`/`Instrument`/etc. into a Mermaid class diagram, render it,
and commit the `.mmd` (and rendered `.png`) into their lab folder.
