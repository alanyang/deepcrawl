# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import random, pymongo
from datetime import datetime
from pymongo import MongoClient
from deepcrawl.items import DouyinItem


class DeepcrawlPipeline(object):

    bulk = []
    max_bulk = 100

    def __init__(self, settings):
        client = MongoClient(settings.get('MONGODB_URL'))
        self.col = client[settings.get('VIDEO_DB')][settings.get('VIDEO_COLLECTION')]
        self.col.create_index([('video_id', pymongo.DESCENDING)], unique = True)
        self.col.create_index([('published', pymongo.DESCENDING)])
        self.col.create_index([('rand', pymongo.DESCENDING)])

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_item(self, item, spider):
        if isinstance(item, DouyinItem):
            self.process_douyin(item, spider)
    
    def process_douyin(self, item, spider):
        item['published'] = datetime.fromtimestamp(item['published'])
        data = dict(item)
        __id = data.pop('video_id')
        data['rand'] = random.randint(0, 100)
        self.col.update({ 'video_id': __id }, {'$set': data}, upsert = True)
        # print(item)


