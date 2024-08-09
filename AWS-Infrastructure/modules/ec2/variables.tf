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

variable "vpc_id" {
  description = "VPC ID of the VPC where the EC2 instances are to be launched"
  type        = string
}

variable "vpc_cidr_block" {
  description = "CIDR block for the VPC where the EC2 instances are to be launched"
  type        = string
}

variable "subnet_id" {
  description = "ID of the subnet where the EC2 instances are to be launched"
  type        = string
}

variable "ec2_instance_type" {
  description = "Instance type of the EC2 instances to be started"
  type        = string
  default     = "t2.micro"
}

variable "capture_transfer_bucket_arn" {
  description = "Name of the S3 bucket for the transfer of network captures from EC2 instances to localhost"
  type        = string
}

variable "resource_name_prefix" {
  description = "Prefix for the names to be applied to the provisioned resources"
  type        = string
}

variable "tags" {
  description = "Common tags to be applied to the provisioned resources"
  type        = map(string)
}
