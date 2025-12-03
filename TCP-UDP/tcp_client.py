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
from uuid import uuid4

from commons import (
    open_tcp_connection,
    random_sleep,
)


def create_cmd_line_args_parser() -> ArgumentParser:
    parser = ArgumentParser(description="TCP Client", formatter_class=RawTextHelpFormatter)

    parser.add_argument(
        "address",
        help="the IP address the client has to connect to"
    )
    parser.add_argument(
        "port",
        help="the TCP port the client has to connect to",
        type=int
    )

    parser.add_argument(
        "-t", "--connect_timeout_sec",
        dest="connect_timeout_sec",
        default=10,
        help="optional connect timeout in seconds (default = 10 sec)",
        type=int,
    )
    parser.add_argument(
        "-r", "--read-timeout-sec",
        dest="read_timeout_sec",
        help="optional read timeout in seconds (default = no timeout)",
        type=float,
    )
    parser.add_argument(
        "-c", "--msg-count",
        dest="msg_count",
        default=10,
        help="optional number of messages to be sent (default = 10)",
        type=int,
    )
    parser.add_argument(
        "-n", "--client-name",
        dest="client_name",
        help="optional client name (if not specified, generated UUID will be used)",
        type=str,
    )

    return parser


def parse_cmd_line_args() -> Namespace:
    parser = create_cmd_line_args_parser()
    params = parser.parse_args()
    return params


def main() -> None:
    cmd_line_args = parse_cmd_line_args()
    client_name = cmd_line_args.client_name or str(uuid4())
    print(f"TCP client (PID = {getpid()}) going to connect to {cmd_line_args.address}:{cmd_line_args.port}")
    print(f"Connect timeout = {cmd_line_args.connect_timeout_sec} sec")
    if cmd_line_args.read_timeout_sec:
        print(f"Read timeout = {cmd_line_args.read_timeout_sec} sec")
    else:
        print("No read timeout configured")
    socket = None
    try:
        socket = open_tcp_connection(cmd_line_args.address, cmd_line_args.port, cmd_line_args.connect_timeout_sec)
        for i in range(1, cmd_line_args.msg_count + 1):
            output_msg = f"Message #{i} from client {client_name}"
            socket.send_text_msg(output_msg)
            print(f"Message sent to server: '{output_msg}'")
            input_msg = socket.recv_text_msg(cmd_line_args.read_timeout_sec)
            print(f"Message from server received: '{input_msg}'")
            random_sleep(min_sec=5, max_sec=25)
    except KeyboardInterrupt:
        print("Keyboard interrupt - exit")
    except (TimeoutError, ConnectionRefusedError, ConnectionResetError) as e:
        print(f"{type(e).__name__}: {str(e)}")
    except Exception as e:
        print(f"Exception caught: {str(e)}")
    finally:
        if socket:
            socket.close()


if __name__ == "__main__":
    main()
