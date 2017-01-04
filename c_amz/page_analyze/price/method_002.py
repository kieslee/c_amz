
# -*- coding: UTF-8 -*-

class GetItem(object):
    __tagclass__ = 'method002'
    __instruction__  = 'dealprice'
    __ex_url__ = 'https://www.amazon.com/Koolife-Sharpener-Coarse-Extra-Fine-Sharpening/dp/B01C1C7A4S/ref=sr_1_1?ie=UTF8&qid=1482236570&sr=8-1&keywords=Koolife+Knife+Sharpener+with+2+Stage+Coarse+%26+Extra-Fine+Sharpening+System+for+Steel+Knives+in+All+Sizes%2CBlack'

    def __init__(self, soup, selector):
        self.soup = soup
        self.selector = selector


    def get_item(self):
        price = None
        price = self.selector.xpath('//*[@id="priceblock_dealprice"]/text()').extract_first()

        return price
