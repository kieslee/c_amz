# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    uuid = scrapy.Field()
    status = scrapy.Field()
    url = scrapy.Field()
    class_name = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    stars = scrapy.Field()
    best_sell_rank = scrapy.Field()
    fail_crawls = scrapy.Field()
