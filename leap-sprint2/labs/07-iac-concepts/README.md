# Module 07 Lab — Read and Annotate a Terraform Config

## Recap: building on Module 06

Module 06's `docker-compose.yml` described a desired state (two services, a network, a port
mapping) in a version-controlled file. This lab applies exactly the same idea one level up:
describing cloud infrastructure, rather than containers, as code.

## Objectives

By the end of this lab you will have:

- Read a short Terraform configuration and understood what each block does
- Used GenAI to explain unfamiliar syntax, then verified the explanation
- Annotated the file with your own comments in your own words
- Understood how this connects to declarative vs imperative approaches, and to CI/CD

## Setup

- [`sample-terraform-config.tf`](../../demos/07-iac-concepts/sample-terraform-config.tf) from
  the demo
- GitHub Copilot Chat
- No Terraform installation or AWS account needed, this is a read-only exercise

## Task sheet

1. **Read it once, unaided**
   Before asking GenAI anything, read through the file and note which blocks you already
   understand, and which are unfamiliar.

2. **Ask GenAI to explain the unfamiliar parts**
   Ask Copilot Chat to explain what each block does. For at least two specific claims in its
   explanation, verify them yourself (for example, look up what
   `aws_s3_bucket_public_access_block` actually controls in the Terraform AWS provider docs).

3. **Annotate the file yourself**
   Make a copy of the file and add a comment above each block, in your own words, explaining
   what it does and, where relevant, why it matters (for example, why block public access on a
   bucket by default).

4. **Declarative vs imperative**
   In two or three sentences, explain why this file is declarative rather than imperative.
   What would an imperative equivalent (a script of `aws` CLI commands) have to handle that this
   file doesn't need to?

5. **Connect it to CI/CD**
   This config would typically run through a pipeline stage that shows what would change
   (`terraform plan`) before another stage actually applies it (`terraform apply`), often
   gated behind an approval. Why might a team want a human approval step specifically before
   `apply`, when they don't necessarily require one before, say, a routine application deploy?

## Acceptance criteria

- You have an annotated copy of the Terraform file with a comment on every resource, variable,
  and output block, in your own words.
- You've verified at least two specific claims from GenAI's explanation against a second
  source.
- You have a written declarative-vs-imperative explanation specific to this file.
- You have a written answer connecting this to a plan/apply pipeline pattern.

If you finish early, look up one other resource type in the AWS provider (for example
`aws_iam_role`) and sketch, in plain English, what block you'd add to attach a minimal
read-only IAM role to this bucket.

## Optional: run it for real (only if you have AWS sandbox access)

Full hands-on cloud work comes in a later sprint, so this part is optional and only for
delegates who already have access to an AWS sandbox account today. If you don't, watch the
trainer's demo instead, don't use production credentials for this under any circumstances.

1. Install Terraform and confirm it with `terraform -version`.
2. Configure sandbox credentials, ideally a named AWS CLI profile rather than raw environment
   variables:
   ```bash
   aws configure --profile sprint2-sandbox
   export AWS_PROFILE=sprint2-sandbox
   ```
3. `terraform init` in the folder containing your annotated config.
4. `terraform plan -var="environment=<your-initials>"` and read through the proposed changes,
   do they match what you expected from your annotation?
5. `terraform apply -var="environment=<your-initials>"`, confirm with `yes`, and check the
   bucket now exists in the AWS S3 console.
6. **Before you finish**: `terraform destroy -var="environment=<your-initials>"`, and confirm
   the bucket is gone. Leaving training resources running, even low-cost ones like an empty S3
   bucket, is a habit worth not building.
