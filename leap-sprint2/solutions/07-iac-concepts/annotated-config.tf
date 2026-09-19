# Instructor reference: an example of a fully annotated version of the sample config.

# Declares which provider plugin this config needs (AWS) and pins a version range,
# so a `terraform init` months from now doesn't silently pull in a breaking new version.
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configures the AWS provider itself: which region Terraform will create resources in.
provider "aws" {
  region = var.aws_region
}

# An input variable: lets whoever runs this config choose a region without editing the file.
# Defaults to eu-west-2 if nothing else is supplied.
variable "aws_region" {
  description = "AWS region to deploy PaySprint's static assets bucket into"
  type        = string
  default     = "eu-west-2"
}

# A required input variable (no default): whoever runs this must say which environment
# they're targeting, this feeds into the bucket's name and tags below.
variable "environment" {
  description = "Deployment environment name, e.g. dev, staging, production"
  type        = string
}

# The main resource: an S3 bucket, named uniquely per environment so dev/staging/production
# never collide. Tags make it easy to find and cost-attribute in the AWS console later.
resource "aws_s3_bucket" "static_assets" {
  bucket = "paysprint-static-assets-${var.environment}"

  tags = {
    Project     = "PaySprint Mobile"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

# Turns on versioning for the bucket: if a file is overwritten or deleted, previous
# versions are kept, protecting against accidental data loss.
resource "aws_s3_bucket_versioning" "static_assets_versioning" {
  bucket = aws_s3_bucket.static_assets.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Explicitly blocks every route that could make this bucket or its contents public,
# even if someone later tries to set a public ACL or bucket policy by mistake.
# This is a deliberate secure-by-default choice, not an accident of omission.
resource "aws_s3_bucket_public_access_block" "static_assets_block" {
  bucket = aws_s3_bucket.static_assets.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# An output: after this config runs, Terraform prints the bucket's actual name,
# useful for other tooling (or a human) that needs to reference it afterwards.
output "bucket_name" {
  description = "Name of the S3 bucket created for static assets"
  value       = aws_s3_bucket.static_assets.bucket
}
