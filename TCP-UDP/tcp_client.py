from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from uuid import uuid4

from commons import open_tcp_connection, random_sleep


def create_cmd_line_args_parser() -> ArgumentParser:
    parser = ArgumentParser(description="TCP Server", formatter_class=RawTextHelpFormatter)

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
        type=int
    )

    return parser


def parse_cmd_line_args() -> Namespace:
    parser = create_cmd_line_args_parser()
    params = parser.parse_args()
    return params


def main() -> None:
    cmd_line_args = parse_cmd_line_args()
    client_name = cmd_line_args.client_name or str(uuid4())
    print(f"TCP client going to connect to {cmd_line_args.address}:{cmd_line_args.port}")
    socket = open_tcp_connection(cmd_line_args.address, cmd_line_args.port, cmd_line_args.connect_timeout_sec)
    for i in range(1, cmd_line_args.msg_count + 1):
        output_msg = f"Message #{i} from client {client_name}"
        socket.send_text_msg(output_msg)
        print(f"Message sent to server: '{output_msg}'")
        input_msg = socket.recv_text_msg()
        print(f"Message from server received: '{input_msg}'")
        random_sleep(min_sec=5, max_sec=25)


if __name__ == "__main__":
    main()
