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

resource "aws_route53_zone" "private_hosted_zone" {
  name    = var.hosted_zone_name
  comment = "Experimental private hosted zone for peered VPCs (${var.resource_name_prefix} demo)"
  vpc {
    vpc_id = var.vpc_id
  }
  tags = merge(var.tags, {
    Name = "${var.resource_name_prefix}-Hosted-Zone"
  })
}

resource "aws_route53_record" "server_ec2_instance_record" {
  zone_id = aws_route53_zone.private_hosted_zone.zone_id
  name    = "server.${var.hosted_zone_name}"
  type    = "A"
  ttl     = var.record_ttl
  records = [var.server_ec2_instance_ip_address]
}

resource "aws_route53_record" "client_1_ec2_instance_record" {
  zone_id = aws_route53_zone.private_hosted_zone.zone_id
  name    = "client-1.${var.hosted_zone_name}"
  type    = "A"
  ttl     = var.record_ttl
  records = [var.client_1_ec2_instance_ip_address]
}

resource "aws_route53_record" "client_2_ec2_instance_record" {
  zone_id = aws_route53_zone.private_hosted_zone.zone_id
  name    = "client-2.${var.hosted_zone_name}"
  type    = "A"
  ttl     = var.record_ttl
  records = [var.client_2_ec2_instance_ip_address]
}

resource "aws_route53_record" "client_3_ec2_instance_record" {
  zone_id = aws_route53_zone.private_hosted_zone.zone_id
  name    = "client-3.${var.hosted_zone_name}"
  type    = "A"
  ttl     = var.record_ttl
  records = [var.client_3_ec2_instance_ip_address]
}

resource "aws_route53_record" "client_4_ec2_instance_record" {
  zone_id = aws_route53_zone.private_hosted_zone.zone_id
  name    = "client-4.${var.hosted_zone_name}"
  type    = "A"
  ttl     = var.record_ttl
  records = [var.client_4_ec2_instance_ip_address]
}
