# Module 5 Demo Guide — CloudFront: CDN Fundamentals & Fronting the Frontend

**Duration:** 50 minutes
**Prerequisite:** Module 4's real `mission-ui` build. A private S3 bucket this time — not the
public one from Module 4.

## Part 0: What a CDN Actually Does (8 min)

A CDN (Content Delivery Network) caches copies of content at edge locations — data centres
distributed around the world, close to where visitors actually are — so a request doesn't have
to travel all the way back to a single origin (here, an S3 bucket in `us-east-1`) every time.
CloudFront is AWS's CDN: a "distribution" is the configuration tying a domain name to an origin
(where the real content lives) and a set of behaviours (how to handle requests — which origin,
what to cache, for how long).

For a single-region app like this one, three concrete benefits, not abstract ones:

- **Latency**: a visitor in Sydney reaches a nearby edge location instead of `us-east-1`
  directly, even though the object was only ever uploaded to one bucket in one region.
- **TLS**: CloudFront provides HTTPS by default, on its own domain, with zero certificate
  configuration — the S3 website endpoint from Module 4 had none.
- **Caching**: a repeat request for the same file is served from the edge cache, without
  touching S3 (or paying its request/transfer cost) at all.

## Part 1: A Genuinely Private Bucket, This Time (7 min)

Unlike Module 4, Block Public Access stays on — untouched:

```bash
aws s3api create-bucket --bucket <bucket-name> --region us-east-1
aws s3api get-public-access-block --bucket <bucket-name>
```

```json
{"PublicAccessBlockConfiguration": {"BlockPublicAcls": true, "IgnorePublicAcls": true,
  "BlockPublicPolicy": true, "RestrictPublicBuckets": true}}
```

Upload the same real `mission-ui` build as Module 4 — the artefact doesn't change, only how it's
served:

```bash
aws s3 sync dist/mission-ui/browser s3://<bucket-name>
```

## Part 2: Origin Access Control — Only CloudFront Can Read (10 min)

An Origin Access Control (OAC) is CloudFront's identity when it talks to S3 — it lets a bucket
policy grant access to "this specific CloudFront distribution," not to the public:

```bash
aws cloudfront create-origin-access-control --origin-access-control-config '{
  "Name": "leap-mission-ui-oac", "SigningProtocol": "sigv4",
  "SigningBehavior": "always", "OriginAccessControlOriginType": "s3"
}'
```

Create the distribution, pointing its origin at the bucket with this OAC attached, then apply
the bucket policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "AllowCloudFrontServicePrincipal",
    "Effect": "Allow",
    "Principal": {"Service": "cloudfront.amazonaws.com"},
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::<bucket-name>/*",
    "Condition": {"StringEquals": {"AWS:SourceArn": "arn:aws:cloudfront::<account>:distribution/<dist-id>"}}
  }]
}
```

A real, worth-naming detail: `put-bucket-policy` **succeeds immediately**, even with Block
Public Access still fully on — a direct contrast with Module 4's `AccessDenied`. The policy's
principal is a specific AWS service (`cloudfront.amazonaws.com`), not `*`, so AWS's
public-access heuristics don't treat it as public at all. Block Public Access blocks policies
that grant access to *anyone*; a policy scoped to one named service, further restricted to one
specific distribution's ARN, was never public to begin with.

## Part 3: Verified — Private Bucket, Public CDN (15 min)

Confirm the bucket is genuinely unreachable directly, first:

```bash
curl -s "https://<bucket-name>.s3.us-east-1.amazonaws.com/index.html"
```

Real output:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Error><Code>AccessDenied</Code><Message>Access Denied</Message>...</Error>
```

Wait for the distribution to finish deploying (`aws cloudfront get-distribution --id <id>
--query 'Distribution.Status'` — this genuinely takes several minutes, not instant), then hit
the CloudFront domain directly:

```bash
curl -s -o /tmp/out.html -w "HTTP %{http_code}\n" https://<distribution-domain>.cloudfront.net/
curl -sI https://<distribution-domain>.cloudfront.net/ | grep -i "x-cache\|via"
```

Real, verified output:

```
HTTP 200
x-cache: Hit from cloudfront
via: 1.1 <edge-id>.cloudfront.net (CloudFront)
```

Open the URL in a real browser: the same Mission Control login screen from Module 4, this time
over HTTPS, on an AWS-provided domain, with the origin bucket completely unreachable directly —
the exact combination Module 4 named as the gap.

## Key Message

The security model here is not "hide the bucket name" — it's a real, enforced trust
relationship: only a specifically-named CloudFront distribution, verified via its ARN in the
bucket policy's condition, can read from the bucket at all, and Block Public Access stays on the
entire time because nothing here actually requires disabling it.

## Transition to the Lab

Candidates build the same pattern with their own bucket and distribution: private bucket, OAC,
distribution, bucket policy scoped to that one distribution's ARN, verified with the same
two-request check — direct S3 access denied, CloudFront access succeeding.
