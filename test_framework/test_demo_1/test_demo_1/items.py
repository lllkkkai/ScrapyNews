# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TestDemo1Item(scrapy.Item):
    # define the fields for your item here like:
    newstitle = scrapy.Field() #标题
    abstract = scrapy.Field()
    content = scrapy.Field()
    keywords = scrapy.Field()
    class_id = scrapy.Field()
    source = scrapy.Field()
    ranking = scrapy.Field()
    href = scrapy.Field()
    time = scrapy.Field()
    place = scrapy.Field()
    terms = scrapy.Field()
    website = scrapy.Field()

class ygnews_mp3_Item(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    mp3_link = scrapy.Field()
    time = scrapy.Field()
    source_link = scrapy.Field()

class ygnewsItem(scrapy.Item):
    news = scrapy.Field()