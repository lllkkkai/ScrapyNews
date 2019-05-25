import scrapy
from test_demo_1.items import ygnews_mp3_Item
import jieba.analyse
import pymysql.cursors

class MySpider(scrapy.Spider):
    sql_time = '2019-05-18 07:00:00'
    name = 'cnr_mp3'
    custom_settings = {
        'ITEM_PIPELINES': {
            'test_demo_1.cnr_mp3_sql.CNR_mp3_Online': 400
        }
    }
    all_article_urls = []
    mp3_id = 0
    stop_words = [',', '.', '?', ':', ';', '"', '\'', '/', '+', '-', '[', ']', '{', '}', '@', '#', '$', '%', '^', '&',
                  '*', '(', ')', '=', '<', '>', '！', '，', '。', '：', '；', '“', '”', '‘', '’', '？', '《', '》', '—', '（',
                  '）', ' ']

    def start_requests(self):
        type_1_base_urls = [
            'http://china.cnr.cn/news/',
        ]
        type_1_urls = []
        for url in type_1_base_urls:
            type_1_urls.append(url)
            page = 1
            while page < 12:
                detail_url = url + 'index_' + str(page) + '.html'
                type_1_urls.append(detail_url)
                page += 1

        for link in type_1_urls:
            print(link)
            yield scrapy.Request(url=link, callback=self.parse_type_1)

        self.connect = pymysql.connect(
            host='47.100.163.195',  # 数据库地址
            port=3306,  # 数据库端口
            db='test',  # 数据库名
            user='recommend',  # 数据库用户名
            passwd='recommend',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
        self.cursor = self.connect.cursor()
        sql = 'select MAX(time) from News where website = "cnr_mp3"'
        self.cursor.execute(sql)
        D = self.cursor.fetchone()
        self.sql_time = D[0]

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
        content = infor.xpath('.//div[@class="articleMain clearfix"]/div[@class="content"]/div[@class="contentText"]//p[not(contains(@align,"center"))][not(contains(@style,"text-align: center;"))]')
        #content_pa = infor.xpath('.//div[@class="articleMain clearfix"]/div[@class="content"]/div[@class="contentText"]//p[not(contains(@align,"center"))][not(contains(@style,"text-align: center;"))]//a')
        body = ""

        for p in content.xpath('string(.)'):
            if (len(p.extract().strip().replace('\n', '').replace('\r', '')) != 0):
                body = body + "**" + p.extract().strip().replace('\n', '').replace('\r', '')

        # source = infor.xpath('.//div[@class="subject"]/div[@class="source"]/span/text()').extract()[1]
        # final_source = source.replace("来源：","")
        title = infor.xpath('.//div[@class="subject"]/h2/text()').extract()[0]
        start_key = ""
        title_no_space = title.strip()
        title_seg = jieba.cut(title_no_space, cut_all=False)
        for word in title_seg:
            if word not in self.stop_words:
                if word != '\t':
                    start_key += word
                    start_key += ","
        # start_key = (",".join(title_seg))
        keywords = start_key

        audio_list = infor.xpath('.//input[@type="hidden"]/@value').extract()
        audio = infor.xpath('.//input[@type="hidden"]/@value').extract_first()
        if len(audio_list):
            if (time > str(self.sql_time)):
                item['content'] = body
                item['time'] = time
                item['audiosurl'] = audio
                item['href'] = response.meta['link']
                item['newstitle'] = title
                item['classid'] = int(31)
                item['website'] = 'cnr_mp3'
                item['source'] = 'cnr_mp3'
                item['keywords'] = keywords
                item['ttsTag'] = int(1)
                item['ranking'] = int(1)
                yield item