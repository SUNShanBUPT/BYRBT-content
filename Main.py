import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import time
from tesserocr import PyTessBaseAPI

se = requests.Session()  # 模拟登陆
requests.adapters.DEFAULT_RETRIES = 15
se.mount('http://', HTTPAdapter(max_retries=3))  # 重联
se.mount('https://', HTTPAdapter(max_retries=3))


class BYRBT(object):

    def __init__(self):
        self.login_url = 'https://bt.byr.cn/login.php'
        self.main_url = 'https://bt.byr.cn'
        self.headers = {
            # 'Host': 'accounts.pixiv.net',
            # 'Origin': 'https://accounts.pixiv.net',
            'Referer': 'https://bt.byr.cn/login.php',
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
        self.imagestring

        self.return_to = 'https://bt.byr.cn'
        self.html_path = 'D:\Software\pythonload\Re.html'
        self.load_path = 'D:\Software\pythonload'  # 存放图片路径
        self.get_number = 10

    def login(self):
        post_key_xml = se.get(self.base_url, headers=self.headers).text
        post_key_soup = BeautifulSoup(post_key_xml, 'lxml')
        self.post_key = post_key_soup.find('input')['value']
        # 构造请求体
        data = {
            'pixiv_id': self.pixiv_id,
            'password': self.password,
            'post_key': self.post_key,
            'return_to': self.return_to
        }
        se.post(self.login_url, data=data, headers=self.headers)