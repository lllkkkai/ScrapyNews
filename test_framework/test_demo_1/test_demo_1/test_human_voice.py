import requests
from urllib import request
import pymysql.cursors
from test_demo_1.mmr import getAbstract
import json

newsid = 1
abs = 'aaaaaaaaaaaaaa'
payload = {
        'newsid' : newsid,
        'abs'    : abs
    }
response = requests.get('http://47.100.163.195/qa-service/tts/generateAudio', params=payload)
result = response.text
all_json = json.loads(result)
print(all_json['data'])