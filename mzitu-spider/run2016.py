# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os



def getPage(page):
    '''
        由整数生成两位数字串
    '''
    if(page < 10):
        return '0'+str(page)
    else:
        return str(page)


def download(filedir, url):
    # 判断一个写真集是否下载过
    if os.path.exists(filedir) == True:
        print(f'{filedir} 已经下载，跳过...')
        return

    ret = requests.get(url=url, headers=headers)
    ret.encoding = ret.apparent_encoding

    soup = BeautifulSoup(ret.text, 'html.parser')
    content = soup.find(name='div', attrs={'class': 'content'})

    # h2 = content.find(name='h2')

    if os.path.exists(filedir) == False:
        os.makedirs(filedir)

    pagenavi = content.find(name='div', attrs={'class': 'pagenavi'})
    page_list = pagenavi.find_all(name='a')
    span = page_list[-2].find(name='span')
    pageNum = int(span.text)    


    # 获取图片url
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
    counter = 0
    for i in range(pageNum):
        counter = counter + 1
        filename = preName + getPage(i+1) + suffix
        src = prefix + filename
        down_img = requests.get(url=src, headers=headers)
        with open(filedir + filename, 'wb') as f:
            f.write(down_img.content)
        # print(f'{i+1}： {filedir}{filename} 下载成功')
    if(counter == pageNum):
        print(f'{filedir} 下载成功 {counter}张')
    else:
        print(f'---------------{filedir} 下载失败, 共{pageNum}张，实际下载{counter}张')







# 配置
# 添加防盗链
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/51.0.2704.63 Safari/537.36', 'Referer': 'https://www.mzitu.com/all/'}


url = 'https://www.mzitu.com/all/'
ret = requests.get(url=url, headers=headers)
ret.encoding = ret.apparent_encoding
# print(ret.text)


# 解析
soup = BeautifulSoup(ret.text, 'html.parser')
all_div = soup.find(name='div', attrs={'class': 'all'})

# 年度列表
year_list = all_div.find_all(name='div', attrs={'class': 'year'})
# 每年的链接列表
ul_list = all_div.find_all(name='ul', attrs={'class': 'archives'})

for year, ul in zip(year_list, ul_list):
    if year.text == '2016年':
        print('ok')
        print('\n'*2)
        print('-'*100)
        print(year.text)
        month_li_list = ul.find_all(name='li')
        for month_li in month_li_list:
            month = month_li.find(name='em')
            # print(month.text)
            if month.text in ['06月', '05月', '04月', '03月', '02月', '01月']:
                print(' '*4 + month.text)
                a_list = month_li.find_all(name='a')
                # print(' '*8 + str(len(a_list)))
                for a in a_list:
                    day = a.previous_element
                    day = day.split(':')[0]
                    href = a.get('href')
                    filedir = '/Users/zhengxiang/spider/www.mzitu.com/data/img/' + year.text + '/' + month.text + '/' + day + '/' + a.text + '/'
                    download(filedir, href)
                    # print(' '*10 + href + ' '*3 + a.text)



