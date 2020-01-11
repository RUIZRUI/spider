# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import threading
import json
import time


'''todo
1. 将视频集中的图片完成下载
2. 多线程下载视频的时候如何end = filesize -1 会出现异常吗
'''

# 配置
# 添加防盗链
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/51.0.2704.63 Safari/537.36'}

rootDir = '/Users/zhengxiang/spider/www.meinvla.net/data/video/'
threadNum = 8   # 允许线程个数



# 多线程合并下载
class DownloadThread(threading.Thread):
    def __init__(self, url, startpos, endpos, fd):
        super(DownloadThread, self).__init__()
        self.url = url
        self.startpos = startpos
        self.endpos = endpos
        self.fd = fd

    def download(self):
        # print(' '*10 + f'start {self.getName()}, ' + time.strftime('%H:%M:%S'))
        headers = {'Range': 'bytes=%d-%d' % (self.startpos, self.endpos)}
        res = requests.get(url=self.url, headers=headers)
        self.fd.seek(self.startpos)
        self.fd.write(res.content)
        print(' '*10 + f'stop {self.getName()}, ' + time.strftime('%H:%M:%S'))
        self.fd.close()

    def run(self):
        self.download()



def isUrl(url):
    '''判断url是否是一个合法的url
    '''
    if(url[:5] == 'http:' or url[:6] == 'https:'):          # 前五位是http:，或者前六位https:
        return True
    else:
        return False


def download(filedir, url):
    '''根据url下载一部视频
    '''
    ret = requests.get(url=url, headers=headers)
    ret.encoding = ret.apparent_encoding

    soup = BeautifulSoup(ret.text, 'html.parser')
    tu_body = soup.find(name='div', attrs={'class': 'tu_body'})

    # 获取标题
    title = tu_body.find(name='h1')
    # print(title.text)
    
    # 获取视频链接
    # iframe = tu_body.find(name='iframe', attrs={'class': 'embed-responsive-item'})
    # iframe框架抓去不到
    # src = iframe.get('src')
    # videoLink = src[src.rfind('?')+4:]      # 切除 ?id=
    # print(videoLink)

    # 获取视频链接
    scriptBody = tu_body.find(name='script')       
    cms_player = json.loads(scriptBody.text[17:-1])             # 切除 'var cms_player = ' 和 ';'
    videoLink = cms_player.get('url')

    # 检测videoLink是否是合法的链接
    if isUrl(videoLink) == False:
        print(f'error, 视频链接{videoLink}无效，可能是图片')
        return

    filename = videoLink[videoLink.rfind('/')+1:]
    filename = title.text + '__' + filename

    if os.path.exists(filedir) == False:
        # 创建文件夹
        os.makedirs(filedir)

    if os.path.exists(filedir + filename) == True:
        # 判断该视频是否已经下载
        print(' ' * 5 + f'{filename} 已经下载，跳过...')
        return
    


    # down_video = requests.get(url=videoLink, headers=headers)
    # with open(filedir + filename, 'wb') as f:
        # f.write(down_video.content)
    
    # 多线程合并下载
    print(' '*5 + f'{filename} 开始下载')
    filesize = int(requests.head(videoLink).headers['Content-Length'])
    threading.BoundedSemaphore(threadNum)   # 允许线程个数
    step = filesize // threadNum    # 整除
    threadList = []     # 线程列表
    start = 0
    end = -1

    tempf = open(filedir + filename, 'w')
    tempf.close()

    with open(filedir + filename, 'rb+') as f:
        # 获取文件句柄
        fileno = f.fileno()     # 返回一个整型的文件描述符，可用于底层操作系统 I/O操作
        while end < filesize - 1:
            start = end + 1
            end = start + step - 1
            if end > filesize:
                end = filesize
            # print(' '*10 + f'start: {start}, end: {end}')
            dup = os.dup(fileno)    # 复制文件句柄
            fd = os.fdopen(dup, 'rb+', -1)
            thread = DownloadThread(videoLink, start, end, fd)
            thread.start()
            threadList.append(thread)
        for thread in threadList:
            thread.join()
    f.close()

    print(' ' *5 + f'{filename} 下载成功')



def getUrl(pageUrl):
    '''在每页解析出每个视频播放页面的链接
       返回结构：/play/466811.html
    '''
    ret = requests.get(url=pageUrl, headers=headers)
    ret.encoding = ret.apparent_encoding

    soup = BeautifulSoup(ret.text, 'html.parser')
    index_body = soup.find(name='div', attrs={'class': 'index-body'})
    # index-body 第一个div即为video_body
    video_body = index_body.find(name='div')
    videoList = video_body.find_all(name='div', attrs={'class': 'index-body-nr-left-1-li xl6 xs4 xm4 xb2'})
    # print(len(videoList))

    # 存放当前页面中返回的url列表
    urlList = []
    for video in videoList:
        a = video.find('a', attrs={'class': 'effect5'})
        urlList.append(a.get('href'))
    return urlList




def getPage(start, end):
    '''下载[start, end)页面上的视频
        start >= 1
        第一页：http://www.meinvla.net/list/1.html
        第二页：http://www.meinvla.net/list/1-2.html
        ...以此类推
    '''
    pageList = []
    if start >= end:
        print('error, 获取页面列表失败，参数不合规范')
        return pageList
    if start == 1:
        pageList.append('/list/1.html')
    else:
        pageList.append('/list/1-' + str(start) + '.html')
    for i in range(end-start-1):
        pageList.append('/list/1-' + str(start+1+i) + '.html')
    
    return pageList



if __name__ == '__main__':
    # 获取页面列表
    pageList = getPage(8,9)
    for page in pageList:
        urlList = getUrl('http://www.meinvla.net' + page)
        print('\n\n')
        print('-'*100)
        print(f'{page} 页面开始下载')
        for url in urlList:
            download('/Users/zhengxiang/spider/www.meinvla.net/data/video/', 'http://www.meinvla.net' + url)






# 测试
# download('/Users/zhengxiang/spider/www.meinvla.net/data/video/', 'http://www.meinvla.net/play/467711.html')
# getUrl('http://www.meinvla.net/list/1-2.html')


