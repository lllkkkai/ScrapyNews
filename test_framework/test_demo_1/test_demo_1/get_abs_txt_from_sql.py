import pymysql.cursors
import os
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
sql = 'select newsid,content,abs from News where website = "cnr" and classid = 0'
cursor.execute(sql)
results = cursor.fetchall()
base_dir = os.getcwd()
fiename = base_dir + '/AbsProblem.txt'
with open(fiename, 'a', encoding='utf-8') as f:
    for wert in results:
        newid = wert[0]
        content = wert[1]
        abs = wert[2]
        f.write(str(newid) + '\n')
        f.write(content + '\n')
        f.write(abs + '\n')

connect.close()