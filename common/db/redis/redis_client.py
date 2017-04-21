import redis
from scrapy.conf import settings

from .redis_constant import RedisConstant


class RedisClient(object):
    def __init__(self):
        super(RedisClient, self).__init__()
        host = settings[RedisConstant.REDIS_HOST]
        port = settings[RedisConstant.REDIS_PORT]

        if host is None or port is None:
            raise ValueError

        self.redis = redis.Redis(host, port, db=0)

    def rpush(self, key, value):
        self.redis.rpush(key, value)

    def sadd(self, key, value):
        self.redis.sadd(key, value)

    def lpop(self, key):
        return self.redis.lpop(key)
