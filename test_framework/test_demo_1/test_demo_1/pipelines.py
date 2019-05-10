# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import pymysql.cursors
from twisted.enterprise import adbapi

class TestDemo1Pipeline(object):
    def process_item(self, item, spider):
        # 获取当前工作目录
        base_dir = os.getcwd()
        fiename = base_dir + '/news510.txt'
        # 从内存以追加的方式打开文件，并写入对应的数据
        with open(fiename, 'a', encoding='utf-8') as f:
            f.write("title:  " + item['newstitle'] + '\n')
            f.write("href:   " + item['href'] + '\n')
            # f.write("Title: " + item['content'] + '\n\n')
            # f.write("mp3:  " + item['time'] + '\n')
            # f.write("Time:" + item['source'] + '\n\n')
            # f.write("First: " + item["seg"] + '\n')
            f.write("摘要:" + item['keywords'] + '\n\n')
            # f.write("原文:\n" + item['desc'] + '\n\n')
        return item

class MysqlScrapyPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        # 读取settings中配置的数据库参数
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

    # pipeline默认调用
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    def _conditional_insert(self, tx, item):
        sql = "insert into newsbook(title,link,desc,time,tag,source) values('%s','%s','%s','%s','%s','%s')"
        params = (item['title'], item['link'], item['desc'], item['time'], item['tag'], item['source'])
        tx.execute(sql, params)

    def _handle_error(self, failue, item, spider):
        print (failue)