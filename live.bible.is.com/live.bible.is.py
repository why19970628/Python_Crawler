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
from crawlerHelper import hash_str_to_md5

ua = UserAgent()


def handel_single_country(country_name_en, country_name_folder, country_name, result_path):
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
        page_content_hash_list = []
        for i in range(1, 35):
            txt_page_url = f'https://live.bible.is/bible/{country_name_en}/{part}/{i}?audio_type=audio'

            json_file = os.path.join(result_path, f"{country_name}.json")

            json_data = ''
            if os.path.exists(json_file):
                with open(json_file, 'r', encoding='utf8', newline='') as json_io:
                    data = json.load(json_io)
                    json_data = data
                    if txt_page_url in data.keys():
                        print(txt_page_url, '已存在！')
                        continue
            if failed > 2:
                print(country_name, '重定向地址, 结束', txt_page_url,)
                break
            try:
                print(txt_page_url)

                page_response, title = get_txt_content(txt_page_url)

                part_folder = os.path.join(country_name_folder, part)
                os.makedirs(part_folder, exist_ok=True)

                txt_save_path = os.path.join(part_folder, str(i) + '.txt')
                print(txt_save_path)

                page_content = get_txt_page(page_response, txt_save_path)

                # 链接重定向问题
                page_content_hash = hash_str_to_md5(page_content)
                # print('page_content_hash', page_content_hash)
                if page_content_hash not in page_content_hash_list:
                    page_content_hash_list.append(page_content_hash)
                else:
                    failed += 1

                dict_ = {
                    txt_page_url: [
                        i,
                        title,
                        part,
                        page_content
                    ]
                }

                if os.path.exists(json_file):
                    with open(json_file, 'r', encoding='utf8', newline='') as json_io:
                        data = json.load(json_io)
                        data.update(dict_)
                        with open(json_file, 'w', encoding='utf8') as json_file:
                            json.dump(data, json_file, indent=2,
                                      ensure_ascii=False)

                else:
                    with open(json_file, 'w', encoding='utf8') as json_file:
                        json.dump(dict_, json_file, indent=2,
                                  ensure_ascii=False)
                time.sleep(0.5)

            except Exception as e:
                print(e)


def get_txt_content(txt_page_url):
    page_response = requests.get(txt_page_url, headers={
        "User_Agent": ua.chrome})
    title = re.findall(
        'book-chapter-text">(.+)</h1', page_response.text)[0]
    title = title.strip()# .split(" ")[0]

    return page_response, title


def get_txt_page(response, txt_save_path):
    # print(response.text)
    tree = etree.HTML(response.text)
    # page_content = tree.xpath('//*[@id="text-container-parent"]/div/main/div[1]/div/p/span/text()')
    page_content_list = tree.xpath('//div//text()')
    page_content = '' .join(page_content_list)
    cut_list = ['\xa0', '']
    for i in cut_list:
        page_content = re.sub(i, '', page_content)
    page_content.replace(
        "Copyrighted Material|Learn More©Bible.is, a ministry ofFaith Comes By Hearing®.Terms and Conditions", "")

    # print(page_content)
    with open(txt_save_path, 'w', encoding='utf8', newline='') as txt_io:
        txt_io.write(page_content)

    return page_content


names = ['瑞典语', '土耳其语', '高棉语', '希腊语', '波兰语', '匈牙利语', '阿拉伯语','菲律宾语', '马来语', 
         '老挝语', '豪萨语', '荷兰语', '尼泊尔语', '泰米尔语']

links = ['SWESFV', 'TURBLI', 'KHMBSC', 'ELLAPE', 'POLNCV', 'HUNHUN', 'ARBWTC', 'TGLPBS', 'ZLMAVB', 
         'LAOUBS', 'HAUCLV', 'NLDHSV', 'NPINRV', 'TAMWTC']


names = names + ['乌尔都语', '泰卢固语', '乌兹别克语', '哈萨克语-国外', '蒙语-新蒙',
                 '塔吉克语', '土库曼语', '希伯来语', '罗马尼亚语', '阿塞拜疆语', '孟加拉语', '西班牙语']

links = links + ['URDWTC', 'TELWTC', 'UZNIBT', 'KAZKAZ', 'KHKNTP',
                 'TGKIBT', 'TUKIBT', 'HEBM95', 'RONCORN', 'AZBEMV', 'BENWTC', 'SPABDA']

# https://live.bible.is/bible/KHMBSC/MAT/1
names = names[10:]
links = links[10:]

# https://live.bible.is/bible/TGLPBS/MAT/1?audio_type=audio
# links = 'view-source:https://live.bible.is/bible/SWESFV/1TH/1'


def get_language_links(result_path):
    for index, link in enumerate(links):
        print(index, names[index].strip(), link.strip())
        country_name = names[index].strip()
        # 每个国家语言的链接
        country_name_folder = os.path.join(result_path, country_name)
        handel_single_country(link, country_name_folder,
                              country_name, result_path)
        time.sleep(5)


def process():
    result_path = '/Volumes/Elements/数据交付/bible'
    os.makedirs(result_path, exist_ok=True)
    get_language_links(result_path)


if __name__ == '__main__':
    process()
