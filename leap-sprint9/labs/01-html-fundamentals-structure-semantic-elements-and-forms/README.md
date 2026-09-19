# Lab 1 — HTML Fundamentals: Structure, Semantic Elements & Forms

## Setup

No build tools, no npm, nothing to install. Edit `index.html` in any plain-text editor
(VS Code is fine — never a word processor like Word, which saves formatting you don't
want). Open the file directly in a browser (double-click it, or drag it into a browser
window) to check your work as you go — no server needed, the `.html` file is the
finished thing.

## Task

Complete the three TODOs in `index.html`, building the mission's login page:

1. **TODO 1** — a `<header>` containing an `<h1>` reading "Mission Control".
2. **TODO 2** — the login form itself, inside `<main>`: an `<h2>Log In</h2>`, a
   username field and a password field (each a `<label for="...">` correctly matched
   to its `<input>`'s `id`), and a submit `<button>`. The username input needs
   `required` and `minlength="3"`; the password input needs `required` and
   `minlength="8"`.
3. **TODO 3** — a `<footer>` containing a `<p>` reading "LEAP Mission
   Control".

Run this now, before changing anything: open `index.html` in a browser. It's blank —
every line of real content is inside HTML comments. That's the starting point.

## Verify

Once all three TODOs are done, open `index.html` in a browser and:

1. **Submit the form empty.** The browser should show its own native validation
   message on the username field (something like "Please fill in this field.") — you
   didn't write this message, the `required` attribute produced it.
2. **Type 1-2 characters into username and submit.** You should get a length-specific
   message (something like "Please lengthen this text to 3 characters or more") — this
   is `minlength` at work, still zero JavaScript.
3. **Click the "Username" label text itself.** Focus should jump into the input. If it
   doesn't, your `<label for="...">` doesn't match the input's `id`.

## A Question Worth Sitting With

`bad-example.html` from today's demo used `<div contenteditable="true">` in place of a
real `<input>`. Visually, once styled, that can be made to look identical to a real
text input. What does a real `<input>` give you for free that `contenteditable` never
will, no matter how much CSS and JavaScript you add on top?
