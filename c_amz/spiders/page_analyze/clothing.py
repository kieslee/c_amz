import re
from base import PA_General
from . import register_page_analyze

pattern = re.compile('.*\n*(#\d+.*in.*)\(')

class Clothing(PA_General):
    def get_Rank(self):
        print 'type: Clothing, do parsing'
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


