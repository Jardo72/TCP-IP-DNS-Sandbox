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

output "server_ec2_instance_id" {
  description = "Instance ID of the EC2 instance serving as server"
  value       = aws_instance.ec2_instance_server.id
}

output "client_1_ec2_instance_id" {
  description = "Instance ID of the EC2 instance serving as client #1"
  value       = aws_instance.ec2_instance_client_1.id
}

output "client_2_ec2_instance_id" {
  description = "Instance ID of the EC2 instance serving as client #2"
  value       = aws_instance.ec2_instance_client_2.id
}

output "client_3_ec2_instance_id" {
  description = "Instance ID of the EC2 instance serving as client #3"
  value       = aws_instance.ec2_instance_client_3.id
}
