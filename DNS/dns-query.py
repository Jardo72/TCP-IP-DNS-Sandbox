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
    for answer in dns.resolver.resolve(dns_name, record_type):
        # print(f"{answer.qname} {answer.rdtype}")
        print(f"Answer = {answer}, type={type(answer)}")


def main() -> None:
    cmd_line_args = parse_cmd_line_args()
    perform_dns_lookup(cmd_line_args.dns_name, cmd_line_args.record_type)


if __name__ == "__main__":
    main()
