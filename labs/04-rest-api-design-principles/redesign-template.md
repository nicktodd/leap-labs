# API Critique & Redesign — Order Management Service

## Part 1: What's Wrong (Critique)

| Endpoint(s) | Problem | Principle violated |
|---|---|---|
| `GET /getAllOrders`, `GET /getOrder?id=123`, `GET /updateOrderStatus`, `GET /orders/123/getFee` | Verbs (`getAll`, `get`, `update`, `get`) embedded in the URL path — the HTTP method should convey the action | Uniform interface / resource naming (no verbs in URLs) |
| `GET /updateOrderStatus?id=123&status=REJECTED` | Uses `GET` to mutate state (changing an order's status) — GET must be safe and side-effect free | HTTP method semantics (GET must be safe) |
| `POST /deleteOrder/123` | Uses `POST` to delete a resource; `DELETE` is the standard method for removal and is idempotent | HTTP method semantics (wrong verb for deletion) |
| `/createOrder` vs `/order` | Two endpoints that both create an order — duplicated, inconsistent resource paths and no strategy for deprecating the old one | Uniform interface / consistent resource identification |
| `/getAllOrders` vs `/getOrder` vs `/order` vs `/createOrder` | Mixed singular/plural naming (`/order` and `/orders/123/getFee`) with no consistent resource root | Uniform interface / consistent resource naming |
| All endpoints | Every response returns HTTP 200, including errors — clients cannot distinguish success from failure without parsing the body | Correct use of HTTP status codes |
| All endpoints | Error responses use `{"success":false,"error":"..."}` body shape — non-standard, client must learn a proprietary envelope | Uniform interface / leveraging HTTP semantics |
| `GET /updateOrderStatus?id=123&status=REJECTED` | Sending a state-change as a GET request means it can be triggered accidentally by link prefetchers, browser history prefetch, or monitoring tools | Safety — GET requests must not change server state |

## Part 2: The Redesign

| Method | URL | Status codes it can return | Idempotent? |
|---|---|---|---|
| `GET` | `/orders` | 200 | Yes — reading a list never changes state |
| `POST` | `/orders` | 201 (created), 400 (validation failure), 401 (unauthenticated), 422 (business rule rejected) | No — each call may create a new order; safe to retry only if the server assigns the ID and the client checks the Location header first |
| `GET` | `/orders/{id}` | 200, 401, 404 (not found) | Yes |
| `PATCH` | `/orders/{id}/status` | 200, 400 (invalid status), 401, 404, 409 (transition not allowed) | Yes — patching to the same status again produces the same result |
| `DELETE` | `/orders/{id}` | 204 (deleted), 401, 404 | Yes — deleting an already-deleted resource returns 404, but the end state is the same |
| `GET` | `/orders/{id}/fee` | 200, 401, 404 | Yes |

## Part 3: Versioning

No, "there has never been a breaking change" is not a good reason to have no versioning strategy. It means you got lucky, not that you have a plan. As soon as the first breaking change is needed — a renamed field, a removed endpoint, a changed response shape — you have no safe path: every client in production breaks simultaneously with no migration window.

I would recommend adding a URL path prefix (`/v1/`) from day one. It costs nothing upfront: you just add the prefix, and all existing clients continue to work once they update their base URL. When a breaking change is eventually needed, you introduce `/v2/` alongside `/v1/`, communicate a deprecation timeline, and remove `/v1/` only after all clients have migrated. This is easier to implement before there are external clients than after.

## Part 4: The Hardest Call

The single most damaging issue is `GET /updateOrderStatus?id=123&status=REJECTED` — a state mutation behind a safe HTTP method. In production, any HTTP-level infrastructure (CDN caches, browser prefetchers, load-balancer health checks, log-scraping crawlers) can and will issue GET requests against discovered URLs. An order status change triggered by a crawler or a cache warming request would be completely invisible in application logs (it looks like a read), non-reproducible, and potentially irreversible — a rejected order cannot automatically be un-rejected. The other issues in the spec cause bad developer experience; this one causes silent, production data corruption.
