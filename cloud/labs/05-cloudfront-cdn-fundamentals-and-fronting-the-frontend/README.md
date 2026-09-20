# Lab 5 - CloudFront: CDN Fundamentals & Fronting the Frontend

## Setup

Access the AWS console and CLI as per your instructor's instructions for this cohort. A working
`mission-ui` build (`ng build --configuration production`).

## Task

### Part 1: A private bucket, deliberately

1. Create a new bucket. This time, leave Block Public Access exactly as created - do not touch
   it. Confirm with `get-public-access-block` that all four settings are still `true`.
2. Upload your `mission-ui` build to it.
3. Confirm the bucket is unreachable: `curl
   https://<bucket-name>.s3.<region>.amazonaws.com/index.html` should return an `AccessDenied`
   error. If it doesn't, stop and check what changed before continuing.

### Part 2: Origin Access Control and a distribution

4. Create an Origin Access Control for S3.
5. Create a CloudFront distribution with your bucket as the origin, the OAC attached to that
   origin, and `index.html` as the default root object.
6. Apply a bucket policy granting `s3:GetObject` to the `cloudfront.amazonaws.com` service
   principal, scoped with a `Condition` to your specific distribution's ARN (not just "any
   CloudFront distribution").
7. Before running the command, predict: will `put-bucket-policy` succeed or fail, given Block
   Public Access is still fully on? Write down your prediction and your reasoning, then run it
   and compare.

### Part 3: Verify both sides

8. Wait for the distribution's status to become `Deployed` (`aws cloudfront get-distribution
   --id <id> --query 'Distribution.Status'`) - this takes several real minutes, not instant.
9. Re-run the direct S3 request from step 3. Confirm it's still denied - nothing about creating
   the distribution should have changed the bucket's own accessibility.
10. Request `https://<distribution-domain>.cloudfront.net/` with `curl -I`. Confirm `HTTP 200`
    and look for the `x-cache` and `via` headers confirming the response came from CloudFront.
11. Open the CloudFront URL in a real browser. Confirm the actual Mission Control login screen
    renders, over HTTPS.

## Verify

Compare your Part 2 prediction and reasoning against `solutions/05-.../model-answers.md`. Your
Part 3 deployment is verified by the real `curl` responses and browser load from steps 9-11.

## Cleanup

Disable the distribution (`Enabled: false` in its config, then wait for that change to deploy),
then delete it, then delete the bucket's contents and the bucket itself. A CloudFront
distribution left running has no compute cost by itself, but every request through it does bill
- tear it down once verified, the same discipline as every other module this week.

## A Question Worth Sitting With

Module 4's bucket needed Block Public Access turned off to work at all. This module's bucket
never needs it turned off, and yet ends up reachable by anyone on the internet who visits the
CloudFront URL. Explain, in your own words, how both of those things can be true at once - what
exactly is the bucket policy granting access to, if not "the public"?
