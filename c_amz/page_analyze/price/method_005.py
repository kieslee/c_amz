
# -*- coding: UTF-8 -*-

class GetItem(object):
    __tagclass__ = 'method005'
    __instruction__  = 'amazon没有销售，但是第三方有售'
    __ex_url__ = 'https://www.amazon.com/Simple-Cleansing-Facial-Wipes-Count/dp/B00C5AHTC0/ref=sr_1_1_a_it?ie=UTF8&qid=1482321941&sr=8-1&keywords=Simple%2BCleansing%2BFacial%2BWipes%2C%2BKind%2Bto%2BSkin%2B25%2BCount%2C%2BTwin%2BPack&th=1'

    def __init__(self, soup, selector):
        self.soup = soup
        self.selector = selector


    def get_item(self):
        price = None
        div_tags = self.soup.find_all(name='span', id='availability')
        if len(div_tags) == 1:
            text = div_tags[0].get_text(strip=True)
            if text.find('Available from') >= 0:
                return 'Available from 3rd party sellers.'

        return price
