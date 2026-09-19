# Lab 4 — S3 Fundamentals & Deploying the Frontend

## Setup

Access the AWS console and CLI as per your instructor's instructions for this cohort. A working
checkout of `mission-ui` (Sprint 9), buildable with `ng build`.

## Task

### Part 1: Create a bucket and hit the real default

1. Create a bucket with a globally-unique name (try `leap-<yourname>-mission-ui` or similar —
   note what happens if the name is already taken by someone else in the world, not just this
   account).
2. Try to configure it for static website hosting and attach a public-read bucket policy
   (ask your instructor for a sample policy JSON, or write one granting `s3:GetObject` to
   principal `*` on `arn:aws:s3:::<bucket-name>/*`). Record the exact error you get.
3. Run `aws s3api get-public-access-block --bucket <bucket-name>` and confirm all four settings
   are `true`. Before reading further, write down in your own words why you think AWS made this
   the default for every new bucket, rather than leaving buckets public by default and requiring
   an explicit step to lock them down.

### Part 2: Deploy the real frontend

4. Deliberately and explicitly disable Block Public Access on your bucket, then apply the
   bucket policy from step 2. Enable static website hosting.
5. Build `mission-ui` for real: `ng build --configuration production`.
6. Sync the build output to your bucket: `aws s3 sync dist/mission-ui/browser
   s3://<bucket-name>`.
7. Verify with a real HTTP request: `curl -s -o /dev/null -w "HTTP %{http_code}\n"
   http://<bucket-name>.s3-website-<region>.amazonaws.com`. Confirm `HTTP 200`.
8. Open the URL in a real browser. Confirm the actual Mission Control login screen renders.

### Part 3: Storage classes and cost

9. Run `aws s3api list-objects-v2 --bucket <bucket-name> --query
   'Contents[].{Key:Key,StorageClass:StorageClass}'`. What storage class did your objects land in
   by default, and is that the right choice for a frontend build that's requested on every page
   load? Justify your answer.
10. In your own words: name the three components of an S3 bill, and which one is most likely to
    dominate for a widely-visited website versus a rarely-visited one.

## Verify

Compare your Part 1 and Part 3 answers against `solutions/04-.../model-answers.md`. Your Part 2
deployment is verified by the real `curl` response and browser load — if either fails, check the
bucket policy's `Resource` ARN matches your bucket name exactly, and that static website hosting
is actually enabled.

## Cleanup

Delete your bucket's contents and the bucket itself once verified — a public bucket left running
after this lab is a real, avoidable exposure, not just a cost concern. Module 5 creates a fresh,
properly private bucket from scratch.

## A Question Worth Sitting With

The bucket you just built is fully public — anyone with the bucket name can list and read
every object in it directly, bypassing your Angular app entirely. What's the most sensitive
thing that could end up in a frontend build's output directory by mistake (think about what a
`ng build` actually bundles), and why does that make "public bucket, public website" a
meaningfully different risk from "public website" alone?
