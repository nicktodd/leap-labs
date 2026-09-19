# Sprint 11 — Project Friday Guidance

## Context

This week's teaching covers cloud engineering foundations, AWS account setup and IAM, networking
(VPC, subnets, security groups), S3, CloudFront, containerising for the cloud and ECR, ECS,
managed data and secrets (RDS, Secrets Manager), observability and cost awareness, and deployment
automation.

This week's deliverable is getting your Angular front end somewhere a real URL reaches it,
deployed by a command your whole team could run, not just the one person who remembers the
steps. It's also the final week of the programme, and this Friday's presentation is the full
programme showcase, not an internal update.

## What to keep in mind

- This week's S3 and CloudFront teaching covers the standard pattern for this: a private bucket,
  never addressed directly, sitting behind a CDN that's the only reader it trusts. Apply that.
  A public bucket is the faster route to something on screen, and it costs you real things:
  plain-HTTP access to your own login page, anything you upload being world-readable, and no
  way to control caching or error handling in front of it.
- Deployment should be one repeatable command, not a sequence of steps in somebody's shell
  history. Running it twice should leave things exactly as running it once did, test that
  rather than assume it.
- Whatever credential runs your deployment should be scoped to only what it needs. If those
  credentials leaked tomorrow, what's the actual blast radius, and does your setup genuinely
  limit it or just assume it does? No long-lived key belongs in your repository, ever, in any
  branch, in any file.
- Once it's deployed, test a route other than the root, not just the homepage. If it breaks,
  that's telling you something real about how a static file store differs from a server that
  understands your application's own routes, and it's worth working out what your CDN needs to
  do about it.
- Your API is still running locally, not deployed. Once your UI is served from somewhere else,
  what actually has to change for your backend to accept a request from that origin at all, and
  is "allow everything" an acceptable answer for a service holding customer positions?
- Real cloud resources cost money and keep running until somebody tells them to stop. Confirm
  with your instructor what your team is responsible for tearing down, and when, before the
  showcase, not after.

## Suggested Friday session

- Apply this week's S3/CloudFront teaching to your own build. Agree who owns the deployment
  script, and actually rehearse running it twice.
- Walk through what changes once your API is called from a different origin than it's used to,
  and decide what you're doing about it.
- Do a final pass on the risk list from every earlier sprint, anything still open needs an
  honest answer in the showcase, not a hope that nobody asks.
- Rehearse the showcase itself: walk the whole platform end to end, and know who's presenting
  which part, so nobody is caught explaining something they didn't build.
- Confirm cost and teardown responsibilities with your instructor.

## What to present: the final showcase

This week's presentation is the programme showcase to stakeholders, the same audience and
stakes as the kickoff day in Sprint 1. Cover:

- The platform end to end: architecture, the decisions that shaped it, and how it's changed
  since the candidate architecture you pitched in Sprint 1.
- A live demo, deployed, not running on someone's laptop.
- If your team built the additional capability from BR-18 in Sprint 10, what it is, why that
  one, and what you deliberately left out.
- Two or three design decisions you'd genuinely defend, and what you rejected along the way.
- Where AI tools helped you across the programme, where they didn't, and how you knew the
  difference.
- What you'd do next if this were a real six-month programme rather than an eleven-week one.
