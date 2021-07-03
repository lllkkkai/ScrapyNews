from urllib import request
from bs4 import BeautifulSoup
import re
import urllib

x = 0
url = "https://www.zhihu.com/question/26541011"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
page = request.Request(url, headers=headers)
page_info = request.urlopen(page).read().decode('utf-8')

soup = BeautifulSoup(page_info, 'html.parser')
imgurls = soup.find_all('img')

for imgurl in imgurls:
    her = imgurl.get('src')
    if re.match(r'^https?://pic.*', her):
        print(her)
        # urllib.request.urlretrieve(her, 'C:\py_result\pic1\%s.jpg' % x)
    x+=1

