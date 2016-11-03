#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import logging
import random
import re
import time
from datetime import datetime, timedelta
from twisted.web._newclient import ResponseNeverReceived
from twisted.internet.error import TimeoutError, ConnectionRefusedError, ConnectError
import fetch_free_proxyes

logger = logging.getLogger(__name__)

class KProxyMiddleware(object):

    DONT_RETRY_ERRORS = (TimeoutError, ConnectionRefusedError, ResponseNeverReceived, ConnectError, ValueError)

    def __init__(self, settings):
        self.proxy_file = "proxyes.dat"
        #self.proxyes = {'local': {'count': 0, 'valid': True}}
        self.proxyes = {}
        self.max_fails = 10
        self.least_len = 5

        if os.path.exists(self.proxy_file):
            with open(self.proxy_file, 'r') as fd:
                lines = fd.readlines()
                for line in lines:
                    line = line.strip()
                    if not line or self.proxyes.has_key(line):
                        continue
                    self.proxyes[line] = {'count': 0, 'valid': True, 'last': 0}

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def fetch_new_proxyes(self):
        logger.info("extending proxyes using fetch_free_proxyes.py")
        new_proxyes = fetch_free_proxyes.fetch_all()
        logger.info("new proxyes: %s" % new_proxyes)

        for np in new_proxyes:
            if np in self.proxyes:
                continue
            else:
                self.proxyes[np] = {'count': 0, 'valid': True, 'last': 0}


    def set_proxy(self, request):
        if 'proxy' in request.meta:
            del request.meta['proxy']

        if len(self.proxyes.keys()) <= self.least_len:
            self.fetch_new_proxyes()

        proxy_list = []
        for p in self.proxyes.keys():
            if self.proxyes[p]['valid']:
                proxy_list.append(p)

        proxy = random.choice(proxy_list)
        if proxy != 'local':
            request.meta['proxy'] = 'http://' + proxy

        return request

    def process_request(self, request, spider):
        self.set_proxy(request)
        if 'proxy' in request.meta:
            logger.info("using proxy %s" % request.meta['proxy'])
        else:
            logger.info("using local")

    def process_response(self, request, response, spider):
        if "proxy" in request.meta.keys():
            logger.debug("%s %s %s" % (request.meta["proxy"], response.status, request.url))
        else:
            logger.debug("None %s %s" % (response.status, request.url))

        if re.search('Robot Check', response.text):
            if 'proxy' in request.meta:
                k = request.meta['proxy']
            else:
                k = 'local'
            self.proxyes[k]['count'] += 1
            if self.proxyes[k]['count'] > self.max_fails:
                del self.proxyes[k]

            new_request = request.copy()
            new_request.dont_filter = True
            self.set_proxy(new_request)
            return new_request

        return response

    def process_exception(self, request, exception, spider):
        print 'in process_exception'
        if isinstance(exception, self.DONT_RETRY_ERRORS):
            if 'proxy' in request.meta:
                k = request.meta['proxy']
            else:
                k = 'local'
            self.proxyes[k]['count'] += 1
            if self.proxyes[k]['count'] > self.max_fails:
                del self.proxyes[k]

            new_request = request.copy()
            new_request.dont_filter = True
            self.set_proxy(new_request)
            return new_request

