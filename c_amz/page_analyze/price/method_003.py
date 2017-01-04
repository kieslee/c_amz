
# -*- coding: UTF-8 -*-

class GetItem(object):
    __tagclass__ = 'method003'
    __instruction__  = 'out of Stock'
    __ex_url__ = 'https://www.amazon.com/Koolife-Sharpener-Coarse-Extra-Fine-Sharpening/dp/B01C1C7A4S/ref=sr_1_1?ie=UTF8&qid=1482236570&sr=8-1&keywords=Koolife+Knife+Sharpener+with+2+Stage+Coarse+%26+Extra-Fine+Sharpening+System+for+Steel+Knives+in+All+Sizes%2CBlack'

    def __init__(self, soup, selector):
        self.soup = soup
        self.selector = selector


    def get_item(self):
        price = None
        div_tags = self.soup.find_all(name='div', id='outOfStock')
        if len(div_tags) != 0:
            return 'Currently unavailable.'

        return price
