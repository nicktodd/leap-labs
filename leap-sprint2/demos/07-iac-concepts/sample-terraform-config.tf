terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region to deploy PaySprint's static assets bucket into"
  type        = string
  default     = "eu-west-2"
}

variable "environment" {
  description = "Deployment environment name, e.g. dev, staging, production"
  type        = string
}

resource "aws_s3_bucket" "static_assets" {
  bucket = "paysprint-static-assets-${var.environment}"

  tags = {
    Project     = "PaySprint Mobile"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_s3_bucket_versioning" "static_assets_versioning" {
  bucket = aws_s3_bucket.static_assets.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "static_assets_block" {
  bucket = aws_s3_bucket.static_assets.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

output "bucket_name" {
  description = "Name of the S3 bucket created for static assets"
  value       = aws_s3_bucket.static_assets.bucket
}
