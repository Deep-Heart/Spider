import scrapy


class BaseUrlItem(scrapy.Item):
    url = scrapy.Field()


class BaseDetailItem(scrapy.Item):
    _id = scrapy.Field()
    class_title = scrapy.Field()
    article_title = scrapy.Field()
    publish_time = scrapy.Field()
    article_tag = scrapy.Field()
    article_content = scrapy.Field()
    article_type = scrapy.Field()
    author_id = scrapy.Field()
    author = scrapy.Field()
    author_icon = scrapy.Field()

ARTICLE_TITLE = 1
ARTICLE_CONTENT = 2
ARTICLE_LINK = 3
