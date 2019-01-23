import scrapy
from scrapy.http import Request
from test_demo_1.items import TestDemo1Item

class MySpider(scrapy.Spider):
    name = 'test1'
    start_urls = ['https://www.cnbeta.com/top10.htm',]

    def parse(self, response):
        items = []
        for infor in response.xpath('//div[@class="item"]'):
            #item = TestDemo1Item()
            #item['title'] = infor.xpath('./dl/dt/a/text()').extract_first()
            #item['desc'] = infor.xpath('normalize-space(./dl/dd/p/text())').extract_first()
            #item['link'] = infor.xpath('./dl/dt/a/@href').extract_first()
            url = infor.xpath('./dl/dt/a/@href').extract_first()
            yield Request(url, callback=self.get_detail)
            #items.append(item)
        #return items

    def get_detail(self, response):
        items = []
        for detail in response.xpath('//div[@class="cnbeta-article"]'):
            item = TestDemo1Item()
            item['title'] = detail.xpath('.//h1/text()').extract_first()
            item['desc'] = detail.xpath('normalize-space(.//div[@class="article-summary"]//p/text())').extract_first()
            # item['link'] = url
            # item['link'] = detail.xpath('./dt/a/@href').extract_first()
            items.append(item)
        yield items



