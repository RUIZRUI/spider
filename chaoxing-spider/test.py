# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import json

# 配置
# 添加防盗链
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    'Cookie': 'k8s=0baa706986b839aba84715acec2e0a4645e084f8; jrose=3CEE2D36C5CA465D8F808546FCC84F32.mooc-1523198214-zz7qv; route=440ceb57420433374ff0504da9778fc7; lv=1; fid=67889; _uid=69768608; uf=fbe48ba271b0dbbdb5427138866c41c2891819d1110d1b2aef06b79cb59fb462852dbd3f4b696450e768b4aebacb023e913b662843f1f4ad6d92e371d7fdf6441f4d46e6e633da49efcee624f188c883c992d031135b2ab786e12ac4b4c2400bee1ac9eb75c67126aa2ebad65cd196bb; _d=1652527990855; UID=69768608; vc=BD3B5D85E3F1CC14E3EB14AAD86C4029; vc2=E27FBEE05EC864744AD2E352B7A688A6; vc3=EXVAKMjVUwPV%2FrNMBsD6lBJpV1wPUSbJV36jH1r81%2FN%2Fh60yMZ53Sm3%2FoonKLXgwwaEjQhzVKMacO9Hq5%2BDi4vhZWZsk3ZN2ZKYAolRGTf%2BS0uNDZHWiBJzR53KMjqQlr46i3bOJ7dFRpurQdbZjhKB94P%2BgThKq8BAZFhuTWLE%3Df5c96c9432fae0adc0ab5f2002e3d5ad; xxtenc=d504f7001b98cd9c1466feb27f4a8871; DSSTASH_LOG=C_38-UN_62371-US_69768608-T_1652527990857; thirdRegist=0',
    'Referer': 'https://mooc1-1.chaoxing.com/',
    'Connection': 'keep-alive'
}

# 目标 url
url = 'https://mooc1-1.chaoxing.com/work/reviewTheList?courseId=223137437&classId=51876029&workId=17997488&isdisplaytable=2&mooc=1&isWork=true&workSystem=0&openc=31aea7eb6e55d090fdd12012590e10d4&ut=t'


url0 = 'https://mooc1-1.chaoxing.com/work/searchMarkList?sw=&workId=17997488&courseId=223137437&pageNum=0&classId=51876029&isdisplaytable=2&isWork=true&tempClassId=51876029&dengji=0&firstHeader=2&schoolId=-1&schoolName=&sort=-1&order=0&workSystem=0&openc=31aea7eb6e55d090fdd12012590e10d4'
url00 ='https://mooc1-1.chaoxing.com/work/searchMarkList?sw=&workId=17997488&courseId=223137437&pageNum=1&classId=51876029&isdisplaytable=2&isWork=true&tempClassId=51876029&dengji=0&firstHeader=2&schoolId=-1&schoolName=&sort=-1&order=0&workSystem=0&openc=31aea7eb6e55d090fdd12012590e10d4'
url01 ='https://mooc1-1.chaoxing.com/work/searchMarkList?sw=&workId=17997488&courseId=223137437&pageNum=1&classId=51876029&isdisplaytable=2&isWork=true&tempClassId=51876029&dengji=0&firstHeader=2&schoolId=-1&schoolName=&sort=-1&order=0&workSystem=0&openc=31aea7eb6e55d090fdd12012590e10d4'
url02 ='https://mooc1-1.chaoxing.com/work/searchMarkList?sw=&workId=17997488&courseId=223137437&pageNum=0&classId=51876029&isdisplaytable=2&isWork=true&tempClassId=51876029&dengji=0&firstHeader=2&schoolId=-1&schoolName=&sort=-1&order=0&workSystem=0&openc=31aea7eb6e55d090fdd12012590e10d4'

url1 = 'https://mooc1-1.chaoxing.com/work/searchMarkList?sw=&workId=17997488&courseId=223137437&pageNum=2&classId=51876029&isdisplaytable=2&isWork=true&tempClassId=51876029&dengji=0&firstHeader=2&schoolId=-1&schoolName=&sort=-1&order=0&workSystem=0&openc=31aea7eb6e55d090fdd12012590e10d4'
url2 = 'https://mooc1-1.chaoxing.com/work/searchMarkList?sw=&workId=17997488&courseId=223137437&pageNum=3&classId=51876029&isdisplaytable=2&isWork=true&tempClassId=51876029&dengji=0&firstHeader=2&schoolId=-1&schoolName=&sort=-1&order=0&workSystem=0&openc=31aea7eb6e55d090fdd12012590e10d4'
url3 = 'https://mooc1-1.chaoxing.com/work/searchMarkList?sw=&workId=17997488&courseId=223137437&pageNum=4&classId=51876029&isdisplaytable=2&isWork=true&tempClassId=51876029&dengji=0&firstHeader=2&schoolId=-1&schoolName=&sort=-1&order=0&workSystem=0&openc=31aea7eb6e55d090fdd12012590e10d4'
url22 ='https://mooc1-1.chaoxing.com/work/searchMarkList?sw=&workId=18314601&courseId=223137437&pageNum=0&classId=51876029&isdisplaytable=2&isWork=true&tempClassId=51876029&dengji=0&firstHeader=2&schoolId=-1&schoolName=&sort=-1&order=0&workSystem=0&openc=31aea7eb6e55d090fdd12012590e10d4'

url4 = 'https://mooc1-1.chaoxing.com/work/getAllWork?classId=51876029&courseId=223137437&isdisplaytable=2&mooc=1&ut=t&enc=0a42d14fca324163cc1467660dd276e2&cpi=93844352&openc=31aea7eb6e55d090fdd12012590e10d4'

if __name__ == '__main__':
    # requests.DEFAULT_RETRIES = 5
    ret = requests.get(url4, headers=headers)
    ret.encoding = ret.apparent_encoding
    print(ret.text)

    # 响应写入文件
    htmlFile = open('index.html', 'w')
    htmlFile.write(ret.text)

    # 解析
    soup = BeautifulSoup(ret.text, 'html.parser')
    table = soup.find(name='table', attrs={'class': 'SJList'})
    if table is None:
        print('学生成绩表格为空')
    else:
        print(table.text)

