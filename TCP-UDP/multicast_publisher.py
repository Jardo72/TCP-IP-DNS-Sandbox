from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from commons import Endpoint, open_multicast_publisher, random_sleep


# see also
# https://stackoverflow.com/questions/603852/how-do-you-udp-multicast-in-python
# https://pythonhint.com/post/9214111898281392/how-do-you-udp-multicast-in-python


def create_cmd_line_args_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Multicast Producer", formatter_class=RawTextHelpFormatter)

    parser.add_argument(
        "address",
        help="the IP address the multicast group the publisher will send messages to"
    )
    parser.add_argument(
        "port",
        help="the UDP port the publisher will send messages to",
        type=int
    )

    return parser


def parse_cmd_line_args() -> Namespace:
    parser = create_cmd_line_args_parser()
    params = parser.parse_args()
    return params


def main() -> None:
    cmd_line_args = parse_cmd_line_args()
    print(f"Multicast publisher is going to publish to {cmd_line_args.address}:{cmd_line_args.port}")
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


if __name__ == "__main__":
    main()
