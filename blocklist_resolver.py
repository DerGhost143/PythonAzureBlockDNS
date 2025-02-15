#!/usr/bin/env python3
import json
import logging
import time
from threading import Lock
from dnslib import DNSRecord, RCODE
from dnslib.server import BaseResolver

logger = logging.getLogger(__name__)

class BlocklistResolver(BaseResolver):
    def __init__(self, upstream_dns='8.8.8.8', blacklist_file="settings/blacklist.json", cache_ttl=60):
        try:
            with open(blacklist_file, "r") as f:
                data = json.load(f)
                self.blacklist = [domain.lower().rstrip('.') for domain in data.get("blacklist", [])]
            logger.debug("Blacklist loaded: %s", self.blacklist)
        except Exception as e:
            logger.error("Error loading blacklist (%s): %s", blacklist_file, e)
            self.blacklist = []
        self.upstream_dns = upstream_dns
        self.cache_ttl = cache_ttl
        self.cache = {}
        self.cache_lock = Lock()

    def resolve(self, request, handler):
        qname = str(request.q.qname).lower().rstrip('.')
        logger.debug("Received DNS query for: %s", qname)
        with self.cache_lock:
            if qname in self.cache:
                reply, expiration = self.cache[qname]
                if time.time() < expiration:
                    logger.debug("Cache hit for: %s", qname)
                    return reply
                else:
                    logger.debug("Cache expired for: %s", qname)
                    del self.cache[qname]
        for blocked in self.blacklist:
            if qname == blocked or qname.endswith('.' + blocked):
                logger.info("Blocking DNS query for: %s (matched: %s)", qname, blocked)
                reply = request.reply()
                reply.header.rcode = RCODE.NXDOMAIN
                return reply
        try:
            logger.info("Forwarding DNS query for: %s to upstream DNS (%s)", qname, self.upstream_dns)
            proxy_response = request.send(self.upstream_dns, 53, tcp=(handler.protocol == 'tcp'))
            reply = DNSRecord.parse(proxy_response)
            logger.debug("Received response from upstream DNS for: %s", qname)
            with self.cache_lock:
                self.cache[qname] = (reply, time.time() + self.cache_ttl)
            return reply
        except Exception as e:
            logger.error("Error forwarding query for %s: %s", qname, e)
            reply = request.reply()
            reply.header.rcode = RCODE.SERVFAIL
            return reply
