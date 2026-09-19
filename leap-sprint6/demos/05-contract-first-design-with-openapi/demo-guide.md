# Module 5 Demo Guide — Contract-First Design with OpenAPI

Build `order-service.yaml` up live, section by section, then validate and preview it.

```bash
npx --yes @redocly/cli lint order-service.yaml
npx --yes @redocly/cli build-docs order-service.yaml -o order-service-docs.html
```

Open the generated HTML in a browser — this is the artefact contract-first design produces:
readable API documentation that exists *before* a single line of Spring Boot code, and that a
non-technical stakeholder could review.

## Contract-First vs. Code-First: Say the Difference Out Loud

**Code-first** (what Modules 2-4 have been doing so far): write the `@RestController`, and the
API's shape is whatever the annotations happen to produce. Anyone wanting to know the contract
has to read the Java code.

**Contract-first**: write the API's contract — request shape, response shape, every status code
it can return — *before* any implementation exists. The contract becomes the thing both sides of
a conversation agree to: a frontend team, another backend team, or a compliance reviewer can all
review `order-service.yaml` without needing to read or run any Java at all.

**Say explicitly**: this changes the conversation with stakeholders. A "can we support this
field?" question gets answered by editing a YAML file and re-sending it for review — not by
writing code, discovering a stakeholder wanted something different, and rewriting it.

## Walk Through the Spec, Section by Section

- **`info`** — title, description, version. Point at `version: 1.0.0` — this is the seed of
  Module 4's versioning discussion, made concrete.
- **`paths./orders.post`** — one operation. `operationId: submitOrder` gives it a stable name
  tooling can reference (code generators, documentation links) independent of the URL.
- **`requestBody`** — the exact shape of what a client must send, with a worked `example`. This
  is Module 4's `OrderRequest` shape, formalised.
- **`responses`** — every status code this operation can actually return, each with its own
  schema. Point out `201` (accepted+executed), `400` (malformed input), `401` (preview of Module
  9's JWT work), and `422` (well-formed but rejected by a business rule — straight from
  `shared/mission-brief.md` requirement 4).
- **`components.schemas`** — `OrderRequest`, `OrderResponse`, `ErrorResponse`, defined once and
  referenced (`$ref`) everywhere they're used, instead of repeated inline.
- **`securitySchemes.bearerAuth`** — declares that this API expects a JWT, without implementing
  any actual security yet. The contract can describe security requirements before Module 9
  builds them.

## Why 422, Not Just 400, for a Rejected Order

This is worth a deliberate pause. A `400` means "I can't even understand what you sent me" — the
JSON was malformed, a required field was missing, a type was wrong. A rejected order (valid
shape, but the client's risk limit would be exceeded) is a **different kind of failure** — the
request was perfectly well-formed, but a business rule said no. Mixing these into one status code
would force every client to inspect the response body just to know which kind of failure
happened; splitting them lets infrastructure (and humans skimming logs) tell them apart at a
glance.

## Validation Is Not Optional

Run `redocly lint` again and deliberately introduce an error (delete a required field from
`OrderRequest`, or leave a `$ref` pointing at nothing) to show a real validation failure. **A
YAML file that "looks right" isn't the same as a spec that's actually valid** — the same
discipline as validating any other structured document earlier in the programme.

## Transition to the Lab

Learners write their own OpenAPI spec for a different mission endpoint — retrieving a
previously-submitted order's status — applying every principle from Module 4 and this module's
contract structure.
