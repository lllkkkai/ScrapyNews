from urllib import request
from bs4 import BeautifulSoup  # Beautiful Soup是一个可以从HTML或XML文件中提取结构化数据的Python库
import re

# 构造头文件，模拟浏览器访问
url = "https://www.cnbeta.com/top10.htm"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
page = request.Request(url, headers=headers)
page_info = request.urlopen(page).read().decode('utf-8')  # 打开Url,获取HttpResponse返回对象并读取其ResposneBody

# 将获取到的内容转换成BeautifulSoup格式，并将html.parser作为解析器
soup = BeautifulSoup(page_info, 'html.parser')
# 以格式化的形式打印html
# print(soup.prettify())

titles = soup.select("dt>a")  # 查找所有a标签中class='title'的语句
with open(r"C:\py_result\titles.txt", "w",encoding='utf-8') as file:
    for title in titles:
        url_in = title.get('href')
        if re.match(r'^https?:/{2}\w.+$', url_in):
            a = 1
        else:
            url_in = "http:"+url_in

        file.write("标题: "+title.string + '\n')
        file.write("链接: "+url_in + '\n')
        print(title.string)
        print(url_in)

        page = request.Request(url_in, headers=headers)
        page_info = request.urlopen(page).read().decode('utf-8')  # 打开Url,获取HttpResponse返回对象并读取其ResposneBody
        soup = BeautifulSoup(page_info, 'html.parser')
        details = soup.select("div>.article-summary>p")  # 查找所有a标签中class='title'的语句
        for detail in details:
            print(detail.get_text())
            file.write("内容: " + detail.get_text() + '\n\n')


'''
# 打印查找到的每一个a标签的string和文章链接
    for title in titles:
        print(title.string)
        print("https://www.cnbeta.com/top10.htm" + title.get('href'))   
'''

# open()是读写文件的函数,with语句会自动close()已打开文件

#     for title in titles:
#         file.write(title.string + '\n')
#         #file.write("http://www.jianshu.com" + title.get('href') + '\n\n')
