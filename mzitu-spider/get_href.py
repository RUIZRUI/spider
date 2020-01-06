# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os


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
    print('\n'*2)
    print('-'*100)
    print(year.text)
    month_li_list = ul.find_all(name='li')
    for month_li in month_li_list:
        month = month_li.find(name='em')
        print(' '*4 + month.text)
        a_list = month_li.find_all(name='a')
        # print(' '*8 + str(len(a_list)))
        for a in a_list:
            day = a.previous_element
            day = day.split(':')[0]
            href = a.get('href')
            # print('-' + day.split(':')[0] + '-')
            print('./data/img/' + year.text + '/' + month.text + '/' + day + '/')
            # print(' '*10 + day + ' '*3 + href + ' '*3 + a.text)


