import re
import time, random
import requests
from lxml import html
from urllib import parse
import xlwt
import pandas as pd

key = '大数据'
key = parse.quote(parse.quote(key))
headers = {'Host': 'search.51job.com',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

def get_links(i):
    url = 'http://search.51job.com/list/000000,000000,0000,00,9,99,' + key + ',2,' + str(i) + '.html'
    r = requests.get(url, headers, timeout=10)
    s = requests.session()
    s.keep_alive = False
    r.encoding = 'gbk'
    reg = re.compile(r'class="t1 ">.*? <a target="_blank" title=".*?" href="(.*?)".*? <span class="t2">', re.S)
    reg1 = re.compile(r'class="t1 ">.*? <a target="_blank" title="(.*?)".*?<span class="t2"><a target="_blank" title="(.*?)" href="(.*?)".*?<span class="t3">(.*?)</span>.*?<span class="t4">(.*?)</span>.*? <span class="t5">(.*?)</span>',re.S)  # 匹配换行符
    links = re.findall(reg, r.text)
    return links


# 多页处理，下载到文件
def get_content(link):
    r1 = requests.get(link, headers, timeout=10)
    s = requests.session()
    s.keep_alive = False
    r1.encoding = 'gbk'
    t1 = html.fromstring(r1.text)
    try:
        job = t1.xpath('//div[@class="tHeader tHjob"]//h1/text()')[0].strip()
        companyname = t1.xpath('//p[@class="cname"]/a/text()')[0].strip()
        print('工作：', job)
        print('公司：', companyname)
        area = t1.xpath('//div[@class="tHeader tHjob"]//p[@class="msg ltype"]/text()')[0].strip()
        print('地区', area)
        workyear = t1.xpath('//div[@class="tHeader tHjob"]//p[@class="msg ltype"]/text()')[1].strip()
        print('工作经验', workyear)
        education = t1.xpath('//div[@class="tHeader tHjob"]//p[@class="msg ltype"]/text()')[2].strip()
        print('学历:', education)
        require_people = t1.xpath('//div[@class="tHeader tHjob"]//p[@class="msg ltype"]/text()')[3].strip()
        print('人数', require_people)
        date = t1.xpath('//div[@class="tHeader tHjob"]//p[@class="msg ltype"]/text()')[4].strip()
        print('发布日期', date)
        describes = re.findall(re.compile('<div class="bmsg job_msg inbox">(.*?)div class="mt10"', re.S), r1.text)
        job_describe = describes[0].strip().replace('<p>', '').replace('</p>', '').replace('<p>', '').replace('<span>', '').replace('</span>', '').replace('\t', '').replace('<', '').replace('<br>', '').replace('\n', '').replace('&nbsp;','')
        print('职位信息', job_describe)
        describes1 = re.findall(re.compile('<div class="tmsg inbox">(.*?)</div>', re.S), r1.text)
        company_describe= describes1[0].strip().replace('<p>', '').replace('</p>', '').replace('<p>', '').replace('<span>','').replace('</span>', '').replace('\t', '').replace('&nbsp;','').replace('<br>', '').replace('<br>', '')
        print('公司信息', company_describe)
        companytypes = t1.xpath('//div[@class="com_tag"]/p/text()')[0]
        print('公司类型', companytypes)
        company_people = t1.xpath('//div[@class="com_tag"]/p/text()')[1]
        print('公司人数',company_people)
        salary=t1.xpath('//div[@class="cn"]/h1/strong/text()')
        salary = re.findall(re.compile(r'div class="cn">.*?<strong>(.*?)</strong>',re.S),r1.text)[0]
        print('薪水',salary)
        labels = t1.xpath('//div[@class="jtag"]/div[@class="t1"]/span/text()')
        label = ''
        for i in labels:
            label = label + ' ' + i
        print('待遇',label)
        datalist = [
            str(area),
            str(companyname),
            str(job),
            str(education),
            str(salary),
            str(label),
            str(workyear),
            str(require_people),
            str(date),
            str(job_describe),
            str(company_describe),
            str(companytypes),
            str(company_people),
            str(link)]
        series = pd.Series(datalist, index=[
            '地区',
            '公司名称',
            '工作',
            'education',
            'salary',
            'welfare',
            '工作经验',
            '需求人数',
            '发布时间',
            '工作介绍',
            '公司介绍',
            '公司规模',
            '公司人数',
            '链接',
            ])
        return (1,series)
    except IndexError:
        print('error,未定位到有效信息导致索引越界')
        series = None
        return (-1, series)


if __name__ == '__main__':
        for a in range(1,2):
            datasets = pd.DataFrame()
            print('正在爬取第{}页信息'.format(a))
            # time.sleep(random.random()+random.randint(1,5))
            links= get_links(a)
            print(links)
            for link in links:
                #time.sleep(random.random() + random.randint(0, 1))
                print(link)
                state,series=get_content(link)
                if state==1:
                    datasets = datasets.append(series, ignore_index=True)
                    print('datasets---------',datasets)


            print('第{}页信息爬取完成\n'.format(a))
        print(datasets)
        datasets.to_csv('51job_test.csv', sep='#', index=False, index_label=False,
                            encoding='utf-8', mode='a+')
