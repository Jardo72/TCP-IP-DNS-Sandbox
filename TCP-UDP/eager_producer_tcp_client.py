from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from random import randint
from uuid import uuid4

from commons import open_tcp_connection, random_sleep


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


def generate_random_msg(client_name: str, seq_no: int) -> dict[str, any]:
    number_count = randint(1000, 3000)
    uuid_count = randint(1000, 3000)
    return {
        "client_name": client_name,
        "sequence_number": seq_no,
        "random_numbers": [randint(10000000, 20000000) for _ in range(number_count)],
        "uuids": [str(uuid4() for _ in range(uuid_count))]
    }


def main() -> None:
    cmd_line_args = parse_cmd_line_args()
    client_name = cmd_line_args.client_name or str(uuid4())
    print(f"TCP client going to connect to {cmd_line_args.address}:{cmd_line_args.port}")
    socket = open_tcp_connection(cmd_line_args.address, cmd_line_args.port, cmd_line_args.connect_timeout_sec)
    for i in range(1, cmd_line_args.msg_count + 1):
        msg = generate_random_msg(client_name, i)
        msg_length = socket.send_json_msg(msg)
        print(f"Message with sequence number = {i} ({msg_length} bytes) sent to server...")
        random_sleep(min_sec=2, max_sec=5)


if __name__ == "__main__":
    main()
