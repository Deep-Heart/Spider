# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from base.pipelines import BaseUrlPipeline, BaseDetailPipeline


class MachineHeartPipeline(BaseUrlPipeline):
    def __init__(self) -> None:
        super().__init__()


class JiqizhixinDetailPipeline(BaseDetailPipeline):
    def __init__(self) -> None:
        super().__init__('jiqizhixin')
