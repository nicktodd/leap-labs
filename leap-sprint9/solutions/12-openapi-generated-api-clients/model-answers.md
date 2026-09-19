# Lab 12 Model Answers

## Verified Output

Built and run for real, against the actual mission service (with springdoc, the two security
annotations, and `produces = APPLICATION_JSON_VALUE` all applied):

- `curl http://localhost:8090/v3/api-docs` returned a real spec whose
  `/accounts/{accountId}/orders` operation matched the real controller exactly.
- Generating the client produced a typed `submitOrder(accountId: number, orderRequestDto:
  OrderRequestDto): Observable<OrderResponseDto>` method.
- Clicking submit in the running app: real `ACCEPTED` response, fee and new holding quantity
  both populated (not `undefined`) — confirmed only after adding `produces =
  APPLICATION_JSON_VALUE`, which this lab's own first attempt was missing, exactly like
  today's demo.
- DevTools Network tab: the order request's `Authorization` header was present and correctly
  formed, attached by `configuration.credentials.bearerAuth`, set once after login.

## Key Points

- **Why the blob bug happened**: the generated client inspects the *declared* response
  content type to decide how to parse the body. Without an explicit `produces`, Spring's
  default content negotiation is permissive (`*/*`), and the generator's `isJsonMime()` check
  correctly refuses to *assume* JSON from an ambiguous declaration — it defensively falls back
  to `blob`. This isn't a generator bug; it's the generator being honest about what the spec
  actually promised.
- **`configuration.credentials`**: set once, right after the login response arrives, and
  every subsequent call through that same service instance picks it up automatically —
  because `addCredentialToHeaders` runs inside the generated method itself, on every call.

## The Reflection Questions

**Why a hand-written call never hits this failure mode**: a hand-written `HttpClient` call
(Module 10/11's style) is told what to expect by the *developer*, not inferred from a
declared content type — `this.http.post<OrderResponseDto>(url, body)` simply asserts "treat
the response as this shape," and `HttpClient`'s default `responseType: 'json'` just parses
whatever comes back as JSON, no content-type inspection involved. This is exactly the
trade-off: a hand-written call is *less safe* (it'll happily "parse" an HTML error page as if
it were JSON and produce nonsense) but can never get confused by an ambiguous or missing
`produces` declaration, because it was never looking at one in the first place. A generated
client is more careful, which is usually a strength — until the server it's generated from
under-declares itself.

**The staleness risk**: this is the same underlying risk as a hand-written interface going
stale — both describe a shape by hand (well, in this case, by tool) at one point in time,
and both can silently disagree with reality later if nobody re-syncs them. What's actually
different is the *failure mode* when they drift: a hand-written interface that's gone stale
still compiles and runs, silently accepting or losing fields at runtime with no signal
anything's wrong. A generated client regenerated against a *newer* real spec, by contrast,
would immediately show TypeScript compile errors wherever the new required field is missing
from existing calls — the staleness becomes a compile-time problem instead of a silent
runtime one, provided the client is actually regenerated. If it's *never* regenerated, though,
both approaches are equally blind to the drift; the compile-time safety is only realised at
the moment someone actually reruns the generator.
