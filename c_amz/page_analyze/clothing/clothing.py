import re
from page_analyze import PA_General

pattern = re.compile('.*\n*(#\d+.*in.*)\(')

class page_analyze(PA_General):
    __tagclass__ = 'Clothing'

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


