# Model Answers - DTOs & Request Validation

## Why `OrderRequestDtoTest` doesn't need a Spring context

Bean Validation annotations (`@NotBlank`, `@Positive`, etc.) are enforced by the
`jakarta.validation` specification, not by Spring itself - Spring's `@Valid` on a controller
parameter is just Spring *calling into* the same validation engine at the right point in request
handling. That means the annotations can be tested directly, with `Validation.build
DefaultValidatorFactory().getValidator()`, exactly as fast and exactly as isolated as any other
unit test this course has written. No embedded Tomcat, no HTTP request, no controller involved -
just the DTO and the validator.

## Why the id lookup lives on the controller, not the service, for now

`OrderController` holds the `orders` map directly in this lab, which is a shortcut - normally
that kind of state belongs in the repository/service layers, not the controller. It's deliberate
here: Module 7 replaces this entire in-memory map with real Postgres persistence behind
`OrderRepository`, and at that point the map disappears and `OrderService`/`OrderRepository` take
over storing and retrieving orders properly. Today's shortcut exists so `GET /orders/{id}` has
something real to return, without building persistence a module early.

## What `multipleViolationsAreAllReported` is actually checking

A request with five invalid fields produces five separate `ConstraintViolation`s, not one
combined failure. This matters for the eventual error response (Module 10): a client fixing only
the first problem they see, resubmitting, and immediately hitting a *second* validation failure
is a frustrating API to use. Bean Validation reports every violation in one pass specifically so
a well-built error response can tell a client everything wrong at once.

## The connection back to the Java week

`@NotBlank`, `@NotNull`, and `@Positive` are declarative versions of exactly the checks
`OrderValidator` (the Java week, Module 12) wrote out by hand in plain Java `if` statements. The
difference is where each kind of check belongs: Bean Validation on the DTO checks that the
*request itself is well-formed* (Module 5's `400` case); `OrderValidator`'s hand-written checks
enforce *business rules* (Module 5's `422` case - a well-formed order that's still rejected for
exceeding a risk limit). Both are validation; they're validating different things, at different
points in the flow.
