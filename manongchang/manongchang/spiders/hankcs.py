# -*- coding: utf-8 -*-
import re
from scrapy import Selector, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from base.items import BaseUrlItem


class HankcsSpider(CrawlSpider):
    name = "hankcs"
    allowed_domains = ["hankcs.com"]
    start_urls = ['http://hankcs.com/']

    custom_settings = {
        'ITEM_PIPELINES': {'manongchang.pipelines.ManongchangPipeline': 300}
    }

    rules = [
        Rule(LinkExtractor(allow=('.html',)), callback='parse_html_url', follow=True),
    ]

    BASE_URL = 'base_url'

    def parse_start_url(self, response):
        hxs = Selector(response)

        topic_list = hxs.xpath('//ul[@class="site-nav site-navbar"]//a//@href').extract()
        for topic in topic_list:
            if str(topic).startswith('http://'):
                yield Request(topic, callback=self.parse_pages, meta={self.BASE_URL: topic})

        # 首页包含的所有url
        # generator = self.parse_pages(response)
        # for f in generator:
        #     yield f

    def parse_pages(self, response):
        hxs = Selector(response)

        page_info = hxs.xpath('//div[@class="pagination"]//ul//li//text()').extract()
        if len(page_info) > 0:

            page = re.search(re.compile('\d+'), str(page_info[-1])).group(0)

            if page is not None:
                base_url = response.meta[self.BASE_URL] if self.BASE_URL in response.meta else response.url
                for index in range(2, int(page)):
                    yield Request(base_url + '/page/' + str(index), callback=self.parse_index_page)

    def parse_html_url(self, response):
        yield self.create_url_item(response.url)

    def parse_index_page(self, response):
        pass

    @staticmethod
    def create_url_item(url):
        item = BaseUrlItem()
        item['url'] = url
        return item
