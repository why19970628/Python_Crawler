# import pandas as pd
# data=pd.read_csv('cleaned.csv')
# data=pd.DataFrame(data)
# area=data.groupby(by='area',axis=0).mean()['price']
# area=area
#
# #print(data.loc[:,'price'].mean())
# #area=data.groupby(by='area')['price']
# print(area)
import requests
from lxml import etree
import pandas as pd
from time import sleep
import random

# cookie
cookie = '你的cookie'
# headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    # 'cookie':cookie
}

# sleep(random.randint(3, 10))
#url = 'https://www.lagou.com/zhaopin/'
#res = requests.get(url, headers=headers)
#print(res.text)

#print('正在抓取第{}页...'.format(i), url)
# 查看网页结构循环页数进行采集
for i in range(1, 2):
    sleep(random.randint(3, 10))
    url = 'https://www.lagou.com/zhaopin/jiqixuexi/{}/?filterOption=3'.format(i)
    res =requests.get(url,headers = headers)
    #print(res.text)
    print('正在抓取第{}页...'.format(i), url)
    # 请求网页并解析
    con = etree.HTML(requests.get(url=url, headers=headers).text)
    # 使用xpath表达式抽取各目标字段
    job_name = [i for i in con.xpath("//a[@class='position_link']/h3/text()")]
    job_address = [i for i in con.xpath("//a[@class='position_link']/span/em/text()")]
    job_company = [i for i in con.xpath("//div[@class='company_name']/a/text()")]
    job_salary = [i for i in con.xpath("//span[@class='money']/text()")]
    job_exp_edu = [i for i in con.xpath("//div[@class='li_b_l']/text()")]
    job_exp_edu2 = [i for i in [i.strip() for i in job_exp_edu] if i != '']
    job_industry = [i.strip() for i in con.xpath("//div[@class='industry']/text()")]
    job_tempation = [i for i in con.xpath("//div[@class='list_item_bot']/div[@class='li_b_r']/text()")]
    job_links = [i for i in con.xpath("//div[@class='p_top']/a/@href")]
    print(job_links)

    # 获取详情页链接后采集详情页岗位描述信息
    job_des =[]
    for link in job_links:
        sleep(random.randint(3, 10))
        print('link:',link)
        con2 = etree.HTML(requests.get(url=link, headers=headers).text)
        #print(con)
        des = [[i for i in con2.xpath("//dd[@class='job_bt']/div/p/text()")]]
        job_des += des
    #print(job_des)
    break #遍历一次

# 对数据进行字典封装
dataset = {
    '岗位名称': job_name,
    '工作地址': job_address,
    '公司': job_company,
    '薪资': job_salary,
    '经验学历': job_exp_edu2,
    '所属行业': job_industry,
    '岗位福利': job_tempation,
    '任职要求': job_des
}

# 转化为数据框并存为csv
data = pd.DataFrame(dataset)
data.to_csv('machine_learning_hz_job2.csv')
