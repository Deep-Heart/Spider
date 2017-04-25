from apscheduler.schedulers.background import BackgroundScheduler
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from scrapy.spiders import CrawlSpider


class KeepSpider(CrawlSpider):
    DEFAULT_IDLE = 3

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.idle_time = kw.pop('idle_time', self.DEFAULT_IDLE)
        self.idle_counter = self.idle_time

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(KeepSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider

    def spider_idle(self):
        self.log('---------- ' + self.name + ' spider idle --------------')

        if self.idle_counter >= self.idle_time:
            self.idle_counter = 0
            self.spider_idle_action()
        else:
            self.idle_counter += 1

        raise DontCloseSpider

    def spider_idle_action(self):
        raise NotImplementedError()


class SchedulerSpider(KeepSpider):
    def __init__(self, interval_arg, *a, **kw):
        super().__init__(*a, **kw)
        self.init_task_scheduler(interval_arg)

    def init_task_scheduler(self, interval_arg):
        if interval_arg is not None and isinstance(interval_arg, dict):
            self.scheduler = BackgroundScheduler()
            self.scheduler.add_job(self.schedule_next_requests, 'interval', **interval_arg)
            try:
                self.scheduler.start()
            except KeyboardInterrupt:
                self.scheduler.shutdown()

    def schedule_next_requests(self):
        for req in self.start_requests():
            if req is not None:
                self.crawler.engine.crawl(req, spider=self)

    def spider_idle_action(self):
        pass

