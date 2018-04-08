# -*- coding: utf-8 -*-
import scrapy, re, json
from deepcrawl.items import DouyinItem
from deepcrawl.utils import atoi

class DouyinSpider(scrapy.Spider):
    name = 'douyin'
    allowed_domains = ['douyin.com', 'iesdouyin.com']
    start_urls = ['https://www.iesdouyin.com/aweme/v1/hot_aweme/?cursor=0&count=32&aweme_id=6539858082434911492']
    aweme_url = 'https://www.iesdouyin.com/aweme/v1/hot_aweme/?cursor=0&count={}&aweme_id={}'

    def __init__(self, *args, **kwargs):
        scrapy.Spider.__init__(self, *args, **kwargs)
        self.parse = self.parse_aweme

    def mobile_headers(self):
        return { 'User-Agent': self.settings.attributes.get('MOBILE_USER_AGENT', '').value }

    def video_url(self, id):
        return 'https://www.iesdouyin.com/share/video/' + id

    def __aweme_url__(self, id, count):
        return self.aweme_url.format(count, id)

    def __parse(self, resp):
        match = re.compile(r'var data = \[(.*?)\];')
        data = json.loads(match.findall(resp.text)[0])
        aweme = self.__aweme_url__(data['statistics']['aweme_id'], data['statistics']['play_count'])
        yield scrapy.Request(aweme, self.parse_aweme, headers=self.mobile_headers(), dont_filter=True)

    def parse_aweme(self, resp):
        data = json.loads(resp.text)
        for video in data['aweme_list']:
            aweme = self.__aweme_url__(video['statistics']['aweme_id'], video['statistics']['play_count'])
            item  = DouyinItem()
            cover = video['video']['cover']['url_list'][0]
            author = video['author']
            avator = dict(small = author['avatar_thumb']['url_list'][0], middle = author['avatar_medium']['url_list'][0], larger = author['avatar_larger']['url_list'][0])

            music = video['music']
            msc = music.get('cover_thumb', {}).get('url_list', [''])[0]
            mmc = music.get('cover_large', {}).get('url_list', [''])[0]
            mlc = music.get('cover_hd', {}).get('url_list', [''])[0]
            music_cover = dict(small = msc, middle = mmc, larger = mlc)


            item['video_id']  = video['statistics']['aweme_id']
            item['video_url'] = self.video_url(video['statistics']['aweme_id'])
            item['covers']    = dict(small = cover, middle = cover, larger = cover)
            item['author']    = {'uid': author['uid'], 'avator': avator, 'nick': author['nickname'], 'gender': author['gender'], 'signature': author['signature']}
            item['published'] = video['create_time']
            if music:
                item['music']     = dict(duration = music['duration'], cover = music_cover, name = music['music_name'], author = music['author_name'], mid = music['mid'])
            item['dynamic_cover'] = video['video']['dynamic_cover']['url_list'][0]
            item['description'] = video['desc']

            statistics = video['statistics']
            stat = dict( play = atoi(statistics['play_count']), comment = atoi(statistics['comment_count']), share = atoi(statistics['share_count']), digg = atoi(statistics['digg_count']))
            item['stat'] = stat

            yield item
            yield scrapy.Request(aweme, self.parse_aweme, headers=self.mobile_headers(), dont_filter=True)

