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

// TODO:
// - we will also need access to the S3 bucket for transfer of network captures
// - special IAM policy will be needed for that purpose
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
    "arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM"
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
    from_port   = 0
    to_port     = 65535
    cidr_blocks = [var.vpc_cidr_block]
    description = "Allow any outbound UDP traffic to any host within this VPC"
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
  egress {
    protocol    = "icmp"
    from_port   = -1
    to_port     = -1
    cidr_blocks = [var.vpc_cidr_block]
    description = "Allow outbound ICMP traffic to any host within this VPC"
  }
  tags = merge(var.tags, {
    Name = "${var.resource_name_prefix}-EC2-Client-SG"
  })
}