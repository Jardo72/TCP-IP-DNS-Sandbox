from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from commons import TCPSocket, open_tcp_listener


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
    return params


def main() -> None:
    cmd_line_args = parse_cmd_line_args()
    print(f"TCP server going to bind to {cmd_line_args.address}:{cmd_line_args.port}")
    try:
        listener = open_tcp_listener(cmd_line_args.address, cmd_line_args.port)
        connection, (remote_address, remote_port) = listener.accept()
        client_socket = TCPSocket(connection)
        rcv_buf_size = client_socket.get_rcv_buff_size()
        print(f"Client connection accepted from ({remote_address}:{remote_port}), input buffer size = {rcv_buf_size} bytes...")
        input("Press enter to start reading the data")
        while True:
            client_socket.recv_json_msg()
    except KeyboardInterrupt:
        print("Keyboard interrupt - exit")


if __name__ == "__main__":
    main()
