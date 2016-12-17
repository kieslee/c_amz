
# -*- coding: UTF-8 -*-
import re

pattern = re.compile('.*\n*(#\d+.*in.*)\(')

class GetItem(object):
    __tagclass__ = 'method001'
    __instruction__  = 'Clothing分类的一种方法'
    __ex_url__ = 'https://www.amazon.com/Levis-Mens-505-Regular-Jean/dp/B001H0FVAG/ref=zg_bs_apparel_2?_encoding=UTF8&refRID=FPM24D8XBGDW9DH5NB4G&th=1&psc=1'

    def __init__(self, soup, selector):
        self.soup = soup
        self.selector = selector


    def get_item(self):
        rank_tags = self.soup.find_all(id='SalesRank')
        if len(rank_tags) != 1:
            return None

        rank_tag = rank_tags[0]
        if rank_tag.b.text != 'Amazon Best Sellers Rank:':
            return None

        rank_tag_nearby = rank_tag.b.next_sibling
        m = pattern.match(rank_tag_nearby)
        if m:
            return m.group(1)
        else:
            zg_hrsr_item = rank_tag.find_all('li')[0]
            return zg_hrsr_item.text
