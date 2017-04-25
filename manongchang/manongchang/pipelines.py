# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from base.pipelines import BaseUrlPipeline, BaseDetailPipeline


class ManongchangPipeline(BaseUrlPipeline):
    def __init__(self) -> None:
        super().__init__()


class ManongchangDetailPipeline(BaseDetailPipeline):
    def __init__(self) -> None:
        super().__init__('monongchang')
