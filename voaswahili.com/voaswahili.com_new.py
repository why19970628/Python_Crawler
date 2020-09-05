# -*- coding: utf8 -*-
from functools import wraps
import datetime
import sys
import json
import os
import requests
from lxml import etree
from fake_useragent import UserAgent
from urllib.parse import quote, urlencode
import urllib
import time
import string
from crawlerHelper import con_redis, download, callback, download2
admin = 'https://www.voaswahili.com/navigation/allsites?withmediaplayer=1'

ua = UserAgent()

import socket
socket.setdefaulttimeout(10)

# https://av.voanews.com/clips/VKE/2020/09/02/20200902-220000-VKE076-program_hq.mp3?download=1
# https://av.voanews.com/clips/VKE/2020/09/01/20200901-220000-VKE076-program_hq.mp3?download=1

# 'https://av.voanews.com/clips/VKE/2020/08/31/20200831-133000-VKE076-program.mp3?download=1'


# '\nEnglish\n',
# 'https://www.voanews.com',

used_name = ['\nLearning English\n', ]
used_link = ['https://learningenglish.voanews.com', ]

no_usename = ['\nShqip\n', ]
no_link = ['https://www.zeriamerikes.com']


names = ['匈牙利', '克罗地亚', '高棉']
links = ['https://www.amerikayidzayn.com'
         'https://www.amerikiskhma.com',
         'https://www.voacambodia.com']

# links = links[12:]
# names = names[12:]


def get_time_list():
    today = datetime.datetime.now()
    date_list = []
    date_list2 = []

    for i in range(1, 600):
        days = today - datetime.timedelta(days=i)
        result = days.strftime("%Y/%m/%d")
        result2 = days.strftime("%Y%m%d")
        date_list.append(result)
        date_list2.append(result2)

    return date_list[::-1], date_list2[::-1]


def handel_single_country_date(current_url):
    for i in range(3):
        try:
            response = requests.get(current_url, headers={
                "User_Agent": ua.chrome})
        except Exception as err:
            print(f"错误信息:\t\t\t{err}")
            continue
        if response.status_code == 200:
            return response
        time.sleep(1)
    return 1


def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate), end='')
        sys.stdout.flush()


def cost(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print('花费', start - end, 's')
        return res

    return wrapper


@cost
def download_vedio(vedio_page_link, vedio_save_path):
    try:
        download(vedio_page_link, vedio_save_path, callback)
    except Exception as e:
        print(e)


def get_language_links(result_path):
    pass
    # for index, link in enumerate(links):
    #     print(index, names[index].strip(), link.strip())
    #     country_name = names[index].strip()
    #     single_language_url = link.strip() + '/radio/schedul'
    #     # 每个国家语言的链接
    #     country_name_folder = os.path.join(result_path, country_name)
    #     handel_single_country(single_language_url, link,
    #                           country_name_folder, country_name)
    #     time.sleep(5)


def process():
    time1, time2 = get_time_list()
    result_path = '/Volumes/Elements/中科大/高棉2'
    os.makedirs(result_path, exist_ok=True)

    for index, value in enumerate(time1):
        url = f'https://av.voanews.com/clips/VKE/{value}/{time2[index]}-220000-VKE076-program.mp3?download=1'
        print(url)

        save_path = os.path.join(result_path, f'{time2[index]}.mp3')
        download_vedio(url, save_path)


if __name__ == '__main__':
    # result_path = sys.argv[1]
    process()
    # handel_single_country()
