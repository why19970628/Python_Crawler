# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
db = pymysql.connect("localhost", "root", "root123", "chat")
# db = client["dangdang_db"]
cursor = db.cursor()


class DangdangBookPipeline:
    def process_item(self, item, spider):
        """保存数据到mongodb"""
        print("8888"*10, item)
        sql = "insert into dangdang(content) values(%s)" % item
        print(sql)
        print("666")
        cursor.execute(sql)
        db.commit()
        db.close
        return item
