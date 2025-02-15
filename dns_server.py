#!/usr/bin/env python3
import logging
from dnslib.server import DNSServer, DNSLogger
from blocklist_resolver import BlocklistResolver

def start_dns_servers():
    resolver = BlocklistResolver(upstream_dns='8.8.8.8', blacklist_file="settings/blacklist.json")
    logger = DNSLogger()
    logging.getLogger("dnslib.server").setLevel(logging.DEBUG)
    logging.info("Starting DNS servers...")
    udp_server = DNSServer(resolver, port=53, address="0.0.0.0", logger=logger)
    udp_server.start_thread()
    logging.info("UDP DNS server running on 0.0.0.0:53")
    tcp_server = DNSServer(resolver, port=53, address="0.0.0.0", tcp=True, logger=logger)
    tcp_server.start_thread()
    logging.info("TCP DNS server running on 0.0.0.0:53")
    return udp_server, tcp_server
