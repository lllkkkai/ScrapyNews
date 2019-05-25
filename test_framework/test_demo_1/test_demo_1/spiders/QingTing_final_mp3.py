import scrapy
import re
from test_demo_1.items import QingTing_mp3_Item
import html as ht
import requests
from lxml import html
import json
import jieba.analyse

class MySpider(scrapy.Spider):
    sql_time = '2019-05-18 13:45:00'
    name = 'QingTing_mp3'
    all_article_urls = []
    mp3_id = 0
    stop_words = [',', '.', '?', ':', ';', '"', '\'', '/', '+', '-', '[', ']', '{', '}', '@', '#', '$', '%', '^', '&',
                  '*', '(', ')', '=', '<', '>', '！', '，', '。', '：', '；', '“', '”', '‘', '’', '？', '《', '》', '—', '（',
                  '）', ' ']

    def start_requests(self):
        type_2_base_urls = [
            'https://www.qingting.fm/channels/138208/',
            'https://www.qingting.fm/channels/139110/',
            'https://www.qingting.fm/channels/285108/',
            'https://www.qingting.fm/channels/138214/',
        ]

        type_2_urls = []

        for url in type_2_base_urls:
            page = 1
            while page < 25:
                detail_url = url + str(page)
                type_2_urls.append(detail_url)
                page += 1

        for link in type_2_urls:
            print(link)
            yield scrapy.Request(url=link, meta={'link': link}, callback=self.parse_details_QingTing)

    def parse_details_QingTing(self, response):
        rep = requests.get(response.meta['link'])
        HTML = rep.content
        tree = html.fromstring(HTML)
        Html = html.tostring(tree).decode()

        r = re.findall(r'<script type="text/javascript">\n([\s\S]+?)</script>', ht.unescape(Html), re.M)
        str = r[0].replace("window.__initStores=", "")
        d = json.loads(str)

        list = d['AlbumStore']['plist']
        for i in list:
            if i['update_time'] > self.sql_time:
                item = QingTing_mp3_Item()
                item['audiosurl'] = 'https://od.qingting.fm/' + i['file_path']
                item['newstitle'] = i['name']
                item['time'] = i['update_time']
                item['classid'] = int(31)
                item['website'] = 'QingTing_FM'
                item['source'] = 'QingTing_FM'

                start_key = ""
                title_no_space = i['name'].strip()
                title_seg = jieba.cut(title_no_space, cut_all=False)
                for word in title_seg:
                    if word not in self.stop_words:
                        if word != '\t':
                            start_key += word
                            start_key += ","
                # start_key = (",".join(title_seg))
                item['keywords'] = start_key
                item['ttsTag'] = int(1)
                item['ranking'] = int(1)

                yield item
