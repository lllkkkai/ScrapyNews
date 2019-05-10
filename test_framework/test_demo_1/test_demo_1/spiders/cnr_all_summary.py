import scrapy
import re
import jieba.analyse
from test_demo_1.items import TestDemo1Item
import codecs
from test_demo_1.textrank4zh import TextRank4Keyword, TextRank4Sentence

class MySpider(scrapy.Spider):
    name = 'cnr_all_summary'

    handle_httpstatus_list = [404, 500]
    all_article_urls = []
    first_start_flag = 0    # 0 means first-start
                            # 1 means update
    sample_time = '2019-03-06 18:00:00'  # Get the newst time from sql

    stop_words = [',','.','?',':',';','"','\'','/','+','-','[',']','{','}','@','#','$','%','^','&','*','(',')','=','<','>','！','，','。','：','；','“','”','‘','’','？','《','》','—','（','）',' ']

    def start_requests(self):
        type_1_base_urls = [
            # 'http://china.cnr.cn/yaowen/',
            # 'http://news.cnr.cn/dj/',
            # 'http://china.cnr.cn/xwwgf/',
            # 'http://news.cnr.cn/comment/sp/',
            # 'http://news.cnr.cn/comment/latest/',
            # 'http://news.cnr.cn/native/gd/',
            'http://news.cnr.cn/native/city/',
            # 'http://news.cnr.cn/native/comment/',
            # 'http://news.cnr.cn/local/tj/',
            # 'http://news.cnr.cn/gjxw/gnews/',
            # 'http://finance.cnr.cn/2014jingji/djbd/',
            # 'http://finance.cnr.cn/2014jingji/yw/',
            # 'http://finance.cnr.cn/2014jingji/jrlc/',
            # 'http://finance.cnr.cn/jysk/',
            # 'http://finance.cnr.cn/2014jingji/stock/',
            # 'http://finance.cnr.cn/2014jingji/glwjr/',
            # 'http://finance.cnr.cn/2014jingji/glwjr/',
            # 'http://sports.cnr.cn/basket_ball/basketballhot/',
            # 'http://sports.cnr.cn/news/',
            # 'http://sports.cnr.cn/internal/news/'
            # 'http://sports.cnr.cn/international/news/',
            # 'http://sports.cnr.cn/synthesize/news/',
            # 'http://sports.cnr.cn/ice_snow/ice_snow/',
            # 'http://sports.cnr.cn/Industry/',
            # 'http://sports.cnr.cn/Original/',
            # 'http://edu.cnr.cn/list/',
            # 'http://edu.cnr.cn/kaos/gk/',
            # 'http://edu.cnr.cn/lxcg/',
            # 'http://edu.cnr.cn/zxx/',
            # 'http://edu.cnr.cn/zhic/',
            # 'http://edu.cnr.cn/dj/',
            # 'http://edu.cnr.cn/gc/',
            # 'http://ent.cnr.cn/zx/',
            # 'http://ent.cnr.cn/dj/',
            # 'http://ent.cnr.cn/wy/',
            # 'http://ent.cnr.cn/gy/',
            # 'http://ent.cnr.cn/chuanmei/',
            # 'http://www.cnr.cn/chanjing/gundong/',
            # 'http://www.cnr.cn/chanjing/dujia/',
            # 'http://www.cnr.cn/chanjing/guancha/',
            # 'http://www.cnr.cn/chanjing/jujiao/',
            # 'http://www.cnr.cn/chanjing/wenhua/',
            # 'http://www.cnr.cn/chanjing/nengyuan/',
            # 'http://www.cnr.cn/chanjing/fangchan/',
            # 'http://www.cnr.cn/chanjing/jiadian/',
            # 'http://www.cnr.cn/chanjing/kuaixiao/',
            # 'http://www.cnr.cn/chanjing/huodong/',
            # 'http://tech.cnr.cn/techds/',
            # 'http://tech.cnr.cn/techit/',
            # 'http://tech.cnr.cn/techhlw/',
            # 'http://tech.cnr.cn/techyd/',
            # 'http://tech.cnr.cn/digi/',
            # 'http://tech.cnr.cn/techtj/',
            # 'http://tech.cnr.cn/techgsrw/',
            # 'http://tech.cnr.cn/techxp/',
            # 'http://tech.cnr.cn/techtx/',
            # 'http://tech.cnr.cn/techqyqs/',
            # 'http://travel.cnr.cn/2011lvpd/gny/news/',
            # 'http://travel.cnr.cn/2011lvpd/cjy/news/',
            # 'http://travel.cnr.cn/hydt/',
            # 'http://travel.cnr.cn/dj/',
            # 'http://travel.cnr.cn/railway/',
            # 'http://health.cnr.cn/jkjryw/',
            # 'http://health.cnr.cn/jkysbj/',
            # 'http://health.cnr.cn/xljt/',
            # 'http://health.cnr.cn/my/',
            # 'http://health.cnr.cn/s/',
            # 'http://health.cnr.cn/populirization/',
            # 'http://health.cnr.cn/jkbgt/',
            # 'http://health.cnr.cn/jkgdxw/',
            # 'http://health.cnr.cn/yg/',
            # 'http://health.cnr.cn/qy/',
            # 'http://auto.cnr.cn/2015rmgz/',
            # 'http://auto.cnr.cn/zcxg/',
            # 'http://gongyi.cnr.cn/news/',
            # 'http://gongyi.cnr.cn/qiye/',
            # 'http://gongyi.cnr.cn/star/',
            # 'http://gongyi.cnr.cn/story/',
            # 'http://gongyi.cnr.cn/huodong/',
            # 'http://gongyi.cnr.cn/shalong/',
            # 'http://gongyi.cnr.cn/point/',
            # 'http://gongyi.cnr.cn/xingdong/',
            # 'http://gongyi.cnr.cn/top/',
            # 'http://country.cnr.cn/gundong/',
            # 'http://country.cnr.cn/market/',
            # 'http://country.cnr.cn/snsp/',
            # 'http://country.cnr.cn/mantan/',
            # 'http://country.cnr.cn/bangyang/',
            # 'http://country.cnr.cn/xtxq/',
        ]

        type_2_base_urls = [
            'http://finance.cnr.cn/315/gz/',
            'http://finance.cnr.cn/txcj/',
            'http://finance.cnr.cn/jjpl/',
        ]
        type_3_base_urls = [
            'http://military.cnr.cn/gz/',
            'http://military.cnr.cn/zgjq/',
        ]
        type_4_base_urls = [
            'http://military.cnr.cn/gjjs/',
            'http://military.cnr.cn/ycdj/',
            'http://military.cnr.cn/zgjq/gcdt/',
            'http://military.cnr.cn/zgjq/lj/',
            'http://military.cnr.cn/zgjq/hj/',
            'http://military.cnr.cn/zgjq/kj/',
            'http://military.cnr.cn/zgjq/ep/',
        ]
        type_5_base_urls = [
            'http://auto.cnr.cn/zxss/',
            'http://auto.cnr.cn/2015xc/',
            'http://auto.cnr.cn/qczcjj/',
            'http://auto.cnr.cn/ygbgt/',
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
            while page < 3:    # if page < 10 you get 404 here deal it quick
                detail_url = url + 'index_' + str(page) + '.html'
                type_1_urls.append(detail_url)
                page += 1

        for url in type_2_base_urls:
            # print(url.split('/')[-3]) #get the origin tag (only in native,gjxw)
            type_2_urls.append(url)
            page = 1
            while page < 3:
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
        #
        # for link in type_3_urls:
        #     print(link)
        #     yield scrapy.Request(url=link, callback=self.parse_type_3)
        #
        # for link in type_4_urls:
        #     print(link)
        #     yield scrapy.Request(url=link, callback=self.parse_type_4)
        #
        # for link in type_5_urls:
        #     print(link)
        #     yield scrapy.Request(url=link, callback=self.parse_type_5)
        #
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

    def switch_test_item(self,item):
        switcher = {
            "2014jkpd": 21,
            "chanjing": 8,
            "china": 1,
            "comment": 6,
            "dj": 1,
            "ent": 12,
            "gundong": 8,
            "jingji": 8,
            "jkgdxw": 21,
            "jy": 20,
            "list": 0,
            "lvyou": 17,
            "native": 1,
            "newscenter": 0,
            "tech": 9,
            "techgd": 9,
            "2013qcpd": 19,
            "gongyi": 18,
            "news": 1,
            "ylzt": 18,
            "zgxc": 1,
            "jmhd": 4,
            "js2014": 4,
            "yc": 19,
            "rdzx" : 19,
            "hngd" : 19,
            "theory": 0,
        }
        return switcher.get(item, "other")

    def parse_details(self,response):
        item = TestDemo1Item()
        # tag = response.xpath('//p[@class="daoHang"]/a/text()').extract()[1] # Bug Here !
        infor = response.xpath('//div[@class="article"]')
        time = infor.xpath('.//div[@class="subject"]/div[@class="source"]/span/text()').extract()[0]
        source = infor.xpath('.//div[@class="subject"]/div[@class="source"]/span/text()').extract()[1]
        final_source = source.replace("来源：","")
        title = infor.xpath('.//div[@class="subject"]/h2/text()').extract()[0]

        # 图片新闻没有contentText
        content = infor.xpath('.//div[@class="articleMain clearfix"]/div[@class="content"]/div[@class="contentText"]//p[not(contains(@align,"center"))][not(contains(@style,"text-align: center;"))]')
        body = ""
        terms = ""
        for p in content.xpath('string(.)'):
            if (len(p.extract().strip().replace('\n', '').replace('\r', '')) != 0):
                body = body + "**" + p.extract().strip().replace('\n', '').replace('\r', '')
                terms = terms + p.extract().strip().replace('\n', '').replace('\r', '')

        # jieba here
        temp_key = jieba.analyse.extract_tags(terms, topK=6)
        final_key = (",".join(temp_key))
        temp_seg = jieba.cut(terms, cut_all=False)
        final_seg = (",".join(temp_seg))

        start_key = ""
        title_no_space = title.strip()
        title_seg = jieba.cut(title_no_space, cut_all=False)
        for word in title_seg:
            if word not in self.stop_words:
                if word != '\t':
                    start_key += word
                    start_key += ","
        # start_key = (",".join(title_seg))
        keywords = start_key + final_key

        if terms != "":
            item['newstitle'] = title
            item['time'] = time
            item['source'] = final_source
            item['href'] = response.meta['link']
            item['class_id'] = self.switch_test_item((response.meta['link']).split('/')[3])
            item['content'] = body
            #item['place'] = self.switch_test_item((response.meta['link']).split('/')[3])
            # item['place'] = (response.meta['link']).split('/')[3]
            item['terms'] = final_seg
            item['keywords'] = keywords
            item['ranking'] = int(0)
            # item['abstract'] = ""
            item['website'] = "cnr"
            return item
        # detail_article = article.xpath('normalize-space(string(.))').extract()[0].replace(u'\u3000',u'').replace(u'\xa0', u' ')
        # body = ""
        # count = 0
        # first_part = ""
        # # count表示自然段数
        # for p in article.xpath('normalize-space(string(.))'):
        #     if (count != 0):
        #         count += 1
        #         if (len(p.extract().strip().replace('\n', '').replace('\r', '').replace(u'\u3000',u'').replace(u'\xa0', u' ')) != 0):
        #             body = body + "\n" + p.extract().strip().replace('\n', '').replace('\r', '')
        #             if(self.countCharacters(first_part) < 150):
        #                 final_first_part = first_part + p.extract().strip().replace('\n', '').replace('\r', '')
        #                 if(self.countCharacters(final_first_part) < 300):
        #                     first_part = final_first_part
        #
        #     if (count == 0):
        #         count += 1
        #         if (len(p.extract().strip().replace('\n', '').replace('\r', '').replace(u'\u3000',u'').replace(u'\xa0', u' ')) != 0):
        #             body = p.extract().strip().replace('\n', '').replace('\r', '')
        #             first_part = body
        #
        # first_part_list = first_part.split('。')
        # second_part = ""
        # tr4s = TextRank4Sentence()
        # tr4s.analyze(text=body, lower=True, source='all_filters')
        # for item in tr4s.get_key_sentences(num=7):
        #     for p in first_part_list:
        #         flag = 0
        #         if item.sentence == p:
        #             flag = 1
        #             break
        #
        #         if item.index == 0:
        #             flag = 1
        #             break
        #     if flag == 0:
        #         second_part = second_part + item.sentence + "。"
        #
        # summary = first_part + second_part

    def parse_details_type_3(self,response):
        item = TestDemo1Item()
        infor = response.xpath('//div[@class="wh635 left"]/div[@class="wh610 left"]')
        time = infor.xpath('./p[@class="f12_898787 lh20 left"]/span[@id="pubtime_baidu"]/text()').extract()
        final_time = time[0]
        source = infor.xpath('./p[@class="f12_898787 lh20 left"]/span[@id="source_baidu"]/a/text()').extract()
        final_source = source[0]
        title = infor.xpath('.//h1[@class="f24 lh40 fb txtcenter f12_292929 yahei"]/text()').extract()[0]

        # 图片新闻没有contentText
        content = infor.xpath('.//div[@class="left f12_292929 sanji_left yahei"]/div[@class="TRS_Editor"]//p')
        #detail_article = article.xpath('normalize-space(string(.))').extract()[0].replace(u'\u3000',u'').replace(u'\xa0', u'')
        body = ""
        terms = ""
        for p in content.xpath('string(.)'):
            if (len(p.extract().strip().replace('\n', '').replace('\r', '')) != 0):
                body = body + "**" + p.extract().strip().replace('\n', '').replace('\r', '')
                terms = terms + p.extract().strip().replace('\n', '').replace('\r', '')

        temp_key = jieba.analyse.extract_tags(terms, topK=6)
        final_key = (",".join(temp_key))
        temp_seg = jieba.cut(terms, cut_all=False)
        final_seg = (",".join(temp_seg))

        start_key = ""
        title_no_space = title.strip()
        title_seg = jieba.cut(title_no_space, cut_all=False)
        for word in title_seg:
            if word not in self.stop_words:
                if word != '\t':
                    start_key += word
                    start_key += ","
        # start_key = (",".join(title_seg))
        keywords = start_key + final_key

        if terms != "":
            item['time'] = final_time
            item['source'] = final_source
            item['href'] = response.meta['link']
            item['newstitle'] = title
            item['content'] = body
            item['class_id'] = self.switch_test_item((response.meta['link']).split('/')[3])
            item['terms'] = final_seg
            item['keywords'] = keywords
            item['website'] = "cnr"
            #item['abstract'] = ""
            #item['place'] = (response.meta['link']).split('/')[3]
            item['ranking'] = int(0)

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

