# -*- coding: utf-8 -*-
import scrapy
import re

class QsbkSpiderSpider(scrapy.Spider):
    name = 'qsbk_spider'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']
    base_domain='https://www.qiushibaike.com'

    def parse(self, response):
        duanzi_divs1=response.xpath("//div[@id='content-left']/div")
        #duanzi_divs=duanzi_divs1.xpath("./div[@class='article block untagged mb15 typs_long']")
        print(len(duanzi_divs1))
        for duanzi_div in duanzi_divs1:

            author=duanzi_div.xpath(".//div[@class='author clearfix']/a/h2/text()").get()#.strip()#.extract_first()
            print(author)
            content=duanzi_div.xpath(".//div[@class='content']/span/text()").getall()#.extract_first()
            content=''.join(content)
            print(content)
            duanzi = {'author': author, 'content': content}
            yield duanzi
        next_url=response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
        if not next_url:
            return
        else:
            yield scrapy.Request(self.base_domain+next_url,callback=self.parse)

        #content = .xpath("//div[@class='col1']//a[@class='contentHerf']/div[@class='content']/span/text()").getall()
        #links = response.xpath("//div[@id='content-left']/div/a/@href").extract()
        ##links = 'https://www.qiushibaike.com' + links
        #author=response.xpath("//div[@id='content-left']/div/div//h2/text()").get().strip()#.extract()

        #print(content)
        #print(len(content))
        #print(links)
        #print(author)
        #content
        #content=self.clear_span_br(content)
        #for i in range(len(author)):
        #    content[i] = ''.join(content[i]).strip()
        #    author[i] = ''.join(author[i]).strip()
        #    duanzi={'author':author[i],'content':content[i]}
        #    print(content[i])
        #    print(author[i])
        #yield duanzi
#