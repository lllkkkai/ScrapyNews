from urllib import request
from bs4 import BeautifulSoup
import re
import urllib

x = 0
for i in range(1,2):
    if i > 1:
        url = "https://tieba.baidu.com/p/2555125530"+"?pn="+str(i)
    else:
        url = "https://tieba.baidu.com/p/2555125530"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    page = request.Request(url, headers=headers)
    page_info = request.urlopen(page).read().decode('utf-8')

    soup = BeautifulSoup(page_info, 'html.parser')
    imgurls = soup.find_all('img')

    for imgurl in imgurls:
        her = imgurl.get('src')
        if re.match(r'^https?://imgsa.baidu.com.*', her):
            print(her)
            # urllib.request.urlretrieve(her, 'C:\py_result\pic1\%s.jpg' % x)
            x+=1

