#
# Copyright 2026 Jaroslav Chmurny
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
    List,
    Optional,
)

from marshmallow_dataclass import class_schema
from pyroute2 import (
    IPRoute,
    NetNS,
    netns,
)
from yaml import safe_load


@dataclass(frozen=True)
class NetworkNamespace:
    name: str
    ip_address: str
    description: Optional[str] = None


@dataclass(frozen=True)
class NetworkBridge:
    name: str
    description: Optional[str] = None


@dataclass(frozen=True)
class Configuration:
    bridge: NetworkBridge
    namespaces: List[NetworkNamespace]


def epilog() -> str:
    return """
Demo application to create and destroy network namespaces and a bridge connecting them
according to the specified configuration.

Example configuration file (YAML format):

bridge:
    name: BRIDGE-01
namespaces:
    - name: NS-01
      ip_address: 10.0.0.1/24
      description: First network namespace
    - name: NS-02
      ip_address: 10.0.0.2/24
      description: Second network namespace
"""


def create_cmd_line_agrs_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="Network Namespaces Demo",
        formatter_class=RawTextHelpFormatter,
        epilog=epilog()
    )

    parser.add_argument(
        "command",
        choices=["apply", "destroy"],
        help="the action to be performed (apply or destroy)",
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
    print(f"Going to read configuration from file {filename}")
    with open(filename, 'r') as config_file:
        data = safe_load(config_file)
    schema = class_schema(Configuration)()
    return schema.load(data)


def configure_namespace_veth(namespace: NetworkNamespace) -> None:
    ns_veth = f"{namespace.name}-ns-veth"
    ip_addr, prefix_len = namespace.ip_address.split('/')
    with NetNS(namespace.name) as ns:
        # bring up loopback
        lo_idx = ns.link_lookup(ifname="lo")[0]
        ns.link("set", index=lo_idx, state="up")
        print(f"Loopback brought up in namespace {namespace.name}")

        # assign IP and bring up the veth inside the namespace
        ns_veth_idx = ns.link_lookup(ifname=ns_veth)[0]
        ns.addr("add", index=ns_veth_idx, address=ip_addr, prefixlen=int(prefix_len))
        ns.link("set", index=ns_veth_idx, state="up")
        print(f"Interface {ns_veth} configured with {namespace.ip_address} and brought up")


def create_namespace(ip_route: IPRoute, bridge_name: str, namespace: NetworkNamespace) -> None:
    # create network namespace
    netns.create(namespace.name)
    print(f"Namespace {namespace.name} created...")

    # create veth pair: root-veth <-> ns-veth
    root_veth = f"{namespace.name}-root-veth"
    ns_veth = f"{namespace.name}-ns-veth"
    ip_route.link("add", ifname=root_veth, kind="veth", peer=ns_veth)
    print(f"Veth pair created: {root_veth} <-> {ns_veth}")

    # move namespace veth to the namespace
    ns_veth_idx = ip_route.link_lookup(ifname=ns_veth)[0]
    ip_route.link("set", index=ns_veth_idx, net_ns_fd=namespace.name)
    print(f"Veth {ns_veth} moved to namespace {namespace.name}")

    # attach the root veth to bridge and bring it up
    bridge_idx = ip_route.link_lookup(ifname=bridge_name)[0]
    root_veth_idx = ip_route.link_lookup(ifname=root_veth)[0]
    ip_route.link("set", index=root_veth_idx, master=bridge_idx)
    ip_route.link("set", index=root_veth_idx, state="up")
    print(f"Veth {root_veth} attached to bridge {bridge_name} and brought up")

    # configure IP and bring up the veth inside the namespace
    configure_namespace_veth(namespace)


def apply_config(config: Configuration) -> None:
    with IPRoute() as ip_route:
        # create bridge first
        ip_route.link("add", ifname=config.bridge.name, kind="bridge")
        bridge_idx = ip_route.link_lookup(ifname=config.bridge.name)[0]
        ip_route.link("set", index=bridge_idx, state="up")
        print(f"Bridge {config.bridge.name} created and up...")
        
        for namespace in config.namespaces:
            create_namespace(ip_route, config.bridge.name, namespace)


def destroy_config(config: Configuration) -> None:
    with IPRoute() as ip_route:
        # remove namespaces first — deleting ns-veth also auto-deletes its root-veth peer
        for namespace in config.namespaces:
            netns.remove(namespace.name)
            print(f"Namespace {namespace.name} removed...")

        # then delete the bridge
        bridge_idx = ip_route.link_lookup(ifname=config.bridge.name)[0]
        ip_route.link("set", index=bridge_idx, state="down")
        ip_route.link("delete", index=bridge_idx)
        print(f"Bridge {config.bridge.name} deleted...")


def main() -> None:
    cmd_line_args = parse_cmd_line_args()
    try:
        config = read_config(cmd_line_args.config_file)
        if cmd_line_args.command == "apply":
            apply_config(config)
        else:
            destroy_config(config)
    except:
        print_exc()


if __name__ == "__main__":
    main()
