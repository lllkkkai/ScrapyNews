from scrapy import Spider, Request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class MySpider(Spider):
    name = "my_spider"

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
        yield Request(url=url, callback=self.parse)

    def parse(self, response):
        # domain = response.url.split("/")[-1]
        # filename = '%s.html' % domain
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        sums = response.xpath('//div[@class="items-area"]/div[@class="item"]/dl/dt/a/text()').extract()
        for sum in sums:
            print(sum)
        print('---------------------------------------------------')