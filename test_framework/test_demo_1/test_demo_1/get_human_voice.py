import requests
import pymysql.cursors
from test_demo_1.mmr import getAbstract

connect = pymysql.connect(
            host='47.100.163.195',  # 数据库地址
            port=3306,  # 数据库端口
            db='test',  # 数据库名
            user='recommend',  # 数据库用户名
            passwd='recommend',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
        # 通过cursor执行增删查改
cursor = connect.cursor()
sql = 'select newsid,content from News where website = "cnr" and abs is null'
cursor.execute(sql)
results = cursor.fetchall()
connect.close()

connect2 = pymysql.connect(
            host='47.100.163.195',  # 数据库地址
            port=3306,  # 数据库端口
            db='test',  # 数据库名
            user='recommend',  # 数据库用户名
            passwd='recommend',  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
        # 通过cursor执行增删查改
cursor2 = connect2.cursor()
for wert in results:
    newsid = wert[0]
    content = wert[1]
    abs = getAbstract(content)
    sql2 = 'UPDATE News SET abs = %s where newsid = %s;'
    cursor2.execute(sql2,(abs,newsid))
    connect2.commit()




# r = requests.get('http://47.100.163.195/qa-service/tts/generateAudio', params=payload)