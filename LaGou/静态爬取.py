import json
import time
import requests
from bs4 import BeautifulSoup
import pprint
import pandas as pd
import random

# 定义抓取主函数
def lagou_dynamic_crawl():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Host': 'www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': None,
        'X-Requested-With': 'XMLHttpRequest'
    }

    # 创建一个职位列表容器
    positions = []
    # 30页循环遍历抓取
    start=time.time()
    for page in range(1,10):
        print('正在抓取第{}页...'.format(page))
        # 构建请求表单参数
        params = {
            'first': 'true',
            'pn': page,
            'kd': '数据挖掘'
        }

        # 构造请求并返回结果
        url1='https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false'
        url='https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput='
        s = requests.Session()  # 建立session
        s.get(url=url, headers=headers, timeout=3)
        cookie = s.cookies  # 获取cookie
        result = s.post(url=url1, headers=headers, data=params, cookies=cookie, timeout=3)#.text
        # 将请求结果转为json
        #pprint.pprint(result)
        json_result = result.json()
        #pprint.pprint(json_result)
        # 解析json数据结构获取目标信息
        position_info = json_result['content']['positionResult']['result']
        # 循环当前页每一个职位信息，再去爬职位详情页面
        for position in position_info:
            # 把我们要爬取信息放入字典
            result = {}

            result['position_name']=position['positionName']
            result['area']=position['district']
            result['work_year']=position['workYear']
            result['education']=position['education']
            result['salary']=position['salary']
            result['city']=position['city']
            result['pompany_name']=position['companyFullName']
            result['address']=position['businessZones']
            result['label']=position['companyLabelList']
            result['formatCreateTime'] = position['formatCreateTime']
            result['stage']=position['financeStage']
            result['size']=position['companySize']
            result['advantage']=position['positionAdvantage']
            result['industry']=position['industryField']
            result['industryLables']=position['industryLables']
            # 找到职位 ID
            result['position_id']=position['positionId']
            position_id= position['positionId']
            print(position_id)
            recruit_detail(position_id)
            # 根据职位ID调用描述函数获取职位JD
            result['position_detail'],result['link']= recruit_detail(position_id)
            positions.append(result)
            time.sleep(random.randint(4,7))
    df = pd.DataFrame(positions)
    df.to_csv('lagou1.csv', index=False)
    elapsed = (time.time() - start)
    print(elapsed)
    print('全部数据采集完毕。')


import re
# 定义抓取岗位描述函数
def recruit_detail(position_id):
    url = 'https://www.lagou.com/jobs/%s.html' % position_id

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01'
        ,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Host': 'www.lagou.com',
        'Referer':url
    }
    result = requests.get(url,headers = headers)
    time.sleep(1)
    # 解析职位要求text
    soup = BeautifulSoup(result.text, 'html.parser')
    job_jd = soup.find(class_="job-detail")

    # 通过尝试发现部分记录描述存在空的情况
    # 所以这里需要判断处理一下
    if job_jd != None:
        job_jd = ''.join(re.split('\s',job_jd.text))
        # print(job_jd)
        # job_jd = job_jd.text.strip().replace('<p>', '').replace('</p>', '').replace('<p>', '').replace('<span>', '').replace('</span>', '').replace('\t', '').replace('<', '').replace('<br>', '').replace('\n', '').replace('&nbsp;','').replace(' ','')
    else:
        job_jd = 'null'
        print('Null')
    return job_jd,url
    print(job_jd)
    print(url)

if __name__ == '__main__':
    lagou_dynamic_crawl()