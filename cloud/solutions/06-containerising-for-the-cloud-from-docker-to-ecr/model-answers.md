# Lab 6 Model Answers

## Verified Output

Run for real, against two repositories created and populated during preparation (account ID and
exact image digests are illustrative - yours will differ):

- Two real Docker builds, using the Spring and Node weeks' existing Dockerfiles unchanged.
- `docker push` for both tags of both images: real per-layer `Pushed` confirmations, with the
  second tag's push reusing every layer from the first (`Layer already exists`).
- `aws ecr describe-images`: three image entries for `leap-mission-service`, only one carrying
  tags (`["latest", "<git-sha>"]`); the other two `null`.
- After deleting the local image and pulling fresh from ECR: a real container startup log,
  `Started MissionServiceApplication in 0.911 seconds`, from an image that existed nowhere but
  ECR moments before.

## Part 1: The Untagged Image Count

The mismatch between the number of image entries and the number of tagged ones is not an error
- it's a real side effect of how modern Docker builds work. Since Docker 23, `docker build` uses
BuildKit's `buildx` builder by default, which produces an image *index* containing build
attestations (provenance and SBOM metadata) as separate manifests alongside the actual runnable
image. ECR lists every manifest in that index as its own entry; only the top-level manifest
receives the tag that was actually pushed. The untagged entries are legitimate, real parts of
the build - not corruption, not a mistake - but also not anything ECS or a human will ever pull
by reference again.

## Part 2: Why the Lifecycle Policy Matters

A single untagged manifest is a trivially small cost on its own - the concern is what happens at
scale, over time. Every `docker build` that gets pushed adds one or more of these untagged
entries; a team pushing several times a day, every working day, accumulates hundreds of
orphaned, unreferenced manifests within a few months, each one billing storage indefinitely with
no automatic cleanup and no legitimate future use. The lifecycle policy automates exactly the
kind of cleanup this week has applied manually to every other billed resource (S3 buckets,
CloudFront distributions) - the difference is that container registries accumulate this waste
continuously, as a side effect of normal, correct usage, not as a one-off leftover resource
someone forgot to delete.

## The Reflection Question

The lifecycle policy in this lab targets `tagStatus: untagged` specifically, so it would **not**
touch any of ten differently-tagged versions of `leap-mission-service` - each real, intentional
tag is left alone regardless of age. This is the correct scope: a policy that also aggressively
expired old *tagged* versions would risk deleting an image ECS still references. Module 7's task
definitions pin a specific image tag (not `latest`, deliberately, for reproducibility) - if a
lifecycle policy deleted that exact tag out from under a running or soon-to-be-deployed task
definition, the next deployment or task restart would fail to pull an image that no longer
exists, a real, avoidable outage caused by cleanup automation being scoped too broadly. Untagged
images are always safe to expire because nothing can be currently depending on a reference that
doesn't exist; tagged images require a genuine retention policy (keep the last N, or keep
anything referenced by a live task definition), not a blanket time-based rule.
