# Module 07 Lab — Discussion Answers (Instructor Reference)

## Declarative vs imperative, for this file

This file is declarative: it states the desired end state (one S3 bucket, versioned, with
public access blocked) and leaves Terraform to work out how to get there, including checking
what already exists and only changing what's different. An imperative equivalent, a script of
`aws s3api create-bucket`, `aws s3api put-bucket-versioning`, and so on, would have to handle
its own error checking (does the bucket already exist? did the last command actually succeed?),
its own idempotency (running it twice shouldn't fail or duplicate anything), and its own
ordering logic. Terraform handles all of that for you, that's the main practical benefit of
declarative tools.

## Connecting to CI/CD (plan vs apply)

`terraform plan` shows exactly what would change, without changing anything, a diff for
infrastructure, similar in spirit to `git diff` before a commit. `terraform apply` actually
makes the change. Teams often gate `apply` behind a human approval specifically because
infrastructure changes can be destructive in ways application deploys usually aren't, deleting
a database, changing network access rules, or removing a security control can have
consequences that are hard or impossible to roll back, unlike redeploying a previous
application version. A routine app deploy is usually safely reversible; a `terraform apply`
sometimes isn't, that asymmetry is why extra caution is common at that specific step.

## Setup and run walkthrough (for the optional live/demo section)

```bash
terraform -version
# Terraform v1.8.x

aws configure --profile sprint2-sandbox
export AWS_PROFILE=sprint2-sandbox

terraform init
# Initializing the backend...
# Initializing provider plugins...
# - Finding hashicorp/aws versions matching "~> 5.0"...
# - Installing hashicorp/aws v5.x...
# Terraform has been successfully initialized!

terraform plan -var="environment=training"
# Terraform will perform the following actions:
#
#   # aws_s3_bucket.static_assets will be created
#   + resource "aws_s3_bucket" "static_assets" { ... }
#
#   # aws_s3_bucket_versioning.static_assets_versioning will be created
#   + resource "aws_s3_bucket_versioning" ... { ... }
#
#   # aws_s3_bucket_public_access_block.static_assets_block will be created
#   + resource "aws_s3_bucket_public_access_block" ... { ... }
#
# Plan: 3 to add, 0 to change, 0 to destroy.

terraform apply -var="environment=training"
# (type "yes" to confirm)
# aws_s3_bucket.static_assets: Creating...
# aws_s3_bucket.static_assets: Creation complete
# aws_s3_bucket_versioning.static_assets_versioning: Creating...
# aws_s3_bucket_public_access_block.static_assets_block: Creating...
#
# Apply complete! Resources: 3 added, 0 changed, 0 destroyed.
#
# Outputs:
# bucket_name = "paysprint-static-assets-training"

terraform destroy -var="environment=training"
# (type "yes" to confirm)
# Destroy complete! Resources: 3 destroyed.
```

**Instructor note:** `plan`'s "3 to add" count is a useful thing to have delegates predict
*before* running it, based on reading the file, then check their prediction against the real
output. It's a quick, concrete way to confirm they actually understood the resource blocks
rather than just skimmed them.

## What to check as an instructor

- Annotations are in the delegate's own words, not GenAI's explanation copy-pasted unchanged.
- At least one annotation correctly identifies the security intent of
  `aws_s3_bucket_public_access_block`, not just what it technically does.
- The declarative-vs-imperative answer is specific to *this file*, not a generic definition
  copied from a textbook.
- The plan/apply answer correctly identifies irreversibility/blast-radius as the reason for
  extra caution, not just "because it's infrastructure."
