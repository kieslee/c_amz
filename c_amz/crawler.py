#-*- coding: UTF-8 -*-

import socket
import struct
import math
import os
import sys
import time
import traceback
import json
import importlib

import conf

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.amz_product_crawl import AmazonSpider_01

import page_analyze
from page_analyze import find_needed_packages, register_page_analyze
from page_analyze import display_registed_class

# 设置本机的hostname，用该名字去redis中读取相应的任务
AmazonSpider_01.hostname = conf.crawl_hostname

import multiprocessing
from multiprocessing import Process

from acache import l_pop


def crawl_process():
    process = CrawlerProcess(get_project_settings())
    process.crawl(AmazonSpider_01)
    process.start()

PAGE_ANALYZE_DIR = 'page_analyze'
exclude_filename = ['__init__.py', 'base.py']

if __name__  == '__main__':
    # 获取所有的package
    package_list = find_needed_packages('page_analyze')

    print 'list packages:'
    for p in package_list:
        print p

    for p in package_list:
        mymodule = importlib.import_module(p)
        myclass = mymodule.page_analyze

        register_page_analyze(myclass)

    display_registed_class()

    '''
    while True:
        pid = Process(target=crawl_process, args=())
        pid.start()
        pid.join()

        time.sleep(5)
        '''
    #crawl_process()
