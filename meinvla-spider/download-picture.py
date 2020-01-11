# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import threading


# 配置
# 添加防盗链
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/51.0.2704.63 Safari/537.36'}

rootDir = '/Users/zhengxiang/spider/www.meinvla.net/data/img/'
        



# 多线程类
class downloadThread(threading.Thread):
    def __init__(self, threadID, startIndex, endIndex):
        '''这里不能使用start和end作为参数，会与线程内部的start()方法重名，引起错误
        '''
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.startIndex = startIndex
        self.endIndex = endIndex

    def run(self):
        # 获取页面列表
        pageList = getPage(self.startIndex, self.endIndex)
        for page in pageList:
            urlList = getUrl('http://www.meinvla.net' + page)
            print('\n\n')
            print('-'*100)
            print(f'{page} 页面开始下载')
            for url in urlList:
                download('/Users/zhengxiang/spider/www.meinvla.net/data/img/', 'http://www.meinvla.net' + url)




def download(filedir, url):
    ''' 根据图片url下载一套写真集
    '''
    ret = requests.get(url=url, headers=headers)
    ret.encoding = ret.apparent_encoding

    soup = BeautifulSoup(ret.text, 'html.parser')
    tu_bodyplay = soup.find(name='div', attrs={'class': 'tu_bodyplay'})


    # 判断是否由于未登录而只是下载的几张样例
    neir_denglu = tu_bodyplay.find(name='div', attrs={'class': 'neir_denglu'})
    if neir_denglu != None:
        filedir += 'unlogin/'

    
    title = soup.find(name='div', attrs={'class': 'title1'}).find(name='h1')
    filedir += title.text + '/'


    if os.path.exists(filedir) == True:
        # 判断是否重复下载，最小单位是一个写真集
        print(' '*5 + f'{filedir} 已经下载，跳过...')
        return
    else:
        os.makedirs(filedir)



    # 获取图片a元素
    pictures = tu_bodyplay.find_all(name='img')
    for picture in pictures:
        # 获取图片超链接
        href = picture.get('src')
        # 获取图片名字
        filename = href[href.rfind('/')+1:]
        down_img = requests.get(url='http:'+href, headers=headers)
        with open(filedir + filename, 'wb') as f:
            f.write(down_img.content)
        # print(' '*10 + f'{filename} 下载成功')

    print(' '*5 + f'{title.text} 下载成功')

        


def getUrl(pageUrl):
    '''在每页中解析出每套写真集
    返回结构：/play/4016511.html
    '''
    ret = requests.get(url=pageUrl, headers=headers)
    ret.encoding = ret.apparent_encoding

    soup = BeautifulSoup(ret.text, 'html.parser')
    albumList = soup.find_all(name='div', attrs={'class': 'index-body-nr-left-1-li xl6 xs4 xm4 xb3'})

    # 存放当前页面返回的url列表
    urlList = []
    for album in albumList:
        a = album.find(name='a', attrs={'class': 'effect5'})
        urlList.append(a.get('href'))
    return urlList


def getPage(start, end):
    '''下载[start, end)页面的上写真集
    start >= 1
    第一页: http://www.meinvla.net/list/3.html
    第二页: http://www.meinvla.net/list/3-2.html
        ... 以此类推
    '''
    pageList = []
    if start >= end:
        print('error, 获取页面列表失败，参数不合规范')
        return pageList
    if start == 1:
        pageList.append('/list/3.html')
    else:
        pageList.append('/list/3-' + str(start) + '.html')
    for i in range(end-start-1):
        pageList.append('/list/3-' + str(start+1+i) + '.html')
    
    return pageList
    


if __name__ == '__main__':
    # 获取页面列表
    '''pageList = getPage(1,2)
    for page in pageList:
        urlList = getUrl('http://www.meinvla.net' + page)
        print('\n\n')
        print('-'*100)
        print(f'{page} 页面开始下载')
        for url in urlList:
            download('/Users/zhengxiang/spider/www.meinvla.net/data/img/', 'http://www.meinvla.net' + url)'''
    # 创建线程
    thread1 = downloadThread(1, 1, 101)     # 1 ~ 100
    thread2 = downloadThread(2, 101, 201)   # 101 ~ 201
    thread3 = downloadThread(3, 201, 301)   # 201 ~ 301
    thread4 = downloadThread(4, 301, 401)   # 301 ~ 401
    thread5 = downloadThread(5, 401, 501)   # 401 ~ 501

    # 开启线程
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    print('下载完毕！') 









# download('/Users/zhengxiang/spider/www.meinvla.net/data/img/', 'http://www.meinvla.net/play/4016511.html')
# getUrl('http://www.meinvla.net/list/3.html')
# pageList = getPage(1,11)
# for page in pageList:
    # print(page)





        
        



