import redis
from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint


class RedisURLFilter(BaseDupeFilter, redis.StrictRedis):

  def __init__(self, *args, **kwargs):
    self.key = kwargs.pop('key', 'Crawl::redisURLDupeKey')
    redis.StrictRedis.__init__(self, **kwargs)

  @classmethod
  def from_settings(cls, settings):
    return cls(host = settings.get('REDIS_HOST'), port = settings.getint('REDIS_PORT'), password = settings.get('REDIS_PASSWORD'))

  def request_seen(self, request):
    fp = request_fingerprint(request)
    return self.sadd(self.key, fp)