# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TestDemo1Item(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    title = scrapy.Field() #标题
    summary = scrapy.Field()
    content = scrapy.Field()
    keywords = scrapy.Field()
    class_id = scrapy.Field()
    source = scrapy.Field()
    ranks = scrapy.Field()
    url = scrapy.Field()
    time = scrapy.Field()
    place = scrapy.Field()
    terms = scrapy.Field()

class ygnewsItem(scrapy.Item):
    title = scrapy.Field() #标题
    link = scrapy.Field() #链接
    desc = scrapy.Field() #简述
    time = scrapy.Field() #发布时间
    tag = scrapy.Field()  #tag
    source = scrapy.Field() # 稿源
    keyword = scrapy.Field() #
    seg = scrapy.Field() #


