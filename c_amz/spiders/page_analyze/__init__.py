from bs4 import BeautifulSoup
from scrapy.selector import Selector

import base

page_analyze_classes = []

page_analyze_classes.append(base.PA_General)


def register_page_analyze(c):
    page_analyze_classes.append(c)


class PAGE_ITEM(object):
    def __init__(self, content):
        self.content = content
        self.soup = BeautifulSoup(content)
        self.selector = Selector(text=content)

        self.parsed = False

        # wanted infos
        self.title = None
        self.price = None
        self.stars = None
        self.best_sell_rank = None

    def get_Infos(self):
        global page_analyze_classes
        for pa_class in page_analyze_classes:
            if self.parsed:
                break

            page_item = pa_class(self.soup, self.selector)
            if self.title is None:
                self.title = page_item.get_ProductTitle()
            if self.price is None:
                self.price = page_item.get_Price()
            if self.stars is None:
                self.stars = page_item.get_Stars()
            if self.best_sell_rank is None:
                self.best_sell_rank = page_item.get_Rank()

            if self.title is not None and self.price is not None \
                    and self.stars is not None and self.best_sell_rank is not None:
                self.parsed = True
                break

        return self.title, self.price, self.stars, self.best_sell_rank
