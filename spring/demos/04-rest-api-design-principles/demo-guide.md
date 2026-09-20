# Module 4 Demo Guide - REST API Design Principles

Run the app first, exercise every operation live, then walk back through what each one
demonstrates.

```bash
mvn spring-boot:run

curl http://localhost:8080/orders
curl -si -X POST http://localhost:8080/orders -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL","quantity":100,"price":150.00}'
curl http://localhost:8080/orders/1
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/orders/999
curl -s -o /dev/null -w "%{http_code}\n" -X DELETE http://localhost:8080/orders/1
curl -s -o /dev/null -w "%{http_code}\n" -X DELETE http://localhost:8080/orders/1
```

## Resources, Not Actions - the Single Biggest Rule

`@RequestMapping("/orders")` - a **noun**, plural, naming the resource. Point at what's *not*
here: no `/getOrders`, no `/createOrder`, no verb anywhere in a URL. **The HTTP method is the
verb.** `GET /orders` and `POST /orders` are two different operations on the *same* resource
path - that's the whole idea.

## Verbs Mapped to Meaning, Not Just Convention

- **GET** - read, never changes anything. Safe to call any number of times, safe to cache,
  safe to retry automatically if it fails
- **POST** - create something new. `POST /orders` twice with identical data creates two
  different orders - that's correct, not a bug, because the client is asking for a new thing
  each time
- **DELETE** - remove a resource. Run the demo's last two `curl` calls again and watch: the
  **second** `DELETE` still returns a clean `404`, not a `500` - deleting something that's
  already gone is not an error condition

## Status Codes That Actually Mean Something

Point at each response as it happens:
- `200 OK` - the GET succeeded, here's the resource
- `201 Created` - POST succeeded, a new resource now exists - **and look at the `Location`
  header**: it points straight at the new resource's own URL (`/orders/1`). A client can follow
  that header immediately without guessing the new ID from the response body
- `404 Not Found` - GET or DELETE on an id that doesn't exist
- `204 No Content` - DELETE succeeded, there's nothing meaningful to send back

**Say explicitly what's conspicuously absent today**: everything here is a "happy path plus
not-found" status code. `400 Bad Request` (malformed input) doesn't exist yet - that's Module 6's
job, once there's real request validation to fail.

## Idempotency, Named Directly

Ask the group: which of GET, POST, DELETE can you safely retry if the network drops the response
partway through? **GET**: yes, always. **DELETE**: yes - the second call just finds nothing to
delete. **POST**: **no** - retrying a POST you're not sure succeeded risks creating a duplicate
order. This is why network-flaky clients (mobile apps, retry logic in other services) need to
know which operations are safe to blindly retry and which aren't.

## Versioning: Mentioned, Not Built Today

No versioning strategy exists in this demo - there's only one version of this API so far. Name
the two common approaches anyway, briefly:
- **URI versioning**: `/v1/orders`, `/v2/orders` - visible, simple, but changes every client's URL
- **Header versioning**: `Accept: application/vnd.mission.v1+json` - keeps URLs stable, more
  complex to implement and to test

Neither is used yet in this mission service - worth a one-line note that this is a decision the
team would make explicitly once there's a second version to support, not something to build
speculatively now.

## Transition to the Lab

Learners critique a deliberately poorly-designed API (verbs in URLs, GET used to mutate state,
inconsistent status codes) and redesign it properly, applying every principle from today.
