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

from page_analyze import PAGE_ITEM

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
        method_type = p.split('.')[1]
        print 'method_type: ', method_type
        mymodule = importlib.import_module(p)
        myclass = mymodule.GetItem

        register_page_analyze(myclass, method_type)

    display_registed_class()

    f = open(sys.argv[1], 'r')
    content = f.read()
    page_item = PAGE_ITEM(content)
    print 'title: ', page_item.get_title()
    print 'price: ', page_item.get_price()
    print 'sell rank: ', page_item.get_sell_rank()
