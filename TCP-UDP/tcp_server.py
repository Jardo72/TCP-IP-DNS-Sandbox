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
from itertools import count
from os import getpid
from threading import Thread, current_thread

from colorama import init as colorama_init
from colorama import Style

from commons import TCPSocket, open_tcp_listener, next_color


class ClientThread(Thread):

    seq = count(1)

    def __init__(self, socket: TCPSocket) -> None:
        super().__init__(name=f"Worker-{next(self.seq)}")
        self._socket = socket
        self._color = next_color()

    def run(self) -> None:
        try:
            while True:
                input_msg = self._socket.recv_text_msg()
                output_msg = f"Response to message: {input_msg}"
                self._socket.send_text_msg(output_msg)
                print(f"{self._color}{current_thread().name}: {output_msg}{Style.RESET_ALL}")
        except EOFError:
            print(f"{self._color}{current_thread().name}: EOF - client has disconnected{Style.RESET_ALL}")
        except Exception as e:
            print(f"{self._color}{current_thread().name}: Unexpected error: {str(e)}{Style.RESET_ALL}")
        finally:
            self._socket.close()


def create_cmd_line_args_parser() -> ArgumentParser:
    parser = ArgumentParser(description="TCP Server", formatter_class=RawTextHelpFormatter)

    parser.add_argument(
        "address",
        help="the IP address the server has to bind to (use 0.0.0.0 to bind to all network interfaces)"
    )
    parser.add_argument(
        "port",
        help="the TCP port the server has to bind to (between 1024 and 65535)",
        type=int
    )
    parser.add_argument(
        "-r", "--reuse-port",
        dest="reuse_port",
        default=False,
        action="store_true",
        help="if specified, the SO_REUSEPORT socket option will be set on the server socket"
    )

    return parser


def parse_cmd_line_args() -> Namespace:
    parser = create_cmd_line_args_parser()
    params = parser.parse_args()
    if not (1024 <= params.port <= 65535):
        parser.error("Port must be between 1024 and 65535.")
    return params


def main() -> None:
    colorama_init()
    cmd_line_args = parse_cmd_line_args()
    print(f"TCP server (PID = {getpid()}) going to bind to {cmd_line_args.address}:{cmd_line_args.port}")
    listener = None

    try:
        listener = open_tcp_listener(cmd_line_args.address, cmd_line_args.port, cmd_line_args.reuse_port)
        while True:
            connection, (remote_address, remote_port) = listener.accept()
            print(f"Client connection accepted from ({remote_address}:{remote_port})...")
            client_thread = ClientThread(TCPSocket(connection))
            client_thread.start()
    except KeyboardInterrupt:
        print("Keyboard interrupt - exit")
    except Exception as e:
        print(f"Exception caught: {str(e)}")
    finally:
        if listener:
            listener.close()


if __name__ == "__main__":
    main()
