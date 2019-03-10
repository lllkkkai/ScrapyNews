import scrapy
from test_demo_1.items import TestDemo1Item
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import jieba.analyse

class MySpider(scrapy.Spider):
    name = 'roll_store_test'
    sample_time = '2019-03-06 18:00:00' # Get the newst time from sql
    all_article_urls = []

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        self.browser = webdriver.Chrome(executable_path=(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'), chrome_options=chrome_options)
        self.browser.set_page_load_timeout(120)

    def closed(self, spider):
        print("spider closed")
        self.browser.close()

    def start_requests(self):
        cnbeta_urls = ['https://www.cnbeta.com/category/tech.htm',
                       'https://www.cnbeta.com/category/game.htm',
                       'https://www.cnbeta.com/category/funny.htm',
                       'https://www.cnbeta.com/category/science.htm',
                       'https://www.cnbeta.com/category/comic.htm',
                       'https://www.cnbeta.com/category/movie.htm',
                       'https://www.cnbeta.com/category/soft.htm',
                       'https://www.cnbeta.com/category/music.htm',
                        ]

        url='https://www.cnbeta.com/category/tech.htm'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # normal item article
        for infor in response.xpath('//div[@class="items-area"]'):
            links = infor.xpath('./div[@class="item"]/dl/dt/a/@href').extract()
            tags = infor.xpath('./div[@class="item"]/div[@class="meta-data"]/label/text()').extract()
            for (link,tag) in zip(links,tags):
                if (link not in self.all_article_urls):
                    self.all_article_urls.append(link)
                    yield scrapy.Request(url=link, meta={'link':link, 'tag':tag}, callback=self.parse_details)

        # Top 6 hot small item
        for hot in response.xpath('//div[@class="cnbeta-hot-small-figure"]'):
            hot_links = hot.xpath('./div[@class="item"]/a/@href').extract()
            for url in hot_links:
                # print(url.split('/')[-2])
                if (url not in self.all_article_urls):
                    self.all_article_urls.append(url)
                    yield scrapy.Request(url=url, meta={'link':url}, callback=self.parse_details)

        # Top 1 hotest medium item
        for hot_est in response.xpath('//div[@class="cnbeta-hot-big-figure"]'):
            hot_est_link = hot_est.xpath('./a/@href').extract()
            for hot_url in hot_est_link:
                if (hot_url not in self.all_article_urls):
                    self.all_article_urls.append(hot_url)
                    yield scrapy.Request(url=hot_url, meta={'link':hot_url}, callback=self.parse_details)

    def switch_test_item(self,item):
        switcher = {
            "tech": 0,
            "movie": 1,
            "music": 2,
            "game": 3,
            "comic": 4,
            "science": 5,
            "soft": 6,
            "funny": 7,
        }
        return switcher.get(item, "other")

    def parse_details(self,response):
        item = TestDemo1Item()

        infor = response.xpath('//div[@class="cnbeta-article"]')
        time = infor.xpath('.//div[@class="meta"]/span/text()').extract()[0]
        final_time = time.replace("年","-").replace("月","-").replace("日","")

        sources = infor.xpath('.//div[@class="meta"]/span[@class="source"]')
        detail_source = sources.xpath('string(.)').extract()[0]
        final_source = detail_source.replace("稿源：","")
        title = infor.xpath('.//h1/text()').extract()[0]
        desc = infor.xpath('.//div[@class="article-summary"]/p')
        detail_desc = desc.xpath('normalize-space(string(.))').extract()[0]

        temp_key = jieba.analyse.extract_tags(detail_desc,topK=3)
        final_key = (",".join(temp_key))

        temp_seg = jieba.cut(detail_desc, cut_all=False)
        final_seg = ("/".join(temp_seg))

        detail_tag = self.switch_test_item((response.meta['link']).split('/')[-2])

        if (self.sample_time < final_time):
            # if news time late than the sample time
            # store in the item
            item['time'] = final_time
            item['source'] = final_source
            item['link'] = response.meta['link']
            item['title'] = title
            item['desc'] = detail_desc
            item['tag'] = "" #
            item['seg'] = final_seg
            item['keyword'] = final_key
            yield item

