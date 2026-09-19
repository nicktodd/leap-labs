# Lab 13 — Reactive Forms: Building, Submitting & Handling Responses

## Setup

Your own `mission-ui` from Module 12, with the generated `OrderControllerService` and
`MissionApi` working. Same running backends as Module 11/12.

## Task

### Part 1: Build the reactive form

1. Import `ReactiveFormsModule` into `PlaceOrder`'s `imports` array.
2. Build a `FormGroup` with `FormBuilder` matching `OrderRequestDto`'s shape: `ticker`,
   `instrumentType`, `quantity`, `price`, `side`. Add `Validators.required` to every field,
   and `Validators.min(0.01)` to `quantity` and `price`.
3. Bind the template with `[formGroup]`/`formControlName`, and show a per-field error message
   when a control is `invalid && touched`.
4. On `(ngSubmit)`: if the form is invalid, call `markAllAsTouched()` and return; otherwise
   read `getRawValue()` and call `missionApi.submitOrder(...)`.

### Part 2: Surface the real server message

5. In `mission-api.ts`'s `catchError`, change the error handling to read `error.error?.message`
   (the real response body from Sprint 6's `GlobalExceptionHandler`) before falling back to
   `error.message`.

## Verify

1. **Client-side validation**: clear the quantity field, click elsewhere, confirm a
   `field-error` message appears without submitting anything.
2. **A real success**: fill in a valid `BUY` order and submit. Confirm the real `ACCEPTED`
   response with a fee and new holding quantity.
3. **A real business-rule rejection you trigger yourself**: submit a `SELL` order for far
   more shares than your test account actually holds (check your holdings first). Confirm the
   real message — something like `cannot sell more than the current holding` — not a generic
   `422` status line. If you still see a generic message, you haven't finished Part 2.
4. Query Postgres before and after your successful order, the same way Module 11/12 did —
   confirm the rejected `SELL` order changed **nothing** in the database.

## A Question Worth Sitting With

`Validators.min(0.01)` on `quantity` and a server-side check of `quantity <= 0` in
`OrderValidator` look almost identical. Given that, is the server-side check now redundant —
could it safely be deleted since the client "already" validates this? Argue for or against,
specifically referencing what Module 4's `novalidate` discussion already established about
client-side-only validation.

A second question: today's fix read `error.error?.message` with an optional chain (`?.`),
not `error.error.message`. What real situation would make `error.error` itself `undefined` or
not have a `.message` property, and what would the UI show in that case with the code as
written?
