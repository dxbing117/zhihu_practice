# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo

class ZhihuPipeline(object):
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
        # self.file = "需要调试的url.text"

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]
        # self.f = open(self.file, 'a', encoding='utf-8')

    def close_spider(self, spider):
        self.client.close()
        # self.f.close()

    def process_item(self, item, spider):
        self.db['zhihu_users'].update({'name': item['name']}, {'$set': item}, True)
        # if item['problem_url']:
        #     self.f.write(item['problem_url'])
        return item

