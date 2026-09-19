# Lab 12 — OpenAPI-Generated API Clients

## Setup

Your own `mission-ui` from Module 11, plus the same running mission service, auth service,
and `sprint6-postgres`. Add `springdoc-openapi-starter-webmvc-ui` (version `2.6.0`) to the
mission service's `pom.xml` if it isn't there yet, and confirm you can fetch a real spec:

```bash
curl http://localhost:8090/v3/api-docs
```

You'll also need the two annotations from today's demo on the real mission service (ask your
trainer if these aren't already applied to the class copy):

- `@SecurityScheme(name = "bearerAuth", type = SecuritySchemeType.HTTP, scheme = "bearer",
  bearerFormat = "JWT")` on `MissionServiceApplication`
- `@SecurityRequirement(name = "bearerAuth")` on `OrderController`
- `@PostMapping(produces = MediaType.APPLICATION_JSON_VALUE)` — **the important one**. Without
  this, the generated client will treat every response as an untyped blob and every field
  will come back `undefined` in your component. Today's demo hit this for real; don't skip it.

## Task

1. Save the live spec and generate a client:

   ```bash
   curl http://localhost:8090/v3/api-docs -o mission-service-openapi.json
   npx @openapitools/openapi-generator-cli generate \
     -i mission-service-openapi.json \
     -g typescript-angular \
     -o src/app/generated/mission-api-client \
     --additional-properties=ngVersion=21.0.0,providedInRoot=true
   ```

2. Register the generated client's base path in `app.config.ts`:

   ```typescript
   import { provideApi } from './generated/mission-api-client';
   // add provideApi('http://localhost:8090') to providers
   ```

3. In `mission-api.ts`, `inject()` the generated `OrderControllerService` alongside your
   existing `HttpClient`. Replace the hand-written
   `this.http.post(MISSION_URL, order, { headers: {...} })` call with the generated service's
   `submitOrder(accountId, order)` method — set
   `this.orderApi.configuration.credentials = { bearerAuth: () => token }` right after the
   login call succeeds, **before** calling `submitOrder`.

4. Update any hand-written `OrderRequest`/`OrderResponse` interfaces to use the generated
   `OrderRequestDto`/`OrderResponseDto` instead, and fix any resulting type errors.

## Verify

1. Query Postgres before, exactly as Module 11.
2. Click your submit button. Confirm the same real `ACCEPTED` response, with a real fee and
   new holding quantity — not `undefined` anywhere.
3. Query Postgres again — confirm the same `+1` (or whatever your test order submits).
4. Open DevTools' Network tab, find the order request, and confirm the `Authorization` header
   is present and correctly formed — attached automatically by the generated client, not by
   code you wrote for this specific call.

## A Question Worth Sitting With

Today's demo (and this lab, if you hit it) showed a generated client failing in a way a
hand-written call never would: treating a real, successful JSON response as an untyped blob
because the server didn't declare `produces = application/json`. Why does a hand-written
`HttpClient` call (Module 10/11's style) never have this specific failure mode — what is it
doing differently that a generated client, by design, doesn't do?

A second question: `mission-service-openapi.json` was fetched once and committed as a file,
then used to generate the client. What happens to your generated client if the real
controller's `OrderRequestDto` gains a new required field next sprint, and nobody regenerates
the client? Is this risk different in kind from the risk of a hand-written interface going
stale, or just the same risk with a different first step?
