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
  description = "VPC ID of the VPC to associate the private hosted zone with"
  type        = string
}

variable "hosted_zone_name" {
  description = "The name of the Route 53 hosted zone to be created"
  type        = string
}

variable "record_ttl" {
  description = "TTL (in seconds) for the Route 53 records to be created"
  type        = number
}

variable "server_ec2_instance_ip_address" {
  description = "IP address of the EC2 instance serving as server"
  type        = string
}

variable "client_1_ec2_instance_ip_address" {
  description = "IP address of the EC2 instance serving as client #1"
  type        = string
}

variable "client_2_ec2_instance_ip_address" {
  description = "IP address of the EC2 instance serving as client #2"
  type        = string
}

variable "client_3_ec2_instance_ip_address" {
  description = "IP address of the EC2 instance serving as client #3"
  type        = string
}

variable "client_4_ec2_instance_ip_address" {
  description = "IP address of the EC2 instance serving as client #4"
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
