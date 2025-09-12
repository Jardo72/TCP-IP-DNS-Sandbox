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
from dataclasses import dataclass
from traceback import print_exc
from typing import (
    Optional,
    Tuple,
)

from pyroute2 import (
    IPRoute,
    netns,
)


@dataclass(frozen=True)
class NetworkNamespace:
    name: str
    description: Optional[str] = None


@dataclass(frozen=True)
class NetworkBridge:
    name: str
    description: Optional[str] = None


@dataclass(frozen=True)
class Configuration:
    bridge: NetworkBridge
    namespaces: Tuple[NetworkNamespace, ...]


def epilog() -> str:
    return """
"""


def create_cmd_line_agrs_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="Network Namespaces Demo",
        formatter_class=RawTextHelpFormatter,
        epilog=epilog()
    )

    parser.add_argument(
        "command",
        choices=["create", "destroy"],
        help="the IP address the server has to bind to (use 0.0.0.0 to bind to all network interfaces)",
    )
    parser.add_argument(
        "config_file",
        help="the name of the file with the configuration to applied or destroyed",
    )

    return parser


def parse_cmd_line_args() -> Namespace:
    parser = create_cmd_line_agrs_parser()
    return parser.parse_args()


def read_config(filename: str) -> Configuration:
    # with open(filename, "r") as config_file:
    #     ...
    return Configuration(
        bridge=NetworkBridge(name="BRIDGE-01"),
        namespaces=(
            NetworkNamespace(name="NS-01"),
            NetworkNamespace(name="NS-02"),
        ),
    )


def create_config(config: Configuration) -> None:
    with IPRoute() as ip_route:
        for namespace in config.namespaces:
            netns.create(namespace.name)
            print(f"Namespace {namespace.name} created...")
        ip_route.link("add", ifname=config.bridge.name, kind="bridge")
        ip_route.link("set", ifname=config.bridge.name, state="up")
        print(f"Bridge {config.bridge.name} created and up...")


def destroy_config(config: Configuration) -> None:
    with IPRoute() as ip_route:
        ip_route.link("set", ifname=config.bridge.name, state="down")
        ip_route.link("delete", ifname=config.bridge.name, kind="bridge")
        print(f"Bridge {config.bridge.name} deleted...")
        for namespace in config.namespaces:
            netns.remove(namespace.name)
            print(f"Namespace {namespace.name} removed...")


def main() -> None:
    cmd_line_args = parse_cmd_line_args()
    try:
        config = read_config(cmd_line_args.config_file)
        if cmd_line_args.command == "create":
            create_config(config)
        else:
            destroy_config(config)
    except:
        print_exc()


if __name__ == "__main__":
    main()
