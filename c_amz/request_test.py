import sys

from spiders.page_analyze import PAGE_ITEM
from spiders.page_analyze import register_page_analyze

from c_amz.page_analyze import clothing


def parse_func_test(content):
    page_item = PAGE_ITEM(content)
    # (title, price, stars, best_sell_rank) = page_item.get_Infos()
    page_item.get_Infos()

    print 'title:', page_item.title
    print 'price:', page_item.price
    print 'stars:', page_item.stars
    print 'best sell rank:', page_item.best_sell_rank


if __name__ == '__main__':
    register_page_analyze(clothing.Clothing)

    f = open(sys.argv[1])
    content = f.read()

    parse_func_test(content)

    '''
    soup = BeautifulSoup(content)
    sel = Selector(text=content)
    import pdb; pdb.set_trace()
    rank = sel.xpath('//*[@id="SalesRank"]/text()[1]').extract_first()
    print rank
    import pdb;
    pdb.set_trace()
    for tag in soup.find_all('div'):
        t_id = tag.get('id')
        try:
            if 'dpx-amazon-sales-rank_feature_div' not in t_id:
                continue
        except Exception, e:
            continue

        #import pdb; pdb.set_trace()
        for li in tag.find_all('li'):
            print li.b.get_text()
            '''

