# DNS Server

A lightweight DNS server implemented in Python using UDP sockets. The server handles DNS binary packet parsing, generates RFC 1035 compliant responses, supports domain name compression via pointer offsets, forwards queries to an upstream DNS resolver, and handles client requests concurrently using multithreading.

## Features

- **UDP Server**: Listens for incoming DNS requests over UDP on port 2053.
- **Header Parsing & Generation**: Decodes 12-byte DNS headers, bitwise flag handling (QR, OPCODE, AA, TC, RD, RA, Z, RCODE), and generates RFC 1035 compliant response headers.
- **Question Section Parsing**: Parses question records, domain name labels, QTYPE, and QCLASS.
- **DNS Compression & Decompression**: Supports compressed domain name labels using 2-byte pointer offsets (`0xC000`).
- **Upstream Forwarding & Resolution**: Resolves records by querying a configurable upstream DNS resolver (e.g. `--resolver <ip>:<port>`), adjusts compression pointers in upstream answers, and relays answers back to clients.
- **Concurrent Processing**: Multi-threaded request processing using Python's `threading` module.

## Getting Started

### Prerequisites

- Python 3.10+ (or [uv](https://github.com/astral-sh/uv))

### Running the Server

Run the server using `uv`:

```sh
uv run -m app.main
```

Or pass an upstream resolver:

```sh
uv run -m app.main --resolver 8.8.8.8:53
```

You can test queries using `dig`:

```sh
dig @127.0.0.1 -p 2053 google.com
```

## Project Structure

```text
├── app/
│   ├── main.py            # DNS server implementation
│   └── dns_forwarder.py   # DNS forwarding and resolution utility
├── notes/
│   ├── dns server.md      # DNS protocol and packet format notes
│   ├── dns.md             # Additional DNS architecture notes
│   └── udp socket programming.md # UDP socket programming concepts
├── pyproject.toml
└── README.md
```
