# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

class TestDemo1Pipeline(object):
    def process_item(self, item, spider):
        # 获取当前工作目录
        base_dir = os.getcwd()
        fiename = base_dir + '/news223.txt'
        # 从内存以追加的方式打开文件，并写入对应的数据
        with open(fiename, 'a') as f:
            f.write("Tag:   " + item['tag'] + '\n')
            f.write("Time:  " + item['time'] + '\n')
            f.write("Source:" + item['source'] + '\n')
            f.write("Title: " + item['title'] + '\n')
            f.write("link:  " + item['link'] + '\n')
            f.write("Desc:  " + item['desc'] + '\n\n')
        return item