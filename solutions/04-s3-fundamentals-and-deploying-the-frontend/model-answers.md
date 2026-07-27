# Lab 4 Model Answers

## Verified Output

Run for real, against a bucket created and torn down during preparation (bucket name shown here
is illustrative — bucket names are globally unique, so yours will differ):

- `put-bucket-policy` before disabling Block Public Access: real `AccessDenied`, naming
  `BlockPublicPolicy` specifically as the setting that stopped it.
- `get-public-access-block`: all four settings `true` on a brand-new bucket, with no
  configuration applied yet.
- `ng build --configuration production`: real output, `Application bundle generation complete
  [1.911 seconds]`, producing `dist/mission-ui/browser/` with `index.html` and eleven JS/CSS
  chunk files.
- `aws s3 sync`: eleven real upload confirmations, one per file.
- `curl -s -o /dev/null -w "HTTP %{http_code}\n" http://<bucket>.s3-website-us-east-1.amazonaws.com`:
  `HTTP 200`.
- A real browser load of that URL: the actual Mission Control login screen, served with no
  server or container running anywhere.

## Part 1: Why Block Public Access Defaults to On

Every new S3 bucket denies public access by default because, for years, an accidentally-public
bucket containing sensitive data (customer records, internal documents, credentials) was one of
the most common real-world cloud security incidents — nearly always caused by someone applying a
public-read policy for a legitimate reason (hosting a website, sharing one file) without
realising it exposed the *entire* bucket, or applying it to the wrong bucket entirely. Making
public access an explicit, deliberate, individually-confirmed action (as this lab's Part 2
requires) means a bucket can never become public by mistake, forgetting a step, or copying a
policy from the wrong tutorial — it has to be turned off on purpose, every time.

## Part 3: Storage Classes and Cost

New objects land in the Standard storage class by default. This is the correct choice for
`mission-ui`'s build output — Standard is priced for data accessed frequently, and a frontend
build is requested by every single visitor's browser on every page load, the exact access
pattern Standard is designed and priced for. Infrequent Access or Glacier would be actively
wrong here: both charge a per-GB retrieval fee on top of storage, which would apply to *every*
page load — for frequently-accessed data, a cheaper storage price with a retrieval fee attached
ends up more expensive overall than Standard's simpler, no-retrieval-fee pricing.

An S3 bill has three components: storage (per GB per month, based on how much data sits in the
bucket), requests (per thousand GET/PUT/LIST/etc. calls), and data transfer out to the internet
(free to upload into S3, charged to serve back out). For a genuinely popular website, data
transfer out dominates — every visitor downloading the same JavaScript bundles adds up fast, and
this exact cost is why Module 5 puts CloudFront in front of the bucket, since CloudFront caches
responses at edge locations and serves repeat requests without going back to S3 (or paying its
transfer cost) at all. For a rarely-visited site, storage cost dominates simply because there's
almost no request or transfer activity to bill.

## The Reflection Question

The most sensitive thing that can end up in a frontend build's output by mistake is a secret
that should never have been compiled into client-side code in the first place — an API key, a
signing secret, or a hardcoded credential accidentally referenced in a component or environment
file, which `ng build` bundles into the shipped JavaScript exactly like any other source code. A
public website alone already exposes that secret to anyone who opens their browser's dev tools
and reads the JavaScript source — but a *public bucket* on top of that is a meaningfully
different, wider exposure: it lets someone list and download every object directly (bypassing
`index.html` and the app entirely), including any build artefact, source map, or leftover file
that was never meant to be linked from the site at all, not just the files an ordinary visitor's
browser would ever request.
