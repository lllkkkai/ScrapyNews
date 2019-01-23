# -*- coding: utf-8 -*-
import scrapy
from test_demo_1.items import TestDemo1Item

class HuxiuSpider(scrapy.Spider):
    name = "huxiu"
    allowed_domains = ["huxiu.com"]
    start_urls = ['http://huxiu.com/index.php']

    def parse(self, response):
        #items = []
        data = response.xpath('//div[@class="mod-info-flow"]/div/div[@class="mob-ctt"]')
        for sel in data:
            item = TestDemo1Item()
            if len(sel.xpath('./h2/a/text()').extract()) <= 0:
                item['title'] = 'No title'
            else:
                item['title'] = sel.xpath('./h2/a/text()').extract()[0]
            if len(sel.xpath('./h2/a/@href').extract()) <= 0:
                item['link'] = 'link在哪里！！！！！！！！'
            else:
                item['link'] = sel.xpath('./h2/a/@href').extract()[0]
            url = response.urljoin(item['link'])
            if len(sel.xpath('div[@class="mob-sub"]/text()').extract()) <= 0:
                item['desc'] = '啥也没有哦...'
            else:
                item['desc'] = sel.xpath('div[@class="mob-sub"]/text()').extract()[0]
            #item['posttime'] = sel.xpath('./div[@class="mob-author"]/span/@text()').extract()[0]
            print(item['title'], item['link'], item['desc'])
            #items.append(item)
        #return items
            yield scrapy.Request(url,callback=self.parse_article)

    def parse_article(self,response):
        detail = response.xpath('//div[@class="article-wrap"]')
        item = TestDemo1Item()
        item['title'] = detail.xpath('./h1/text()')[0].extract().strip()
        item['link'] = response.url
        item['posttime'] = detail.xpath('./div/div[@class="column-link-box"]/span[1]/text()')[0].extract()
        print(item['title'],item['link'],item['posttime'])
        yield item