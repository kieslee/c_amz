# -*- coding: utf-8 -*-
import scrapy
import re
import sys
import json
import pdb
import redis
from retrying import retry

r_host = '127.0.0.1'
r_port = 6379
r_db = 1

pool = None
r = None

def get_cache():
    global pool, r

    if pool is None:
        pool = redis.ConnectionPool(host=r_host, port=r_port, db=r_db, socket_timeout=10)

    r = redis.Redis(connection_pool=pool)
    return r


def get_keys():
    global r
    if r is None:
        r = get_cache()

    return r.keys()


def get_value(k):
    global r
    if r is None:
        r = get_cache()

    return r.get(k)

def set_value(k, v):
    global r
    if r is None:
        r = get_cache()

    r.set(k, v)


class AmazonSpider(scrapy.Spider):
    name = "amazon_collect_all_tags"
    allowed_domains = ["amazon.com", "baidu.com"]
    start_urls = (
        'https://www.amazon.com/Best-Sellers/zgbs/ref=zg_mg_tab',
    )

    def parse(self, response):
        lis = response.xpath('/html/body/div[4]/div[2]/div/div[1]/div/div[2]/div/div[2]/ul/ul/li')
        for li in lis:
            url = response.urljoin(li.xpath('./a/@href').extract_first())
            class_name = li.xpath('./a/text()').extract_first()
            r = scrapy.Request(url, callback=self.parse_class_pages)
            r.meta['class_name'] = class_name
            yield r


    def tag_selected_parse(self, response):
        #pdb.set_trace()
        ul = response.xpath('//*[@id="zg_browseRoot"]')
        while True:
            try:
                li = ul.xpath('./li')
                if len(li) == 0:
                    return None
                ul = ul.xpath('./ul')
                span_class_name = li.xpath('./span/@class').extract_first()
                if span_class_name == 'zg_selected':
                    return ul
            except Exception, e:
                return None

        return None


    def parse_class_pages(self, response):
        class_name = response.meta['class_name']
        yield {'class_name': class_name, 'url': response.url}

        ul = self.tag_selected_parse(response)
        if ul is not None:
            lis = ul.xpath('./li')
            for li in lis:
                url = li.xpath('./a/@href').extract_first()
                sub_class_name = li.xpath('./a/text()').extract_first()
                r = scrapy.Request(url, callback=self.parse_class_pages)
                r.meta['class_name'] = class_name + ":" + sub_class_name
                yield r

class AmazonSpider2(scrapy.Spider):
    name = "amazon_collect_all_products"
    allowed_domains = ["amazon.com"]
    '''
    start_urls = (
        'https://www.amazon.com/Best-Sellers/zgbs/ref=zg_mg_tab',
    )
    '''

    def start_requests(self):
        key_list = get_keys()
        for k in key_list:
            url = get_value(k)
            class_name = k
            r = scrapy.Request(url, callback=self.parse)
            r.meta['class_name'] = class_name
            yield r


    def parse(self, response):
        class_name = response.meta['class_name']
        divs = response.xpath('//*[@id="zg_centerListWrapper"]/div[contains(@class, "zg_itemImmersion")]')
        for div in divs:
            url = div.xpath('./div/div[2]/a/@href').extract_first().strip('\n')
            rank = div.xpath('./div/span/text()').extract_first().strip('.')
            #r = scrapy.Request(url, callback=self.parse_products)
            #r.meta['class_name'] = class_name
            #r.meta['rank'] = rank
            yield {'class_name': class_name, 'rank': rank, 'url': url}
            
        page2 = response.xpath('//*[@id="zg_page2"]/a/@href').extract_first()
        r = scrapy.Request(page2, callback=self.parse_class_pages)
        r.meta['class_name'] = class_name
        yield r
        
        page3 = response.xpath('//*[@id="zg_page3"]/a/@href').extract_first()
        r = scrapy.Request(page3, callback=self.parse_class_pages)
        r.meta['class_name'] = class_name
        yield r
        
        page4 = response.xpath('//*[@id="zg_page4"]/a/@href').extract_first()
        r = scrapy.Request(page4, callback=self.parse_class_pages)
        r.meta['class_name'] = class_name
        yield r
        
        page5 = response.xpath('//*[@id="zg_page5"]/a/@href').extract_first()
        r = scrapy.Request(page5, callback=self.parse_class_pages)
        r.meta['class_name'] = class_name
        yield r


    def parse_class_pages(self, response):
        class_name = response.meta['class_name']
        divs = response.xpath('//*[@id="zg_centerListWrapper"]/div[contains(@class, "zg_itemImmersion")]')
        for div in divs:
            url = div.xpath('./div/div[2]/a/@href').extract_first().strip('\n')
            rank = div.xpath('./div/span/text()').extract_first().strip('.')
            #r = scrapy.Request(url, callback=self.parse_products, dont_filter=True)
            #r.meta['class_name'] = class_name
            #r.meta['rank'] = rank
            yield {'class_name': class_name, 'rank': rank, 'url': url}

