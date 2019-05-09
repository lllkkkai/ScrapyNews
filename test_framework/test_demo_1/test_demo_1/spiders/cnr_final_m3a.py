import scrapy
import re
from test_demo_1.items import ygnews_mp3_Item
import pymysql.cursors
import html as ht
import requests
from lxml import html
import json

class MySpider(scrapy.Spider):
    sql_time = '2018-01-01 00:00:00'
    name = 'cnr_final_m3a'
    all_article_urls = []
    mp3_id = 0

    def start_requests(self):
        type_1_base_urls = [
            'http://china.cnr.cn/news/',
        ]
        type_2_base_urls = [
            'https://www.qingting.fm/channels/138208/'
        ]
        type_1_urls = []
        type_2_urls = []

        for url in type_1_base_urls:
            type_1_urls.append(url)
            page = 1
            while page < 10:
                detail_url = url + 'index_' + str(page) + '.html'
                type_1_urls.append(detail_url)
                page += 1

        for url in type_2_base_urls:
            page = 1
            while page < 20:
                detail_url = url + str(page)
                type_2_urls.append(detail_url)
                page += 1

        for link in type_1_urls:
            print(link)
            yield scrapy.Request(url=link, callback=self.parse_type_1)

        for link in type_2_urls:
            print(link)
            yield scrapy.Request(url=link, meta={'link': link}, callback=self.parse_details_QingTing)

        # self.connect = pymysql.connect(
        #     host='127.0.0.1',  # 数据库地址
        #     port=3306,  # 数据库端口
        #     db='newsdata',  # 数据库名
        #     user='root',  # 数据库用户名
        #     passwd='',  # 数据库密码
        #     charset='utf8',  # 编码方式
        #     use_unicode=True)
        # self.cursor = self.connect.cursor()
        #
        # sql = 'select MAX(time) from news'
        # self.cursor.execute(sql)
        # D = self.cursor.fetchone()
        # self.sql_time = D[0]

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
            if (time > str(self.sql_time)):
                item['time'] = time
                item['audiosurl'] = audio
                item['href'] = response.meta['link']
                item['newstitle'] = title
                item['classid'] = int(31)
                item['website'] = 'cnr_mp3'
                item['source'] = 'cnr_mp3'
                return item

    def parse_details_QingTing(self,response):
        rep = requests.get(response.meta['link'])
        HTML = rep.content
        tree = html.fromstring(HTML)
        Html = html.tostring(tree).decode()

        r = re.findall(r'<script type="text/javascript">\n([\s\S]+?)</script>', ht.unescape(Html), re.M)
        str = r[0].replace("window.__initStores=","")
        d = json.loads(str)

        list = d['AlbumStore']['plist']
        for i in list:
            item = ygnews_mp3_Item()
            item['audiosurl'] = 'https://od.qingting.fm/' + i['file_path']
            item['newstitle'] = i['name']
            item['time'] = i['update_time']
            item['href'] = ''
            item['classid'] = int(31)
            item['website'] = 'cnr_mp3'
            item['source'] = 'cnr_mp3'
            yield item
