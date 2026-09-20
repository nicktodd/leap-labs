# Module 6 Demo Guide - Containerising for the Cloud: From Docker to ECR

**Duration:** 45 minutes
**Prerequisite:** Docker installed and running. Local checkouts of the Spring week's mission service
and the Node week's auth service, each with a working multi-stage `Dockerfile` already written.

## Part 0: Recapping Containerisation, Framed for a Cloud Target (8 min)

The Spring and Node weeks already wrote real multi-stage Dockerfiles - a build stage with the full compiler
toolchain, a run stage with only the JRE (or, for the auth service, only Node and the compiled
JS) and the built artefact. The reasoning was smaller images and a smaller attack surface; that
reasoning doesn't change moving to AWS. What changes is *where the image lives once built*.

Right now, `docker build` produces an image that exists only on one laptop's local Docker
engine. ECS (Module 7 onward) needs to pull that image from somewhere every AWS account can
reach - a registry. ECR (Elastic Container Registry) is AWS's own registry, and today's job is
getting a real image from local Docker into it.

## Part 0b: What a Registry Actually Is, and How push/pull Work (8 min)

Before touching ECR specifically, establish the general pattern. A container registry stores
images the same way a package registry (npm, Maven Central) stores packages - versioned, named
artefacts, addressable by anyone with the right access. A *repository* is one image's home
inside a registry: `leap-mission-service` is a repository; `latest` and a git SHA are two tags
within that one repository, not two separate repositories. Docker Hub is the best-known public
registry; ECR is AWS's own, private by default, living inside one specific account and region.

Exactly two commands cover the entire interaction with any registry:

```bash
docker push <registry>/<repository>:<tag>
docker pull <registry>/<repository>:<tag>
```

An image is stored as a set of content-addressed layers, not one opaque blob - `push` uploads
only the layers the registry doesn't already have, then records the tag against them; `pull`
downloads only the layers the local machine doesn't already have, then assembles the image from
them locally. This is the same behaviour already seen once this module: pushing a second tag of
an identical image reused every layer from the first push.

Authentication is the one thing that genuinely differs between registries. The traditional
pattern, e.g. Docker Hub:

```bash
docker login docker.io
# Username: alex-morgan
# Password: ********
```

A real username and a real, long-lived password, typed once and cached locally until it's
changed or revoked by hand. It works, but the password itself is the credential - if it leaks,
it stays valid until someone notices and rotates it.

ECR does the same `docker login` under the hood, but the "password" is never typed or stored
anywhere:

```bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
```

`get-login-password` calls ECR's `GetAuthorizationToken` API using whatever IAM identity is
already active - the same identity Module 2's `aws sts get-caller-identity` confirmed, not a
separate registry account. The token it returns is valid for 12 hours and worthless afterward,
piped straight into `docker login` as the password, with the username fixed as the literal
string `AWS`. Nobody types a password, nobody stores one long-term - only someone who already
holds valid IAM credentials can ever request a token in the first place.

## Part 1: Building the Real Images (7 min)

Nothing new here - the exact Dockerfiles from the Spring and Node weeks:

```bash
cd mission-service && docker build -t leap-mission-service:latest .
cd auth-service && docker build -t leap-auth-service:latest .
```

Real output - two working multi-stage builds, not placeholders:

```
naming to docker.io/library/leap-mission-service:latest done
naming to docker.io/library/leap-auth-service:latest done
```

## Part 2: Creating ECR Repositories and Pushing (10 min)

```bash
aws ecr create-repository --repository-name leap-mission-service
aws ecr create-repository --repository-name leap-auth-service
```

Each repository gets a real, unique URI:
`<account-id>.dkr.ecr.us-east-1.amazonaws.com/leap-mission-service`.

Docker needs to authenticate to ECR before it can push - a short-lived token, not a long-lived
password:

```bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
```

Tag and push, with two tags per image - `latest`, and a real git commit SHA for the source that
produced it:

```bash
docker tag leap-mission-service:latest <account-id>.dkr.ecr.../leap-mission-service:latest
docker tag leap-mission-service:latest <account-id>.dkr.ecr.../leap-mission-service:<git-sha>
docker push <account-id>.dkr.ecr.../leap-mission-service:latest
docker push <account-id>.dkr.ecr.../leap-mission-service:<git-sha>
```

Real output worth pointing out: pushing the second tag reuses layers already uploaded for the
first (`Layer already exists`) - ECR, like Docker Hub, stores layers content-addressably, so two
tags of the identical image cost no extra upload or storage.

## Part 3: A Real Surprise - Untagged Images Appear on Their Own (10 min)

Check what actually landed in the repository:

```bash
aws ecr describe-images --repository-name leap-mission-service \
  --query 'imageDetails[].imageTags'
```

Real output - three image entries, only one carrying both tags:

```
[null, null, ["latest", "<git-sha>"]]
```

Modern `docker build` (buildx, the default builder since Docker 23) produces an image *index*
with build attestations (provenance and SBOM metadata) as separate manifests alongside the
actual image - ECR lists each manifest in the index, and only the top-level one carries the tag
that was pushed. The two `null`-tagged entries are real, legitimate parts of the build; they're
also, left alone, images nobody will ever reference again, quietly billing for storage forever.

## Part 4: The Fix - A Lifecycle Policy (10 min)

```bash
aws ecr put-lifecycle-policy --repository-name leap-mission-service \
  --lifecycle-policy-text file://expire-untagged.json
```

```json
{
  "rules": [{
    "rulePriority": 1,
    "description": "Expire untagged images after 1 day",
    "selection": {"tagStatus": "untagged", "countType": "sinceImagePushed",
                   "countUnit": "days", "countNumber": 1},
    "action": {"type": "expire"}
  }]
}
```

This is a real, verified pattern worth naming as a preview of Module 10: cloud resources don't
clean themselves up, and a registry that accumulates untagged layers from every build,
indefinitely, is a genuine, avoidable cost - the same discipline this week has applied to
every other billed resource, just automated instead of manual.

## Part 5: Verified - A Pulled Image Actually Runs (5 min)

Prove the pushed image isn't corrupted or incomplete - delete the local copy, pull it back down
fresh, and run it:

```bash
docker rmi <account-id>.dkr.ecr.../leap-mission-service:latest
docker pull <account-id>.dkr.ecr.../leap-mission-service:latest
docker run -d -p 18090:8080 <account-id>.dkr.ecr.../leap-mission-service:latest
```

Real, verified startup log - a genuine Spring Boot application, pulled entirely from ECR:

```
Started MissionServiceApplication in 0.911 seconds (process running for 1.092)
```

## Key Message

An ECR repository is a real, versioned home for a container image - the exact image that ran
locally is provably the same one ECS pulls later this week, verified by pulling it back down
and running it, not assumed from a successful `docker push`.

## Transition to the Lab

Candidates build and push their own mission-service and auth-service images, apply the same
lifecycle policy to their own repositories, and verify by pulling one image back down fresh and
running it locally.
