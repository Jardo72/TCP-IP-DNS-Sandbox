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

output "vpc_id" {
  description = "VPC ID of the provisioned VPC"
  value       = vpc.tcp_ip_demo_vpc.id
}

output "vpc_subnet_id" {
  description = "Subnet ID of the private subnet within the VPC"
  value = vpc.tcp_ip_demo_vpc.private_subnets[0]
}
