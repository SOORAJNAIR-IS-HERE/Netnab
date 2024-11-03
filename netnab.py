#!/usr/bin/env python3

import socket
import threading
from queue import Queue
from datetime import datetime
import argparse
import os
import json
import pyfiglet
import time
from colorama import Fore, Style, init
import logging
import struct

# Initialize colorama and logging
init(autoreset=True)
logging.basicConfig(filename='netnab.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# ThreadLock to print from threads safely
thread_lock = threading.Lock()

# Queue for storing port numbers to be scanned
port_queue = Queue()

# ANSI escape codes for formatting
BOLD = "\033[1m"
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
WHITE = "\033[97m"

# List to hold scan results
scan_results = []

def print_banner():
    banner = pyfiglet.figlet_format("Netnab")
    version = "v1.0.0"
    banner_lines = banner.splitlines()
    version_padding = max(len(line) for line in banner_lines) - len(version)
    print(f"{CYAN}{' ' * version_padding}{version}{RESET}")
    print(f"{WHITE}{banner}{Style.RESET_ALL}")

known_services = {
    1: "tcpmux",
    2: "compressnet - Management Utility",
    3: "compressnet - Compression Process",
    5: "rje - Remote Job Entry",
    7: "echo -",
    9: "discard",
    11: "systat",
    13: "daytime",
    17: "qotd",
    18: "msp",
    19: "chargen",
    20: "ftp-data",
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    37: "time",
    39: "rlp",
    42: "nameserver",
    43: "whois",
    49: "tacacs",
    53: "domain",
    67: "bootps",
    68: "bootpc",
    69: "tftp",
    70: "gopher",
    79: "finger",
    80: "http",
    88: "kerberos",
    101: "hostname - NIC",
    102: "iso-tsap",
    107: "rtelnet",
    109: "pop2 v2",
    110: "pop3 v3",
    111: "sunrpc",
    113: "auth",
    115: "sftp",
    117: "uucp-path",
    119: "nntp",
    123: "ntp",
    135: "EPMAP",
    137: "netbios-ns",
    138: "netbios-dgm",
    139: "netbios-ssn",
    143: "imap",
    161: "snmp",
    162: "snmptrap",
    177: "xdmcp",
    179: "bgp",
    194: "irc",
    201: "appleqtc",
    264: "BGMP",
    318: "TSP",
    381: "HP Openview - HP performance data collector",
    389: "HP Openview - HP data alarm manager",
    411: "Multiple uses - Direct Connect Hub, Remote MT Protocol",
    412: "Multiple uses - Direct Connect Client-to-Client, Trap Convention Port",
    427: "SLP",
    443: "https",
    445: "microsoft-ds",
    464: "Kerberos",
    465: "smtps",
    497: "Dantz Retrospect",
    500: "isakmp",
    512: "rexec",
    513: "rlogin",
    514: "syslog",
    515: "printer",
    520: "rip",
    521: "RIPng (IPv6)",
    540: "UUCP",
    546: "DHCPv6",
    547: "DHCPv6",
    560: "rmonitor",
    563: "NNTP over TLS/SSL",
    548: "AFP",
    554: "RTSP",
    587: "smtp",
    591: "FileMaker",
    593: "Microsoft DCOM",
    596: "SMSD",
    631: "ipp",
    639: "MSDP",
    646: "LDP (MPLS)",
    691: "Microsoft Exchange Routing",
    636: "ldaps",
    860: "iSCSI",
    873: "rsync",
    902: "VMware Server",
    912: "NFS",
    989: "FTPS - (data) over TLS/SSL",
    990: "FTPS - (control) over TLS/SSL",
    993: "imaps",
    995: "pop3s",
    1194: "openvpn",
    1080: "socks",
    1433: "ms-sql-s",
    1434: "ms-sql-m",
    1521: "oracle-db",
    1723: "pptp",
    1812: "radius",
    1813: "radius accounting",
    1883: "mqtt",
    2049: "nfs",
    2082: "cPanel (default)",
    2083: "cPanel (secure)",
    2095: "webmail (default)",
    2096: "webmail (secure)",
    2222: "directadmin",
    3306: "mysql",
    3389: "ms-wbt-server",
    3690: "svn",
    4444: "metasploit",
    4662: "edonkey",
    5432: "postgresql",
    5500: "VNC (default)",
    5631: "pcanywhere",
    5900: "vnc",
    6379: "redis",
    6665: "irc",
    6666: "irc",
    6667: "irc",
    6668: "irc",
    6669: "irc",
    6881: "bittorrent",
    6882: "bittorrent",
    6883: "bittorrent",
    6884: "bittorrent",
    6885: "bittorrent",
    6886: "bittorrent",
    6887: "bittorrent",
    6888: "bittorrent",
    6889: "bittorrent",
    8080: "http-proxy - HTTP Proxy",
}

thread_lock = threading.Lock()
scan_results = []

def grab_banner(ip, port):
    """Attempt to grab the service banner from the specified IP and port."""
    banner = None

    try:
        with socket.create_connection((ip, port), timeout=2) as sock:
            # Specific request based on known service
            if port == 80 or port == 443:  # HTTP/HTTPS
                sock.sendall(b"HEAD / HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n".format(ip).encode())
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            elif port == 135:  # EPMAP (this is an example; RPC requires specific handling)
                # Custom RPC request would go here
                sock.sendall(b"YOUR_RPC_REQUEST_HERE")  # Placeholder
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            elif port == 139:  # netbios-ssn
                # Simple connection attempt (might need more for SMB)
                sock.sendall(b"\x00\x00\x00\x00")  # Placeholder for a SMB request
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            else:
                # Generic connection for other services
                sock.sendall(b"HELLO")  # Placeholder for a generic request
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()

            if not banner:
                banner = "No banner retrieved"
    except socket.timeout:
        banner = "Timeout retrieving banner"
    except Exception as e:
        banner = f"Error retrieving banner: {str(e)}"

    return banner

# Function to scan a port
def scan_port(ip, port, timeout, protocol, service_version=False):
    try:
        if protocol == "tcp":
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif protocol == "udp":
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))

        if protocol == "tcp":
            result = sock.connect_ex((ip, port))
            is_open = (result == 0)
        elif protocol == "udp":
            sock.sendto(b"", (ip, port))
            is_open = True

        sock.close()
    except (socket.gaierror, socket.timeout):
        is_open = False

    if is_open:
        service = known_services.get(port, "Unknown")
        banner = None

        # Attempt to grab the banner if service_version is enabled
        if service_version:
            try:
                with socket.create_connection((ip, port), timeout) as sock:
                    if service in ["http", "https"]:
                       sock.sendall(b"HEAD / HTTP/1.1\r\nHost: {}\r\n\r\n".format(ip).encode())
                    else:
                        sock.sendall(b"\r\n")  # Send a generic request to other services
                    banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            except Exception as e:
                banner = f"Error retrieving banner: {str(e)}"

        # Only acquire the lock when updating shared resources
        with thread_lock:
            print(f"[+] {WHITE}Port {BOLD}{port}{RESET} {protocol.upper()} OPEN ({GREEN}{service}{RESET})")
            if banner:
                print(f"{WHITE}Service Version Banner:")
                for line in banner.splitlines():
                    print(f"- {line}")

        with thread_lock:
            scan_results.append({
                "port": port,
                "protocol": protocol,
                "status": "OPEN",
                "service": service,
                "banner": banner if service_version else None
            })
    else:
        with thread_lock:
            scan_results.append({
                "port": port,
                "protocol": protocol,
                "status": "CLOSED"
            })

# Thread worker function
# Thread worker function
def worker(ip, timeout, protocol, service_version, total_ports):
    while not port_queue.empty():
        port = port_queue.get()
        scan_port(ip, port, timeout, protocol, service_version) 

# Host Discovery via Ping
def is_host_up(ip):
    response = os.system(f"ping -c 1 -W 1 {ip} > /dev/null 2>&1")
    return response == 0

# Main function to scan ports
def scan_ports(ip, start_port, end_port, num_threads=5, timeout=1, protocol="tcp", service_version=False, output_format="json"):
    print_banner()
    print(f"{WHITE}Starting Netnab 1.0.0SVN at {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}")
    logging.info(f"Starting scan on {ip} on ports {start_port}-{end_port} with {num_threads} threads.")
    time.sleep(0.60)
    print(f"{WHITE}Target: {BOLD}{WHITE}{ip}{RESET}")
    time.sleep(0.30)
    print(f"{WHITE}Protocol: {BOLD}{WHITE}TCP | UDP{RESET}")
    time.sleep(0.40)
    print(f"{WHITE}Threads: {BOLD}{WHITE}{num_threads}{RESET}")
    time.sleep(0.45)
    print(f"{BOLD}{RESET}")

    if not is_host_up(ip):
        print(f"{RED}Host {ip} is down or unresponsive.{RESET}")
        return

    # Populate the port queue
    total_ports = end_port - start_port + 1
    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    # Create and start threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(ip, timeout, protocol, service_version, total_ports))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Output scan results
    tcp_results = [result for result in scan_results if result["protocol"] == "tcp"]
    udp_results = [result for result in scan_results if result["protocol"] == "udp"]
    
    print()

    print(f"{BOLD}{WHITE}Scan completed.{RESET}")
    print(f"{WHITE}Total scanned ports: {BOLD}{total_ports}{RESET}")
    print(f"{WHITE}Open TCP ports: {GREEN}{BOLD}{len([r for r in tcp_results if r['status'] == 'OPEN'])}{RESET}")
    print(f"{WHITE}Open UDP ports: {GREEN}{BOLD}{len([r for r in udp_results if r['status'] == 'OPEN'])}{RESET}")
    print(f"{WHITE}Closed ports: {RED}{BOLD}{total_ports - len([r for r in scan_results if r['status'] == 'OPEN'])}{RESET}")

    if output_format == "json":
        with open('scan_results.json', 'w') as f:
            json.dump(scan_results, f, indent=4)
        print(f"{BOLD}{WHITE}Scan results saved to 'scan_results.json'.{RESET}")
    elif output_format == "text":
        with open('scan_results.txt', 'w') as f:
            for result in scan_results:
                f.write(f"{result}\n")
        print(f"{BOLD}{WHITE}Scan results saved to 'scan_results.txt'.{RESET}")
    elif output_format == "xml":
        # Implement XML export here
        pass

def main():
    parser = argparse.ArgumentParser(description="Netnab - Fast and efficient port scanner.")
    
    # Positional argument for the IP address
    parser.add_argument("ip", help="IP address to scan")

    parser.add_argument("-p", "--ports", type=str, default="1-1000", help="Port range to scan (default: 1-1000)")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Number of threads (1-100, default: 5)")
    parser.add_argument("-T", "--timeout", type=int, default=1, help="Timeout in seconds for each port scan (default: 1)")
    parser.add_argument("-P", "--protocol", choices=["tcp", "udp"], default="tcp", help="Protocol to scan (default: tcp)")
    parser.add_argument("-sv", "--service-version", action="store_true", help="Enable service version detection")
    parser.add_argument("-o", "--output-format", choices=["json", "xml", "text"], default="json", help="Output format (default: json)")
    
    args = parser.parse_args()

    start_port, end_port = map(int, args.ports.split('-'))

    # Validate port range
    if start_port < 1 or start_port > 65535 or end_port < 1 or end_port > 65535:
        print(f"{RED}Error: Port numbers must be between 1 and 65535.{RESET}")
        return
    
    if start_port > end_port:
        print(f"{RED}Error: Start port {start_port} must be less than or equal to end port {end_port}.{RESET}")
        return
    
    # Parse port range
    start_port, end_port = map(int, args.ports.split('-'))
    ip = args.ip
    num_threads = args.threads
    timeout = args.timeout
    protocol = args.protocol
    service_version = args.service_version
    output_format = args.output_format

    # Start scanning
    scan_ports(ip, start_port, end_port, num_threads, timeout, protocol, service_version, output_format)

if __name__ == "__main__":
    main()
