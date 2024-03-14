from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from threading import Thread, current_thread

from colorama import init as colorama_init
from colorama import Style

from commons import TCPSocket, open_tcp_listener, next_color


class ClientThread(Thread):

    def __init__(self, socket: TCPSocket) -> None:
        super().__init__()
        self._socket = socket
        self._color = next_color()

    def run(self) -> None:
        try:
            while True:
                input_msg = self._socket.recv_text_msg()
                output_msg = f"Response to message '{input_msg}'"
                self._socket.send_text_msg(output_msg)
                print(f"{self._color}{current_thread().name}: {output_msg}{Style.RESET_ALL}")
        except EOFError:
            print(f"{self._color}{current_thread().name}: EOF - client has disconnected{Style.RESET_ALL}")


def create_cmd_line_args_parser() -> ArgumentParser:
    parser = ArgumentParser(description="TCP Server", formatter_class=RawTextHelpFormatter)

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
    return params


def main() -> None:
    colorama_init()
    cmd_line_args = parse_cmd_line_args()
    print(f"TCP server going to bind to {cmd_line_args.address}:{cmd_line_args.port}")

    try:
        listener = open_tcp_listener(cmd_line_args.address, cmd_line_args.port)
        while True:
            connection, (remote_address, remote_port) = listener.accept()
            print(f"Client connection accepted from ({remote_address}:{remote_port})...")
            client_thread = ClientThread(TCPSocket(connection))
            client_thread.start()
    except KeyboardInterrupt:
        print("Keyboard interrupt - exit")


if __name__ == "__main__":
    main()
