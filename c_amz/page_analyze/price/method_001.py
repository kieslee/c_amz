
# -*- coding: UTF-8 -*-

class GetItem(object):
    __tagclass__ = 'method001'
    __instruction__  = '标准的方法，绝大多数页面采用这个方法'
    __ex_url__ = 'https://www.amazon.com/Levis-Mens-505-Regular-Jean/dp/B001H0FVAG/ref=zg_bs_apparel_2?_encoding=UTF8&refRID=FPM24D8XBGDW9DH5NB4G&th=1&psc=1'

    def __init__(self, soup, selector):
        self.soup = soup
        self.selector = selector


    def get_item(self):
        price = None
        price = self.selector.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first()
        if price is None:
            price = self.selector.xpath('//*[@id="priceblock_saleprice"]/text()').extract_first()

        return price
