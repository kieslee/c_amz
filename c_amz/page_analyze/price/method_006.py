
# -*- coding: UTF-8 -*-

class GetItem(object):
    __tagclass__ = 'method006'
    __instruction__  = 'Gillette的一种方法'
    __ex_url__ = 'https://www.amazon.com/Gillette-Mach3-Base-Cartridges-Count/dp/B0039LMTHE/ref=sr_1_1_a_it?ie=UTF8&qid=1482322660&sr=8-1&keywords=Gillette%2BMach3%2BBase%2BCartridges%2B15%2BCount&th=1'

    def __init__(self, soup, selector):
        self.soup = soup
        self.selector = selector


    def get_item(self):
        price = None
        price = self.selector.xpath('//*[@id="snsPrice"]/div/span[2]/text()').extract_first()

        return price
