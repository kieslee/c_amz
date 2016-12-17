
# -*- coding: UTF-8 -*-
import re

pattern = re.compile('.*\n*(#\d+.*in.*)\(')

class GetItem(object):
    __tagclass__ = 'method002'
    __instruction__  = 'table的一种方法'
    __ex_url__ = 'https://www.amazon.com/Woodstock-Inspirational-Amazing-Grace-Medium/dp/B00026W5UK/ref=zg_bs_lawn-garden_2?_encoding=UTF8&psc=1&refRID=NT1F8F8MDY5BZH9PH36D'

    def __init__(self, soup, selector):
        self.soup = soup
        self.selector = selector


    def get_item(self):
        for t in self.soup.find_all('table'):
            t_class = t.get('class')
            if t_class is None:
                continue

            if 'prodDetTable' not in t_class:
                continue

            for tr in t.find_all('tr'):
                # print tr.th.get_text()
                if (tr.th.get_text()).find('Sellers Rank') >= 0:
                    return tr.td.get_text().strip(' ')

        return None
