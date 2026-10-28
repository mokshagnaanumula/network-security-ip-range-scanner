# Network Security IP Range Scanner

A conservative IPv4 CIDR host-discovery tool for your own lab or an authorized network.

## Problem and objective

Defenders need a basic view of which lab addresses respond to a discovery probe. This prototype validates a small network range, probes each address with the platform `ping` utility, and reports active or no response.

## Features

- Strict IPv4 CIDR input and host-count cap.
- Configurable timeout, bounded concurrency, progress-safe output, and error handling.
- No port scanning or exploitation.

## Technology

Python 3.10+ standard library; uses the system `ping` command.

## Setup and run

```bash
python scanner.py 192.168.1.0/28 --timeout 1
```

Only run inside your own lab or with explicit authorization. The default cap is 256 addresses.

## How it works

The program expands the CIDR into host addresses (including IPv4 network/broadcast where the prefix is /31 or /32 according to Python's host iterator), invokes one bounded ping process per address, and labels a successful reply active. No reply is marked no response, which does not prove a host is offline because ICMP may be filtered.

## Screenshots and demo

No screenshots or public demo are included. Capture a run against a small private lab subnet.

## Tests

Run `python -m unittest discover -s tests -v` from this repository root.

## Security considerations

Keep scans within authorized address space. Probe traffic may be logged. ICMP filtering, routing, and host firewalls produce false negatives. Large ranges are rejected to reduce accidental load.

## Future improvements

Add IPv6, ARP discovery for local Ethernet, JSON export, and explicit allowlist confirmation.
