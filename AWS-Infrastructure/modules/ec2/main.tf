#
# Copyright 2024 Jaroslav Chmurny
#
# This file is part of TCP/IP & DNS Sandbox.
#
# TCP/IP & DNS Sandbox is free software developed for educational purposes.
# It is licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

data "aws_ami" "latest_amazon_linux_ami" {
  owners      = ["137112412989"]
  most_recent = true
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

resource "aws_iam_policy" "capture_transfer_bucket_access_policy" {
  name = "${var.resource_name_prefix}-CaptureTransfer-Bucket-AccessPolicy"
  policy = jsonencode({
    Version : "2012-10-17",
    Statement : [
      {
        Sid : "AllowS3BucketAccess",
        Effect : "Allow",
        Action : [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket",
        ],
        Resource : [
          var.capture_transfer_bucket_arn,
          "${var.capture_transfer_bucket_arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role" "ec2_iam_role" {
  name = "${var.resource_name_prefix}-EC2-IAM-Role"
  assume_role_policy = jsonencode({
    Version : "2012-10-17",
    Statement : [
      {
        Sid : "AllowEC2Assume",
        Action : "sts:AssumeRole",
        Principal : {
          Service : "ec2.amazonaws.com"
        },
        Effect : "Allow"
      }
    ]
  })
  managed_policy_arns = [
    # needed in order to be able to connect to the EC2 instances via the SSM Session Manager
    "arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM",
    aws_iam_policy.capture_transfer_bucket_access_policy.arn
  ]
  tags = merge(var.tags, {
    Name = "${var.resource_name_prefix}-EC2-IAM-Role"
  })
}

resource "aws_iam_instance_profile" "ec2_instance_profile" {
  name = "${var.resource_name_prefix}-EC2-Instance-Profile"
  role = aws_iam_role.ec2_iam_role.name
  tags = merge(var.tags, {
    Name = "${var.resource_name_prefix}-EC2-Instance-Profile"
  })
}

resource "aws_security_group" "ec2_server_security_group" {
  name        = "${var.resource_name_prefix}-EC2-Server-SG"
  description = "Security group protecting EC2 instance running the server/producer applications"
  vpc_id      = var.vpc_id
  ingress {
    protocol    = "icmp"
    from_port   = -1
    to_port     = -1
    cidr_blocks = [var.vpc_cidr_block]
    description = "Allow inbound ICMP traffic from any host within this VPC"
  }
  ingress {
    protocol    = "tcp"
    from_port   = 1234
    to_port     = 1234
    cidr_blocks = [var.vpc_cidr_block]
    description = "Allow inbound TCP traffic to port 1234 from any host within this VPC"
  }
  egress {
    protocol    = "icmp"
    from_port   = -1
    to_port     = -1
    cidr_blocks = [var.vpc_cidr_block]
    description = "Allow outbound ICMP traffic to any host within this VPC"
  }
  egress {
    protocol    = "tcp"
    from_port   = 443
    to_port     = 443
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow outbound HTTPS traffic (needed for the SSM Agent)"
  }
  egress {
    protocol    = "udp"
    from_port   = 1234
    to_port     = 1234
    cidr_blocks = [var.vpc_cidr_block]
    description = "Allow outbound UDP traffic to port 1234 to any host within this VPC"
  }
  tags = merge(var.tags, {
    Name = "${var.resource_name_prefix}-EC2-Server-SG"
  })
}

resource "aws_security_group" "ec2_client_security_group" {
  name        = "${var.resource_name_prefix}-EC2-Client-SG"
  description = "Security group protecting EC2 instance running the client/consumer applications"
  vpc_id      = var.vpc_id
  ingress {
    protocol    = "icmp"
    from_port   = -1
    to_port     = -1
    cidr_blocks = [var.vpc_cidr_block]
    description = "Allow inbound ICMP traffic from any host within this VPC"
  }
  ingress {
    protocol    = "udp"
    from_port   = 1234
    to_port     = 1234
    cidr_blocks = [var.vpc_cidr_block]
    description = "Allow inbound UDP traffic to port 1234 from any host within this VPC"
  }
  egress {
    protocol    = "icmp"
    from_port   = -1
    to_port     = -1
    cidr_blocks = [var.vpc_cidr_block]
    description = "Allow outbound ICMP traffic to any host within this VPC"
  }
  egress {
    protocol    = "tcp"
    from_port   = 1234
    to_port     = 1234
    cidr_blocks = [var.vpc_cidr_block]
    description = "Allow outbound TCP traffic to port 1234 to any host within this VPC"
  }
  tags = merge(var.tags, {
    Name = "${var.resource_name_prefix}-EC2-Client-SG"
  })
}

resource "aws_instance" "ec2_instance_server" {
  ami                    = data.aws_ami.latest_amazon_linux_ami.id
  instance_type          = var.ec2_instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [aws_security_group.ec2_server_security_group.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2_instance_profile.name
  user_data              = templatefile("${path.module}/ec2-user-data.tftpl", {})
  tags = merge(var.tags, {
    Name = "${var.resource_name_prefix}-EC2-Server"
  })
}

resource "aws_instance" "ec2_instance_client" {
  ami                    = data.aws_ami.latest_amazon_linux_ami.id
  instance_type          = var.ec2_instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [aws_security_group.ec2_client_security_group.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2_instance_profile.name
  user_data              = templatefile("${path.module}/ec2-user-data.tftpl", {})
  tags = merge(var.tags, {
    Name = "${var.resource_name_prefix}-EC2-Client"
  })
}
