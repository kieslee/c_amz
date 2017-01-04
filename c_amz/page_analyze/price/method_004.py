
# -*- coding: UTF-8 -*-

class GetItem(object):
    __tagclass__ = 'method004'
    __instruction__  = 'amazon没有销售，但是第三方有售'
    __ex_url__ = 'https://www.amazon.com/Stanley-J7CS-Battery-Starter-Compressor/dp/B00RZXVQSU/ref=sr_1_1?ie=UTF8&qid=1482288569&sr=8-1&keywords=Stanley+J7CS+350+Amp+Battery+Jump+Starter+with+Compressor'

    def __init__(self, soup, selector):
        self.soup = soup
        self.selector = selector


    def get_item(self):
        price = None
        div_tags = self.soup.find_all(name='div', id='availability')
        if len(div_tags) == 1:
            text = div_tags[0].get_text(strip=True)
            if text.find('Available from') >= 0:
                return 'Available from 3rd party sellers.'

        return price
