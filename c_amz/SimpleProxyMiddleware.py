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

    def __init__(self, settings):
        self.proxy = 'http://fr.proxymesh.com:31280'

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)


    def set_proxy(self, request):
        request.meta['proxy'] = self.proxy


    def process_request(self, request, spider):
        self.set_proxy(request)
