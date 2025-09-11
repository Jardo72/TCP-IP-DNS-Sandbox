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

output "ec2_subnet_cidr" {
  description = "CIDR block of the private subnet within the VPC where the EC2 instances are running"
  value       = module.vpc.subnet_cidr
}

output "server_ec2_instance_id" {
  description = "Instance ID of the EC2 instance serving as server"
  value       = module.ec2.server_ec2_instance_id
}

output "server_ec2_instance_ip_address" {
  description = "IP address of the EC2 instance serving as server"
  value       = module.ec2.server_ec2_instance_ip_address
}

output "server_ec2_instance_dns_name" {
  description = "DNS name of the EC2 instance serving as server"
  value = module.route53.server_ec2_instance_dns_name
}

output "client_1_ec2_instance_id" {
  description = "Instance ID of the EC2 instance serving as client #1"
  value       = module.ec2.client_1_ec2_instance_id
}

output "client_1_ec2_instance_ip_address" {
  description = "IP address of the EC2 instance serving as client #1"
  value       = module.ec2.client_1_ec2_instance_ip_address
}

output "client_1_ec2_instance_dns_name" {
  description = "DNS name of the EC2 instance serving as client #1"
  value = module.route53.client_1_ec2_instance_dns_name
}

output "client_2_ec2_instance_id" {
  description = "Instance ID of the EC2 instance serving as client #2"
  value       = module.ec2.client_2_ec2_instance_id
}

output "client_2_ec2_instance_ip_address" {
  description = "IP address of the EC2 instance serving as client #2"
  value       = module.ec2.client_2_ec2_instance_ip_address
}

output "client_2_ec2_instance_dns_name" {
  description = "DNS name of the EC2 instance serving as client #2"
  value = module.route53.client_2_ec2_instance_dns_name
}

output "client_3_ec2_instance_id" {
  description = "Instance ID of the EC2 instance serving as client #3"
  value       = module.ec2.client_3_ec2_instance_id
}

output "client_3_ec2_instance_ip_address" {
  description = "IP address of the EC2 instance serving as client #3"
  value       = module.ec2.client_3_ec2_instance_ip_address
}

output "client_3_ec2_instance_dns_name" {
  description = "DNS name of the EC2 instance serving as client #3"
  value = module.route53.client_3_ec2_instance_dns_name
}

output "application_port" {
  description = "TCP and UDP port the applications will use"
  value       = var.application_port
}
