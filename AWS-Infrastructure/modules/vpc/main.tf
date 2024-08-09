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

data "aws_availability_zones" "available" {}

module "vpc" {
  source             = "terraform-aws-modules/vpc/aws"
  version            = "5.12.0"
  name               = "${var.resource_name_prefix}-VPC"
  cidr               = var.vpc_cidr_block
  azs                = data.aws_availability_zones.available.names
  private_subnets    = [cidrsubnet(var.vpc_cidr_block, 4, 0)]
  public_subnets     = [cidrsubnet(var.vpc_cidr_block, 4, 1)]
  enable_nat_gateway = true
}
