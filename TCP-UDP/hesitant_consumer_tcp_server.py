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

from argparse import (
    ArgumentParser,
    Namespace,
    RawTextHelpFormatter,
)
from os import getpid

from commons import (
    TCPSocket,
    open_tcp_listener,
)


def create_cmd_line_args_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Hesitant Consumer TCP Server", formatter_class=RawTextHelpFormatter)

    parser.add_argument(
        "address",
        help="the IP address the server has to bind to (use 0.0.0.0 to bind to all network interfaces)"
    )
    parser.add_argument(
        "port",
        help="the TCP port the server has to bind to",
        type=int
    )

    return parser


def parse_cmd_line_args() -> Namespace:
    parser = create_cmd_line_args_parser()
    params = parser.parse_args()
    if not (1024 <= params.port <= 65535):
        parser.error("Port must be between 1024 and 65535.")
    return params


def main() -> None:
    cmd_line_args = parse_cmd_line_args()
    print(f"TCP server (PID = {getpid()}) going to bind to {cmd_line_args.address}:{cmd_line_args.port}")
    listener = None
    try:
        listener = open_tcp_listener(cmd_line_args.address, cmd_line_args.port)
        connection, remote_address = listener.accept()
        rcv_buf_size = connection.get_rcv_buff_size()
        print(f"Client connection accepted from ({remote_address.host}:{remote_address.port}), input buffer size = {rcv_buf_size} bytes...")
        input("Press enter to start reading the data")
        while True:
            connection.recv_json_msg()
    except KeyboardInterrupt:
        print("Keyboard interrupt - exit")
    except Exception as e:
        print(f"Exception caught: {str(e)}")
    finally:
        if listener:
            listener.close()


if __name__ == "__main__":
    main()
