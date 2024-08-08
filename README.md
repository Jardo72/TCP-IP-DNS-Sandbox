# TCP/IP & DNS Sandbox

## Introduction
Set of demo/experimental applications for demonstration of TCP/IP and DNS implemented in Python. The project involves several subfolders which are briefly described in a subsequent section of this document. Each subdirectory has its own requirements.txt file defining the dependencies (PyPI modules) required by the application(s) present in the subdirectory. Each subdirectory has also its own README.md file, which provides more details about the application(s) present in the subdirectory.

## Demo Applications
| Subdirectory         | Description                                                              |
| -------------------- | ------------------------------------------------------------------------ |
| [TCP-UDP](./TCP-UDP) | Demonstration of TCP and UDP communication (incl. broadcast & multicast) |
| [DNS](./DNS)         | Demonstration of DNS queries based on the dnspython module               |

## AWS Infrastructure
The [AWS-Infrastructure](./AWS-Infrastructure) subdirectory contains a Terraform configuration that can be used to provision an AWS infrastructure suitable for the demonstration of the [TCP-UDP](./TCP-UDP) demo applications.

## Cheat Sheets
| Tool        | Cheat Sheet    |
| ----------- | -------------- |
| nc          |                |
| netstat     |                |
| ss          |                |
| tcpdump     |                |


See also:
* [Markdown to PDF](https://www.pdfforge.org/online/en/markdown-to-pdf)
* [Comparison Between ss vs netstat Commands](https://tecadmin.net/comparison-between-ss-vs-netstat-commands/)
