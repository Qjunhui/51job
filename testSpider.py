#-*- codeing = utf-8 -*-
#@Time : 2020/5/26 3:03 下午
#@Author : 钱俊慧
#@File : testSpider.py
#@Software : PyCharm

from bs4 import BeautifulSoup

# urlList
# html = open('jobUrlList.html','r')
# bs = BeautifulSoup(html, 'html.parser')
# elDiv = bs.select('.el > .t1 > span > a')
#
# for link in elDiv:
#     print(link['href'])

html = open('jobPage.html','r',encoding='gbk')
bs = BeautifulSoup(html, 'html.parser')

job_name = bs.select('.cn>h1')
for jname in job_name:
    job_name = jname['title']

company_name = bs.select('.cname>.catn')
for cname in company_name:
    company_name = cname['title']

jobmsg = bs.select('.msg')
print(jobmsg)
for jmsg in jobmsg:
    jobmsg = jmsg['title'].split('|')

    area = jobmsg[0].strip()
    if len(jobmsg) == 4:
        educate = jobmsg[1].strip()
    else:
        educate = jobmsg[2].strip()

salary = bs.select('.cn>strong')
for s in salary:
    salary = s.text

info = bs.select('.job_msg>p')
jobMsg = ''
for item in info:
    jobMsg += item.text
info = jobMsg


# print(job_name)
# print(area)
# print(company_name)
# print(salary)
# print(educate)
# print(info)




