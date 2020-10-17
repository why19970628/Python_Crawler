import os
import re
import json
import requests
from fake_useragent import UserAgent
from crawler.crawlerHelper import save_json
ua = UserAgent()

def storage(message, format_text):
    dicts = {
        "source_id": int(message["guid"]),
        "source_url": "cn.haiwainet.opa",
        "newsType": "news",
        "title": message["title"],
        "release_time": message["pubtime"],
        "create_time": message["pubtime"],
        "format_text": format_text,
        "article_url": message["link"],
        "image_urls": message['image_urls'],
        "source": "海外网",
    }
    print(dicts)
    base_path = '/Users/stardust/Downloads/数据交付/新华社图片/人民日报海外'
    json_file_path = os.path.join(base_path, dicts['title'] + '.json')
    save_json(json_file_path, dicts)


def download(html, message):
    pattern = re.compile('\d+-\d+-\d+ \d+:\d+:\d+[\s\S]*?</div>')
    exist = re.findall(pattern, html)
    if not exist:
        return
    pattern = re.compile('海外网')
    source = re.findall(pattern, exist[0])
    if not source:
        return
    pattern = re.compile('(<div class="c mlr20" id="cen">)([\s\S]*?)(</div>)')
    format_text = re.findall(pattern, html)
    if format_text:
        format_text = format_text[0][1]
    else:
        pattern = re.compile('(<div class="contentMain">)([\s\S]*?)(</div>)')
        format_text = re.findall(pattern, html)[0][1]
    format_text = re.sub('<div[\s\S]*?>', " ", format_text)
    format_text = re.sub('</div>', " ", format_text)
    image_urls = re.findall('img src="(.*?)" ', format_text)
    domain_image = 'http://statics.haiwainet.cn/images/logoS.jpg'
    if domain_image in image_urls:
        image_urls.remove('http://statics.haiwainet.cn/images/logoS.jpg')
    message['image_urls'] = image_urls
    storage(message, format_text)



def connect(message):
    url = message["link"]
    response = requests.get(url, headers={"User_Agent": ua.chrome})
    response.encoding = "utf-8"
    if response.status_code == 200:
        html = response.text
        download(html, message)
    else:
        return True


def getURL(html):
    data = json.loads(html)
    msg = data["result"]
    for message in msg:
        number = int(message["guid"])
        # if rechecking(number, source_url="cn.haiwainet.opa"):
        #     return True
        mistake = connect(message)
        if mistake:
            return True


def starts():
    n = 1
    while True:
        url = "http://opa.haiwainet.cn/apis/news?catid=3541093&num=10&page=" + str(n)
        response = requests.get(url, headers={"User_Agent": ua.chrome})
        response.encoding = "utf-8"
        if response.status_code == 200:
            html = response.text
            mistake = getURL(html)
            if mistake:
                break
            n += 1
        else:
            break


if __name__ == '__main__':
    starts()