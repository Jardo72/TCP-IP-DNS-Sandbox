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

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

import dns.rdataclass
import dns.rdatatype
import dns.resolver


def create_cmd_line_args_parser() -> ArgumentParser:
    parser = ArgumentParser(description="DNS Query Tool", formatter_class=RawTextHelpFormatter)

    parser.add_argument(
        "dns_name",
        help="the DNS name to be resolved"
    )
    parser.add_argument(
        "record_type",
        help="the desired DNS record type"
    )

    return parser

def parse_cmd_line_args() -> Namespace:
    parser = create_cmd_line_args_parser()
    params = parser.parse_args()
    return params


def perform_dns_lookup(dns_name: str, record_type: str) -> None:
    print(f"Query - DNS name = {dns_name}, desired record type = {record_type}")
    print("Answers")
    for answer in dns.resolver.resolve(dns_name, record_type):
        rdtype = dns.rdatatype.to_text(answer.rdtype)
        rdclass = dns.rdataclass.to_text(answer.rdclass)
        
        # TODO: remove
        # print(f"Answer = {answer}, type = {type(answer)}")
        # print(f"type = {rdtype}, class = {rdclass}")

        if rdtype in {"A", "AAAA"}:
            print(f"- address = {answer.address}, type = {rdtype}, class = {rdclass}")
        if rdtype in {"MX"}:
            print(f"- address = {answer.exchange}, preference = {answer.preference}, type = {rdtype}, class = {rdclass}")
        if rdtype in {"NS"}:
            print(f"- address = {answer.target}, type = {rdtype}, class = {rdclass}")
        if rdtype in {"SOA"}:
            print(f"- master name = {answer.mname}, responsible name = {answer.rname}, serial = {answer.serial}")


def main() -> None:
    cmd_line_args = parse_cmd_line_args()
    perform_dns_lookup(cmd_line_args.dns_name, cmd_line_args.record_type)


if __name__ == "__main__":
    main()
