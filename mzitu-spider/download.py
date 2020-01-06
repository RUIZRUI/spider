# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os


# 配置
# 添加防盗链
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/51.0.2704.63 Safari/537.36', 'Referer': 'https://www.mzitu.com/all/'}


# 爬取单个页面的内容
url = 'https://www.mzitu.com/216363'
ret = requests.get(url=url, headers=headers)
ret.encoding = ret.apparent_encoding
# print(ret.text)


## 解析
soup = BeautifulSoup(ret.text, 'html.parser')
content = soup.find(name='div', attrs={'class': 'content'})
# 获取标题
h2 = content.find(name='h2')

# 创建目录
dirType = './data/img/' + h2.text + '/'
if os.path.exists(dirType) == False:
    os.makedirs(dirType)


# 获取总页数
pagenavi = content.find(name='div', attrs={'class': 'pagenavi'})
page_list = pagenavi.find_all(name='a')
span = page_list[-2].find(name='span')
pageNum = int(span.text)



def getPage(page):
    '''
        由整数生成两位数字串
    '''
    if(page < 10):
        return '0'+str(page)
    else:
        return str(page)


# 获取图片url
filedir = dirType
main_image = content.find(name='div', attrs={'class': 'main-image'})
image = main_image.find(name='img')
src = image.get('src')
index = int(src.rfind('/'))
prefix = src[:index+1]
filename = src[index+1:]
preName = filename[:3]
page = int(filename[3:5])
comma_index = filename.rfind('.')
suffix = filename[comma_index:]



# 根据图片url的规律爬取数据
for i in range(pageNum):
    filename = preName + getPage(i+1) + suffix
    src = prefix + filename
    down_img = requests.get(url=src, headers=headers)
    with open(filedir + filename, 'wb') as f:
        f.write(down_img.content)
    print(f'{i+1}： {filename} 下载成功')



