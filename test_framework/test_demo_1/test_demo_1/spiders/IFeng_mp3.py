import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class MySpider(scrapy.Spider):
    name = 'ifeng_mp3'
    url = 'http://diantai.ifeng.com/#!/category/1/193187'

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        self.browser = webdriver.Chrome(executable_path=(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'), chrome_options=chrome_options)
        self.browser.set_page_load_timeout(120)
        self.browser.get("http://diantai.ifeng.com/#!/category/1/193187")

        time.sleep(3)

        # try:
        #     element = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "content")))
        # finally:
        #     print(self.browser.page_source)
        #     self.browser.close()
        print(self.browser.page_source)
        self.browser.close()

    # def closed(self, spider):
    #     print("spider closed")
    #     self.browser.close()
    #
    # def start_requests(self):
    #
    #     cnbeta_urls = ['http://diantai.ifeng.com/#!/category/1/193187',
    #                     ]
    #     for url in cnbeta_urls:
    #         yield scrapy.Request(url=url, callback=self.parse)
    #
    # def parse(self, response):
    #     self.browser.get(self.url)
    #     print(self.browser.page_source)
