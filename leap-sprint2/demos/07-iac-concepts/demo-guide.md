# Demo: Module 07 — Infrastructure as Code Concepts

**Duration:** 16 minutes (10 core + 6 optional setup-and-run walkthrough)
**Prerequisite:** `sample-terraform-config.tf` open. GitHub Copilot Chat available. The core
demo needs no Terraform installation or cloud account. Part 6 (setup and run) needs the
trainer's own AWS sandbox account and the Terraform CLI, delegates without AWS access yet
watch this part rather than run it themselves, full hands-on cloud work comes in a later
sprint.

## Part 1: You've already written IaC (2 min)

Narration: Module 06's `docker-compose.yml` was Infrastructure as Code, just for containers
rather than cloud infrastructure. It described the desired end state (two services, a network,
a port mapping) in a version-controlled file, and a tool made that state real. Terraform and
CloudFormation apply exactly the same idea to VMs, networks, storage, and entire cloud
environments.

## Part 2: Why IaC matters (2 min)

- **Repeatability**: the same config produces the same environment, every time, no manual
  clicking through a cloud console
- **Auditability**: every change to infrastructure is a diff in git history, exactly like code
- **Version control**: infrastructure changes go through the same PR review as Module 03/04,
  a second pair of eyes before anything real changes

## Part 3: Declarative vs imperative (2 min)

Narration, pointing at the comparison diagram: an imperative script says exactly *how* to get
somewhere, step by step (create this, then that, then configure this). A declarative config
says *what* the end state should look like, and leaves the tool to work out how to get there,
including figuring out what already exists and what needs to change. Terraform and
CloudFormation are declarative. A shell script that runs `aws` CLI commands in sequence is
imperative.

## Part 4: Reading the sample config with GenAI (3 min)

Open `sample-terraform-config.tf`. Select the whole file and ask Copilot Chat:

```text
Explain what each block in this Terraform file does, in plain English.
```

Narration: read the explanation aloud. It should describe the provider block (which cloud,
which region), the two variables (region, environment), the S3 bucket resource, the versioning
and public-access-block resources attached to it, and the output. Critique it, same habit as
every prior module: does the explanation correctly identify that `block_public_acls` and
friends exist specifically to stop the bucket being made public by accident?

## Part 5: Common tools, briefly (1 min)

- **Terraform**: multi-cloud, declarative, HCL syntax, what this sample config uses
- **CloudFormation**: AWS-native equivalent, declarative, JSON or YAML
- **Ansible**: configuration management, more procedural in how playbooks run, agentless

## Part 6: Setting up and running Terraform for real (6 min, optional)

Narration: everything so far has been reading. This part shows the config from Part 4 actually
becoming a real S3 bucket, using the trainer's AWS sandbox account. S3 is used deliberately: no
compute running up a bill while idle, no networking or security-group complexity, and trivially
easy to fully tear down at the end.

**1. Install Terraform.** Download from developer.hashicorp.com/terraform/install, or via a
package manager (`choco install terraform` on Windows, `brew install terraform` on macOS).
Confirm with:

```bash
terraform -version
```

**2. Configure AWS credentials.** Terraform needs credentials the same way the AWS CLI does.
Simplest option for training purposes, environment variables scoped to a sandbox account:

```bash
export AWS_ACCESS_KEY_ID="<sandbox-access-key>"
export AWS_SECRET_ACCESS_KEY="<sandbox-secret-key>"
export AWS_DEFAULT_REGION="eu-west-2"
```

Narration: never commit these to a repo, and never use production credentials for a training
exercise. A named AWS CLI profile (`aws configure --profile sprint2-sandbox`) is the safer
long-term habit, mention it exists even if the demo uses environment variables for speed.

**3. Initialise the working directory:**

```bash
terraform init
```

Narration: downloads the AWS provider plugin declared in the `terraform` block, and sets up
local state tracking. This only needs doing once per directory, or whenever providers change.

**4. Preview the change:**

```bash
terraform plan -var="environment=training"
```

Narration: point out the `+` markers, everything Terraform proposes to *create*. Nothing has
happened to AWS yet, this is the "diff" from Module 07's slides, made real.

**5. Apply it:**

```bash
terraform apply -var="environment=training"
```

Confirm with `yes` when prompted. Narration: Terraform now calls the AWS API, creates the
bucket, versioning config, and public-access block, and prints the `bucket_name` output.
Briefly show the bucket now existing in the AWS S3 console, tying the file back to something
real.

**6. Tear it down:**

```bash
terraform destroy -var="environment=training"
```

Narration: **always destroy training resources afterwards.** This is exactly why S3 was chosen,
a forgotten EC2 instance costs money by existing; a forgotten empty S3 bucket essentially
doesn't, but tidy up regardless, it's the habit that matters more than this specific case.

## Key message

Infrastructure as Code takes the same discipline you already apply to application code, review,
version control, repeatable builds, and applies it to the environments that code runs in. You
don't need to be a Terraform expert to read a config and understand what it's asking for, that's
exactly the skill this lab practises, and Part 6 shows that the same file is also a short,
predictable path to something real.
