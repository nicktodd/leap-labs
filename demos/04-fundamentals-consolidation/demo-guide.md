# Demo: Module 4 — Python Fundamentals Consolidation Lab

**Duration:** 10 minutes
**Files:** `unfamiliar_snippet.py`
**Prerequisite:** GitHub Copilot Chat available.

This module is deliberately light on new material and slides — Modules 1-3 already gave you
everything you need. The demo just sets up two things: reading code you didn't write, and using
GenAI responsibly while you build. Most of the time today goes to the lab itself, an extended
exercise: a small command-line compliance-checking tool.

## Part 1: Reading unfamiliar code (4 min)

Put `unfamiliar_snippet.py` on screen without narrating it first. Give the room 90 seconds to
read it silently, then ask: "what does this function actually do, and what would it return for
a specific set of inputs?" before revealing the answer.

Narration: reading code you didn't write, and correctly predicting its behaviour before running
it, is a skill separate from writing code, and one you'll use constantly on a real team, most of
the code you touch professionally, someone else wrote first.

## Part 2: Using GenAI responsibly on your own code (6 min)

Recap the pattern from Sprint 2 and Sprint 3: GitHub Copilot Chat is a learning aid, not a
substitute for understanding your own code, and every suggestion gets read and critiqued before
it's accepted, never pasted in blind.

For today's lab specifically, good uses of Copilot Chat include:

- *"Explain what this traceback means"* when you hit an error you don't recognise
- *"What's a cleaner way to write this nested if/elif chain?"* — then decide for yourself whether
  the suggestion is actually clearer, or just different (the same judgement call from Sprint 3
  Module 5)
- *"What edge cases might this function miss?"* as a check on your own thinking before your
  partner reviews it

Not-good uses: asking Copilot to write the whole tool for you, then submitting code you can't
explain. The acceptance criteria for this lab explicitly requires you to be able to walk a
partner through every function you wrote — code you can't explain doesn't meet that bar,
regardless of whether it runs.

## Key message

You already have every Python concept this lab needs, from Modules 1-3. Today is about applying
them together, at a slightly larger scale than any single earlier lab, and being able to explain
what you built, not just get it running.
