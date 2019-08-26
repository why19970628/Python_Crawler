# -*- coding: utf-8 -*-
import scrapy
from dangdang.items import DangdangItem
from scrapy.http import Request


class DdSpider(scrapy.Spider):
    name = 'dd'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://dangdang.com/']

    def parse(self, response):
        item=DangdangItem()
        item['title']=response.xpath("//a[@class='pic']/@title").extract
        item['link'] = response.xpath("//a[@class='pic']/@href").extract
        item['comment'] = response.xpath("//a[@class='search_comment_num']/text()").extract
        print(item['title'])
        print(item['link'])
        print(item['comment'])
        yield item

        #for i in range(1,5):
        #    url='http://search.dangdang.com/?key=%B3%CC%D0%F2%C9%E8%BC%C6&act=input&page_index'+str(i)
        #    yield Request(url,callback=self.parse)

