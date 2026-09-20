# Sprint 6 - Project Friday Guidance

## Context

This week's teaching covers microservices, Spring Boot, layered architecture, REST API design,
contract-first design with OpenAPI, DTOs and validation, persistence with MyBatis, JWT
validation and error handling.

This week's deliverable is a REST service that exposes your Sprint 5 domain rules and your
Sprint 3 data over HTTP: something a client can call to place an order and see the result,
secured, and returning errors in a form a caller can act on.

## The trap to avoid

This is the first time your Sprint 5 domain gets called by something real. That's worth treating
as a test of last week's decisions, not just this week's build:

- Did the domain module survive being wired into a real service unmodified, or did you find
  yourself bending a rule to fit the controller, or adding a business decision at the service
  layer instead of calling into the domain? Notice it now, it gets more expensive to unpick the
  more that gets built on top of it.
- This week's contract-first lesson exists for a reason: design the shape of the API, and what an
  error looks like, before you write a controller. What's actually in your contract, and would it
  make sense to someone who's never seen your database?
- BR-09 says the fill, the cash movement and the trade record have to succeed or fail together,
  even under failure. What in your service actually enforces that? "They should be atomic" is a
  hope. What makes it true?
- The spec's own assumptions (section 10) say a representative sign-in fixture would exist so
  delivery isn't blocked waiting on a real identity solution, because building real authentication
  is later work. That's your team's decision to make, not something this guide imposes: leave the
  service open for now and pick it up as a backlog item, stand up a throwaway stub just enough to
  test the JWT validation you're taught this week, or build real authentication early if you'd
  rather do it once. All three are legitimate. What isn't is drifting into one of them without
  choosing.

## Suggested Friday session

- Design your API contract as a team before anyone writes a controller: the operations, the
  shape of a response, and what an error looks like, consistently, across every one of them.
- Trace one order end to end through your layers and check whether a business decision has
  leaked into the wrong one.
- Decide as a team whether you're leaving this service open for now, stubbing authentication, or
  building it for real, and record the decision rather than letting it happen by default.
- Walk through error handling: what does the API actually return for each failure case your
  Sprint 5 domain already defines?
- Get the service running as a container in your own environment, alongside what you've already
  built.
- Revisit the OWASP Top 10 material from Sprint 2 against this specific service, not as a
  checklist exercise, what actually applies here?
- Refine the backlog against what building the API has taught you about the schema and the
  rules underneath it.

## What to present to the class

- A walkthrough of your API contract and how the implementation satisfies it.
- Your team's decision on authentication this sprint, open, stubbed, or built for real, and why.
- One place your Sprint 3 or Sprint 5 decisions caused friction here, and how you handled it. Hint - you are allowed to change things!
- How you're enforcing BR-09 in this service.
- An updated backlog.
