# -*- coding: utf8 -*-
import sys
import os
import requests
from lxml import etree
from fake_useragent import UserAgent
from urllib.parse import quote, urlencode
import urllib
import time
import string
version_links = ['hjb', 'ljb', 'bsd', 'rjb'] # 'sjb',
admin = 'https://www.yixuela.com/'
subject = 'yuwen/'

ua = UserAgent()


def get_url_link():
    for version in version_links:
        # 版本
        version_subject_url = admin + 'books/' + version + '/' + subject
        # 年级
        # for i in range(1,13):
        #     grade = f'g{i}/'
        # print(version_subject_url)
        yield version_subject_url, version


def crwal_artile_content(artitle_content_url, article_folder):
    """
    文章详情页爬取图片
    """
    response = requests.get(artitle_content_url, headers={
                            "User_Agent": ua.chrome})
    # print(response.text)
    tree = etree.HTML(response.text)
    image_name = tree.xpath(
        '/html/body/section/div[3]/div[1]/div[2]/img/@src')
    for index, name in enumerate(image_name):
        name = name.split('/')[-1]
        image_save_path = os.path.join(article_folder, name)
        ori_url = image_name[index]
        url = quote(ori_url, safe='/:?=')
        urllib.request.urlretrieve(url, image_save_path)
        print(f'{image_save_path} 爬取成功！')


def crwal_artile(content_link, result_folder):
    response = requests.get(content_link, headers={"User_Agent": ua.chrome})
    tree = etree.HTML(response.text)
    article_name = tree.xpath(
        '//div[@class="right-menu bg-white mt-10"]/nav/ul/li/a/text()')
    article_link = tree.xpath(
        '//div[@class="right-menu bg-white mt-10"]/nav/ul/li/a/@href')
    for index, name in enumerate(article_name):
        article_folder = os.path.join(result_folder, name)
        os.makedirs(article_folder, exist_ok=True)
        artitle_content_url = admin + article_link[index]
        try:
            crwal_artile_content(artitle_content_url, article_folder)
        except Exception as e:
            print(e)
        time.sleep(1)


def run(url, result_path, version):
    response = requests.get(url, headers={"User_Agent": ua.chrome})
    tree = etree.HTML(response.text)
    title = tree.xpath('//div[@class="list-warp"]/div//a/text()')
    title_link = tree.xpath('//div[@class="list-warp"]/div//a/@href')
    title_ = [i for i in title if len(i.replace(" ", '')) > 2]

    for index, title1 in enumerate(title_):
        content_link = admin + title_link[index * 2]
        result_folder = os.path.join(result_path, f'{version}/{title1}')
        os.makedirs(result_folder, exist_ok=True)
        try:
            crwal_artile(content_link, result_folder)
            time.sleep(2)
        except Exception as e:
            print(e)

    # if len(title_) != len(title_link):
    #     raise Exception('title length error')


def process(result_path):
    for url, version in get_url_link():
        print(url)
        run(url, result_path, version)
        time.sleep(5)


if __name__ == '__main__':
    result_path = sys.argv[1]
    process(result_path)
