import pymongo, sys

class VideoStore(pymongo.MongoClient):
  def __init__(self, *args, **kwargs):
    url = kwargs.pop('url')
    pymongo.MongoClient.__init__(self, url)
    self.db = self[kwargs['db']]
    self.collection = self[kwargs['collection']]

  @classmethod
  def from_crawler(cls, crawler):
    settings = crawler.settings
    return cls(url = settings.get('MONGODB_URL'), db = settings.get('VIDEO_DB'), collection = settings.get('VIDEO_COLLECTION'))


  def item_scraped(self, item, spider):
    print('****')
    sys.exit(0)
  