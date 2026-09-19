# Module 4 Lab — REST API Design Principles

## Objectives

By the end of this lab you will have:

- Critiqued a real (deliberately poor) API design against REST principles
- Proposed a corrected resource/verb structure, with proper status codes and idempotency

## Setup

- `bad-api-spec.md` — the API to critique
- `redesign-template.md` — fill this in as your deliverable
- Today's demo (`OrdersController.java`) as a working example of the patterns you're applying

## Task

### Part 1 — Critique

Read `bad-api-spec.md`. It works, in the sense that every endpoint does what it claims — your
job is to identify what's wrong with *how it's designed*, not whether it functions. Look for:

- Verbs in URLs, where the HTTP method should be doing that job
- An HTTP method used for the wrong kind of operation (especially: anything using `GET` to
  change data)
- Inconsistent resource naming (is it `/order` or `/orders`? Does that matter?)
- Status codes that don't reflect what actually happened
- Anything that makes the API harder to use safely from a network-flaky client

### Part 2 — Redesign

Using `redesign-template.md`, rewrite the API properly: one resource path, the right HTTP verb
for each operation, real status codes, and a note on which operations are safe to retry blindly.

### Part 3 — Versioning

Answer the versioning question in the template — this is a judgement call, not a right/wrong
answer, but you should be able to justify your position.

## Deliverable

A completed `redesign-template.md`.

## Acceptance criteria

- At least 6 distinct issues identified in Part 1, each naming a specific endpoint and a
  specific REST principle it violates
- The redesign uses no verbs in any URL — the HTTP method carries that meaning instead
- At least three different status codes appear across the redesign (not everything returning 200)
- Every redesigned operation has an explicit idempotency answer (yes/no), with reasoning for at
  least the POST/create operation
- A model answer is available in `../../solutions/04-rest-api-design-principles/` once you've
  had a go
