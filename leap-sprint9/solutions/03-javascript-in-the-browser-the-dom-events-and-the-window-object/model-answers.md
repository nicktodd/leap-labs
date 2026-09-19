# Lab 3 Model Answers

## Verified Output

Ran headlessly with Playwright end to end:

- Submitting with `ab` / `short` produced the message `Username needs 3+ characters,
  password needs 8+.` and `#username` gained the class `invalid`.
- Fixing both fields and resubmitting produced `Welcome, nicktodd. (No real request sent
  yet - Module 4 adds fetch().)`, and `#username`'s value was empty afterwards — confirming
  `form.reset()` ran and the page never navigated (no error running headlessly, which fails
  fast on an actual page load).

## Key Points

- **TODO 1**: `document.getElementById("login-form")` vs `document.querySelector("#username")`
  — both work for an id, but `querySelector` accepts *any* CSS selector, so it's the one
  worth defaulting to once a class, attribute, or descendant selector is needed instead of
  a bare id.
- **TODO 2**: `event.preventDefault()` has to run *unconditionally*, first — see the
  reflection question below. Reading `.value` off both inputs, then computing
  `usernameOk`/`passwordOk` as plain booleans before touching the DOM at all keeps the
  validation logic testable in principle, separate from the DOM updates that follow.
  `markInvalid()` runs on *both* inputs every submit, not just the failing one — otherwise
  a previously-invalid field that's now fixed would keep its red border forever.
- **TODO 3**: the `"input"` event fires on every keystroke (unlike `"change"`, which waits
  for the field to lose focus) — exactly what's needed for the invalid state to clear the
  moment the 3rd character is typed, not a keystroke later.

## The Reflection Questions

**Why `preventDefault()` unconditionally, not just on failure**: if it only ran inside the
invalid branch, a *valid* submission would fall through to the browser's default behaviour —
a full page navigation/reload — right as the success message was about to render. The
message would flash and vanish, and `form.reset()` would run on a page that's already
being torn down. `preventDefault()` has to run first, before any branching, because "stay on
this page and let JavaScript handle it" is true for every submission, not just the invalid
ones.

**What the JavaScript version can do that native `required`/`minlength` couldn't**: the
native version can only show one message at a time, styled entirely by the browser (Module
3's own earlier screenshot showed the native bubble covering the password field). The
JavaScript version can show both fields' problems in one message, style that message to match
the rest of the page exactly, and — critically — combine with server-side responses the same
way from Module 4 onward: a `fetch()` failure can reuse `showMessage(..., "error")` unchanged,
where a native validation bubble has no equivalent for "the server rejected this."
