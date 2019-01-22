# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TutorialPipeline(object):
    def process_item(self, item, spider):
        fileName = 'gzsxy.txt'
        with open(fileName, 'a') as fp:
            fp.write(item['title'].encode('utf8') + '\t')
            fp.write(item['description'].encode('utf8') + '\t')
            fp.write(item['time'].encode('utf8') + '\t')
        return item
