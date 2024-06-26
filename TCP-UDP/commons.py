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

from dataclasses import dataclass
from enum import IntEnum, unique
from itertools import cycle
from json import dumps, loads
from random import random
from socket import (
    create_connection,
    create_server,
    inet_aton,
    socket,
    AF_INET,
    INADDR_ANY,
    IPPROTO_IP,
    IPPROTO_UDP,
    IP_ADD_MEMBERSHIP,
    IP_MULTICAST_TTL,
    SOCK_DGRAM,
    SOL_SOCKET,
    SO_RCVBUF,
    SO_REUSEADDR,
    SO_SNDBUF,
)
from struct import calcsize, pack, unpack
from time import sleep

from colorama import Fore


_ENCODING      = "utf-8"
_HEADER_FORMAT = ">HH"
_HEADER_SIZE   = calcsize(_HEADER_FORMAT)


_COLORS = cycle([
    Fore.RED,
    Fore.GREEN,
    Fore.BLUE,
    Fore.YELLOW,
    Fore.MAGENTA,
    Fore.CYAN,
    Fore.LIGHTRED_EX,
    Fore.LIGHTGREEN_EX,
    Fore.LIGHTBLUE_EX,
    Fore.LIGHTMAGENTA_EX,
])


@unique
class MessageType(IntEnum):
    TEXT = 1
    JSON = 2


@dataclass(frozen=True)
class Endpoint:
    address: str
    port: int


class TCPSocket:

    def __init__(self, socket: socket) -> None:
        self._socket = socket

    def get_snd_buff_size(self) -> int:
        return self._socket.getsockopt(SOL_SOCKET, SO_SNDBUF)

    def get_rcv_buff_size(self) -> int:
        return self._socket.getsockopt(SOL_SOCKET, SO_RCVBUF)

    def send_text_msg(self, msg: str) -> int:
        payload = bytes(msg, _ENCODING)
        return self._send_msg(MessageType.TEXT, payload)

    def send_json_msg(self, msg: dict[str, any]) -> int:
        payload = bytes(dumps(msg), _ENCODING)
        return self._send_msg(MessageType.JSON, payload)

    def _send_msg(self, msg_type: MessageType, payload: bytes) -> int:
        header = pack(_HEADER_FORMAT, len(payload), msg_type)
        self._socket.sendall(header)
        self._socket.sendall(payload)
        return len(header) + len(payload)

    def recv_text_msg(self) -> str | None:
        length, msg_type = self._recv_header()
        if msg_type != MessageType.TEXT:
            raise ValueError(f"Unexpected message type: {msg_type}.")
        payload = self._socket.recv(length)
        return payload.decode(_ENCODING)

    def recv_json_msg(self) -> dict[str, any]:
        length, msg_type = self._recv_header()
        if msg_type != MessageType.JSON:
            raise ValueError(f"Unexpected message type: {msg_type}.")
        payload = self._socket.recv(length)
        return loads(payload.decode(_ENCODING))

    def _recv_header(self) -> tuple[int, int]:
        header_as_bytes = self._socket.recv(_HEADER_SIZE)
        if not header_as_bytes:
            raise EOFError("EOF encountered when attempting to read from the socket.")
        return unpack(_HEADER_FORMAT, header_as_bytes)

    def close(self) -> None:
        self._socket.close()


class UDPSocket:

    def __init__(self, socket: socket, msg_size: int) -> None:
        self._socket = socket
        self._msg_size = msg_size

    def send_text_msg(self, dst: Endpoint, msg: str) -> None:
        payload = bytes(dumps(msg), _ENCODING)
        self._send_msg(dst, MessageType.TEXT, payload)

    def send_json_msg(self, dst: Endpoint, msg: dict[str, any]) -> None:
        payload = bytes(dumps(msg), _ENCODING)
        self._send_msg(dst, MessageType.JSON, payload)

    def _send_msg(self, dst: Endpoint, msg_type: MessageType, payload: bytes) -> None:
        header = pack(_HEADER_FORMAT, len(payload), msg_type)
        buffer = header + payload
        padding_length = self._msg_size - len(buffer)
        buffer += padding_length * b'\0'
        self._socket.sendto(buffer, (dst.address, dst.port))

    def recv_text_msg(self) -> tuple[Endpoint, str]:
        datagram, (address, port) = self._socket.recvfrom(self._msg_size)
        msg_length, msg_type = unpack(_HEADER_FORMAT, datagram[0 : _HEADER_SIZE])
        if msg_type != MessageType.TEXT:
            raise ValueError(f"Unexpected message type: {msg_type}.")
        payload = datagram[_HEADER_SIZE:_HEADER_SIZE + msg_length]
        return (
            Endpoint(address=address, port=port),
            payload.decode(_ENCODING)
        )

    def recv_json_msg(self) -> tuple[Endpoint, dict[str, any]]:
        datagram, (address, port) = self._socket.recvfrom(self._msg_size)
        msg_length, msg_type = unpack(_HEADER_FORMAT, datagram[0:_HEADER_SIZE])
        if msg_type != MessageType.JSON:
            raise ValueError(f"Unexpected message type: {msg_type}.")
        payload = datagram[_HEADER_SIZE:_HEADER_SIZE + msg_length]
        return (
            Endpoint(address=address, port=port),
            loads(payload.decode(_ENCODING))
        )

    def close(self) -> None:
        self._socket.close()


def open_tcp_listener(address: str, port: int) -> socket:
    return create_server((address, port), family=AF_INET)


def open_tcp_connection(address: str, port: int, timeout_sec: int) -> TCPSocket:
    connection = create_connection((address, port), timeout=timeout_sec)
    return TCPSocket(connection)


def open_udp_listener(address: str, port: int, msg_size: int = 4096) -> UDPSocket:
    listener = socket(AF_INET, SOCK_DGRAM)
    listener.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    listener.bind((address, port))
    return UDPSocket(listener, msg_size)


def open_udp_client(msg_size: int = 4096) -> UDPSocket:
    return UDPSocket(socket(AF_INET, SOCK_DGRAM), msg_size)


def open_multicast_publisher(msg_size: int) -> UDPSocket:
    publisher = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    publisher.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, 2)
    return UDPSocket(publisher, msg_size)


def open_multicast_subscriber(address: str, port: int, msg_size: int = 4096) -> UDPSocket:
    subscriber = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    subscriber.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    subscriber.bind(("", port))

    membership_request = pack('4sL', inet_aton(address), INADDR_ANY)
    subscriber.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, membership_request)

    return UDPSocket(subscriber, msg_size)


def random_sleep(min_sec: int, max_sec:int) -> float:
    duration_sec = min_sec + random() * (max_sec - min_sec)
    sleep(duration_sec)


def next_color() -> str:
    return next(_COLORS)
