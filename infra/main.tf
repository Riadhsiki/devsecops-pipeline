resource "aws_security_group" "ssh_restricted" {
  #checkov:skip=CKV2_AWS_5: sample file, no instance is deployed. Reviewed by Riadh 2026-10-09
  name        = "ssh-restricted"
  description = "SSH from the admin network only"
  ingress {
    description = "SSH from admin network"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/24"]
  }
}

resource "aws_s3_bucket" "data" {
  #checkov:skip=CKV_AWS_18: demo bucket, access logging needs a separate log bucket. Reviewed by Riadh 2026-10-09
  #checkov:skip=CKV_AWS_144: no cross-region replication needed for demo data. Reviewed by Riadh 2026-10-09
  #checkov:skip=CKV2_AWS_61: no retention policy required for demo data. Reviewed by Riadh 2026-10-09
  #checkov:skip=CKV2_AWS_62: no event consumer exists. Reviewed by Riadh 2026-10-09
  bucket = "devsecops-demo-bucket"
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket                  = aws_s3_bucket.data.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_kms_key" "data" {
  description         = "KMS key for the data bucket"
  enable_key_rotation = true
}

resource "aws_s3_bucket_versioning" "data" {
  bucket = aws_s3_bucket.data.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.data.arn
    }
  }
}

data "aws_caller_identity" "current" {}

resource "aws_kms_key_policy" "data" {
  key_id = aws_kms_key.data.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "AdminOnly"
      Effect    = "Allow"
      Principal = { AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root" }
      Action    = "kms:*"
      Resource  = "*"
    }]
  })
}
