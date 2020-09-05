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
from crawlerHelper import con_redis, download, callback
admin = 'https://www.voaswahili.com/navigation/allsites?withmediaplayer=1'

ua = UserAgent()



# https://av.voanews.com/clips/VKE/2020/09/02/20200902-220000-VKE076-program_hq.mp3?download=1
# https://av.voanews.com/clips/VKE/2020/09/01/20200901-220000-VKE076-program_hq.mp3?download=1

# '\nEnglish\n',
# 'https://www.voanews.com',

used_name = ['\nLearning English\n', ]
used_link = ['https://learningenglish.voanews.com', ]

no_usename = ['\nShqip\n', ]
no_link = ['https://www.zeriamerikes.com']


# names = ['\nBosanski\n', '\nΕλληνικά\n', '\nМакедонски\n', '\nSrpski\n', '\nУкраїнська\n', '\nՀայերեն\n', '\nAzerbaijani\n', '\nქართული\n', '\nРусский\n', '\nBurmese\n', '\n粤语\n', '\n中文\n', '\nBahasa Indonesia\n', '\nខ្មែរ\n', '\nKhmer\n', '\n한국어\n', '\nລາວ\n', '\nไทย\n', '\nབོད་ཡིག\n', '\nTibetan\n', '\nTiếng Việt\n', '\nO‘zbek\u200e\n',
#          '\nবাংলা\n', '\nدری\n', '\nپښتو\n', '\nوی او اې ډيوه ريډیو\n', '\nاردو\n', '\nAfaan Oromoo\n', '\nአማርኛ\n', '\nBambara\n', '\nFrançais\n', '\nHausa\n', '\nKinyarwanda / Kirundi\n', '\nLingala\n', '\nNdebele\n', '\nPortuguês\n', '\nShona\n', '\nSoomaaliga\n', '\nKiswahili\n', '\nትግርኛ\n', '\nZimbabwe\n', '\nفارسی\n', '\nكوردی\n', '\nKurdi\n', '\n\u200eTürkçe\n', '\nCreole\n', '\n\u200eEspañol\n']
# links = ['https://ba.voanews.com', 'https://gr.voanews.com', 'https://mk.voanews.com', 'https://www.glasamerike.net', 'https://ukrainian.voanews.com', 'https://www.amerikayidzayn.com', 'https://www.amerikaninsesi.org', 'https://www.amerikiskhma.com', 'https://www.golos-ameriki.ru', 'https://burmese.voanews.com', 'https://www.voacantonese.com', 'https://www.voachinese.com', 'https://www.voaindonesia.com', 'https://khmer.voanews.com', 'https://www.voacambodia.com', 'https://www.voakorea.com', 'https://lao.voanews.com', 'https://www.voathai.com', 'https://www.voatibetan.com', 'https://www.voatibetanenglish.com', 'https://www.voatiengviet.com', 'https://www.amerikaovozi.com',
#          'https://www.voabangla.com', 'https://www.darivoa.com', 'https://www.pashtovoa.com', 'https://www.voadeewanews.com', 'https://www.urduvoa.com', 'https://www.voaafaanoromoo.com', 'https://amharic.voanews.com', 'https://www.voabambara.com', 'https://www.voaafrique.com', 'https://www.voahausa.com', 'https://www.radiyoyacuvoa.com', 'https://www.voalingala.com', 'https://www.voandebele.com', 'https://www.voaportugues.com', 'https://www.voashona.com', 'https://www.voasomali.com', 'https://www.voaswahili.com', 'https://tigrigna.voanews.com', 'https://www.voazimbabwe.com', 'https://ir.voanews.com', 'https://www.dengiamerika.com', 'https://www.dengeamerika.com', 'https://www.amerikaninsesi.com', 'https://www.voanouvel.com', 'https://www.voanoticias.com']

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

    for i in range(60, -1, -1):
        days = today - datetime.timedelta(days=i)
        result = days.strftime("%Y/%m/%d")
        result2 = days.strftime("%Y-%m-%d")
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
    # try:
    response = requests.get(vedio_page_link, headers={
                            "User_Agent": ua.chrome})
    tree = etree.HTML(response.text)
    try:
        vedio_href = tree.xpath(
            '//*[@id="content"]/div[2]/div/div/div/div[4]/div/div[2]/div/div/ul/li[2]/a/@href')[0]
        vedio_name = tree.xpath(
            '//*[@id="content"]/div[2]/div/div/div/div[1]/h1/text()')[0]
    except Exception as e:
        vedio_href = tree.xpath(
            '//*[@id="content"]/div[2]/div/div/div/div[4]/div/div[2]/div/div/ul/li/a/@href')[0]
        vedio_name = tree.xpath(
            '//*[@id="content"]/div[2]/div/div/div/div[1]/h1/text()')[0]
    time_str = str(time.time())

    # print(vedio_href, vedio_name)
    vedio_save_path_name = os.path.join(
        vedio_save_path, vedio_name.strip() + f'_{time_str}' + ".mp3")
    save_list = vedio_save_path_name.split('/')
    result = save_list[-3] + '/' + save_list[-2] + '/' + save_list[-1]
    print('链接:', vedio_href, '保存:',  vedio_save_path_name)

    con_redis().lpush('country', json.dumps({vedio_href: result}))  # 输出的结果是1

    try:
        download(
            vedio_href, vedio_save_path_name, callback)
    except Exception as e:
        print(e)


def get_video_by_date(response, country_admin_link, country_name_folder, folder_date_name):
    tree = etree.HTML(response.text)
    vedio_page_urls = tree.xpath(
        '//*[@id="content"]/div/div/div/div[2]/div[3]/div/div/div/div[2]/a/@href')
    # ['/a/5486855.html', '/a/5487137.html']
    # print(vedio_page_urls)
    if len(vedio_page_urls) > 0:
        vedio_save_path = os.path.join(country_name_folder, folder_date_name)
        os.makedirs(vedio_save_path, exist_ok=True)
        for vedio_page in vedio_page_urls:
            # 音频页面url
            vedio_page_link = country_admin_link + vedio_page
            print('音频页面url', vedio_page_link)
            try:
                download_vedio(vedio_page_link, vedio_save_path)
                time.sleep(0.5)
            except Exception as e:
                print('下载错误', e)
            time.sleep(1)


def handel_single_country(single_language_url, country_admin_link, country_name_folder, country_name):
    response = requests.get(single_language_url, headers={
        "User_Agent": ua.chrome})
    time_lists, time_lists2 = get_time_list()
    no_redict_url = response.url
    # print(no_redict_url)
    # 拼接国家 每个日期的链接
    count = 1
    for index, url_suffix in enumerate(time_lists):
        if count > 10:
            break
        if no_redict_url == 'https://www.voanews.com/radio/schedul':
            no_redict_url = 'https://www.voanews.com/radio/schedul/46'
        current_url = no_redict_url + '/' + url_suffix
        print(f'当前国家: {country_name}, 日期:', url_suffix)
        # print('        音频链接:', current_url)
        # 获取每个国家/每个日期/所有音频链接 res
        result = handel_single_country_date(current_url)
        # print(result)
        if result != 1:
            # 获取每个日期的音频
            try:
                get_video_by_date(result, country_admin_link,
                                  country_name_folder,  time_lists2[index])
                time.sleep(2)
            except Exception as e:
                print('获取日期链接出错', e)
        else:
            print('无音频, 请检查音频地址: ==>', current_url)
            count = count + 1
        time.sleep(1)


def get_language_links(result_path):
    for index, link in enumerate(links):
        print(index, names[index].strip(), link.strip())
        country_name = names[index].strip()
        single_language_url = link.strip() + '/radio/schedul'
        # 每个国家语言的链接
        country_name_folder = os.path.join(result_path, country_name)
        handel_single_country(single_language_url, link,
                              country_name_folder, country_name)
        time.sleep(5)


def process():
    result_path = '/Volumes/Elements/中科大'
    get_language_links(result_path)


if __name__ == '__main__':
    # result_path = sys.argv[1]
    process()
    # handel_single_country()
