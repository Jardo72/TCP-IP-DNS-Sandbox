from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from colorama import init as colorama_init
from colorama import Style

from commons import Endpoint, next_color, open_udp_listener


class ColorRegistry:

    def __init__(self) -> None:
        self._entries = {}

    def get(self, client: Endpoint) -> str:
        if client not in self._entries:
            self._entries[client] = next_color()
        return self._entries[client]


def create_cmd_line_args_parser() -> ArgumentParser:
    parser = ArgumentParser(description="UDP Server", formatter_class=RawTextHelpFormatter)

    parser.add_argument(
        "address",
        help="the IP address the server has to bind to (use 0.0.0.0 to bind to all network interfaces)"
    )
    parser.add_argument(
        "port",
        help="the UDP port the server has to bind to",
        type=int
    )

    return parser


def parse_cmd_line_args() -> Namespace:
    parser = create_cmd_line_args_parser()
    params = parser.parse_args()
    return params


def main() -> None:
    colorama_init()
    cmd_line_args = parse_cmd_line_args()
    print(f"UDP server going to bind to {cmd_line_args.address}:{cmd_line_args.port}")
    
    try:
        udp_listener = open_udp_listener(cmd_line_args.address, cmd_line_args.port)
        color_registry = ColorRegistry()
        while True:
            endpoint, input_msg = udp_listener.recv_text_msg()
            color = color_registry.get(endpoint)
            output_msg = f"Response to message '{input_msg}'"
            udp_listener.send_text_msg(endpoint, output_msg)
            print(f"{color}{output_msg} send to {endpoint.address}:{endpoint.port}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print("Keyboard interrupt - exit")


if __name__ == "__main__":
    main()
