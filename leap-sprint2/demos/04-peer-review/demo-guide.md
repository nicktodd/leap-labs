# Demo: Module 04 — Peer Review & Code Review Etiquette

**Duration:** 10 minutes
**Prerequisite:** none new, builds directly on Module 03's PR mechanics.

## Part 1: Building on Module 03 (1 min)

Narration: Module 03 gave you the mechanics of review, a comment, an approval, a change
request. This module is about doing that well: what to actually look for, and how to say it.

## Part 2: Why review at all? (2 min)

Three purposes, shown on the slide diagram:

- **Quality**: catches bugs, edge cases, and design issues before they reach main
- **Knowledge sharing**: spreads understanding of the codebase across the whole team, not just
  the author
- **Team standards**: keeps naming, structure, and conventions consistent over time

Ask the room: which of these three matters most to *them* personally? There's no wrong answer,
but most people undervalue knowledge sharing until they're the one who has to maintain code
they've never seen before.

## Part 3: A bad comment vs a good comment (3 min)

Show a small snippet on screen (any short method with an obvious issue, e.g. an unvalidated
input or a poorly named variable) and contrast two review comments:

```text
Bad:  "This is wrong."
Good: "This doesn't check for a null input before calling .length() on it, which will throw
       an NPE if the caller passes null. Could we add a null check at the top, or document
       that null isn't a valid argument here?"
```

Narration: the good comment names the specific issue, explains the consequence, and offers a
path forward, a question, not a command. That's the difference between "specific, constructive,
kind" and just being right.

## Part 4: Receiving feedback (2 min)

Narration: the flip side matters just as much. When you get a comment:

- Assume good intent, the reviewer is trying to help the code, not attack you
- If you disagree, ask a clarifying question rather than immediately defending your choice
- Actioning a comment isn't admitting failure, it's the process working as intended

## Part 5: Beyond syntax (2 min)

A review that only checks "does it compile" has missed most of the value. Walk through what
else to look for: logic (does it actually do what it claims), naming (will this make sense to
someone else in six months), security (anything that looks like an OWASP category from Module
09), and tests (is the behaviour actually verified, not just exercised).

## Key message

Code review is a conversation, not a gate to get past. The best reviews leave the author's code
better *and* leave the author feeling like a colleague helped them, not like they failed an
exam.
