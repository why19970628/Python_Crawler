# -*- coding: utf8 -*-
import re
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

ua = UserAgent()



def handel_single_country(country_name_en, country_name_folder, country_name):
    link = f'https://live.bible.is/bible/{country_name_en}/MAT/1?audio_type=audio'
    print(country_name_folder, link)
    response = requests.get(link, headers={
        "User_Agent": ua.chrome})

    tree = etree.HTML(response.text)
    vedio_page_urls = tree.xpath('/html/body/script[1]/text()')

    # chapter = re.findall('"testaments":(.*?),"audioType',
    #                      str(vedio_page_urls))[0]
    # chapter = eval(chapter)
    # parts = [k for k, v in chapter.items() if v == "NT"]

    chapters = re.findall(r'"\w{2,3}":"\w{2,3}"', str(vedio_page_urls))
    chapters = chapters[1:]
    parts = []
    for chapter in chapters:
        [k, v] = chapter.replace('"', '').split(':')
        if k not in parts and v == 'NT':
            parts.append(k)
    for part in parts:
        # success = 0
        failed = 0
        for i in range(1, 35):
            txt_page_url = f'https://live.bible.is/bible/{country_name_en}/{part}/{i}?audio_type=audio'
            if failed >= 5:
                break
            try:
                print(txt_page_url)
                page_response = requests.get(txt_page_url, headers={
                                        "User_Agent": ua.chrome})
                title = re.findall('book-chapter-text">(.+)</h1', page_response.text)[0]
                title = title.strip().split(" ")[0]
                part_folder = os.path.join(country_name_folder, title)
                os.makedirs(part_folder, exist_ok=True)


                txt_save_path = os.path.join(part_folder, str(i) + '.txt')
                print(txt_save_path)

                get_txt_page(page_response, txt_save_path)
                time.sleep(2)
            except Exception as e:
                failed += 1
                print(e)

def get_txt_page(response, txt_save_path):
    # print(response.text)
    tree = etree.HTML(response.text)
    # page_content = tree.xpath('//*[@id="text-container-parent"]/div/main/div[1]/div/p/span/text()')
    page_content_list = tree.xpath('//div//text()')
    page_content = '' .join(page_content_list)
    cut_list = ['\xa0', '']
    for i in cut_list:
        page_content = re.sub(i, '', page_content)
    page_content.replace("Copyrighted Material|Learn More©Bible.is, a ministry ofFaith Comes By Hearing®.Terms and Conditions", "")

    # print(page_content)
    with open(txt_save_path, 'w', encoding='utf8', newline='') as txt_io:
        txt_io.write(page_content)


names = ['瑞典语']

links = ['SWESFV']

# links = 'view-source:https://live.bible.is/bible/SWESFV/1TH/1'


def get_language_links(result_path):
    for index, link in enumerate(links):
        print(index, names[index].strip(), link.strip())
        country_name = names[index].strip()
        # 每个国家语言的链接
        country_name_folder = os.path.join(result_path, country_name)
        handel_single_country(link, country_name_folder, country_name)
        time.sleep(5)


def process():
    result_path = '/Volumes/Elements/数据交付/bible'
    os.makedirs(result_path, exist_ok=True)
    get_language_links(result_path)


if __name__ == '__main__':
    process()
