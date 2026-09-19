# Module 3 Lab — OOAD: From Requirements to Objects

## Objectives

By the end of this lab you will have:

- Identified candidate entities, responsibilities, and relationships directly from a set of
  business requirements
- Practised deciding what is a class, what is an attribute, and whose responsibility a given
  piece of behaviour is
- Produced a first-draft object model for the mission you'll build for the rest of Sprint 5

## Setup

This is a paper/whiteboard exercise, done in pairs. No code, no UML tooling — that comes in
Modules 4-5. Work from `../../shared/mission-brief.md`.

## Task

Read the mission brief's requirements list (1-7). Then, as a pair, work through the same process
the instructor demonstrated:

### Step 1 — List every noun

Don't filter yet — write down everything: client, portfolio, holding, order, instrument, risk
limit, validation, fee, confirmation, settlement report, and anything else you spot.

### Step 2 — List every verb

submit, validate, reject, execute, calculate, update, record, produce, and anything else.

### Step 3 — Sort the nouns

For each noun, decide: is this a **class** (has identity and behaviour), or just an **attribute**
of some other class (a plain value)? Use `worksheet-template.md` to record your answers. There
isn't always one right answer — if you and your partner disagree, write down both views and the
reasoning. That disagreement is useful input for Module 6's peer review.

Some to argue about deliberately:
- Is a `Portfolio` its own class, or just a collection living on `Client`?
- Is `RiskLimit` a class, or an attribute of `Client`?
- Is a rejected order still an `Order`, or a different kind of thing?

### Step 4 — Assign responsibilities

For each verb, decide which class's job it is. Watch for the temptation to put everything on one
"manager" class that does all the work — that's a smell worth noticing now, even though the fix
(SOLID) comes in Modules 7-8.

### Step 5 — Sketch the relationships

Informally — arrows and words on paper, not UML notation. Who holds a reference to whom? Who
depends on whom to do their job?

## Deliverable

A filled-in copy of `worksheet-template.md` (or your own equivalent, in whatever form your pair
prefers — text, sticky notes photographed, a shared doc). Keep it. You will:

- Compare it against another pair's version in Module 6 (peer review)
- Turn it into UML class and sequence diagrams in Modules 4-5
- Revisit it in Module 14 to discuss what changed and why

## Acceptance criteria

There is no "correct" answer checked automatically in this module — the artefact is the worksheet
itself. A strong worksheet:

- Lists at least eight candidate entities from the requirements, with a class/attribute decision
  and a one-line reason for each
- Assigns every verb from requirements 3-6 to a specific class (not left unassigned, not all
  dumped onto one class)
- Identifies at least one genuinely ambiguous decision and states the reasoning behind the choice
  made, rather than silently picking one
- Sketches the "has many / refers to / coordinates" relationships between the entities identified

A model answer is available in `../../solutions/03-ooad-from-requirements-to-objects/` once you've
had a go — resist looking at it first.
