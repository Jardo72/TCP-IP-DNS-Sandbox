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
from random import randint
from socket import timeout
from uuid import uuid4
from typing import (
    Any,
    Dict,
)

from commons import (
    open_tcp_connection,
    random_sleep,
)


def create_cmd_line_args_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Eager Producer TCP Client", formatter_class=RawTextHelpFormatter)

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
        type=int
    )
    parser.add_argument(
        "-w", "--write-timeout-sec",
        dest="write_timeout_sec",
        default=10,
        help="optional write timeout in seconds (default = 10 sec)",
        type=float,
    )
    parser.add_argument(
        "-c", "--msg-count",
        dest="msg_count",
        default=50,
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


def generate_random_msg(client_name: str, seq_no: int) -> Dict[str, Any]:
    number_count = randint(400, 800)
    uuid_count = randint(400, 800)
    return {
        "client_name": client_name,
        "sequence_number": seq_no,
        "random_numbers": [randint(10000000, 20000000) for _ in range(number_count)],
        "uuids": [str(uuid4() for _ in range(uuid_count))]
    }


def main() -> None:
    cmd_line_args = parse_cmd_line_args()
    client_name = cmd_line_args.client_name or str(uuid4())
    print(f"TCP client (PID = {getpid()}) going to connect to {cmd_line_args.address}:{cmd_line_args.port}")
    print(f"Message count = {cmd_line_args.msg_count}")
    print(f"Connect timeout = {cmd_line_args.connect_timeout_sec} sec")
    if cmd_line_args.write_timeout_sec:
        print(f"Write timeout = {cmd_line_args.write_timeout_sec} sec")
    else:
        print("No write timeout configured")
    socket = None
    try:
        socket = open_tcp_connection(cmd_line_args.address, cmd_line_args.port, cmd_line_args.connect_timeout_sec)
        snd_buff_size = socket.get_snd_buff_size()
        print(f"Connection established, output buffer = {snd_buff_size} bytes")
        cumulative_byte_count = 0
        for i in range(1, cmd_line_args.msg_count + 1):
            msg = generate_random_msg(client_name, i)
            msg_length = socket.send_json_msg(msg, timeout_sec=cmd_line_args.write_timeout_sec)
            cumulative_byte_count += msg_length
            print(f"Message with sequence number = {i} ({msg_length} bytes, totally {cumulative_byte_count} bytes) sent to server...")
            random_sleep(min_sec=2, max_sec=5)
    except KeyboardInterrupt:
        print("Keyboard interrupt - exit")
    except (timeout, TimeoutError, ConnectionRefusedError, ConnectionResetError) as e:
        print(f"{type(e).__name__}: {str(e)}")
    except Exception as e:
        print(f"Exception caught: {str(e)}")
    finally:
        if socket:
            socket.close()


if __name__ == "__main__":
    main()
