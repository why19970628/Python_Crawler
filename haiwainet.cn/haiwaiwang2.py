'''
http://news.haiwainet.cn/
海外网原创新闻信息爬取
'''
import os

from config import *
import requests
import time, datetime
import random
import re
import json
import redis
import hashlib
from pyquery import PyQuery as pq
from crawler.crawlerHelper import save_json


BASE_URL = 'http://opa.haiwainet.cn/apis/news'


# 链接redis数据库
headers = {
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36', }
# 当前日期
date = datetime.datetime.now().strftime('%Y-%m')


def get_md5(url):
    '''把目标url进行哈希'''
    md5 = hashlib.md5()
    md5.update(url.encode('utf-8'))
    return md5.hexdigest()


def news_url(pages=0):
    '''获取详细新闻的链接'''
    while True:
        pages += 1
        s_time = str(int(time.time() * 1000))
        params = {
            'catid': '3541093',
            'num': '10',
            'page': pages,
            'moreinfo': '1',
            'relation': '1',
            'format': 'jsonp',
            'callback': 'jQuery11020' + str(''.join(random.choice('0123456789') for i in range(16))) + '_' + s_time,
            '_': str(int(s_time) + random.randint(1, 5))
        }
        response = requests.get(BASE_URL, headers=headers, params=params)
        result = re.search('"result":(.*?)}\);', response.text).group(1)
        res = json.loads(result)
        for item in res:
            news_time = datetime.datetime.strptime(item['pubtime'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m')
            # 判断是不是当月的数据，不是则返回False
            # if date != news_time:
            #     return False

            # res = red.sadd(SET_URL, get_md5(item['link']))  # 注意是 保存set的方式
            # if res == 0:  # 若返回0,说明插入不成功，表示有重复
            #     continue
            # else:
            yield item['link']


def news_info(url):
    '''对新闻网站进行解析，提取数据'''
    doc = pq(url, encoding='utf-8')
    time.sleep(random.random())
    title = doc('.show_wholetitle').text()
    date = doc('span.first').text()
    n_source = doc('div.contentExtra span:contains(来源)')
    source = n_source.text().split('：')[1] if n_source else '无'
    content = doc('div.contentMain p').text()
    point = doc('div.summary')
    digested = point.text() if point else '无'
    images = doc('div.contentMain p img[src^="http"]')
    image_url = re.findall('img src="(.*?)" ', str(images))
    return {
        'title': title,
        'digested': digested,
        'date': date,
        'source': source,
        'content': content,
        'image_urls': image_url,
        'url': url
    }




def main():
    for item in news_url():
        data = news_info(item)
        base_path = '/Users/stardust/Downloads/数据交付/新华社图片/人民日报海外'
        json_file_path = os.path.join(base_path, data['title'] + '.json')
        print(json_file_path)
        save_json(json_file_path, data)
if __name__ == '__main__':
    main()