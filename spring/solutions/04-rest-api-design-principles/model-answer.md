# Model Answer - API Critique & Redesign

## Part 1: What's Wrong

| Endpoint(s) | Problem | Principle violated |
|---|---|---|
| `GET /getAllOrders`, `GET /getOrder`, `POST /createOrder`, `POST /deleteOrder/123` | Verbs (`get`, `create`, `delete`) baked into the URL | Resources should be nouns; the HTTP method is the verb |
| `GET /updateOrderStatus?id=123&status=REJECTED` | `GET` is used to change state | `GET` must be safe - it should never mutate anything. A crawler, a cache, or a browser prefetch could accidentally reject a real order |
| `POST /order` vs `POST /createOrder` vs `/orders/123/...` | Three different naming conventions for the same resource in one API | Inconsistent resource naming makes the API unpredictable to use |
| `/orders/123/getFee` | A verb nested inside an otherwise resource-shaped path | Same issue as above, inconsistently applied |
| Every endpoint returns `200`, with `success: true/false` in the body | Status codes carry no real meaning; clients must parse the body just to know if a call succeeded | HTTP status codes exist specifically so infrastructure (caches, load balancers, monitoring, retry logic) can understand outcomes without reading the body |
| No versioning strategy, justified by "no breaking change has happened yet" | Confuses "we haven't needed it" with "we don't need a plan for when we do" | Not a REST principle exactly, but a real operational risk - the first breaking change will be unplanned |
| `POST /deleteOrder/123` | `POST` used for a delete operation | `DELETE` is the correct verb; using `POST` hides the operation's idempotency from anything that understands HTTP semantics (caches, proxies) |

## Part 2: The Redesign

| Method | URL | Status codes it can return | Idempotent? |
|---|---|---|---|
| `GET` | `/orders` | `200` | Yes - always safe to repeat |
| `GET` | `/orders/{id}` | `200`, `404` | Yes |
| `POST` | `/orders` | `201` (with `Location` header), `400` | **No** - each call creates a new order |
| `PATCH` | `/orders/{id}/status` | `200`, `404`, `409` (if the status transition isn't valid) | Yes - setting status to `REJECTED` twice in a row leaves the same end state |
| `DELETE` | `/orders/{id}` | `204`, `404` | Yes - deleting twice is safe |
| `GET` | `/orders/{id}/fee` | `200`, `404` | Yes |

Note `PATCH` rather than `PUT` for the status update - `PATCH` means "apply this partial
change," which matches "set the status field" better than `PUT`'s "replace this resource
entirely."

## Part 3: Versioning

Disagree with the spec's reasoning. "No breaking change has happened yet" describes luck, not a
plan - the day a breaking change *is* needed, every existing client breaks simultaneously with no
migration path, because there was never a mechanism for two versions to coexist.

**Recommendation**: adopt URI versioning (`/v1/orders`) now, even with only one version in
existence. The cost today is minimal - every path gains a `/v1` prefix - and it means the first
real breaking change can ship as `/v2/orders` alongside the still-working `/v1/orders`, giving
clients time to migrate instead of breaking overnight.

## Part 4: The Hardest Call

**`GET /updateOrderStatus` is the most dangerous issue.** Anything that treats `GET` as safe by
convention - a browser prefetching links, a monitoring tool polling endpoints, a CDN caching
responses - could silently trigger a real order status change with no user action at all. The
other issues (verbs in URLs, inconsistent status codes) make the API unpleasant and confusing to
use correctly; this one makes it possible to corrupt real data *by accident*, through
infrastructure that has no idea it's doing anything risky.
