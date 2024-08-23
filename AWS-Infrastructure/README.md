# AWS Infrastructure
Terraform configuration allowing to provision AWS infrastructure that can be used to run the [TCP/IP demo applications](../TCP-UDP). The overall setup is depicted by the following diagram:
![application-diagram](./diagram.png)

The EC2 instances automatically download the Python code from this Git repositary upon the start. The entire repo is downloaded to the `/opt/tcp-ip-sandbox` directory. As AWS does not support broadcast and multicast communication, UDP broadcast and UDP multicast applications will not work. However, the other applications work properly. The EC2 instance marked as server in the diagram is supposed to run the server applications. The EC2 instances marked as client in the diagram are supposed to run the client applications.

Network troubleshooting tools like netstat and tcpdump are installed on all EC2 instances. In addition, all EC2 instances have access to the S3 bucket. Therefore, network captures created with tcpdump can be uploaded to the S3 bucket, so you can download the capture files to your localhost and analyze them with Wireshark.
