#!/usr/bin/env python3
"""Small, rate-bounded IPv4 ICMP discovery for authorized labs."""
import argparse
import concurrent.futures
import ipaddress
import platform
import subprocess


def probe(address, timeout):
    if platform.system().lower().startswith("win"):
        command = ["ping", "-n", "1", "-w", str(int(timeout * 1000)), str(address)]
    else:
        command = ["ping", "-c", "1", "-W", str(max(1, int(timeout))), str(address)]
    try:
        result = subprocess.run(command, capture_output=True, timeout=timeout + 2, check=False)
        return str(address), "active" if result.returncode == 0 else "no response"
    except (OSError, subprocess.TimeoutExpired):
        return str(address), "no response"


def parse_network(value):
    network = ipaddress.ip_network(value, strict=False)
    if network.version != 4:
        raise ValueError("Only IPv4 CIDR ranges are supported.")
    if network.num_addresses > 256:
        raise ValueError("Range exceeds the 256-address safety limit.")
    return network


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("network", help="IPv4 CIDR, e.g. 192.168.1.0/28")
    parser.add_argument("--timeout", type=float, default=1.0)
    args = parser.parse_args()
    try:
        network = parse_network(args.network)
        if args.timeout < .2 or args.timeout > 5:
            raise ValueError("Timeout must be between 0.2 and 5 seconds.")
        addresses = list(network.hosts())
        print(f"Authorized discovery of {network}: {len(addresses)} host addresses")
        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
            results = list(pool.map(lambda ip: probe(ip, args.timeout), addresses))
        for address, state in results:
            print(f"{address:>15}  {state}")
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
