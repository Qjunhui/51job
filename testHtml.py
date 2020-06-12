#-*- codeing = utf-8 -*-
#@Time : 2020/5/26 3:09 下午
#@Author : 钱俊慧
#@File : testHtml.py
#@Software : PyCharm

import urllib.request
import urllib.error
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

url = 'https://jobs.51job.com/beijing-cpq/122304887.html?s=01&t=0'
# 得到指定url的网页内容
def askURL(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    html = ''
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('gbk')
        print(html)
    except urllib.error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)
    return html


if __name__ == "__main__":
    askURL(url)