# Module 5 Lab — Contract-First Design with OpenAPI

## Objectives

By the end of this lab you will have:

- Understood why writing the contract before the code changes the conversation with stakeholders
- Written a valid OpenAPI spec for a real mission endpoint

## Setup

- Node.js (for `npx`) — no separate install needed
- `order-service.yaml` — a starter spec with `TODO` markers, for `GET /orders/{id}`
- Today's demo (`order-service.yaml` for `POST /orders`) as a worked reference for structure

## The Endpoint

`GET /orders/{id}` — retrieve the status of a previously submitted order (the response you'd
have gotten back from Module 4/5's `POST /orders`, looked up again later).

## Task

Fill in every `TODO` in `order-service.yaml`:

1. Write a real `summary` for the operation
2. Define the `id` path parameter properly — `name`, `in: path`, `required: true`, and a `schema`
3. Add a `404` response for an id that doesn't exist, referencing `ErrorResponse` (already
   defined in the file)
4. Add a `401` response for a missing/invalid JWT, also referencing `ErrorResponse`

## Validate

```bash
npx --yes @redocly/cli lint order-service.yaml
```

This must pass with **no errors** (a warning or two about the license field is fine — the same
warning appears in today's demo spec). Treat a lint error the way you'd treat a failing test:
something is still wrong, keep going.

## Deliverable

A completed, validated `order-service.yaml`.

## Acceptance criteria

- `redocly lint order-service.yaml` reports 0 errors
- The `id` path parameter is properly defined (the linter will catch this if it's missing —
  that's the `path-parameters-defined` rule)
- `200`, `401`, and `404` responses are all present, each with a schema
- The `401` and `404` responses both reference `ErrorResponse`, not `OrderResponse`
