import scrapy
import re
from test_demo_1.items import ygnews_mp3_Item
import html as ht
import requests
from lxml import html
import json

class MySpider(scrapy.Spider):
    name = 'qingting'
    all_article_urls = []
    mp3_id = 0

    def start_requests(self):
        base_urls = [
            'https://www.qingting.fm/channels/139566',
        ]

        for link in base_urls:
            print(link)
            yield scrapy.Request(url=link, callback=self.parse_details)

    def parse_details(self,response):
        infor = response.xpath('.//script[@*]//text()')

        rep = requests.get('https://www.qingting.fm/channels/283966/')
        HTML = rep.content
        tree = html.fromstring(HTML)
        Html = html.tostring(tree).decode()

        r = re.findall(r'<script type="text/javascript">\n([\s\S]+?)</script>', ht.unescape(Html), re.M)
        print(r[0])
        str = r[0].replace("window.__initStores=","")
        d = json.loads(str)

        list = d['AlbumStore']['plist']
        for i in list:
            item = ygnews_mp3_Item()
            item['mp3_link'] = 'https://od.qingting.fm/' + i['file_path']
            item['title'] = i['name']
            item['time'] = i['update_time']
            yield item




