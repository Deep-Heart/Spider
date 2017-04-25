# -*- coding: utf-8 -*-
import json

from scrapy import Request, Selector, FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from base.base_spider import SchedulerSpider
from base.items import BaseUrlItem


class JiqizhixinSpider(SchedulerSpider):
    name = "jiqizhixin"
    allowed_domains = ["jiqizhixin.com"]
    base_url = 'http://jiqizhixin.com'
    start_urls = [base_url]

    custom_settings = {
        'ITEM_PIPELINES': {'machine_heart.pipelines.MachineHeartPipeline': 300}
    }

    more_url = base_url + '/portal/index/more'

    rules = [
        Rule(LinkExtractor(allow=('/article/*',)), callback='parse_article'),
    ]

    def __init__(self, *a, **kw):
        super().__init__({'hours': 3}, *a, **kw)

    def parse_start_url(self, response):
        hxs = Selector(response)

        class_link = hxs.xpath('//ul[@class="am-menu-nav am-avg-sm-1"]//li//a//@href').extract()
        print(class_link)
        for link in class_link:
            if str(link).find(self.base_url) > 0:
                yield Request(link, callback=self.request_page)
            else:
                yield Request(self.base_url + link, callback=self.request_page)

        yield self.create_more_request(1)

    def create_more_request(self, p):
        index = {'p': str(p)}
        return FormRequest(self.more_url, callback=self.request_more,
                           method='POST', formdata=index, meta=index)

    def parse_article(self, response):
        yield self.create_url_item(response.url)

    def request_more(self, response):
        try:
            result = json.loads(response.body.decode('utf-8'))
            for article in result['list']:
                yield self.create_url_item(self.base_url + article['url'])

            if result['last_page'] is False:
                yield self.create_more_request(int(response.meta['p']) + 1)
        except Exception as e:
            print(e)

    def create_url_item(self, url):
        item = BaseUrlItem()
        item['url'] = url
        return item

    def request_page(self, response):
        print(response.url)

        hxs = Selector(response)
        pages = hxs.xpath('//div[@class="al-turnpage"]//a//@href').extract()

        last_page = str(pages[-1])
        last_index = int(last_page.split('/')[-1])
        index_prefix = last_page[0: last_page.rindex('/') + 1]

        for index in range(2, last_index):
            yield Request(self.base_url + index_prefix + str(index))
