# Demo: Module 05 — GitHub Copilot as a Learning Aid

**Duration:** 10 minutes
**Prerequisite:** IntelliJ IDEA 2025.1 with GitHub Copilot installed and signed in (from Module
02 environment setup). Have `unfamiliar-jenkinsfile-snippet.txt` and
`unfamiliar-dockerfile-snippet.txt` open in the editor.

> **Scope reminder for delegates:** today Copilot is a *learning aid* only — asking it to
> explain things. You are not using it to write or complete code this week. Hands-on
> Copilot-assisted coding is covered in a later sprint.

## Part 1: Opening Copilot Chat (2 min)

```text
Open the Copilot Chat panel in IntelliJ (View > Tool Windows > GitHub Copilot Chat,
or the Copilot icon in the toolbar)
```

Narration: this is the same chat surface they'll use throughout the programme. Today the only
mode in scope is asking questions — no inline completions, no agent mode, no "write this for
me."

## Part 2: Asking Copilot to explain unfamiliar syntax (4 min)

With `unfamiliar-jenkinsfile-snippet.txt` open, select the whole file and ask:

```text
Explain what each stage in this Jenkinsfile does, in plain English.
```

Narration: read the response aloud. Point out specific claims it makes, e.g. what
`archiveArtifacts fingerprint: true` does, and note that we will *verify* rather than blindly
trust each claim.

Repeat with `unfamiliar-dockerfile-snippet.txt`:

```text
Explain what each line of this Dockerfile does and why the base image choice matters.
```

## Part 3: Critiquing the explanation for accuracy (3 min)

Ask the class: does the explanation actually match what we already know from Module 03/04
about permissions, processes, and environment variables? Cross-check one specific claim (for
example, what `fingerprint: true` really does) against the official Jenkins documentation
sidebar or a quick web search, and confirm or correct it out loud.

Narration: this is the core skill for today — GenAI output is a fast first draft of
understanding, not a verified answer. You still own checking it, especially before it informs
a decision or gets repeated to a teammate.

## Part 4: What this is not (1 min)

Show that we are **not** doing this:

```text
Write a Jenkinsfile for a Java Maven project     <- code generation, out of scope this week
Complete this Dockerfile for me                  <- code generation, out of scope this week
```

Narration: same tool, different use. Learning-aid prompts ask it to explain something that
already exists; code-generation prompts ask it to create something new. The second category
starts in a later sprint, with its own module on responsible use.

## Key message

Used well, Copilot Chat turns unfamiliar syntax into a fast first-pass explanation — but every
explanation gets checked, not trusted blindly, and this week that is the *only* way you're
allowed to use it.
