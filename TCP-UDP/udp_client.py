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
from uuid import uuid4

from commons import Endpoint, open_udp_client, random_sleep


def create_cmd_line_args_parser() -> ArgumentParser:
    parser = ArgumentParser(description="UDP Client", formatter_class=RawTextHelpFormatter)

    parser.add_argument(
        "address",
        help="the IP address the client will send messages to"
    )
    parser.add_argument(
        "port",
        help="the UDP port the client will send messages to",
        type=int
    )

    parser.add_argument(
        "-c", "--msg-count",
        dest="msg_count",
        default=10,
        help="optional number of messages to be sent (default = 10)",
        type=int
    )
    parser.add_argument(
        "-n", "--client-name",
        dest="client_name",
        help="optional client name (if not specified, generated UUID will be used)",
        type=str
    )

    return parser


def parse_cmd_line_args() -> Namespace:
    parser = create_cmd_line_args_parser()
    params = parser.parse_args()
    return params


def main() -> None:
    cmd_line_args = parse_cmd_line_args()
    client_name = cmd_line_args.client_name or str(uuid4())
    destination = Endpoint(cmd_line_args.address, cmd_line_args.port)
    client = open_udp_client()
    for i in range(1, cmd_line_args.msg_count + 1):
        output_msg = f"Message #{i} from client {client_name}"
        client.send_text_msg(destination, output_msg)
        print(f"Message sent to server: '{output_msg}'")
        _, input_msg = client.recv_text_msg()
        print(f"Message from server received: '{input_msg}'")
        random_sleep(min_sec=5, max_sec=20)


if __name__ == "__main__":
    main()
