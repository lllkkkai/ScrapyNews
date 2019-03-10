import scrapy
from test_demo_1.items import TestDemo1Item

class MySpider(scrapy.Spider):
    name = 'cnr_all_spider'

    handle_httpstatus_list = [404, 500]
    all_article_urls = []
    first_start_flag = 0    # 0 means first-start
                            # 1 means update
    sample_time = '2019-03-06 18:00:00'  # Get the newst time from sql

    def start_requests(self):
        type_1_base_urls = [
            'http://news.cnr.cn/native/gd/',
            'http://news.cnr.cn/gjxw/gnews/',
        ]
        type_2_base_urls = [
            'http://finance.cnr.cn/txcj/',
        ]
        type_1_urls = []
        type_2_urls = []
        for url in type_1_base_urls:
            # print(url.split('/')[-3]) #get the origin tag (only in native,gjxw)
            type_1_urls.append(url)
            page = 1
            while page < 10:    # if page < 10 you get 404 here
                detail_url = url + 'index_' + str(page) + '.html'
                type_1_urls.append(detail_url)
                page += 1

        for url in type_2_base_urls:
            # print(url.split('/')[-3]) #get the origin tag (only in native,gjxw)
            type_2_urls.append(url)
            page = 1
            while page < 10:
                detail_url = url + 'index_' + str(page) + '.html'
                type_2_urls.append(detail_url)
                page += 1

        # for link in type_1_urls:
        #     print(link)
        #     yield scrapy.Request(url=link, callback=self.parse_type_1)

        for link in type_2_urls:
            print(link)
            yield scrapy.Request(url=link, callback=self.parse_type_2)

    '''
    type-1-native-international-other
    国内滚动_
    http://news.cnr.cn/native/gd/
    即时要闻_
    http://news.cnr.cn/gjxw/gnews/
    独家报道_
    http://finance.cnr.cn/2014jingji/djbd/
    要闻_
    http://finance.cnr.cn/2014jingji/yw/
    金融理财_
    http://finance.cnr.cn/2014jingji/jrlc/
    交易实况_
    http://finance.cnr.cn/jysk/
    证券市场_
    http://finance.cnr.cn/2014jingji/stock/
    科技金融_
    http://finance.cnr.cn/2014jingji/glwjr/
    央广网独家报道_
    http://news.cnr.cn/dj/
    '''

    def parse_type_1(self, response):
        for infor in response.xpath('//div[@class="articleList"]'):
            links = infor.xpath('./ul/li/a/@href').extract()
            for link in links:
                # print(link)
                if(link not in self.all_article_urls):
                    self.all_article_urls.append(link)
                    yield scrapy.Request(url=link, meta={'link':link}, callback=self.parse_details)

    '''
    type-2-finance
    天天315
    http://finance.cnr.cn/315/gz/
    天下财经
    http://finance.cnr.cn/txcj/
    财经评论
    http://finance.cnr.cn/jjpl/
    '''

    def parse_type_2(self, response):
        # print("come in 2")
        links = response.xpath('.//ul[@class="f14 lh24 f12_5a5a5a left"]/li/span/a/@href').extract()
        for link in links:
            if (link not in self.all_article_urls):
                self.all_article_urls.append(link)
                yield scrapy.Request(url=link, meta={'link':link}, callback=self.parse_details)

    '''
    type-3-military
    
    '''

    def parse_type_3(self, response):
        links = response.xpath('.//ul[@class="erji_left"]/li/span/a/@href').extract()
        for link in links:
            if (link not in self.all_article_urls):
                self.all_article_urls.append(link)
                yield scrapy.Request(url=link, meta={'link':link}, callback=self.parse_details)

    '''
    '''

    def parse_type_4(self, response):
        links = response.xpath('.//ul[@class="grid left"]/li/span/a/@href').extract()
        for link in links:
            if (link not in self.all_article_urls):
                self.all_article_urls.append(link)
                yield scrapy.Request(url=link, meta={'link':link}, callback=self.parse_details)


    def parse_details(self,response):
        item = TestDemo1Item()
        # tag = response.xpath('//p[@class="daoHang"]/a/text()').extract()[1] # Bug Here !
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

