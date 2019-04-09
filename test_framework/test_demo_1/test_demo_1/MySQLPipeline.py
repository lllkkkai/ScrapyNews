import pymysql.cursors

class MySQLPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='127.0.0.1',  # 数据库地址
            port=3306,  # 数据库端口
            db='newsdata',  # 数据库名
            user='root',  # 数据库用户名
            passwd='',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        self.cursor.execute(
            """insert into news_cnbeta(id,title,summary,content,keywords,class_id,source,ranks,url,time,place,terms) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",  # 纯属python操作mysql知识，不熟悉请恶补
            (item['id'], item['title'], item['summary'], item['content'], item['keywords'], item['class_id'], item['source'], item['ranks'], item['url'], item['time'], item['place'], item['terms']))
        # 提交sql语句
        self.connect.commit()
        return item  # 必须实现返回