import scrapy
from test_demo_1.items import TestDemo1Item
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class MySpider(scrapy.Spider):
    name = 'roll_re'

    # def __init__(self, scrapy_task_id=None, *args, **kwargs):
    #     self.url_src = "http://www.baidu.com"

    def start_requests(self):
        #start_urls = []
        url='https://www.cnbeta.com/category/tech.htm'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.log(response.url)

        urls = [
                'https://www.cnbeta.com/category/tech.htm',
                ]

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(executable_path=(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'), chrome_options=chrome_options)
        for url in urls:
            try:
                print(url)
                driver.get(url)
                # 模拟鼠标滚到底部(加载100条数据)
                for _ in range(10):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    driver.implicitly_wait(10)  # 隐性等待,最长10秒

                print (driver.page_source)
                # soup = bs(driver.page_source, 'lxml')
                # articles = soup.find_all(href=re.compile("/a_\w+?/"), text=re.compile(".+"))
                # for article in articles:
                #     for key in self.df_keys:
                #         item = VideoItem()  # 自定义的Item
                #         item['title'] = article.text
                #         item['href'] = article['href']
                #         self.log(item)
                #         yield item



            except Exception as e:
                print
                e
                if driver == None:
                    driver = webdriver.Chrome(executable_path=(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'), chrome_options=chrome_options)

        if driver != None:
            driver.quit()
