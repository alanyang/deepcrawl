# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DeepcrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class VideoItem(scrapy.Item):
    video_id  = scrapy.Field()
    video_url = scrapy.Field()
    covers    = scrapy.Field()
    author    = scrapy.Field()
    published = scrapy.Field()

class DouyinItem(VideoItem):
    music         = scrapy.Field()
    dynamic_cover = scrapy.Field()
    description   = scrapy.Field()
    stat          = scrapy.Field()

    