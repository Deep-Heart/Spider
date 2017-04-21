# -*- coding: utf-8 -*-
from scrapy import Selector, Spider
from scrapy_redis.spiders import RedisSpider

from base.items import BaseDetailItem


class HankcsDetailSpider(Spider):
    name = "hankcs_detail"
    allowed_domains = ["hankcs.com"]
    start_urls = ['http://www.hankcs.com/ml/the-perceptron-learning-procedure.html']

    redis_key = 'hankcs'

    def parse(self, response):
        hxs = Selector(response)
        item = BaseDetailItem()

        item['_id'] = response.url
        item['class_title'] = hxs.xpath('//div[@class="article-meta"]//span[1]//a//text()').extract()
        item['article_title'] = hxs.xpath('//h1[@class="article-title"]//a//text()').extract_first()
        item['publish_time'] = hxs.xpath('//div[@class="article-meta"]//span[last()-3]//text()').extract_first()
        item['article_tag'] = item['class_title']

        # article_title = hxs.xpath('//article[@class="article-content"]//h2//text()').extract()
        # article_content = hxs.xpath('//article[@class="article-content"]//p//text()').extract()
        # article_link = hxs.xpath('//article[@class="article-content"]//p//img//@src').extract()

        article = hxs.xpath('//article[@class="article-content"]//p//text() |'
                            ' //article[@class="article-content"]//h2//text() |'
                            ' //article[@class="article-content"]//p//img//@src').extract()

        item['article_content'] = article

        yield item
