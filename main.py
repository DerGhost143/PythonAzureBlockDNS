#!/usr/bin/env python3
import time
import logging
from dns_server import start_dns_servers

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info("Initializing DNS server...")
    udp_server, tcp_server = start_dns_servers()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shutting down DNS server...")
