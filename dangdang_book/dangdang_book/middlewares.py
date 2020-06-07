# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random


class DangdangBookDownloaderMiddleware:

    def process_request(self, request, spider):
        """添加随机UA跟代理IP"""
        ua = random.choice(spider.settings.get("UA_LIST"))
        request.headers["User-Agent"] = ua

        # request.meta["proxy"] = "https://125.115.126.114:888"

    def process_response(self, request, response, spider):
        """查看UA有没有设置成功"""
        # print("777", request.headers["User-Agent"])
        return response


