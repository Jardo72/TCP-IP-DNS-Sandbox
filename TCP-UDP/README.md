# TCP/UDP Demos

## Intruduction
* application protocol - PDU structure
* source code organization with commons.py module
* 3rd party modules/dependencies
* command line arguments - how to get help


## Status

| Demo                 | File(s)                                                       | Status               |
| -------------------- | ------------------------------------------------------------- | -------------------- |
| TCP Unicast          | tcp_client.py, tcp_server.py                                  | Implemented          |
| TCP Window = 0       | eager_producer_tcp_client.py, hesitant_consumer_tcp_server.py | Implemented          |
| UDP Unicast          | udp_client.py, udp_server.py                                  | Implemented          |
| UDP Broadcast        | broadcast_udp_publisher.py, broadcast_udp_consumer.py         | Implemented          |
| Multicast            | multicast_publisher.py, multicast_subscriber.py               | Implemented          |


## TCP Unicast Communication
Simple demonstration of TCP communication.
Files:
* [tcp_server.py](./tcp_server.py) opens a TCP socket in listening mode and accepts incoming connections. For each connection, a new worker thread is started. The worker reads text messages from its TCP connection and sends answers.
* [tcp_client.py](./tcp_client.py) establishes a TCP connection to the given IP address and TCP port. In addition, it repeatedly sends text messages to the TCP connections, 


## TCP Window Size Zero Indication Demo

Files:
* [hesitant_consumer_tcp_server.py](./hesitant_consumer_tcp_server.py) accepts incoming TCP connections. However, it does not read any data from the TCP connections, so can be used to demonstrate the window size zero indication.
* [eager_producer_tcp_client.py](./eager_producer_tcp_client.py) establishes a TCP connection to the given IP address and TCP port, and it periodically sends some random data over the TCP connection.


## UDP Unicast Communication

Files:
* [udp_server.py](./udp_server.py) opens a UCP post in listening mode.
* [udp_client.py](./udp_client.py)


## UDP Broadcast Communication
Simple demonstration of UDP broadcast communication. Applications:
* [broadcast_udp_publisher.py](./broadcast_udp_publisher.py) repeatedly publishes text messages to the specified broadcast IP address and UDP port.
* [broadcast_udp_consumer.py](./broadcast_udp_consumer.py) repeatedly consumes text messages from the specified IP address and UDP port.


## Multicast Communication
Simple demonstration of UDP multicast communication. Applications:
Files:
* [multicast_publisher.py](./multicast_publisher.py) repeatedly publishes text messages to the specified multicast IP address and UDP port.
* [multicast_subscriber.py](./multicast_subscriber.py) repeatedly consumes text messages from the specified multicast IP address and UDP port.
