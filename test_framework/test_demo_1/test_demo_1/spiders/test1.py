import scrapy
import re
from scrapy.http import Request
from test_demo_1.items import TestDemo1Item
from scrapy.linkextractor import LinkExtractor

class MySpider(scrapy.Spider):
    name = 'test1'
    start_urls = [
                  'https://www.cnbeta.com/category/science.htm',
                  'https://www.cnbeta.com/category/movie.htm',
                  'https://www.cnbeta.com/category/music.htm',
                  'https://www.cnbeta.com/category/game.htm',
                  'https://www.cnbeta.com/category/comic.htm',
                  'https://www.cnbeta.com/category/soft.htm',
                  'https://www.cnbeta.com/category/tech.htm',
                  'https://www.cnbeta.com/category/funny.htm'
                  ]

    def parse(self, response):
        items = []
        a = 0
        for infor in response.xpath('//div[@class="item"]'):
            item = TestDemo1Item()
            item['title'] = infor.xpath('./dl/dt/a/text()').extract_first()
            item['desc'] = infor.xpath('normalize-space(./dl/dd/p/text())').extract_first()
            item['link'] = infor.xpath('./dl/dt/a/@href').extract_first()
            #item['time'] = infor.xpath('./div[@class="meta-data"]/ul/li/text()').extract_first()
            #link need re beacaues //hot.funny.com
            #time

            # if re.match(r'^https?:/{2}\w.+$', item['link']):
            #     a = 1
            # else:
            #     item['link'] = "http:" + item['link']
            items.append(item)
            a+=1
        return items
        # link = LinkExtractor(restrict_xpaths='//a[@href]')
        # links = link.extract_links(response)
        # for i in links:
        #     print(i)

    # news total link
    # def get_detail(self,response):
    #     item = TestDemo1Item()
    #     t = response.xpath('//div[@class="cnbeta-article"]//h1/text()').extract_first()
    #     if t:
    #         item['title'] = t
    #     d = response.xpath('//div[@class="cnbeta-article"]//div[@class="article-summary"]/p/text()').extract_first()
    #     if d:
    #         item['desc'] = d
    #     time = response.xpath('//div[@class="cnbeta-article"]//span/text()').extract_first()
    #     if time:
    #         item['time'] = time
    #     return item







        # items = []
        # for infor in response.xpath('//div[@class="item"]'):
            #item = TestDemo1Item()
            #item['title'] = infor.xpath('./dl/dt/a/text()').extract_first()
            #item['desc'] = infor.xpath('normalize-space(./dl/dd/p/text())').extract_first()
            #item['link'] = infor.xpath('./dl/dt/a/@href').extract_first()
            #url = infor.xpath('./dl/dt/a/@href').extract_first()
            #yield Request(url, callback=self.get_detail)
            #items.append(item)
            #self.get_detail(response,item)
        # return items

    # def get_detail(self, response):
    #     items = []
    #     for detail in response.xpath('//div[@class="cnbeta-article"]'):
    #         item = TestDemo1Item()
    #         item['title'] = detail.xpath('.//h1/text()').extract_first()
    #         item['desc'] = detail.xpath('normalize-space(.//div[@class="article-summary"]//p/text())').extract_first()
    #         # item['link'] = url
    #         # item['link'] = detail.xpath('./dt/a/@href').extract_first()
    #         items.append(item)
    #     yield items



