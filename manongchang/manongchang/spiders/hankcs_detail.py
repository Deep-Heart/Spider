# -*- coding: utf-8 -*-
from scrapy import Selector

from base.bloom_redis.spiders import RedisSpider
from base.items import BaseDetailItem, ARTICLE_TITLE, ARTICLE_CONTENT, ARTICLE_LINK


class HankcsDetailSpider(RedisSpider):
    name = "hankcs_detail"
    allowed_domains = ["hankcs.com"]
    start_urls = ['http://www.hankcs.com/ml/the-perceptron-learning-procedure.html']

    redis_key = 'hankcs'

    custom_settings = {
        'ITEM_PIPELINES': {'manongchang.pipelines.ManongchangDetailPipeline': 300},
        'SCHEDULER': 'base.bloom_redis.scheduler.Scheduler',
        'SCHEDULER_PERSIST': True,
        'SCHEDULER_QUEUE_CLASS': 'base.bloom_redis.queue.SpiderQueue',
    }

    def parse(self, response):
        hxs = Selector(response)
        item = BaseDetailItem()

        item['_id'] = response.url
        item['class_title'] = hxs.xpath('//div[@class="article-meta"]//span[1]//a//text()').extract()
        item['article_title'] = hxs.xpath('//h1[@class="article-title"]//a//text()').extract_first()
        item['publish_time'] = hxs.xpath('//div[@class="article-meta"]//span[last()-3]//text()').extract_first()
        item['article_tag'] = item['class_title']

        article_title = hxs.xpath('//article[@class="article-content"]//h2//text()').extract()
        article_content = hxs.xpath('//article[@class="article-content"]//p//text()').extract()
        article_link = hxs.xpath('//article[@class="article-content"]//p//img//@src').extract()

        article = hxs.xpath('//article[@class="article-content"]//p//text() |'
                            ' //article[@class="article-content"]//h2//text() |'
                            ' //article[@class="article-content"]//p//img//@src').extract()

        article_type = []
        for content in article:
            if content in article_title:
                article_type.append(ARTICLE_TITLE)
            elif content in article_content:
                article_type.append(ARTICLE_CONTENT)
            elif content in article_link:
                article_type.append(ARTICLE_LINK)

        item['article_content'] = article
        item['article_type'] = article_type

        item['author'] = 'hankcs'
        item['author_id'] = 'hankcs'
        item['author_icon'] = hxs.xpath('//div[@class="logo"]//a//img//@src').extract_first()

        yield item
