# -*- coding: utf-8 -*-
import scrapy
# 额外导入以下类
from scrapy_redis.spiders import RedisSpider
from copy import deepcopy
import time
# 继承导入的类
class DdBookSpider(RedisSpider):
    name = 'dd_book'
    allowed_domains = ['dangdang.com']
    redis_key = "dd_book"   # redis中插入（lpush dd_book http://category.dangdang.com/?ref=www-0-C）
    # start_urls = ["http://category.dangdang.com/"]
    def parse(self, response):
        """图书大类"""
        # 先分组
        div_list = response.xpath('//div[@class="classify_books"]/div[@class="classify_kind"]')
        for div in div_list:
            item = {}
            item["大标题"] = div.xpath('.//a/text()').extract_first()
            li_list = div.xpath('.//ul[@class="classify_kind_detail"]/li')
            for li in li_list:
                item["小标题"] = li.xpath('./a/text()').extract_first()
                sm_url = li.xpath('./a/@href').extract_first()
                #print(sm_url, item["小标题"])
                time.sleep(2)

                # 请求详情页
                if sm_url != "javascript:void(0);":
                    print("请求详情页:" ,sm_url)
                    yield scrapy.Request(sm_url, callback=self.book_details, meta={"item": deepcopy(item)})

    def book_details(self, response):
        """提取图书数据"""
        item = response.meta["item"]
        # 给每本书分组
        li_list = response.xpath('//ul[@class="bigimg"]/li')
        for li in li_list:
            item["图书标题"] = li.xpath('./a/@title').extract_first()
            item["作者"] = li.xpath('./p[@class="search_book_author"]/span[1]/a/@title').extract_first()
            item["图书简介"] = li.xpath('./p[@class="detail"]/text()').extract_first()
            item["价格"] = li.xpath('./p[@class="price"]/span[@class="search_now_price"]/text()').extract_first()
            item["电子书价格"] = li.xpath('./p[@class="price"]/a[@class="search_e_price"]/i/text()').extract_first()
            item["日期"] = li.xpath('./p[@class="search_book_author"]/span[2]/text()').extract_first()
            item["出版社"] = li.xpath('./p[@class="search_book_author"]/span[3]/a/@title').extract_first()
            item["图片"] = li.xpath('./a/img/@src').extract_first()
            item["图书链接"] = li.xpath('./a/@href').extract_first()

            yield item

        # 翻页
        next_url = response.xpath('//a[text()="下一页"]/@href').extract_first()
        if next_url is not None:
            next_url = "http://category.dangdang.com" + next_url
            yield scrapy.Request(next_url, callback=self.book_details, meta={"item": deepcopy(item)})

# lpush dd_book http://category.dangdang.com/?ref=www-0-C

# ╭─mac@huayang ~/Stardust/scrapy_project/scrapy-redis-dangdang.cm-master  
# ╰─➤  PYTHONPATH=$(pwd) python3 -m scrapy runspider spiders/dd_book.py