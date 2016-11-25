import sys
from bs4 import BeautifulSoup
from scrapy.selector import Selector

class PA_General(object):

    def __init__(self, soup, selector):
        self.soup = soup
        self.selector = selector

    def get_ProductTitle(self):
        p = self.selector.xpath('//*[@id="productTitle"]/text()').extract_first().strip('\n          ')
        return p

    def get_Price(self):
        price = self.selector.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first()
        if price is None:
            price = self.selector .xpath('//*[@id="priceblock_saleprice"]/text()').extract_first()

        return price

    def get_Stars(self):
        stars = self.selector.xpath('//*[@id="reviewStarsLinkedCustomerReviews"]/i/span/text()').extract_first()
        if stars is not None:
            return stars
        
        stars = self.selector.xpath('//*[@id="acrCustomerWriteReviewText"]/text()').extract_first()
        if stars == 'Be the first to review this item':
            stars = '0.0 out of 5 stars'
        if stars is not None:
            return stars

        return stars

    def get_Rank(self):
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
