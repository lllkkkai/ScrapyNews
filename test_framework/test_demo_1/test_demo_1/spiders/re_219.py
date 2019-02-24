import scrapy

class MySpider(scrapy.Spider):
    name = 're_219'
    start_urls = [
                  'https://www.cnbeta.com/category/tech.htm',
                  ]

    def parse(self, response):
        for infor in response.xpath('//div[@class="items-area"]'):
            links = infor.xpath('./div[@class="item"]/dl/dt/a/@href').extract()
            titles = infor.xpath('./div[@class="item"]/dl/dt/a/text()').extract()
            texts = infor.xpath('./div[@class="item"]/dl/dd')
            detail_text = texts.xpath('string(.)').extract()
            # print(detail_text)
            tags = infor.xpath('./div[@class="item"]/div[@class="meta-data"]/label[@class="labels tech"]/text()').extract()

            for (a,b,c) in zip(links,titles,tags):
                print(c)
                print(a)
                print(b)
                #yield scrapy.Request(url=a, callback=self.parse_details)
                # skip the link url to get time source

    def parse_details(self,response):
        for infor in response.xpath('//div[@class="cnbeta-article"]'):
            times = infor.xpath('.//div[@class="meta"]/span/text()').extract()[0]
            sources = infor.xpath('.//div[@class="meta"]/span[@class="source"]')
            detail_source = sources.xpath('string(.)').extract()[0]
            detail_source_links = infor.xpath('.//div[@class="meta"]/span[@class="source"]/a/@href').extract()[0]
            # some articles may have no source link
        print(times)
        print(detail_source_links)
        print(detail_source)
