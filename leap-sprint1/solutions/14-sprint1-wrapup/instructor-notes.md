# Module 14 Lab — Instructor Notes

This lab has no "solution" in the usual sense, it's a checklist, not an exercise with a single
right answer. These notes cover what "good" looks like for each section, and the most common
gaps to watch for.

## What good looks like

- **Environment**: no surprises expected here if Module 02 was solid; if someone still can't
  open Docker Desktop or sign in to GitHub by this point, that's a priority fix before anything
  else.
- **Linux & PowerShell**: the one-sentence pipe-difference answer is the real signal, delegates
  who can recite commands but can't explain *why* PowerShell pipes differ from bash pipes
  haven't internalised Module 04 yet.
- **GenAI**: watch for delegates who used Copilot for code generation this week rather than
  explanation, that's a scope misunderstanding from Module 05 worth correcting now, before the
  hands-on Copilot sprint later in the programme normalises the wrong habit.
- **Git & GitHub**: a real commit history and a real, resolved merge conflict are non-negotiable
  here, both were hands-on in Modules 06-07 and shouldn't need reconstructing from memory.
- **CI/CD & Jenkins**: the CI vs Delivery vs Deployment distinction is the one people blur, if
  someone can't state it cleanly, point them back to Module 09's slides rather than re-teaching
  it from scratch.
- **Docker**: "has a working Dockerfile they wrote themselves" is deliberately stricter than
  "can explain what a Dockerfile does", writing one from a blank file is a different skill.
- **Team Repo**: this section doubles as a check on Module 12/13's actual outcome, if a team's
  Jenkins job isn't green by now, that's worth flagging to the team directly, not just noting.

## Common gaps and quick fixes

| Gap | Likely cause | Quick fix |
|---|---|---|
| Can't SSH into Linux host | Credentials or network issue from Module 02/03 | Re-issue credentials, confirm VPN/network access |
| Confuses push and pull | Mixed up direction, common early on | Point back to Module 08's local-vs-remote diagram |
| Can't explain fast-forward merge | Skipped or rushed Module 07's mechanics slides | Walk through the diagram again one-on-one |
| Jenkins job never went green | Broken Jenkinsfile syntax, or Docker not running on the agent | Check Console Output together, same diagnose loop from Module 10 |
| No Dockerfile of their own | Copied a teammate's rather than writing one | Have them write one from a blank file, live, with you watching |

## Running the session

Fifteen to twenty minutes total: five for the checklist walkthrough as a pair, the rest for
closing gaps. Circulate rather than lecture, this module works best as one-on-one triage.
