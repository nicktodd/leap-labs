# Lab 1 Model Answers

## Verified Output

Opening the completed `index.html` and reading its accessibility tree directly (the
same query a screen reader effectively makes):

```
textbox "Username" type="text"
textbox "Password" type="password"
button "Log In" type="submit"
```

Submitting empty:

```
Please fill in this field.
```

Submitting with a 2-character username:

```
Please lengthen this text to 3 characters or more (you are currently using 2 characters).
```

Both messages are the browser's own, verbatim — nothing here is custom JavaScript.

## Key Points

- **TODO 1**: `<header>`/`<h1>` over a generic `<div>` mainly matters for document
  outline and landmark navigation — screen reader users frequently jump between
  landmarks (header, main, footer) rather than reading a page top to bottom.
- **TODO 2**: the `for`/`id` pairing is the single most commonly-skipped detail in a
  first HTML form. Without it, clicking the label text does nothing, and a screen
  reader announces the input with no name at all — it becomes "edit text, blank"
  instead of "edit text, Username."
- **TODO 3**: `<footer>` here is trivial content but the same landmark principle as
  TODO 1 — it's what lets a screen reader user jump straight past boilerplate.

## The Reflection Question

A real `<input>` gets, for free, with zero JavaScript: keyboard focus and tab order
that behaves correctly by default; the browser's native validation (`required`,
`minlength`, `type="email"`, etc.); OS-level autofill and password manager
integration (`autocomplete="username"` / `"current-password"`); mobile keyboards that
adapt to the input type (a numeric keypad for `type="number"`, an `@`-friendly layout
for `type="email"`); and a correct accessibility role out of the box, with no ARIA
attributes needed.

`contenteditable="true"` gives you an editable region and nothing else. Every one of
those behaviours would need to be hand-built and hand-maintained — including,
ironically, re-implementing basic keyboard editing edge cases (selection, undo,
copy-paste) that a real `<input>` already gets from the browser's own text-editing
engine. This is the running theme of the next three modules: the platform already
does more than it gets credit for, and the cases where you genuinely need to reach
past it are much narrower than "just style a div to look right."
