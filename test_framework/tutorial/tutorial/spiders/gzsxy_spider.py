import scrapy

class QuotesSpider(scrapy.Spider):
    name = "gzsxy"
    start_urls = []
    for i in range(2,10):
        start_urls.append("http://news.gzcc.cn/html/xiaoyuanxinwen/"+ str(i) +".html")

    def parse(self, response):
        for quote in response.css('div.news-list-text'):
            yield {
                'title': quote.css('div.news-list-title::text').extract_first(),
                'description': quote.css('div.news-list-description::text').extract_first(),
                'time': quote.css('div.news-list-info > span.fa fa-clock-o::text').extract(),
            }

        # next_page_url = response.css('//li[@class="next"]/a/@href').extract_first()

        # if next_page_url is not None:
        #     yield scrapy.Request(response.urljoin(next_page_url))