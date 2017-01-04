
# -*- coding: UTF-8 -*-
import re

pattern = re.compile('.*\n*(#\d+.*in.*)\(')

class GetItem(object):
    __tagclass__ = 'method001'
    __instruction__  = '标准的做法'
    __ex_url__ = 'https://www.amazon.com/Levis-Mens-505-Regular-Jean/dp/B001H0FVAG/ref=zg_bs_apparel_2?_encoding=UTF8&refRID=FPM24D8XBGDW9DH5NB4G&th=1&psc=1'

    def __init__(self, soup, selector):
        self.soup = soup
        self.selector = selector


    def get_item(self):
        div_tags = self.soup.find_all(name='div', id='feature-bullets')
        if len(div_tags) != 1:
            return None

        div_tag = div_tags[0]

        li_list = div_tag.find_all(name='li', id='')
        listing = ''
        for li in li_list:
            con = li.get_text(strip=True)
            listing = listing + con + '.'

        return listing
