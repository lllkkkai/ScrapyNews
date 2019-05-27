import requests
import pymysql.cursors
from test_demo_1.mmr import getAbstract
import json

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
sql = 'select newsid,abs from News where website in ("cnr","cnbeta") and audiosurl is null limit 0,2'
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
    abs = wert[1]
    payload = {
        'newsid' : newsid,
        'abs'    : abs
    }
    response = requests.get('http://47.100.163.195/qa-service/tts/generateAudio', params=payload)
    all_json = json.loads(response)
    audiosurl = all_json['data']
    sql2 = 'UPDATE News SET audiosurl = %s where newsid = %s;'
    cursor2.execute(sql2,(audiosurl,newsid))
    connect2.commit()
