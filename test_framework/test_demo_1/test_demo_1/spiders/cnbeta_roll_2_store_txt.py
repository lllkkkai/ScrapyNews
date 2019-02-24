import scrapy
from test_demo_1.items import TestDemo1Item
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class MySpider(scrapy.Spider):
    name = 'roll_store_test'

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        self.browser = webdriver.Chrome(executable_path=(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'), chrome_options=chrome_options)
        self.browser.set_page_load_timeout(90)

    def closed(self, spider):
        print("spider closed")
        self.browser.close()

    def start_requests(self):
        #start_urls = []
        url='https://www.cnbeta.com/category/tech.htm'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for infor in response.xpath('//div[@class="items-area"]'):
            links = infor.xpath('./div[@class="item"]/dl/dt/a/@href').extract()
            tags = infor.xpath('./div[@class="item"]/div[@class="meta-data"]/label/text()').extract()
            for (link,tag) in zip(links,tags):
                yield scrapy.Request(url=link, meta={'link':link, 'tag':tag}, callback=self.parse_details)

    def parse_details(self,response):
        item = TestDemo1Item()

        infor = response.xpath('//div[@class="cnbeta-article"]')
        time = infor.xpath('.//div[@class="meta"]/span/text()').extract()[0]
        sources = infor.xpath('.//div[@class="meta"]/span[@class="source"]')
        detail_source = sources.xpath('string(.)').extract()[0]
        title = infor.xpath('.//h1/text()').extract()[0]
        desc = infor.xpath('.//div[@class="article-summary"]/p')
        detail_desc = desc.xpath('normalize-space(string(.))').extract()[0]

        item['time'] = time
        item['source'] = detail_source
        item['link'] = response.meta['link']
        item['title'] = title
        item['desc'] = detail_desc
        item['tag'] = response.meta['tag']
        return item

