# -*- coding:utf-8 -*-
import requests
import re
import json
from multiprocessing import Pool



def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


import pandas as pd

def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',
        re.S)
    items = re.findall(pattern, html)
    #print(items)
    content = []
    for item in items:
        dataset = {}
        dataset['index']=item[0]
        print(dataset['index'])
        dataset['image']=item[1]
        dataset['title']=item[2].strip()
        dataset['actor']=item[3].strip()[3:] if len(item[3]) > 3 else ''
        dataset['time'] =item[4].strip()[5:] if len(item[4]) > 5 else ''
        dataset['score']=item[5].strip() + item[6].strip()
        content.append(dataset)
    return content



def write_to_file(content):
    df = pd.DataFrame(content)
    #print(df.index)
    df.to_csv('maoyan.csv',index=False,mode='a+')

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    data=parse_one_page(html)
    write_to_file(data)

import time
if __name__ == '__main__':

    start=time.time()
    pool=Pool()

    pool.map(main,[i*10 for i in range(10)])
    # for i in range(10):
    #     main(offset=i * 10)

    print('花费时间:',time.time()-start)