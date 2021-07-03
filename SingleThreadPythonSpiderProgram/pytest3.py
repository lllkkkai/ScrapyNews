from urllib import request
from bs4 import BeautifulSoup  # Beautiful Soup是一个可以从HTML或XML文件中提取结构化数据的Python库

# 构造头文件，模拟浏览器访问
for i in range(2,20):
    url = "http://news.gzcc.cn/html/xiaoyuanxinwen/"+ str(i)+".html"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    page = request.Request(url, headers=headers)
    page_info = request.urlopen(page).read().decode('utf-8')  # 打开Url,获取HttpResponse返回对象并读取其ResposneBody

# 将获取到的内容转换成BeautifulSoup格式，并将html.parser作为解析器
    soup = BeautifulSoup(page_info, 'html.parser')
# 以格式化的形式打印html
# print(soup.prettify())

    titles = soup.find_all('div',class_="news-list-title")  # 查找所有a标签中class='title'的语句
    # with open(r"C:\py_result\titles.txt", "w") as file:  # 在磁盘以只写的方式打开/创建一个名为 articles 的txt文件
    #     for title in titles:
    #         file.write(title.string + '\n')
    for title in titles:
        print(title.string)

'''
# 打印查找到的每一个a标签的string和文章链接
    for title in titles:
        print(title.string)
        print("https://www.cnbeta.com/top10.htm" + title.get('href'))   
'''

# open()是读写文件的函数,with语句会自动close()已打开文件

#         #file.write("http://www.jianshu.com" + title.get('href') + '\n\n')
