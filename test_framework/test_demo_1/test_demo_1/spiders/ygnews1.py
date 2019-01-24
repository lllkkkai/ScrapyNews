import scrapy
import re
from scrapy.http import Request
from test_demo_1.items import ygnewsItem
from scrapy.linkextractor import LinkExtractor

class MySpider(scrapy.Spider):
    name = 'ygnews1'
    start_urls = [
        'http://military.cnr.cn/gz/20190123/t20190123_524491287.html',
                  ]

    def get_detail(self, response):
        item = ygnewsItem()
        item['title'] = response.xpath('./dl/dt/a/text()').extract_first()
        item['text'] = response.xpath('normalize-space(./dl/dd/p/text())').extract_first()
        item['link'] = response.xpath('./dl/dt/a/@href').extract_first()
        return item



