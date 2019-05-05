import scrapy
import re
from test_demo_1.items import ygnews_mp3_Item

class MySpider(scrapy.Spider):
    name = 'cnr_get_mp3_2'
    all_article_urls = []
    mp3_id = 0

    def start_requests(self):
        type_1_base_urls = [
            'http://china.cnr.cn/yaowen/',
        ]
        type_1_urls = []

        for url in type_1_base_urls:
            # print(url.split('/')[-3]) #get the origin tag (only in native,gjxw)
            type_1_urls.append(url)
            page = 1
            while page < 5:    # if page < 10 you get 404 here deal it quick
                detail_url = url + 'index_' + str(page) + '.html'
                type_1_urls.append(detail_url)
                page += 1

        for link in type_1_urls:
            print(link)
            yield scrapy.Request(url=link, callback=self.parse_type_1)

    def parse_type_1(self, response):
        for infor in response.xpath('//div[@class="articleList"]'):
            links = infor.xpath('./ul/li/a/@href').extract()
            for link in links:
                # print(link)
                if(link not in self.all_article_urls):
                    self.all_article_urls.append(link)
                    yield scrapy.Request(url=link, meta={'link':link}, callback=self.parse_details)

    def parse_details(self,response):
        item = ygnews_mp3_Item()
        # tag = response.xpath('//p[@class="daoHang"]/a/text()').extract()[1] # Bug Here !
        infor = response.xpath('//div[@class="article"]')
        time = infor.xpath('.//div[@class="subject"]/div[@class="source"]/span/text()').extract()[0]
        # source = infor.xpath('.//div[@class="subject"]/div[@class="source"]/span/text()').extract()[1]
        # final_source = source.replace("来源：","")
        title = infor.xpath('.//div[@class="subject"]/h2/text()').extract()[0]
        audio_list = infor.xpath('.//input[@type="hidden"]/@value').extract()
        audio = infor.xpath('.//input[@type="hidden"]/@value').extract_first()
        if len(audio_list):
            item['id'] = self.mp3_id
            item['time'] = time
            item['mp3_link'] = audio
            item['source_link'] = response.meta['link']
            item['title'] = title
            self.mp3_id += 1
        # item['desc'] = ""
        # item['tag'] = (response.meta['link']).split('/')[3]
        # item['seg'] = ""
        # item['keyword'] = ""
            return item

