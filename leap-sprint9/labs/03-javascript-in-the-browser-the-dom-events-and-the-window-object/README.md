# Lab 3 — JavaScript in the Browser: The DOM, Events & the Window Object

## Setup

No build tools, no npm. Edit `script.js` in any plain-text editor, then open `index.html` in
a browser (double-click it) to check your work. `index.html` already has
`<script src="script.js"></script>` at the end of `<body>`, and `<form id="login-form"
novalidate>` — `novalidate` turns off the browser's own popup validation from Module 1 so
your JavaScript owns the whole experience, same as today's demo.

## Task

Complete the three TODOs in `script.js`:

1. **TODO 1** — select the form, the two inputs, and the message element using
   `document.getElementById` and `document.querySelector`.
2. **TODO 2** — handle the form's `submit` event: prevent the page reload, read both input
   values, validate them (username 3+ characters, password 8+ characters), mark invalid
   inputs, and show an error or success message accordingly.
3. **TODO 3** — clear the username's invalid state as the user types, once it reaches 3+
   characters, without waiting for another submit.

Run this now, before changing anything: open `index.html`, fill in anything, and click "Log
In". Nothing happens — no listener exists yet. That's the starting point.

## Verify

Once all three TODOs are done:

1. Submit the form with a 2-character username and a 5-character password. Both inputs
   should get a red border, and a red message should appear reading "Username needs 3+
   characters, password needs 8+." — the page should **not** reload (check the URL bar
   doesn't flash).
2. Start typing in the username field until it reaches 3 characters — its red border should
   clear on its own, before you submit again.
3. Fill in a valid username (3+ characters) and password (8+ characters) and submit. A green
   message should appear reading "Welcome, `<your username>`." and the form should clear.
4. Open DevTools (F12) → Console tab. There should be no errors logged at any point in this
   flow.

## A Question Worth Sitting With

`event.preventDefault()` is called at the very top of the submit handler, before any
validation happens. What would go wrong if it were called only inside the `if (!usernameOk
|| !passwordOk)` block instead — i.e., only when the form is invalid?

A second question: today's `novalidate` attribute switched off the browser's built-in
`required`/`minlength` validation from Module 1. Given that this lab's JavaScript now
duplicates those same rules (3+ / 8+ characters) by hand, what does the JavaScript version
let you do that the browser's native validation couldn't?
