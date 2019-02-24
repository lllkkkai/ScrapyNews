import scrapy
from test_demo_1.items import TestDemo1Item

class MySpider(scrapy.Spider):
    name = 'data_store_test'
    start_urls = [
                  'https://www.cnbeta.com/category/tech.htm',
                  ]

    def parse(self, response):
        for infor in response.xpath('//div[@class="items-area"]'):
            links = infor.xpath('./div[@class="item"]/dl/dt/a/@href').extract()
            # titles = infor.xpath('./div[@class="item"]/dl/dt/a/text()').extract()
            # texts = infor.xpath('./div[@class="item"]/dl/dd')
            # detail_text = texts.xpath('string(.)').extract()
            # tags = infor.xpath('./div[@class="item"]/div[@class="meta-data"]/label[@class="labels tech"]/text()').extract()
            for link in links:
                yield scrapy.Request(url=link, meta={'link':link}, callback=self.parse_details)

    def parse_details(self,response):
        item = TestDemo1Item()

        infor = response.xpath('//div[@class="cnbeta-article"]')
        time = infor.xpath('.//div[@class="meta"]/span/text()').extract()[0]
        sources = infor.xpath('.//div[@class="meta"]/span[@class="source"]')
        detail_source = sources.xpath('string(.)').extract()[0]
        title = infor.xpath('.//h1/text()').extract()[0]
        desc = infor.xpath('.//div[@class="article-summary"]/p')
        detail_desc = desc.xpath('string(.)').extract()[0]

        item['time'] = time
        item['source'] = detail_source
        item['link'] = response.meta['link']
        item['title'] = title
        item['desc'] = detail_desc
        return item

