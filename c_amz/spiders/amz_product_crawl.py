# -*- coding: utf-8 -*-
import json
import scrapy

from page_analyze import PAGE_ITEM
# parse class
from page_analyze import clothing

from page_analyze import register_page_analyze

from acache import l_pop, r_push, l_index, l_rem
from conf import crawl_result_succ, crawl_result_fail

from items import ProductItem

RE_PATTERN = ['//*[@id="productDetails_db_sections"]']

register_page_analyze(clothing.Clothing)


class AmazonSpider_01(scrapy.Spider):
    name = "amz_product_crawl_01"
    allowed_domains = ["amazon.com"]

    '''
    def add_urls(self, url_list):
        for u in url_list:
            self.start_urls.append(u)
            '''

    def start_requests(self):
        for i in [0,1,2,3,4]:
            try:
                item_str = l_index(self.hostname, i)
                item = json.loads(item_str)
            except Exception, e:
                return
            r = scrapy.Request(item['url'], callback=self.parse)
            r.meta['uuid'] = item['uuid']
            r.meta['value'] = item_str
            r.meta['class_name'] = item['class_name']
            yield r


    def parse(self, response):
        item = ProductItem()
        page_item = PAGE_ITEM(response.text)
        # (title, price, stars, best_sell_rank) = page_item.get_Infos()
        page_item.get_Infos()
        if page_item.parsed:
            item['uuid'] = response.meta['uuid']
            item['status'] = True
            item['title'] = page_item.title
            item['price'] = page_item.price
            item['stars'] = page_item.stars
            item['best_sell_rank'] = page_item.best_sell_rank
        else:
            item['uuid'] = response.meta['uuid']
            item['status'] = False
            item['fail_crawls'] = []
            if page_item.title is None:
                item['fail_crawls'].append('title')
            else:
                item['title'] = page_item.title

            if page_item.price is None:
                item['fail_crawls'].append('price')
            else:
                item['price'] = page_item.price

            if page_item.stars is None:
                item['fail_crawls'].append('stars')
            else:
                item['stars'] = page_item.stars

            if page_item.best_sell_rank is None:
                item['fail_crawls'].append('best_sell_rank')
            else:
                item['best_sell_rank'] = page_item.best_sell_rank

            item['url'] = response.url
            item['class_name'] = response.meta['class_name']

        l_rem(self.hostname, response.meta['value'])

        yield item
