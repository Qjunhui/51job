from flask import Flask,render_template
import sqlite3 # 数据库

import jieba # 分词
from matplotlib import pyplot as plt # 绘图，数据可视化
from wordcloud import WordCloud # 词云
from PIL import Image # 图片处理
import numpy as np # 矩阵运算

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


# index
@app.route('/index')
def index():
    return home()


# main
@app.route('/main')
def main():
    dataList = []
    con = sqlite3.connect('51job.db')
    cur = con.cursor()
    sql = 'select * from job where length(educate) <= 2'
    data = cur.execute(sql)
    for item in data:
        dataList.append(item)
    cur.close()
    con.close()

    return render_template('main.html',msgs = dataList)


# educate
@app.route('/educate')
def educate():
    educate = [] # 学历
    educateJson = []
    con = sqlite3.connect('51job.db')
    cur = con.cursor()
    sql = 'select educate,count(educate) from job where length(educate) <= 2 group by educate'
    data = cur.execute(sql)
    for item in data:
        educate.append(item[0])
        educateJson.append({'value':item[1],'name':item[0]})

    cur.close()
    con.close()
    return render_template('educate.html',educate=educate,educateJson=educateJson)


# word
@app.route('/word')
def word():
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
    plt.show() # 显示生成的词云图片

    # 输出词云文件到文件
    # plt.savefig('./static/images/job.jpg')

    return render_template('word.html')


# about
@app.route('/about')
def about():
    return render_template('about.html')



if __name__ == '__main__':
    app.run()