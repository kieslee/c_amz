# -*- coding: utf-8 -*-
import scrapy
import re


class AmazonSpider(scrapy.Spider):
    name = "amazon_bs"
    allowed_domains = ["amazon.com", "baidu.com"]
    start_urls = (
        'https://www.amazon.com/Best-Sellers/zgbs/ref=zg_mg_tab',
    )

    def parse(self, response):
	if re.search('Robot Check', response.text):
	    r = scrapy.Request(response.url, callback=parse)
	    r.meta['change_proxy']=True
	    yield r
	    return
	lis = response.xpath('/html/body/div[4]/div[2]/div/div[1]/div/div[2]/div/div[2]/ul/ul/li')
	i = 0
	for li in lis:
	    i += 1
	    url = response.urljoin(li.xpath('./a/@href').extract_first())
	    class_name = li.xpath('./a/text()').extract_first()
	    #yield {'url': url, 'class_name': class_name}
	    r = scrapy.Request(url, callback=self.parse_class_pages_first)
	    r.meta['class_name'] = class_name
	    yield r
	    if i > 2:
		break

    def parse_class_pages_first(self, response):
	if re.search('Robot Check', response.text):
	    r = scrapy.Request(response.url, callback=parse_class_pages_first)
	    r.meta['change_proxy']=True
	    yield r
	    return
        class_name = response.meta['class_name']
	divs = response.xpath('//*[@id="zg_centerListWrapper"]/div[contains(@class, "zg_itemImmersion")]')
	for div in divs:
	    url = div.xpath('./div/div[2]/a/@href').extract_first().strip('\n')
	    rank = div.xpath('./div/span/text()').extract_first().strip('.')
	    r = scrapy.Request(url, callback=self.parse_products)
	    r.meta['class_name'] = class_name
	    r.meta['rank'] = rank
	    yield r
	
	return 

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
	if re.search('Robot Check', response.text):
	    r = scrapy.Request(response.url, callback=parse_class_pages, dont_filter=True)
	    r.meta['change_proxy']=True
	    yield r
	    return
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
	    r = response.request
	    #r = scrapy.Request(response.url, callback=self.parse_products, dont_filter=True)
	    r.dont_filter = True
	    r.meta['change_proxy'] = True
	    #r.meta['class_name'] = class_name
	    #r.meta['rank'] = rank
	    yield r
