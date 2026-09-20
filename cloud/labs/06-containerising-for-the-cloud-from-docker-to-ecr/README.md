# Lab 6 - Containerising for the Cloud: From Docker to ECR

## Setup

Access to your Linux Docker host - connect in your preferred way - with
the AWS CLI configured. Checkouts of the mission service (the Spring week) and the auth service (the Node
week) cloned or copied onto that host, each already containing a working `Dockerfile`.

## Task

### Part 1: Build and push both images

1. Build both images locally with `docker build`, using the existing Dockerfiles unchanged.
2. Create two ECR repositories, one per service.
3. Authenticate Docker to ECR with `aws ecr get-login-password`.
4. Tag and push each image with two tags: `latest`, and a real identifier for the exact source
   that produced it (a git commit SHA is a good choice - `git rev-parse --short HEAD`).
5. Run `aws ecr describe-images` on one of your repositories. How many image entries do you see,
   and how many of them actually carry a tag? If the numbers don't match, don't assume it's an
   error - investigate what `docker build` actually produced before concluding something's
   wrong.

### Part 2: Fix the untagged-image accumulation

6. Write and apply an ECR lifecycle policy that expires untagged images after a short window
   (a day is reasonable for this lab).
7. In your own words: why does this matter for cost, given that a single untagged manifest from
   one build is a tiny amount of storage? What happens after months of regular pushes without
   this policy?

### Part 3: Verify the pushed image is real and correct

8. Delete your local copy of one image (`docker rmi`), pull it back down from ECR, and run it.
9. Confirm from the container's logs that it actually started successfully - not just that
   `docker run` returned without an error.

## Verify

Compare your Part 1 and Part 2 answers against `solutions/06-.../model-answers.md`. Part 3 is
verified by your own container's real startup logs - if the pulled image doesn't start, compare
its digest against what `docker push` reported to confirm you pulled the image you think you
did.

## Cleanup

Leave your two ECR repositories and their images in place - Module 7 onward pulls directly from
them to build ECS task definitions. Unlike a running container or an EC2 instance, an ECR
repository holding a couple of small images costs a genuinely trivial amount to leave in place,
and rebuilding identical images from scratch next module would be wasted effort for no real
savings.

## A Question Worth Sitting With

The lifecycle policy in this lab targets untagged images specifically, not old tagged ones. If
you pushed ten different versions of `leap-mission-service`, all tagged with different git SHAs,
would this lifecycle policy delete any of them? Should it? What real problem would a policy that
*also* aggressively deleted old tagged versions risk causing for Module 7's ECS work later this
week?
