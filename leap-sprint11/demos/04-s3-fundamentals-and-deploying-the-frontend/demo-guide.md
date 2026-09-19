# Module 4 Demo Guide — S3 Fundamentals & Deploying the Frontend

**Duration:** 50 minutes
**Prerequisite:** Module 3's VPC work (not directly used here — S3 is a global-ish service, not
VPC-scoped). A working `ng build` of `mission-ui` from Sprint 9.

## Part 0: What S3 Actually Is (8 min)

S3 (Simple Storage Service) is an object store, not a filesystem and not a database — it stores
arbitrary blobs of data (an HTML file, a JPEG, a JSON document, a multi-gigabyte backup) as
"objects," each identified by a key (its path-like name) inside a "bucket" (a flat, top-level
container). There is no real directory structure underneath — `holdings/summary.json` and
`orders/2024.json` are two unrelated object keys that merely *look* hierarchical; S3's console
renders the `/` characters as folders for convenience, but there's no actual nested filesystem.

Every bucket name must be globally unique across every AWS account on the planet, not just this
account — a real, sometimes-surprising constraint the first time someone tries `my-bucket` and
finds it already taken by a stranger.

## Part 1: Storage Classes and Pricing, at a High Level (7 min)

S3 offers several storage classes trading cost against retrieval speed and frequency — Standard
(the default, for frequently-accessed data), Infrequent Access (cheaper storage, a retrieval fee,
for data touched occasionally), Glacier (cheapest storage, slow retrieval, for archives). This
sprint uses Standard exclusively — `mission-ui`'s static build is accessed constantly by anyone
visiting the site, the exact profile Standard is priced for.

Pricing has three components worth naming explicitly, since all three show up on a real bill:
storage (per GB per month), requests (per thousand GET/PUT/LIST calls), and data transfer out to
the internet (typically the largest line item for a busy site — transfer *into* S3 is free).

## Part 2: A Real Default Nobody Expects on the First Try (10 min)

Create a bucket and try to make it public the "obvious" way:

```bash
aws s3api create-bucket --bucket <bucket-name> --region us-east-1
aws s3api put-bucket-website --bucket <bucket-name> --website-configuration \
  '{"IndexDocument": {"Suffix": "index.html"}, "ErrorDocument": {"Key": "index.html"}}'
aws s3api put-bucket-policy --bucket <bucket-name> --policy file://public-read-policy.json
```

Real, verified output — a first-try failure, not a hypothetical:

```
An error occurred (AccessDenied) when calling the PutBucketPolicy operation: User:
.../alex.morgan is not authorized to perform: s3:PutBucketPolicy on resource:
"arn:aws:s3:::<bucket-name>" because public policies are prevented by the BlockPublicPolicy
setting in S3 Block Public Access.
```

Every new bucket, in every AWS account, has all four Block Public Access settings enabled by
default — this is a deliberate AWS platform decision (made permanent account-wide default in
2023) specifically because accidentally-public S3 buckets containing sensitive data
were, for years, one of the most common real-world cloud security incidents. The error is the
platform doing its job, not a bug to work around casually.

Confirm this directly before proceeding:

```bash
aws s3api get-public-access-block --bucket <bucket-name>
```

```json
{
  "PublicAccessBlockConfiguration": {
    "BlockPublicAcls": true, "IgnorePublicAcls": true,
    "BlockPublicPolicy": true, "RestrictPublicBuckets": true
  }
}
```

## Part 3: Deploying the Real Frontend (15 min)

Since this module's job is deliberately public static hosting (Module 5 fixes this properly with
CloudFront and a private bucket — this module's public bucket is a deliberate, temporary
stepping stone, not the sprint's final answer), disable Block Public Access explicitly and
knowingly:

```bash
aws s3api put-public-access-block --bucket <bucket-name> --public-access-block-configuration \
  BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false
aws s3api put-bucket-policy --bucket <bucket-name> --policy file://public-read-policy.json
```

Build the real `mission-ui` and upload it:

```bash
cd mission-ui
npx ng build --configuration production
aws s3 sync dist/mission-ui/browser s3://<bucket-name>
```

Real, verified output — an actual `ng build`, not a placeholder:

```
Application bundle generation complete. [1.911 seconds]
Output location: .../mission-ui/dist/mission-ui
```

```
upload: dist/mission-ui/browser/index.html to s3://<bucket-name>/index.html
upload: dist/mission-ui/browser/chunk-BTWH3LUR.js to s3://<bucket-name>/chunk-BTWH3LUR.js
... (10 more files)
```

Verify with a real HTTP request against the actual S3 website endpoint, not the console:

```bash
curl -s -o /dev/null -w "HTTP %{http_code}\n" \
  http://<bucket-name>.s3-website-us-east-1.amazonaws.com
```

```
HTTP 200
```

Open the URL in a real browser: the actual Mission Control login screen renders, served
entirely from S3 — no server, no container, nothing running continuously. This directly proves
Module 1's claim that S3 "never executes anything" — nothing was deployed except static files,
and the browser did all the work rendering Angular's compiled JavaScript.

## Part 4: What Just Got Built vs What Module 5 Fixes (5 min)

Name the real gap in what was just built: the bucket is now fully public — anyone
with the bucket name can list and read every object directly, and the URL is an ugly
`s3-website-us-east-1.amazonaws.com` address with no TLS. Module 5 solves both: CloudFront sits
in front of the bucket, the bucket goes back to fully private (Block Public Access re-enabled),
and only CloudFront — via an Origin Access Control — is allowed to read from it.

## Key Message

S3 stores objects, not files in folders, and every new bucket is private by default for a real,
deliberate security reason — making one public is an explicit, auditable action, never an
accident. Today's public bucket works and serves the real Angular app, but it's a stepping
stone: Module 5 replaces the public bucket with a private one, fronted properly.

## Transition to the Lab

Candidates create their own bucket, hit the same Block Public Access error, work through the
fix deliberately, and deploy their own `mission-ui` build, verifying it with a real HTTP request
and a real browser load — the same two-step verification used here.
