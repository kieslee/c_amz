# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from acache import r_push

from conf import crawl_result_succ, crawl_result_fail

class CAmzPipeline(object):
    def get_result_dict(self, item):
        result_dict = {}
        if item['status']:
            result_dict['uuid'] = item['uuid']
            result_dict['title'] = item['title']
            result_dict['price'] = item['price']
            result_dict['stars'] = item['stars']
            result_dict['best_sell_rank'] = item['best_sell_rank']
        else:
            result_dict['uuid'] = item['uuid']
            result_dict['fail_crawls'] = item['fail_crawls']
            result_dict['url'] = item['url']
            result_dict['class_name'] = item['class_name']
            try:
                result_dict['title'] = item['title']
            except Exception, e:
                pass
            try:
                result_dict['price'] = item['price']
            except Exception, e:
                pass
            try:
                result_dict['stars'] = item['stars']
            except Exception, e:
                pass
            try:
                result_dict['best_sell_rank'] = item['best_sell_rank']
            except Exception, e:
                pass
        return result_dict


    def process_item(self, item, spider):
        result_dict = self.get_result_dict(item)
        if item['status']:
            r_push(crawl_result_succ, json.dumps(result_dict))
        else:
            r_push(crawl_result_fail, json.dumps(result_dict))
        return item
