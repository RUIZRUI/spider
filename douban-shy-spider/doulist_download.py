# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


## 配置
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/51.0.2704.63 Safari/537.36'}
choice = 1
url = ''
pageNum = 1
dirType = ''

if choice == 1:
    url = 'https://www.douban.com/doulist/111715969/'
    dirType = './data/img/柠檬和sydlafay/私房自拍/'


## 下载页面
# ret = requests.get(url='https://www.douban.com/photos/album/127493069/')

counter = 0     # 下载总数
for i in range(pageNum):
    print('\n'*2)
    print('-'*100)
    print(f'第{i+1}页开始下载...')
    ret = requests.get(url=url, headers=headers)
    # print(ret)
    # 指定编码等于原始页面编码
    ret.encoding = ret.apparent_encoding
    # print(ret.text)



    ## 解析
    soup = BeautifulSoup(ret.text, 'html.parser')       # lxml更快
    divs = soup.find_all(name='div', attrs={'class': 'doulist-item'})

    filedir = dirType
    for div in divs:
        img = div.find_all(name='img')[0]
        # print(counter + ':  ' + img.get('href'))
        src = img.get('src')
        filename = src.split('/')[-1]
        down_img = requests.get(url=src, headers=headers)               # 这里添加headers，可以使图片可以下载成功
        with open(filedir + str(i+1) + '-' + filename, 'wb') as f:
            f.write(down_img.content)
        counter += 1
        print(f"{counter}:  {filename} 下载成功")


