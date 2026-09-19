# Lab 2 — CSS Fundamentals: Selectors, the Box Model & Layout

## Setup

No build tools, no npm. Edit `styles.css` in any plain-text editor, then open
`index.html` in a browser (double-click it) to check your work. `index.html` already
has `<link rel="stylesheet" href="styles.css" />` in its `<head>` — that's the entire
connection, given, nothing to change there.

## Task

Complete the five TODOs in `styles.css`:

1. **TODO 1** — a `box-sizing: border-box` reset on `*`, first in the file.
2. **TODO 2** — Flexbox layout on `body` (column, full height) and `main` (centring
   its content both ways).
3. **TODO 3** — box model spacing and a Flexbox column on `form` itself, so its
   children space out evenly with no individual margins.
4. **TODO 4** — pick your own accent colour (named, hex, or `rgb()`) for the button
   and header backgrounds, keeping the white text readable against it.
5. **TODO 5** — one `@media (max-width: 480px)` breakpoint that drops the form's
   border, radius, and max-width on narrow screens.

Run this now, before changing anything: open `index.html` in a browser. The form sits
top-left, unstyled and un-centred — every rule not yet written is missing. That's the
starting point.

## Verify

Once all five TODOs are done, open `index.html` and resize the browser window (or use
your browser's device toolbar) across roughly 900px and 375px wide:

1. **At ~900px**: the form should float as a bordered, rounded card, centred both
   horizontally and vertically between the header and footer, in your chosen colour.
2. **At ~480px or narrower**: the form should lose its border and rounded corners and
   go edge-to-edge — that's TODO 5's `@media` block taking over.
3. **Check the box model directly**: right-click the form → Inspect (Module 1's own
   technique) → look at the "Box Model" panel your browser's DevTools shows. `width`
   should read close to 360px total, not 360px-plus-padding — that's `border-box` at
   work.
4. **Check your colour choice is readable**: white text on a very light or very
   saturated background can fail readability fast — if your button text is hard to
   read at a glance, pick a darker (or differently saturated) shade.

## A Question Worth Sitting With

`.field` (a class selector) sets `display: flex` on both the username and password
wrapper divs. If you also added a rule targeting `#username` that set
`display: block`, which one would actually apply, and why — tie your answer to what
today's demo showed with `specificity-demo.html`.

A second question, this time about organisation rather than mechanics: `styles.css`
never styles by `#login-form`, even though that id exists in the HTML. Given what
today's demo said about ids and specificity, why might that be a deliberate choice
rather than an oversight?
