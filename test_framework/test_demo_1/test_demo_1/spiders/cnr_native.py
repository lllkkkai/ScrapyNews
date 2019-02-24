import scrapy
from test_demo_1.items import TestDemo1Item

class MySpider(scrapy.Spider):
    name = 'cnr_native_gd'

    def start_requests(self):
        base_urls = [
            'http://news.cnr.cn/native/gd/',
            'http://news.cnr.cn/gjxw/gnews/',
        ]
        urls = []
        for url in base_urls:
            # print(url.split('/')[-3]) #get the origin tag (only in native,gjxw)
            urls.append(url)
            page = 1
            while page < 10:
                detail_url = url + 'index_' + str(page) + '.html'
                urls.append(detail_url)
                page += 1

        for link in urls:
            print(link)
            yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response):
        for infor in response.xpath('//div[@class="articleList"]'):
            links = infor.xpath('./ul/li/a/@href').extract()
            for link in links:
                # print(link)
                yield scrapy.Request(url=link, meta={'link':link}, callback=self.parse_details)

    def parse_details(self,response):
        item = TestDemo1Item()

        tag = response.xpath('//p[@class="daoHang"]/a/text()').extract()[1]
        infor = response.xpath('//div[@class="article"]')
        time = infor.xpath('.//div[@class="subject"]/div[@class="source"]/span/text()').extract()[0]
        sources = infor.xpath('.//div[@class="subject"]/div[@class="source"]/span/text()').extract()[1]
        title = infor.xpath('.//div[@class="subject"]/h2/text()').extract()[0]
        article = infor.xpath('.//div[@class="articleMain clearfix"]/div[@class="content"]/div[@class="contentText"]')
        detail_article = article.xpath('normalize-space(string(.))').extract()[0]

        print(title)
        #print(tag)
        # print(response.meta['link'])
        # print(time)

        #print(sources.replace('来源：',''))
        #print(detail_article)

        # desc = infor.xpath('.//div[@class="article-summary"]/p')
        # detail_desc = desc.xpath('string(.)').extract()[0]

        # item['time'] = time
        # item['source'] = detail_source
        # item['link'] = response.meta['link']
        # item['title'] = title
        # item['desc'] = detail_desc
        # return item

