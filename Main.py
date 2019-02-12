import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import base64
import re
import json
import sys
import time

se = requests.Session()  # 模拟登陆
requests.adapters.DEFAULT_RETRIES = 15
se.mount('http://', HTTPAdapter(max_retries=3))  # 重联
se.mount('https://', HTTPAdapter(max_retries=3))


class BYRBT(object):

    def __init__(self):
        self.base_url = 'https://bt.byr.cn/login.php'
        self.login_url = 'https://bt.byr.cn/takelogin.php'
        self.main_url = 'https://bt.byr.cn'
        self.headers = {
            'authority': 'bt.byr.cn',
            # 'path':'/login.php',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'cookie':'_ga=GA1.2.388369012.1549942748; _gid=GA1.2.374492651.1549942748; _gat=1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            # 'X-Requested-With': 'XMLHttpRequest'
            # 'Connection': 'close',
        }
        self.proxies = {
            'https': 'https://127.0.0.1:1080',
            'http': 'http://127.0.0.1:1080'
        }
        self.username = 'yjw981213',
        self.password = 'yjw3616807',
        self.return_to = 'https://bt.byr.cn'
        self.load_path = 'D:\Software\pythonload'  # 存放图片路径

    def login(self):
        hash = self.getimagehash()
        self.downloadimg(hash)
        imagestring = input("input string:")  # 人工输入验证码
        # imagestring=self.imagestring()# 自动识别验证码
        # 构造请求体
        data = {
            'username': self.username,
            'password': self.password,
            'imagestring': imagestring,
            'imagehash': hash,
        }
        se.post(self.login_url, data=data, headers=self.headers)

    # 获取图片Hash值
    def getimagehash(self):
        loginhtml = se.get(self.base_url, headers=self.headers)
        with open('D:\\Software\\pythonload\\' + 'loginhtml.html', 'w', encoding='utf-8') as f:
            f.write(loginhtml.text)
        loginsoup = BeautifulSoup(loginhtml.text, features="html.parser")
        with open('D:\\Software\\pythonload\\' + 'loginsoup.html', 'w', encoding='utf-8') as f:
            f.write(loginsoup.prettify())
            imagehash = loginsoup.find("input", type="hidden")
            print(imagehash["value"])
            return imagehash["value"]

    # 下载验证码图片
    def downloadimg(self, hash):
        imageurl = self.main_url + "/image.php?action=regimage&imagehash=" + str(hash)
        # print(imageurl)
        img = se.get(imageurl, headers=self.headers, proxies=self.proxies)
        with open('D:\\Software\\pythonload\\' + 'image.png', 'wb') as f:  # 图片要用b,对text要合法化处理
            f.write(img.content)  # 保存图片
        print("Finish download image")

    def imagestring(self):
        AK = 'zWezr2iRFcxkw8DRSffdGBGv'
        SK = 'F1aX3xAEQCLMa6kw5GGjofqjKATE3mgQ'
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + AK + '&client_secret=' + SK
        request = requests.get(host)
        # print(request.text)
        content_json = json.loads(request.text)
        access_token = content_json['access_token']
        # print(access_token)
        url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=" + access_token  # accurate_basic
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        # img本地图片
        f = open('D:\\Software\\pythonload\\' + 'image.png', 'rb')  # 二进制方式打开图文件
        img = base64.b64encode(f.read())
        body = {
            # "url":"https://img-blog.csdn.net/2018060214171639"
            "image": img
        }
        r = requests.post(url, data=body)
        # print(r.text)
        # r_json=json.loads(r.text)
        # result=r_json["words_result"]
        # print(result)
        words = re.findall('"words": "(.*?)"}', str(r.text), re.S)
        for each in words:
            print(each)
            last = re.sub('[^a-zA-Z_0-9]', '', each)  # 仅显示识别出的英文与数字
            print(last)
        f.close()
        print(len(last))
        if len(last) == 6:  # 验证码识别验证
            return last
        else:
            sys.exit()

    def check(self):
        mainhtml = se.get(self.main_url, headers=self.headers)
        with open('D:\\Software\\pythonload\\' + 'mainhtml.html', 'w', encoding='utf-8') as f:
            f.write(mainhtml.text)


if __name__ == '__main__':
    byrbt = BYRBT()
    # byrbt.downloadimg()
    # print(byrbt.imagestring())
    byrbt.login()
    byrbt.check()
