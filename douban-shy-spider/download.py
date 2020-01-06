# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os


## 配置
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/51.0.2704.63 Safari/537.36'}
choice = 33
url = ''
pageNum = 0
dirType = ''

if choice == 1:    # 身材辑
    url = 'https://www.douban.com/photos/album/127493069/'
    pageNum = 21
    dirType = './data/img/害羞组/身材辑/'
elif choice == 2:   # 女组员
    url = 'https://www.douban.com/photos/album/105084617/'
    pageNum = 60
    dirType = './data/img/害羞组/女组员/'
elif choice == 3:   # 侧脸
    url = 'https://www.douban.com/photos/album/132192881/'
    pageNum = 4
    dirType = './data/img/害羞组/侧脸/'
elif choice == 4:   # 足
    url = 'https://www.douban.com/photos/album/135128380/'
    pageNum = 1
    dirType = './data/img/害羞组/足/'
elif choice == 5:   # 嘴唇
    url = 'https://www.douban.com/photos/album/116433338/'
    pageNum = 11
    dirType = './data/img/害羞组/嘴唇/'
elif choice == 6:   # 锁骨
    url = 'https://www.douban.com/photos/album/118327139/'
    pageNum = 3
    dirType = './data/img/害羞组/锁骨/'
elif choice == 7:   # 直男
    url = 'https://www.douban.com/photos/album/139203394/'
    pageNum = 25
    dirType = './data/img/MachineGUN/直男/'
elif choice == 8:   # ForLove
    url = 'https://www.douban.com/photos/album/37756733/'
    pageNum = 3
    dirType = './data/img/MachineGUN/ForLove/'
elif choice == 9:   # 给小姐姐拍私房
    url = 'https://www.douban.com/photos/album/1691810236/'
    pageNum = 1
    dirType = './data/img/莫非/给小姐姐拍私房/'
elif choice == 10:
    url = 'https://www.douban.com/photos/album/1661865449/'
    pageNum = 1
    dirType = './data/img/空空如也/青春肉体/'
elif choice == 11:
    url = 'https://www.douban.com/photos/album/1655370576/'
    pageNum = 1
    dirType = './data/img/空空如也/私房2/'
elif choice == 12:
    url = 'https://www.douban.com/photos/album/1654575997/'
    pageNum = 1
    dirType = './data/img/空空如也/私房/'
elif choice == 13:
    url = 'https://www.douban.com/photos/album/1657913869/'
    pageNum = 1
    dirType = './data/img/空空如也/黑白/'
elif choice == 14:
    url = 'https://www.douban.com/photos/album/1662756161/'
    pageNum = 2
    dirType = './data/img/陳叁肾/私房/'
elif choice == 15:
    url = 'https://www.douban.com/photos/album/1650731698/'
    pageNum = 1
    dirType = './data/img/楚九/私房收藏唯美/'
elif choice == 16:
    url = 'https://www.douban.com/photos/album/1653435569/'
    pageNum = 3
    dirType = './data/img/楚九/人像/'
elif choice == 17:
    url = 'https://www.douban.com/photos/album/1658634382/'
    pageNum = 1
    dirType = './data/img/楚九/欧美风/'
elif choice == 18:
    url = 'https://www.douban.com/photos/album/1649191728/'
    pageNum = 1
    dirType = './data/img/楚九/s房/'
elif choice == 19:
    url = 'https://www.douban.com/photos/album/1650176569/'
    pageNum = 3
    dirType = './data/img/楚九/可爱/'
elif choice == 20:
    url = 'https://www.douban.com/photos/album/1650175736/'
    pageNum = 2
    dirType = './data/img/楚九/日系私服/'
elif choice == 21:
    url = 'https://www.douban.com/photos/album/1650175356/'
    pageNum = 1
    dirType = './data/img/楚九/光影/'
elif choice == 22:
    url = 'https://www.douban.com/photos/album/1650175247/'
    pageNum = 2
    dirType = './data/img/楚九/唯美风/'
elif choice == 23:
    url = 'https://www.douban.com/photos/album/1692319895/'
    pageNum = 8
    dirType = './data/img/一个无情的杀手/Girls/'
elif choice == 24:
    url = 'https://www.douban.com/photos/album/1869132775/'
    pageNum = 1
    dirType = './data/img/一个无情的杀手/私房1/'
elif choice == 25:
    url = 'https://www.douban.com/photos/album/1867615634/'
    pageNum = 1
    dirType = './data/img/一个无情的杀手/胶卷写真wing/'
elif choice == 26:
    url = 'https://www.douban.com/photos/album/1651227287/'
    pageNum = 2
    dirType = './data/img/拽玛蒂尼/未命名/'
elif choice == 27:
    url = 'https://www.douban.com/photos/album/1630624769/'
    pageNum = 9
    dirType = './data/img/未羊NAUIL/局部美/'
elif choice == 28:
    url = 'https://www.douban.com/photos/album/155804428/'
    pageNum = 5
    dirType = './data/img/未羊NAUIL/筱山纪信-少女馆/'
elif choice == 29:
    url = 'https://www.douban.com/photos/album/138196870/'
    pageNum = 5
    dirType = './data/img/未羊NAUIL/青山裕企-思春期/'
elif choice == 30:
    url = 'https://www.douban.com/photos/album/138194636/'
    pageNum = 3
    dirType = './data/img/未羊NAUIL/天使心&维纳斯女神/'
elif choice == 31:
    url = 'https://www.douban.com/photos/album/1642818701/'
    pageNum = 2
    dirType = './data/img/luckytoto/牛奶草莓/'
elif choice == 32:
    url = 'https://www.douban.com/photos/album/125558698/'
    pageNum = 1
    dirType = './data/img/一支花洒/私房/'
elif choice == 33:
    url = 'https://www.douban.com/photos/album/122623211/'
    pageNum = 1
    dirType = './data/img/艾门/私房/'

## 下载页面
# ret = requests.get(url='https://www.douban.com/photos/album/127493069/')


# 创建目录
if os.path.exists(dirType) == False:
    os.makedirs(dirType)

# 分页下载
page = 0        # 0 ~ 20，每页18张图片
counter = 0     # 下载总数
for i in range(pageNum):
    print('\n'*2)
    print('-'*100)
    print(f'第{i+1}页开始下载...')
    param = '?m_start=' + str(i*18)
    ret = requests.get(url=url+param, headers=headers)
    # print(ret)
    # 指定编码等于原始页面编码
    ret.encoding = ret.apparent_encoding
    # print(ret.text)



    ## 解析
    soup = BeautifulSoup(ret.text, 'html.parser')       # lxml更快
    div = soup.find(name='div', attrs={'class': 'photolst'})

    img_list = div.find_all(name='img')
    filedir = dirType
    for img in img_list:
        # print(counter + ':  ' + img.get('href'))
        src = img.get('src')
        filename = src.split('/')[-1]
        down_img = requests.get(url=src, headers=headers)               # 这里添加headers，可以使图片可以下载成功
        with open(filedir + str(i+1) + '-' + filename, 'wb') as f:
            f.write(down_img.content)
        counter += 1
        print(f"{counter}:  {filename} 下载成功")


