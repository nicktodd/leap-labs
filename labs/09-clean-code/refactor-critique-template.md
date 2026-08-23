# Refactor Critique — GitHub Copilot Chat

Fill this in after Part 2 of the lab (see `README.md`). The point of this document isn't the
refactor itself — you already did that by hand in Part 1. It's the habit of reading a GenAI
suggestion critically instead of accepting it because it compiles and looks confident.

## What you asked

Paste the prompt you gave Copilot Chat (e.g., "refactor this class for readability" or
"suggest improvements to this method"):

```
<your prompt here>
```

## What it suggested

Paste (or summarise, if long) what Copilot proposed:

```
<copilot's suggestion here>
```

## Your assessment

For **each** distinct change Copilot made or suggested, decide: keep it, reject it, or change
it — and say why, against the checklist.

| Change suggested | Keep / Reject / Modify | Why |
|---|---|---|
| | | |
| | | |
| | | |

## Did it break anything?

Run `mvn test` against Copilot's version (on a throwaway branch or copy, don't overwrite your
own working refactor). Did `OrderCategoriserTest` still pass?

## The one thing worth remembering

In one or two sentences: what's a plausible-looking suggestion Copilot could make (or did make)
that would look like an improvement but actually wasn't one — and how would you catch it if you
weren't looking carefully?
