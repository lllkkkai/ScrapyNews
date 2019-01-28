import scrapy
from test_demo_1.items import TestDemo1Item


class MySpider(scrapy.Spider):
    name = 'cnbeta1'
    start_urls = [
                  # 'https://www.cnbeta.com/category/science.htm',
                  # 'https://www.cnbeta.com/category/movie.htm',
                  # 'https://www.cnbeta.com/category/music.htm',
                  # 'https://www.cnbeta.com/category/game.htm',
                  # 'https://www.cnbeta.com/category/comic.htm',
                  # 'https://www.cnbeta.com/category/soft.htm',
                  'https://www.cnbeta.com/category/tech.htm',
                  # 'https://www.cnbeta.com/category/funny.htm',
                  ]

    def parse(self, response):
        items = []
        a = 0
        for infor in response.xpath('//div[@class="item"]'):
        #     item = TestDemo1Item()
        #     item['title'] = infor.xpath('./dl/dt/a/descendant::text()').extract_first()
        #     item['desc'] = infor.xpath('normalize-space(./dl/dd/p/descendant::text())').extract_first()
            link = infor.xpath('./dl/dt/a/@href').extract()
            if link!= ' ':
                print(link)
                link = 'https://www.cnbeta.com/articles/tech/812773.htm'
                yield scrapy.Request(url=link, callback=self.parse_details)

    def parse_details(self,response):
        print("11111111111111111111111")
        #     item['link'] = link
        #     items.append(item)
        #     a+=1
        # return items






