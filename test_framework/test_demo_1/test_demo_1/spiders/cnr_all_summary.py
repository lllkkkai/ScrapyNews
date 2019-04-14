import scrapy
import re
from test_demo_1.items import ygnewsItem
import codecs
from test_demo_1.textrank4zh import TextRank4Keyword, TextRank4Sentence


class MySpider(scrapy.Spider):
    name = 'cnr_all_summary'

    handle_httpstatus_list = [404, 500]
    all_article_urls = []
    first_start_flag = 0    # 0 means first-start
                            # 1 means update
    sample_time = '2019-03-06 18:00:00'  # Get the newst time from sql

    def start_requests(self):
        type_1_base_urls = [
            'http://china.cnr.cn/yaowen/',
        ]
        type_2_base_urls = [
            'http://finance.cnr.cn/315/gz/',
            'http://finance.cnr.cn/txcj/',
            'http://finance.cnr.cn/jjpl/',
        ]
        type_3_base_urls = [
            'http://military.cnr.cn/gz/',
        ]
        type_4_base_urls = [
            'http://military.cnr.cn/gjjs/',
        ]
        type_5_base_urls = [
            'http://auto.cnr.cn/zxss/',
        ]
        type_6_base_urls = [
            'http://news.cnr.cn/theory/',
        ]
        type_1_urls = []
        type_2_urls = []
        type_3_urls = []
        type_4_urls = []
        type_5_urls = []
        type_6_urls = []
        for url in type_1_base_urls:
            # print(url.split('/')[-3]) #get the origin tag (only in native,gjxw)
            type_1_urls.append(url)
            page = 1
            while page < 5:    # if page < 10 you get 404 here deal it quick
                detail_url = url + 'index_' + str(page) + '.html'
                type_1_urls.append(detail_url)
                page += 1

        for url in type_2_base_urls:
            # print(url.split('/')[-3]) #get the origin tag (only in native,gjxw)
            type_2_urls.append(url)
            page = 1
            while page < 5:
                detail_url = url + 'index_' + str(page) + '.html'
                type_2_urls.append(detail_url)
                page += 1

        for url in type_3_base_urls:
            # print(url.split('/')[-3]) #get the origin tag (only in native,gjxw)
            type_3_urls.append(url)
            page = 1
            while page < 3:
                detail_url = url + 'index_' + str(page) + '.html'
                type_3_urls.append(detail_url)
                page += 1

        for url in type_4_base_urls:
            # print(url.split('/')[-3]) #get the origin tag (only in native,gjxw)
            type_4_urls.append(url)
            page = 1
            while page < 3:
                detail_url = url + 'index_' + str(page) + '.html'
                type_4_urls.append(detail_url)
                page += 1

        for url in type_5_base_urls:
            # print(url.split('/')[-3]) #get the origin tag (only in native,gjxw)
            type_5_urls.append(url)
            page = 1
            while page < 3:
                detail_url = url + 'index_' + str(page) + '.html'
                type_5_urls.append(detail_url)
                page += 1

        for url in type_6_base_urls:
            # print(url.split('/')[-3]) #get the origin tag (only in native,gjxw)
            type_6_urls.append(url)
            page = 1
            while page < 3:
                detail_url = url + 'index_' + str(page) + '.html'
                type_6_urls.append(detail_url)
                page += 1

        for link in type_1_urls:
            print(link)
            yield scrapy.Request(url=link, callback=self.parse_type_1)

        # for link in type_2_urls:
        #     print(link)
        #     yield scrapy.Request(url=link, callback=self.parse_type_2)

        # Time Error : wrong xpath 3.28
        # Text Error : Exit index_2 pages in the text page
        # for link in type_3_urls:
        #     print(link)
        #     yield scrapy.Request(url=link, callback=self.parse_type_3)

        # Time Error : wrong xpath 3.28
        # for link in type_4_urls:
        #     print(link)
        #     yield scrapy.Request(url=link, callback=self.parse_type_4)

        # Time Error : wrong path 3.28 wh645 left
        # for link in type_5_urls:
        #     print(link)
        #     yield scrapy.Request(url=link, callback=self.parse_type_5)

        # for link in type_6_urls:
        #     print(link)
        #     yield scrapy.Request(url=link, callback=self.parse_type_6)

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

    def parse_type_3(self, response):
        links = response.xpath('.//ul[@class="erji_left"]/li/span/a/@href').extract()
        for link in links:
            if (link not in self.all_article_urls):
                self.all_article_urls.append(link)
                yield scrapy.Request(url=link, meta={'link':link}, callback=self.parse_details_type_3)

    def parse_type_4(self, response):
        links = response.xpath('.//div[@class="grid left"]//span[@class="f12_dc0112"]/a/@href').extract()
        for link in links:
            if (link not in self.all_article_urls):
                self.all_article_urls.append(link)
                yield scrapy.Request(url=link, meta={'link':link}, callback=self.parse_details_type_3)

    def parse_type_5(self, response):
        links = response.xpath('.//li[@class="item"]/a/@href').extract()
        for link in links:
            if (link not in self.all_article_urls):
                self.all_article_urls.append(link)
                yield scrapy.Request(url=link, meta={'link':link}, callback=self.parse_details)

    def parse_type_6(self, response):
        links = response.xpath('.//div[@class="wh581 margin"]/div[@class="wh581 left"]/div[@class="left"]/a/@href').extract()
        for link in links:
            link = link.replace('.shtml', '').replace('.','')
            link = "http://news.cnr.cn/theory" + link + ".shtml"
            if (link not in self.all_article_urls):
                self.all_article_urls.append(link)
                yield scrapy.Request(url=link, meta={'link':link}, callback=self.parse_details)

    def parse_details(self,response):
        item = ygnewsItem()
        # tag = response.xpath('//p[@class="daoHang"]/a/text()').extract()[1] # Bug Here !
        infor = response.xpath('//div[@class="article"]')
        time = infor.xpath('.//div[@class="subject"]/div[@class="source"]/span/text()').extract()[0]
        source = infor.xpath('.//div[@class="subject"]/div[@class="source"]/span/text()').extract()[1]
        final_source = source.replace("来源：","")
        title = infor.xpath('.//div[@class="subject"]/h2/text()').extract()[0]

        # 图片新闻没有contentText
        article = infor.xpath('.//div[@class="articleMain clearfix"]/div[@class="content"]/div[@class="contentText"]//p')
        # detail_article = article.xpath('normalize-space(string(.))').extract()[0].replace(u'\u3000',u'').replace(u'\xa0', u' ')
        body = ""
        count = 0
        first_part = ""
        # count表示自然段数
        for p in article.xpath('normalize-space(string(.))'):
            if (count != 0):
                count += 1
                if (len(p.extract().strip().replace('\n', '').replace('\r', '').replace(u'\u3000',u'').replace(u'\xa0', u' ')) != 0):
                    body = body + "\n" + p.extract().strip().replace('\n', '').replace('\r', '')
                    if(self.countCharacters(first_part) < 150):
                        final_first_part = first_part + p.extract().strip().replace('\n', '').replace('\r', '')
                        if(self.countCharacters(final_first_part) < 300):
                            first_part = final_first_part

            if (count == 0):
                count += 1
                if (len(p.extract().strip().replace('\n', '').replace('\r', '').replace(u'\u3000',u'').replace(u'\xa0', u' ')) != 0):
                    body = p.extract().strip().replace('\n', '').replace('\r', '')
                    first_part = body

        second_part = ""
        tr4s = TextRank4Sentence()
        tr4s.analyze(text=body, lower=True, source='all_filters')
        for item in tr4s.get_key_sentences(num=3):
            second_part = second_part + item.sentence + "。"




        # print(title)
        # print(tag)
        # print(response.meta['link'])
        # print(time)

        #print(sources.replace('来源：',''))
        #print(detail_article)

        # desc = infor.xpath('.//div[@class="article-summary"]/p')
        # detail_desc = desc.xpath('string(.)').extract()[0]
        # if detail_article != "":

        item['time'] = time
        item['source'] = final_source
        item['link'] = response.meta['link']
        item['title'] = title
        item['desc'] = body
        item['tag'] = (response.meta['link']).split('/')[3]
        item['seg'] = first_part
        item['keyword'] = second_part
        return item

    def parse_details_type_3(self,response):
        item = ygnewsItem()
        infor = response.xpath('//div[@class="wh635 left"]/div[@class="wh610 left"]')
        time = infor.xpath('./p[@class="f12_898787 lh20 left"]/span[@id="pubtime_baidu"]/text()').extract()
        final_time = time[0]
        source = infor.xpath('./p[@class="f12_898787 lh20 left"]/span[@id="source_baidu"]/a/text()').extract()
        #final_source = source.replace("来源：","")
        final_source = source[0]
        title = infor.xpath('.//h1[@class="f24 lh40 fb txtcenter f12_292929 yahei"]/text()').extract()[0]

        # 图片新闻没有contentText
        article = infor.xpath('.//div[@class="left f12_292929 sanji_left yahei"]/div[@class="TRS_Editor"]')
        detail_article = article.xpath('normalize-space(string(.))').extract()[0].replace(u'\u3000',u'').replace(u'\xa0', u'')

        if detail_article != "":
            item['time'] = final_time
            item['source'] = final_source
            item['link'] = response.meta['link']
            item['title'] = title
            item['desc'] = detail_article
            item['tag'] = ""
            item['seg'] = ""
            item['keyword'] = ""

            return item

    def strQ2B(self,ustring):
        # 字符串全角转半角
        rstring = ""
        for uchar in ustring:
            inside_code = ord(uchar)
            if inside_code == 12288:  # 全角空格直接转换
                inside_code = 32
            elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
                inside_code -= 65248
            rstring += chr(inside_code)
        return rstring

    def querySimpleProcess(self,ss):
        # query预处理,排除中英文数字以外的字符，全部转为小写
        s1 = self.strQ2B(ss)
        s2 = re.sub(r"(?![\u4e00-\u9fa5]|[0-9a-zA-Z]).", " ", s1)
        s3 = re.sub(r"\s+", " ", s2)
        return s3.strip().lower()

    # 判断是否包含中文
    def check_contain_chinese(self,check_str):
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    # 判断是否包含英文
    def check_contain_english(self,check_str):
        for ch in check_str:
            if u'a' <= ch <= u'z' or u'A' <= ch <= u'Z':
                return True
        return False

    # 删除字符串中的英文字母，以便统计字符数之用
    def delete_letters(self,ss):
        rs = re.sub(r"[a-zA-Z]+", "", ss)
        return rs

    # 先行空格分割，得到列表，再行处理列表中的每个元素
    # 例：Smart校服广告曲=6、Disrespectful Breakup=2
    # 异常：C哩C哩=3 ###处理不了
    # 如果元素不包含中文，则该元素长度记为：1+数字个数
    # 如果元素不包含英文，则该元素长度记为：中文字符数+数字个数，可以直接使用len()方法
    # 如果元素同时包含中英文，则该元素长度记为：中文字符数+数字个数+1
    def countCharacters(self,inputStr):
        tmpStr = self.querySimpleProcess(inputStr)
        str2list = tmpStr.strip().split(" ")
        if len(str2list) > 0:
            charsNum = 0  # 初始化字符计数
            for elem in str2list:
                chineseFlag = self.check_contain_chinese(elem)
                englishFlag = self.check_contain_english(elem)
                if englishFlag == False:  # 不包含英文
                    charsNum = charsNum + len(elem)
                    continue
                else:  # 包含英文
                    elem = self.delete_letters(elem)
                    charsNum = charsNum + 1 + len(elem)
            return charsNum
        return 0

