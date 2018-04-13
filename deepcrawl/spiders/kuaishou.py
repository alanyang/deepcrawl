# -*-coding:utf-8-*-
# author : Corleone
from urllib.request import urlopen, Request
import urllib
import json,os,re,socket,time,sys, hashlib
import threading
import logging
import queue, time

logger = logging.getLogger("AppName")
formatter = logging.Formatter('%(asctime)s %(levelname)-5s: %(message)s')
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

video_q = queue.Queue()

def get_video():
    url = "http://101.251.217.210/rest/n/feed/hot?app=0&lon=121.372027&c=BOYA_BAIDU_PINZHUAN&sys=ANDROID_4.1.2&mod=HUAWEI(HUAWEI%20C8813Q)&did=ANDROID_e0e0ef947bbbc243&ver=5.4&net=WIFI&country_code=cn&iuid=&appver=5.4.7.5559&max_memory=128&oc=BOYA_BAIDU_PINZHUAN&ftt=&ud=0&language=zh-cn&lat=31.319303"
    data = {
        'type': '7',
        'page': '2',
        'coldStart': 'false',
        'count': '20',
        'pv': 'false',
        'id': '5',
        'refreshTimes': '4',
        'pcursor': '1',
        'os': 'android',
        'client_key': '3c2cd3f3',
        'sig': '22769f2f5c0045381203fc57d1b5ad9b'
    }
    req = Request(url)
    req.add_header("User-Agent", "kwai-android")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    params = urllib.parse.urlencode(data).encode("utf-8")
    try:
        html = urlopen(req, params).read()
    except:
        html = urlopen(req, params).read()
    result = json.loads(html)
    logger.info(len(result['feeds']))
    for x in result['feeds']:
        try:
            name = x['caption'].replace("\n","")
            logger.info(name)
        except KeyError:
            pass


def main():
    while True:
        get_video()
        time.sleep(1)


if __name__ == '__main__':
    main()