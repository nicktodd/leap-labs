# Lab 5 Model Answers

## Verified Output

Run for real, against a bucket and distribution created and torn down during preparation
(bucket name and distribution domain shown here are illustrative - both are unique per
deployment):

- `get-public-access-block` after bucket creation: all four settings `true`, untouched
  throughout the whole module.
- Direct S3 request before creating the distribution: real `AccessDenied` XML error.
- `put-bucket-policy` with the CloudFront-service-principal policy: succeeded immediately, with
  Block Public Access still fully on.
- Distribution status: `InProgress` for several real minutes, then `Deployed`.
- Direct S3 request again, after the distribution deployed: still `AccessDenied` - unchanged.
- `curl -I https://<distribution-domain>.cloudfront.net/`: `HTTP 200`, headers including
  `x-cache: Hit from cloudfront` and `via: 1.1 <edge-id>.cloudfront.net (CloudFront)`.
- A real browser load of the CloudFront URL: the actual Mission Control login screen, over
  HTTPS.

## Part 2: Predicting the Bucket Policy Result

`put-bucket-policy` succeeds immediately, even with Block Public Access fully on. Block Public
Access's four settings specifically target policies and ACLs that grant access to *the public*
- a principal of `"*"` (anyone) or a well-known "all users" group. A policy whose principal is
`{"Service": "cloudfront.amazonaws.com"}`, further narrowed by a `Condition` naming one specific
distribution's ARN, never grants access to the public at all - it grants access to one named AWS
service, acting on behalf of one named, specific resource. AWS's public-access heuristics
correctly recognise this as not-public and let it through without complaint.

## The Reflection Question

Both things are true at once because "public" and "unreachable by the general public" describe
two different layers, and this lab deliberately keeps them separate. Block Public Access
guards the *bucket's own front door* - whether S3 itself will let anonymous internet traffic
read from the bucket directly, which it never does here; the direct `curl` to the S3 endpoint
fails at every step of this lab, before and after the distribution exists. The bucket policy
doesn't grant access to "the public" at all - it grants `s3:GetObject` to exactly one principal,
the CloudFront service, and only when that request is provably coming from one specific,
named distribution (enforced by the `AWS:SourceArn` condition). Anyone in the world can still
end up seeing the site's content, but only by going through that one distribution, which is the
only thing the bucket actually trusts - not because the bucket itself became public.
