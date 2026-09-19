# Module 12 Lab — Example README Section (Instructor Reference)

A realistic example of what a completed team README should contain, for checking teams' work
against the acceptance criteria.

```markdown
# Sprint Squad Sprint 1 Project

Placeholder repository for our LEAP programme project. Real project work begins properly in a
later sprint; this repo exists so we can practise our Git and CI/CD workflow from Sprint 1
onward.

## Branching Strategy

We're using **trunk-based development**: short-lived feature branches (no more than a day or
two), merged back into `main` after a quick review by another team member. We chose this over
a Gitflow-style setup because we're a 6-person team with no scheduled release cadence yet, and
the extra branches Gitflow would add (develop, release, hotfix) aren't justified until we're
actually shipping something on a schedule. We'll revisit this if it stops working for us.

## Team

- Priya Shah
- Daniel Osei
- Wei Zhang
- Fatima Al-Rashid
- Tom Bergin
- Aisha Bello
```

## Checklist for reviewing a team's repository

- [ ] Repository exists and every team member has push access (confirmed by more than one
      person's commits appearing in the history)
- [ ] `README.md` exists at the repository root
- [ ] `## Branching Strategy` section names a specific strategy (not just "we'll figure it
      out")
- [ ] The strategy has a stated reason connected to team size or release cadence, not just
      copied from the slides
- [ ] Every team member's local clone is in sync with the pushed README (spot-check with
      `git log --oneline` on more than one machine if time allows)
