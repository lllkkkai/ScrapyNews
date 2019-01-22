import re
import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup
from test_demo_1.items import TestDemo1Item

class MySpider(scrapy.Spider):
    name = 'test1'
    allowed_domains = ['cnbeta.com']
    base_url = 'https://www.cnbeta.com/top10.htm'

    def start_requests(self):
        yield Request(self.base_url, self.parse)

    def parse(self, response):
        items = []
        titles = BeautifulSoup(response.text, 'lxml').select('dt>a')
        dess = BeautifulSoup(response.text, 'lxml').select('dd')

        for title,des in zip(titles,dess):
            item = TestDemo1Item()
            item['title'] = str(title.get_text())
            item['des'] = str(des.get_text())
            # item['url'] = url.get_text()
            items.append(item)
        return items


