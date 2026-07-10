# Model Answers — Contract-First Design with OpenAPI

## Why the linter caught the missing path parameter automatically

`path-parameters-defined` isn't a style preference — a path with `{id}` in it and no matching
`parameters` entry is a genuinely broken contract: any code generated from this spec, or any
consumer reading it, would have no idea what `{id}` is supposed to be or what type it takes. This
is the OpenAPI equivalent of Sprint 5's `mmdc` refusing to render a diagram with an unmatched
activation bar — the tool enforces a structural correctness rule that would otherwise only be
caught by someone reading carefully, or not at all.

## Why `401` and `404` both use `ErrorResponse`, not two different schemas

Both are genuinely "something went wrong, here's a message" — there's no reason for a client to
need a different shape depending on *which* error happened, only a different status code and
message. Reusing one `ErrorResponse` schema for every error case keeps client-side error handling
simple: check the status code, then read `message` from the same place regardless of which error
it was.

## Why this spec doesn't include a `400`

`GET /orders/{id}` doesn't take a request body — there's nothing a client could send that's
"malformed" the way a `POST` body could be. The only things that can go wrong are: no such order
(`404`), or not authenticated (`401`). Not every operation needs every status code — the model
answer to "which status codes does this operation return" is always "the ones that can actually
happen for this specific operation," not a fixed checklist applied uniformly everywhere.

## What this spec sets up for later modules

- Module 6 turns `OrderRequest`/`OrderResponse` into real Java DTOs with Bean Validation
  annotations, directly from this schema
- Module 9 makes the `bearerAuth` security requirement, already declared here, actually enforced
- The `422` response from today's demo spec (business-rule rejection) becomes a real code path
  once Module 11's mission build wires `OrderValidator` behind this contract
