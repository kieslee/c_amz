# -*- coding: utf-8 -*-
import scrapy
import re
import sys
import json


class AmazonSpider(scrapy.Spider):
    name = "amazon_bs"
    allowed_domains = ["amazon.com", "baidu.com"]
    start_urls = (
        'https://www.amazon.com/Best-Sellers/zgbs/ref=zg_mg_tab',
    )

    def parse(self, response):
        lis = response.xpath('/html/body/div[4]/div[2]/div/div[1]/div/div[2]/div/div[2]/ul/ul/li')
        for li in lis:
            url = response.urljoin(li.xpath('./a/@href').extract_first())
            class_name = li.xpath('./a/text()').extract_first()
            r = scrapy.Request(url, callback=self.parse_class_pages_first)
            r.meta['class_name'] = class_name
            yield r

    def parse_class_pages_first(self, response):
        class_name = response.meta['class_name']
        divs = response.xpath('//*[@id="zg_centerListWrapper"]/div[contains(@class, "zg_itemImmersion")]')
        for div in divs:
            url = div.xpath('./div/div[2]/a/@href').extract_first().strip('\n')
            rank = div.xpath('./div/span/text()').extract_first().strip('.')
            r = scrapy.Request(url, callback=self.parse_products)
            r.meta['class_name'] = class_name
            r.meta['rank'] = rank
            yield r
            
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
            r = scrapy.Request(url, callback=self.parse_products, dont_filter=True)
            r.meta['class_name'] = class_name
            r.meta['rank'] = rank
            yield r

    def parse_products(self, response):
        class_name = response.meta['class_name']
        rank = response.meta['rank']
        
        name = response.xpath('//*[@id="productTitle"]/text()').extract_first().strip('\n          ')
        price = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first()
        if price is None:
            price = response.xpath('//*[@id="priceblock_saleprice"]/text()').extract_first()
        if price is None:
            price = 'Currently unavailable'
        stars = response.xpath('//*[@id="reviewStarsLinkedCustomerReviews"]/i/span/text()').extract_first()
        if stars is None:
            stars = 'Not Found'
        
        yield {'class_name': class_name, 'rank': rank, 'name': name, 'price': price, 'stars': stars, 'url': response.url}


class AmazonSpider_2(scrapy.Spider):
    name = "amazon_collect_tag_bs"
    allowed_domains = ["amazon.com"]
    start_urls = (
        'https://www.amazon.com/Best-Sellers/zgbs/ref=zg_mg_tab',
    )

    def parse(self, response):
        lis = response.xpath('/html/body/div[4]/div[2]/div/div[1]/div/div[2]/div/div[2]/ul/ul/li')
        for li in lis:
            url = response.urljoin(li.xpath('./a/@href').extract_first())
            class_name = li.xpath('./a/text()').extract_first()
            r = scrapy.Request(url, callback=self.parse_class_pages_first)
            r.meta['class_name'] = class_name
            yield r

    def parse_class_pages_first(self, response):
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

class AmazonSpider_3(scrapy.Spider):
    name = "amazon_collect_products"
    allowed_domains = ["amazon.com"]

    def start_requests(self):
        filename = '/home/kieslee/amz-tag-bs.json'
        file = open(filename, 'r')
        content = file.read()
        con_list = json.loads(content)
        for item in con_list:
            r = self.make_requests_from_url(item['url'])
            r.meta['class_name'] = item['class_name']
            r.meta['rank'] = item['rank']
            yield r

    def parse(self, response):
        class_name = response.meta['class_name']
        rank = response.meta['rank']
        
        try:
            name = response.xpath('//*[@id="productTitle"]/text()').extract_first().strip('\n          ')
            price = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first()
            if price is None:
                price = response.xpath('//*[@id="priceblock_saleprice"]/text()').extract_first()
            if price is None:
                price = 'Currently unavailable'
            stars = response.xpath('//*[@id="reviewStarsLinkedCustomerReviews"]/i/span/text()').extract_first()
            if stars is None:
                stars = 'Not Found'
            
            yield {'class_name': class_name, 'rank': rank, 'name': name, 'price': price, 'stars': stars, 'url': response.url}
        except Exception, e:
            yield {'class_name': class_name, 'rank': rank, 'url': response.url, 'faild': True}

