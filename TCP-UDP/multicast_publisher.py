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
from ipaddress import (
    IPv4Address,
    AddressValueError,
)
from os import getpid

from commons import (
    Endpoint,
    open_multicast_publisher,
    random_sleep,
)


# see also
# https://stackoverflow.com/questions/603852/how-do-you-udp-multicast-in-python
# https://pythonhint.com/post/9214111898281392/how-do-you-udp-multicast-in-python


def epilog() -> str:
    return "Multicast IP addresses are from the range 224.0.0.0 ... 239.255.255.255"


def create_cmd_line_args_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Multicast Producer", formatter_class=RawTextHelpFormatter, epilog=epilog())

    parser.add_argument(
        "address",
        help="the IP address the multicast group the publisher will send messages to (e.g. 224.0.1.1)"
    )
    parser.add_argument(
        "port",
        help="the UDP port the publisher will send messages to",
        type=int
    )

    return parser


def is_multicast_address(address: str) -> bool:
    try:
        ip_address = IPv4Address(address)
        return ip_address.is_multicast
    except AddressValueError:
        return False


def parse_cmd_line_args() -> Namespace:
    parser = create_cmd_line_args_parser()
    params = parser.parse_args()
    if not is_multicast_address(params.address):
        message = f"The specified IP address '{params.address}' is not a valid IPv4 multicast address."
        parser.error(message)
    return params


def main() -> None:
    cmd_line_args = parse_cmd_line_args()
    print(f"Multicast publisher (PID = {getpid()}) is going to publish to {cmd_line_args.address}:{cmd_line_args.port}")
    publisher = None
    try:
        destination = Endpoint(cmd_line_args.address, cmd_line_args.port)
        publisher = open_multicast_publisher(4096)
        i = 1
        while True:
            output_msg = f"Multicast message #{i}"
            publisher.send_text_msg(destination, output_msg)
            print(f"Message sent to subscribers: '{output_msg}'")
            random_sleep(min_sec=5, max_sec=25)
            i += 1
    except KeyboardInterrupt:
        print("Keyboard interrupt - exit")
    except Exception as e:
        print(f"Exception caught: {str(e)}")
    finally:
        if publisher:
            publisher.close()


if __name__ == "__main__":
    main()
