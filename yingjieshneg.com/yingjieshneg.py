# coding = utf-8
import requests, pymysql, json
import time
from fake_useragent import UserAgent
import time, request
from multiprocessing import Pool
import re
import pandas as pd
from datetime import datetime, timedelta
from lxml import etree

date = (datetime.now() - timedelta(days=0)).strftime('%Y-%m-%d')

# date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
ua = UserAgent()


def get_data(url):
    print(url)

    res = requests.get(url, headers={"User-Agent": ua.chrome})
    res.encoding = 'gb2312'
    company_pattern = re.compile(
        'class="jobli".*?<a href="(.*?)" target="_blank"(.*?)</a>.*?<td width="100">.*?span(.*?)</span>', re.S)
    items = re.findall(company_pattern, res.text)
    content = []
    for item in items:
        dataset = {}
        if len(item[2]) > 1 and str(item[2][1:].strip()) == str(date):
            time_ = item[2][1:]
        else:
            continue

        if len(item[0]) > 1:
            if "http" not in item[0]:
                company_url = "http://www.yingjiesheng.com" + item[0]
            else:
                company_url = item[0]
        else:
            continue
        dataset['url'] = company_url
        print(company_url)

        job_content = requests.get(company_url, headers={"User-Agent": ua.chrome})
        if job_content.status_code == 200:
            job_content.encoding = 'gb2312'
            html = etree.HTML(job_content.text)
            jobs = html.xpath("//div[@class='info clearfix']/ol/li/u/text()")
            try:
                job = jobs[-1].replace('<em class="icontop">置顶</em>"', '').strip()
            except:
                job = ""
            des_list = html.xpath("//div[@class='jobIntro']/div//text()")
            if len(des_list) == 0:
                des = ''
            else:
                des = ''
                for i in des_list:
                    i = i.strip().replace("\n", "").replace(" ", "")
                    des = des + " " + i
            print(des)

        else:
            job = ""
            des = ""

        dataset['company'] = item[1][1:].replace('<em class="icontop">置顶</em>','').replace("&nbsp;","").strip() if len(item[1]) > 1 else ''
        dataset["job"] = job
        dataset["des"] = des
        dataset['time'] = (datetime.now() - timedelta(days=0)).strftime('%d/%m/%Y')
        print("*" * 10)
        print(dataset)
        content.append(dataset)
    time.sleep(5)
    # print(content)
    return content


def write_to_file(content):
    df = pd.DataFrame(content)
    time.time()
    df.to_csv(f'{date}_company.csv', index=False, mode='a+', header=False)


def run(page):
    url = f"http://www.yingjiesheng.com/commend-fulltime-{page}.html"
    data = get_data(url=url)
    write_to_file(data)


def run2(page):
    url = f"http://www.yingjiesheng.com/commend-parttime-{page}.html"
    data = get_data(url=url)
    write_to_file(data)


def quchong():
    data = pd.read_csv(f'{date}_company.csv')
    data.columns = ["目标网页", "公司信息", "招聘岗位", "职位描述", "发布日期"]
    a = data.drop_duplicates(subset=['目标网页'], keep='first')
    a.to_csv(f'{date}_company.csv', index=False)


if __name__ == '__main__':
    start = time.time()
    pool = Pool()
    pool.map(run, [i for i in range(1, 8)])
    pool.map(run2, [i for i in range(1, 8)])
    quchong()

    print('花费时间:', time.time() - start)
