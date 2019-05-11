import pymysql.cursors

class MySQLPipeline_cnr(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='47.100.163.195',  # 数据库地址
            port=3306,  # 数据库端口
            db='test',  # 数据库名
            user='recommend',  # 数据库用户名
            passwd='recommend',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        self.cursor.execute(
            """insert into News(newstitle,href,content,classid,ranking,source,time,keywords,terms,website) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",  # 纯属python操作mysql知识，不熟悉请恶补
            (item['newstitle'], item['href'], item['content'],item['class_id'], item['ranking'], item['source'], item['time'],item['keywords'],item['terms'],item['website']))
        # 提交sql语句
        self.connect.commit()
        return item  # 必须实现返回