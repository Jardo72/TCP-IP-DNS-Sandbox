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

from commons import open_multicast_subscriber


def create_cmd_line_args_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Multicast Producer", formatter_class=RawTextHelpFormatter)

    parser.add_argument(
        "address",
        help="the IP address the multicast group the consumer will read messages from"
    )
    parser.add_argument(
        "port",
        help="the UDP port the consumer will read messages from",
        type=int
    )

    return parser


def parse_cmd_line_args() -> Namespace:
    parser = create_cmd_line_args_parser()
    params = parser.parse_args()
    return params


def main() -> None:
    cmd_line_args = parse_cmd_line_args()
    print(f"Multicast subscriber is going to consume from {cmd_line_args.address}:{cmd_line_args.port}")
    try:
        subscriber = open_multicast_subscriber(cmd_line_args.address, cmd_line_args.port, 4096)
        while True:
            _, input_msg = subscriber.recv_text_msg()
            print(f"Message from publisher: '{input_msg}'")
    except KeyboardInterrupt:
        print("Keyboard interrupt - exit")


if __name__ == "__main__":
    main()
