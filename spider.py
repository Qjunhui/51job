#-*- codeing = utf-8 -*-
#@Time : 2020/5/25 4:11 下午
#@Author : 钱俊慧
#@File : spider.py
#@Software : PyCharm


from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.error
from urllib import parse
import sqlite3
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import xlwt

dbPath = "51job.db"
kw = input('请输入岗位关键字：')
keyword = parse.quote(kw)
pageNum = 1
jobList = []

def main():
    baseUrl = "https://search.51job.com/list/010000,000000,0000,00,9,99," + keyword + ",2," + str(pageNum) + ".html"
    # 1.爬取网页
    for i in range(1, 5):
        url = "https://search.51job.com/list/010000,000000,0000,00,9,99," + keyword + ",2," + str(i) + ".html"
        pageList = getlink(url)
        if len(pageList) == 0:
            break
        for jobUrl in pageList:
            getData(jobUrl)
    #3.保存数据
    saveDataDB(jobList,dbPath)


# 获取到工作岗位的链接
def getlink(url):
    jobLink = []
    html = askURL(url)

    bs = BeautifulSoup(html, 'html.parser')
    elDiv = bs.select('.el > .t1 > span > a')

    for link in elDiv:
        jobLink.append(link['href'])
        jobList.append({'job_link':link['href']})
    return jobLink


#爬取网页(一个页面)
def getData(jobUrl):
    # 解析数据
    html = askURL(jobUrl) # 详情页
    bs = BeautifulSoup(html, 'html.parser')

    for job in jobList:
        if jobUrl == job['job_link']:
            job_name = bs.select('.cn>h1')
            for jname in job_name:
                job['job_name'] = jname['title']

            company_name = bs.select('.cname>.catn')
            for cname in company_name:
                job['company_name'] = cname['title']

            jobmsg = bs.select('.msg')
            for jmsg in jobmsg:
                jobmsg = jmsg['title'].split('|')
                job['area'] = jobmsg[0].strip()
                if len(jobmsg) == 4:
                    job['educate'] = jobmsg[1].strip()
                else:
                    job['educate'] = jobmsg[2].strip()

            salary = bs.select('.cn>strong')
            for s in salary:
                job['salary'] = s.text

            info = bs.select('.job_msg>p')
            jobMsg = ''
            for item in info:
                jobMsg += item.text
            job['info'] = jobMsg
    return jobList


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
        # print(html)
    except UnicodeDecodeError:
        response = urllib.request.urlopen(request)
        html = response.read()
    except urllib.error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)
    return html


#保存数据
def saveDataDB(jobList,dbPath):
    # init_db(dbPath)
    conn = sqlite3.connect(dbPath) # 打开或创建数据库文件
    cur = conn.cursor() # 获取游标

    # 插入数据
    for data in jobList:
        sql = '''
            insert into job(
                job_link, 
                job_name, 
                area, 
                company_name, 
                salary, 
                educate, 
                info)
             values ('%s', '%s', '%s', '%s', '%s', '%s', '%s');
        ''' % (data['job_link'], data['job_name'], data['area'], data['company_name'], data['salary'], data['educate'], data['info'])

        cur.execute(sql)
        conn.commit() # 提交数据库操作

    cur.close()
    conn.close() # 关闭数据库连接


# 创建数据表
def init_db(dbPath):
    sql = '''
        create table job(
            id integer primary key autoincrement,
            job_link text,
            job_name text,
            area varchar,
            company_name varchar,
            salary numeric,
            educate text,
            info text
        )
    '''
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # init_db(dbPath)
    main()