# Module 14 Lab — Instructor Notes

No solution in the usual sense, this is a checklist. Notes on what good looks like and common
gaps.

## What good looks like

- **Agile & Ceremonies**: delegates who can point to a *real* sprint goal and *real* retro
  notes from their own team, not a recited definition, have actually internalised the
  ceremonies rather than memorised the vocabulary.
- **Git & Review**: a real reviewer comment on a real PR is non-negotiable, if a team only has
  approvals with no comments, that's a Module 04 gap worth flagging directly.
- **DevOps/CI/CD/IaC**: the Multibranch Pipeline job actually having built a PR automatically is
  the single best signal here, a job that exists but has only ever been manually triggered
  hasn't actually closed Module 08's loop.
- **Security**: five OWASP categories from memory, unprompted, is a reasonable bar, if a
  delegate can only produce them by reading the summary slide, that's a gap.
- **SRE**: the error budget calculation should be fast and confident by now, hesitation here
  usually means Module 12 needs a quick one-on-one refresher, not necessarily a whole re-teach.
- **Mission Day**: teams should be able to reproduce their OWASP category naming without
  looking anything up, this is the most recent and most integrated exercise, gaps here are
  worth taking seriously.

## Common gaps and quick fixes

| Gap | Likely cause | Quick fix |
|---|---|---|
| No real reviewer comments on PRs | Module 04 rushed, or pairs approved without engaging | Have them do one real review, live, before Friday |
| Multibranch Pipeline never auto-triggered | Webhook never actually configured in Module 08 | Check the webhook delivery log in GitHub settings together |
| Can't spell out SLI/SLO/SLA | Terms memorised as letters, not meaning | Walk through the Module 12 diagram again, out loud |
| Vague or missing OWASP categories | Passive exposure (reading slides) rather than active recall | Redo a couple of Module 09's vulnerable-examples cold, unprompted |
| Mission Day fixes not properly committed via PR | Time pressure led to a direct push shortcut | Acceptable if flagged honestly; use it as a live example of a real trade-off under pressure |

## Running the session

Fifteen to twenty minutes: five for the checklist walkthrough as a pair, the rest for closing
gaps. Circulate rather than lecture, this module works best as one-on-one triage, same as
Sprint 1's equivalent.
