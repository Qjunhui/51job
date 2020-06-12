#-*- codeing = utf-8 -*-
#@Time : 2020/5/25 1:40 下午
#@Author : 钱俊慧
#@File : WordCloud.py
#@Software : PyCharm

# pip install jieba 时因国外网站网速太慢出错,故使用国内镜像。
# pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple jieba
import jieba  # 分词
from matplotlib import pyplot as plt # 绘图，数据可视化
from wordcloud import WordCloud # 词云
from PIL import Image # 图片处理
import numpy as np # 矩阵运算
import sqlite3 # 数据库

# 1. 词云所需的文字
con = sqlite3.connect('51job.db')
cur = con.cursor()
sql = 'select company_name from job'
data = cur.execute(sql)
text = ''
for item in data:
    text += item[0]
cur.close()
con.close()
print(text)
# 2.分词
cut = jieba.cut(text)
string = ' '.join(cut)

# 3.背景图片
img = Image.open(r'./static/images/tree.jpeg')
imgArray = np.array(img)  # 将图片转换为数组
wc = WordCloud(
    background_color='white',
    mask=imgArray,
    font_path='/Library/Fonts/Songti.ttc'
)
wc.generate_from_text(string)

# 4.绘图
flg = plt.figure(1)
plt.imshow(wc)
plt.axis('off')  # 是否显示坐标轴
# plt.show()  # 显示生成的词云图片

# 输出词云文件到文件
plt.savefig('./static/images/job.jpg')
