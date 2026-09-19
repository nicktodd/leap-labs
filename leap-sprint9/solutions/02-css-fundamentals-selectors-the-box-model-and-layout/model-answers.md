# Lab 2 Model Answers

## Verified Output

The completed page, screenshotted at two real viewport widths:

- **900px wide**: a centred, bordered, rounded-corner card floating in the middle of
  the page, exactly matching today's demo.
- **375px wide** (below the 480px breakpoint): the same card, edge-to-edge, no border,
  no rounded corners — confirming the `@media` block fired.

## Key Points

- **TODO 1**: `* { box-sizing: border-box; }` has to come *before* anything else
  matters, because every `padding`/`border` value in the rest of the file assumes it's
  already in effect. Without it, `form { max-width: 360px; padding: 32px; }` would
  actually render at 424px (360 + 32px padding × 2 sides), not 360px.
- **TODO 2**: `body { display: flex; flex-direction: column; min-height: 100vh; }`
  makes `body` tall enough to fill the viewport even when there's barely any content;
  `main { flex: 1; ... }` then lets `main` claim all the *leftover* space between the
  fixed-height header and footer, which is what `justify-content`/`align-items` centre
  the form inside of.
- **TODO 3**: `gap: 16px` on a flex column is what spaces the `h2`, both `.field`
  divs, and the button evenly — no `margin-bottom` needed on any of them
  individually, and no risk of a doubled gap if two adjacent elements each had their
  own margin.
- **TODO 4**: any named colour, hex value, or `rgb()` triple works — the solution here
  keeps `#1e6fa8` (the same blue as the demo), but the point is that swapping it is a
  one-line change in exactly two places (`header` and `button`), because both already
  read from real properties rather than something hardcoded per-element.
- **TODO 5**: the breakpoint only touches `main`'s padding and `form`'s
  border/radius/max-width — everything else (colours, fonts, the flex layout inside
  the form) stays exactly as it was, because it doesn't need to change.

## The Reflection Questions

**Specificity**: `#username` wins. An id selector is more specific than a class
selector, regardless of which rule appears later in the file or which one "sounds"
more specific in English — specificity is a strict hierarchy (inline > id > class >
element), not a matter of rule order. `display: block` would apply to `#username`
specifically, and `display: flex` from `.field` would still apply to `#password` (the
other field in the same class), since `#username` only targets one specific element.
This is exactly what `specificity-demo.html` showed with border colour: same conflict,
same resolution rule, different property.

**Why `styles.css` never styles by `#login-form`**: deliberately, not by oversight. An
id selector carries specificity high enough that almost nothing else can override it
without reaching for `!important` — fine for a one-off style that will never need
adjusting, risky for anything that might. Reserving the id for JavaScript to grab
(Module 3's `document.getElementById("login-form")` or similar) keeps two separate
concerns — "how do I find this element in code" and "how is this element styled" —
from fighting over the same attribute. If a future change needs a second login form
on the same page, a second id would be a hard collision; a second element with the
same *class* is exactly what classes are for.
