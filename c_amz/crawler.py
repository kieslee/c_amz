#-*- coding: UTF-8 -*-

import socket
import struct
import math
import sys
import time
import traceback
import json

import conf

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.amz_product_crawl import AmazonSpider_01

# 设置本机的hostname，用该名字去redis中读取相应的任务
AmazonSpider_01.hostname = conf.crawl_hostname

import multiprocessing
from multiprocessing import Process

from acache import l_pop


def crawl_process():
    process = CrawlerProcess(get_project_settings())
    process.crawl(AmazonSpider_01)
    process.start()


if __name__  == '__main__':
    '''
    while True:
        pid = Process(target=crawl_process, args=())
        pid.start()
        pid.join()

        time.sleep(5)
        '''
    crawl_process()
