# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import unquote
import time
from contextlib import closing
from progressBar import ProgressBar


# 防盗链
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/51.0.2704.63 Safari/537.36', 'Referer': 'https://pan.uvooc.com/'}
# 文件保存目录
rootDir = '' 
# 根地址
domain = r'https://pan.uvooc.com'
rootUrl4 = r'/Learn/CET/CET4/'
rootUrl6 = r'/Learn/CET/CET6/'



def getFolderUrl(dict, url):
	''' 
		找到页面文件夹链接
		dict: 上级文件夹路径
	''' 
	# 创建目录
	folderName = getFileName(dict, url)
	if not os.path.exists(folderName):
		os.makedirs(folderName)
	print('---文件夹' + folderName + '开始下载')
	
	# 爬取网页
	try: 
		ret = requests.get(url=domain + url, headers=headers, timeout=30)		# 加上timeout 30秒，不然出现“远程主机强迫关闭异常”
		ret.encoding = ret.apparent_encoding
		soup = BeautifulSoup(ret.text, 'html.parser')
	
	
		folders = soup.find_all(name='li', class_='mdui-list-item mdui-ripple')
		files = soup.find_all(name='li', class_='mdui-list-item file mdui-ripple')
		
		# 递归下载子文件夹
		flag = False
		for folder in folders: 
			if not flag:
				# 列表第一个是父文件夹，跳过
				flag = True
				continue
			childFolder = folder.find('a').get('href')
			childFolder = unquote(childFolder, 'utf-8')
			
			getFolderUrl(folderName, childFolder)
		
		
		# 下载文件
		for file in files:
			fileUrl = file.find('a').get('href')
			fileUrl = unquote(fileUrl, 'utf-8')
			downloadFile(folderName, fileUrl)
			
		
	
	except requests.exceptions.ConnectionError:
		print('*********************文件夹' + folderName + '下载失败，正在重新请求**********************')
		time.sleep(5)
		getFolderUrl(dict, url)
	
		# 暂停1秒，不然远程主机强制关闭连接
		# time.sleep(1)


def downloadFile(folderName, fileUrl):
	''' 
		下载文件
	''' 
	fileName = getFileName(folderName, fileUrl)
	if os.path.exists(fileName):
		print('######文件' + fileName + '已下载##############')
		return
	
	# 下载文件
	try:
		# ret = requests.get(url=domain + fileUrl, headers=headers, timeout=30)
		# ret.encoding = ret.apparent_encoding
		
		# # 保存到磁盘
		# with open(fileName, 'wb') as fp:
		# 	fp.write(ret.content)
		# 	print('------文件' + fileName + '下载完成')
		
		# 下载文件并显示进度条
		with closing(requests.get(url=domain + fileUrl, headers=headers, timeout=30, stream=True)) as response:
			# 单次请求最大值
			chunk_size = 1024
			# 内容体总大小
			content_size = int(response.headers['content-length'])
			progress = ProgressBar(fileName, total=content_size, unit='KB', chunk_size=chunk_size, run_status='正在下载', fin_status='下载完成')
			
			# 保存到磁盘
			with open(fileName, 'wb') as fp:
				for data in response.iter_content(chunk_size=chunk_size):
					fp.write(data)
					progress.refresh(count = len(data))
				print('------文件' + fileName + '下载完成')
			
		
	except requests.exceptions.ConnectionError:
		print('*********************文件' + fileName + '下载失败，正在重新请求**********************')
		time.sleep(5)
		downloadFile(folderName, fileUrl)
	
	
	
	
	
	


def getFileName(dict, url):
	''' 
		根据链接，解析文件名或文件夹名
	''' 
	if url.split('/')[-1] != '':
		fileName = url.split('/')[-1]
	else:
		fileName = url.split('/')[-2]
	
	# 连接上层文件夹路径
	if dict != '':
		fileName = dict + os.sep + fileName
	return fileName



if __name__ == '__main__':
	print('下载四级请输入 4')
	print('下载六级请输入 6')
	choice = input('请输入：').strip()
	
	# requests 配置
	requests.adapters.DEFAULT_RETRIES = 15	# 重连次数
	# 连接活跃状态为 False
	s = requests.session()
	s.keep_alive = False
	
	if choice == '4':
		print('四级文件夹即将开始下载 ...')
		getFolderUrl('', rootUrl4)
	elif choice == '6':
		print('六级文件夹即将开始下载 ...')
		getFolderUrl('', rootUrl6)
	else:
		print('输入有误')