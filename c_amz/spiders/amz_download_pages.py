# -*- coding: utf-8 -*-

import sys

sys.path.append('./')

import json
import scrapy
import sys

from page_analyze import PAGE_ITEM

from conf import input_file, output_dir


class Download_Spider(scrapy.Spider):
    name = 'download_spider'
    allowed_domains = ["amazon.com"]

    def start_requests(self):
        print sys.argv
        f = open(input_file, 'r')
        con = f.read()
        f.close()
        mydict = json.loads(con)
        for item in mydict:
            url = item['url']
            r = scrapy.Request(url, callback=self.parse)
            r.meta['name'] = item['class_name'] + '_' + item['rank']
            yield r

    def parse(self, response):
        page_item = PAGE_ITEM(response.text.encode('utf-8', 'ignore'))
        print 'parse ', response.meta['name']
        title = page_item.get_title()
        price = page_item.get_price()
        sell_rank = page_item.get_sell_rank()
        listing = page_item.get_listing()
        print 'title: ', title
        print 'price: ', price
        print 'sell rank: ', sell_rank
        print 'listing: ', listing

        if title is None or price is None or sell_rank is None or listing is None:
            print 'parse failed'
            f = open(output_dir + '/' + response.meta['name'], 'w')
            f.write(response.text.encode('utf-8', 'ignore'))
            f.close()
        else:
            print 'parse succ'
