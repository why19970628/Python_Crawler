import requests
from urllib import request
from lxml import etree
import os
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

class Spider(object):
    def start_request(self):
        url = 'https://www.qidian.com/all'
        req = request.Request(url,headers=header)
        html= request.urlopen(req).read().decode('utf-8')
        html=etree.HTML(html)
        print(html)
        bigtit_list=html.xpath('//div[@class="book-mid-info"]/h4/a/text()')   ##爬取所有的文章名字
        bigsrc_list = html.xpath('//div[@class="book-mid-info"]/h4/a/@href')

        print(bigtit_list)
        print(bigsrc_list)
        for bigtit,bigsrc in zip(bigtit_list,bigsrc_list):
            if os.path.exists(bigtit)==False:
                os.mkdir(bigtit)
            self.file_data(bigsrc,bigtit)
    def file_data(self,bigsrc,bigtit):   #详情页
        url="http:"+bigsrc
        req = request.Request(url, headers=header)
        html = request.urlopen(req).read().decode('utf-8')
        html = etree.HTML(html)
        print(html)
        Lit_tit_list = html.xpath('//ul[@class="cf"]/li/a/text()')  #爬取每个章节名字
        Lit_href_list = html.xpath('//ul[@class="cf"]/li/a/@href')  #每个章节链接
        for tit,src in zip(Lit_tit_list,Lit_href_list):
            self.finally_file(tit,src,bigtit)

    def finally_file(self,tit,src,bigtit):
        url = "http:" + src
        req = request.Request(url, headers=header)
        html = request.urlopen(req).read().decode('utf-8')
        html = etree.HTML(html)
        text_list = html.xpath('//div[@class="read-content j_readContent"]/p/text()')
        text = "\n".join(text_list)
        file_name = bigtit + "\\" + tit + ".txt"
        print("正在抓取文章：" + file_name)
        with open(file_name, 'a', encoding="utf-8") as f:
            f.write(text)

spider=Spider()
spider.start_request()