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

terraform {
  required_version = ">=1.1"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>5.62.0"
    }
    template = {
      source  = "hashicorp/template"
      version = "~>2.2.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

module "s3" {
  source                  = "./modules/s3"
  capture_transfer_bucket = var.capture_transfer_bucket
  tags                    = var.tags
}

module "vpc" {
  source               = "./modules/vpc"
  vpc_cidr_block       = var.vpc_cidr_block
  resource_name_prefix = var.resource_name_prefix
  tags                 = var.tags
}

module "ec2" {
  source                      = "./modules/ec2"
  vpc_id                      = module.vpc.vpc_id
  vpc_cidr_block              = var.vpc_cidr_block
  ec2_instance_type           = var.ec2_instance_type
  capture_transfer_bucket_arn = module.s3.capture_transfer_bucket_arn
  resource_name_prefix        = var.resource_name_prefix
  tags                        = var.tags
}
