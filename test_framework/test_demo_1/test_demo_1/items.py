# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TestDemo1Item(scrapy.Item):
    title = scrapy.Field() #标题
    url = scrapy.Field() #链接
    desc = scrapy.Field() #简述
    time = scrapy.Field() #发布时间
    source = scrapy.Field()

