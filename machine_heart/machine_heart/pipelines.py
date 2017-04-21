# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from common.db.mongo.mongo_client import MongoClient
from common.db.redis.redis_client import RedisClient


class MachineHeartPipeline(object):
    def __init__(self) -> None:
        super().__init__()
        self.result_client = RedisClient()

    def process_item(self, item, spider):
        self.result_client.sadd(spider.name, item['url'])
        return item


class JiqizhixinDetailPipeline(object):
    collection = 'jiqizhixin'

    def __init__(self) -> None:
        super().__init__()
        self.result_client = MongoClient('detail', self.collection)

    def process_item(self, item, spider):
        self.result_client.replace_one(self.collection, item, upsert=True)
        return item
