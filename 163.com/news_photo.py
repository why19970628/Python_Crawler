import threading
import time
import os
import re
import json
import requests
from selenium import webdriver
from multiprocessing.pool import Pool
from lxml import etree
from fake_useragent import UserAgent


# database config
ua = UserAgent()


# config chromedriver:
prefs = {
    'profile.default_content_setting_values': {
        'images': 2,
        # 'javascript': 2
        # 'User-Agent': ua
    }
}
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', prefs)
options.add_argument('--headless')

# 网易新闻图片分类url:
pic_tabs = [
    'http://news.163.com/photo/#Current',
    'http://news.163.com/photo/#Insight',
    'http://news.163.com/photo/#Week',
    'http://news.163.com/photo/#Special',

    'http://news.163.com/photo/#War',
    'http://news.163.com/photo/#Hk',
    'http://news.163.com/photo/#Discovery',
    'http://news.163.com/photo/#Paper',
]


# http://news.163.com/photo/#Current
def get_photo_source(url):
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    page_source = browser.page_source
    browser.close()
    response = requests.get(url)
    if response.status_code == 200:
        return page_source


def photo(tab_url):
    print(tab_url)
    folder = tab_url.replace("http://news.163.com/photo/#", "")
    json_dir = f"你的本地文件地址"
    os.makedirs(json_dir, exist_ok=True)
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(tab_url)

    while True:
        html_photo = browser.page_source
        # saveHtml(json_dir, html_photo.encode('utf-8'))

        pattern_photo = re.compile(
            '<div class="water-item"(.*?)</div></div>', re.S)
        result = re.findall(pattern_photo, html_photo)[0]

        # 文章链接
        article_par = re.compile('<a href="(.*?)" target', re.S)
        article_urls = re.findall(article_par, result)

        title_par = re.compile('<h3 title="(.*?)" data-title', re.S)
        titles = re.findall(title_par, result)

        image_par = re.compile('src="(.*?)" style', re.S)
        images = re.findall(image_par, result)

        for index, article_url in enumerate(article_urls):
            try:
                single = {
                    "title": titles[index],
                    "article_url": article_url,
                    "article_first_image_url": images[index]
                }
                print(article_url)
                if os.path.exists(os.path.join(json_dir, f'{single["title"]}.json')):
                    print("已存在！")
                    continue

                #获取文章详情
                res = requests.get(article_url, headers={"User_Agent": ua.chrome})
                image_info = re.compile('<textarea name="gallery-data" style="display:none;">(.*?)</textarea>', re.S)
                image_text = re.findall(image_info, res.text)[0]
                content = json.loads(image_text)
                single.update({"image_content":content})

                save_json(json_dir, single)
                time.sleep(3)
            except Exception as e:
                print(e)

        # 翻两页
        try:
            page_convert(browser)
            page_convert(browser)
        except Exception as e:
            print(e)

    browser.close()


def saveHtml(json_dir, file_content):
    # 注意windows文件命名的禁用符，比如 /
    with open(os.path.join(json_dir, "test.txt"), "w", encoding="utf-8") as f:
        # 写文件用bytes而不是str，所以要转码
        f.write(file_content)


def page_convert(browser):
    button = browser.find_element_by_xpath(
        '/html/body/div[2]/div[2]/div[1]/div[1]/a[2]')  # 翻页
    button.click()
    print('正在翻页------------')
    time.sleep(2)



def save_json(json_dir, data):
    # current_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    json_file = os.path.join(json_dir, f'{data["title"]}.json')
    print(json_file)
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def photospider():
    # n = 4
    # for i in range(0, len(pic_tabs), n):
    #     cut_pic_tabs = (pic_tabs[i:i+n])
    #     print(cut_pic_tabs)
    #     t = threading.Thread(target=photo, args=(cut_pic_tabs))  # 注意传入的参数一定是一个元组!
    #     t.start()

    pool = Pool(3)
    pool.map(photo, pic_tabs)


if __name__ == "__main__":
    photospider()
