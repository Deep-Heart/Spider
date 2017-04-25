# -*- coding: utf-8 -*-
from datetime import datetime

from scrapy import Selector

from base.bloom_redis.spiders import RedisSpider
from base.items import BaseDetailItem, ARTICLE_CONTENT, ARTICLE_LINK


class JiqizhixinDetailSpider(RedisSpider):
    name = "jiqizhixin_detail"
    allowed_domains = ["jiqizhixin.com"]
    start_urls = ['http://jiqizhixin.com']

    redis_key = 'jiqizhixin'

    custom_settings = {
        'ITEM_PIPELINES': {'machine_heart.pipelines.JiqizhixinDetailPipeline': 300},
        'SCHEDULER': 'base.bloom_redis.scheduler.Scheduler',
        'SCHEDULER_PERSIST': True,
        'SCHEDULER_QUEUE_CLASS': 'base.bloom_redis.queue.SpiderQueue',
    }

    def parse(self, response):
        hxs = Selector(response)
        item = BaseDetailItem()

        item['_id'] = response.url

        class_title = str(hxs.xpath('//h2[@class="al-column-title"]//text()').extract_first())
        class_title = class_title.strip('\r\n').strip(' ')
        item['class_title'] = class_title

        article_title = str(hxs.xpath('//h2[@class="al-article-title"]//text()').extract_first())
        article_title = article_title.replace('\n', '').rstrip(' ').lstrip(' ')
        item['article_title'] = article_title

        publish_time = str(hxs.xpath('//div[@class="am-fl"]//text()').extract_first())
        publish_time = publish_time.replace('\n', '').replace('\xa0', '').rstrip(' ').lstrip(' ')
        publish_time = datetime.strptime(publish_time, '%Y-%m-%d %H:%M:%S')
        item['publish_time'] = int(publish_time.timestamp())
        item['article_tag'] = hxs.xpath('//span[@class="al-article-tag"]//text()').extract()

        article_content = hxs.xpath('//div[@class="al-article-content"]//p//text()').extract()
        article_link = hxs.xpath('//div[@class="al-article-content"]//p//img//@src').extract()

        article = hxs.xpath('//div[@class="al-article-content"]//p//text() |'
                            ' //div[@class="al-article-content"]//p//img//@src').extract()

        article_type = []
        for content in article:
            if content in article_content:
                article_type.append(ARTICLE_CONTENT)
            elif content in article_link:
                article_type.append(ARTICLE_LINK)

        item['article_content'] = article
        item['article_type'] = article_type

        author = hxs.xpath(
            '//div[@class="al-send-msg-to-anchor Smohan_FaceBox al-clearfix"]//h2//text()').extract_first()
        item['author'] = author
        author_id = hxs.xpath('//div[@class="al-article-authon-header-img"]//a//attribute::href').extract_first()
        author_id = str(author_id).split('/')[-1]
        item['author_id'] = author_id
        author_icon = hxs.xpath('//div[@class="al-article-authon-header-img"]//a//img//attribute::src').extract_first()
        item['author_icon'] = author_icon

        yield item
