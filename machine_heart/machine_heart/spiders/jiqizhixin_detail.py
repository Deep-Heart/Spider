# -*- coding: utf-8 -*-
from datetime import datetime

from scrapy import Selector
from scrapy_redis.spiders import RedisSpider

from base.items import BaseDetailItem


class JiqizhixinDetailSpider(RedisSpider):
    name = "jiqizhixin_detail"
    allowed_domains = ["jiqizhixin.com"]
    start_urls = ['http://jiqizhixin.com']

    redis_key = 'jiqizhixin'

    custom_settings = {
        'ITEM_PIPELINES': {'machine_heart.pipelines.JiqizhixinDetailPipeline': 300}
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

        item['article_content'] = ''
        article_content = hxs.xpath('//div[@class="al-article-content"]//p//text()').extract()
        for content in article_content:
            item['article_content'] += content

        author = hxs.xpath(
            '//div[@class="al-send-msg-to-anchor Smohan_FaceBox al-clearfix"]//h2//text()').extract_first()
        item['author'] = author
        author_id = hxs.xpath('//div[@class="al-article-authon-header-img"]//a//attribute::href').extract_first()
        author_id = str(author_id).split('/')[-1]
        item['author_id'] = author_id
        author_icon = hxs.xpath('//div[@class="al-article-authon-header-img"]//a//img//attribute::src').extract_first()
        item['author_icon'] = author_icon

        yield item

    def make_request_from_data(self, data):
        url = data.decode('utf-8')
        if '://' in url:
            return self.make_requests_from_url(url)
        else:
            self.logger.error("Unexpected URL from '%s': %r", self.redis_key, data)
