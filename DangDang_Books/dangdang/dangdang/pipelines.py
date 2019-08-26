# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DangdangPipeline(object):
    def process_item(self, item, spider):
        #for i in range(0,len(item['link'])):
        #    title=item['title'][i]
        #    link=item['link'][i]
        #    comment=item['comment'][i]
        #    print(title)
        #    print(link)
        #    print(comment)
        #    print('')

        return item
