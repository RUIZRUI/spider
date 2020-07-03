# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import json
import time
import mysql.connector
import getGameIntroduction



# 配置
# 添加防盗链
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/51.0.2704.63 Safari/537.36', 'Referer': 'https://www.3dmgame.com/'}
# 数据保存根目录
# 数据保存根目录
rootDir = ''
# 图像 url
imgUrl = ''
# 安卓游戏主链接
androidGameUrl = 'https://shouyou.3dmgame.com/phb/'



def getPageUrl():
	"""
	功能：
		爬取[start, end) 区间内页面的链接列表

	参数：
		start 满足 start >= 1
		第一页：https://shouyou.3dmgame.com/android/1_1_1_hot/
		第二页：https://shouyou.3dmgame.com/android/1_1_2_hot/
		最后一页：https://shouyou.3dmgame.com/android/1_1_2009_hot/

	返回：
		指定区间的页面链接组成的列表
		list
		元素形式
			第一页：1_1_1/
			第二页：1_1_2/
			最后一页：1_1_2009/
	"""
	pageUrlList = []
	pageUrlList.append('https://shouyou.3dmgame.com/phb/')

	return pageUrlList 




def getGameItem(pageUrl):
	"""
	功能：
		获取指定页面中游戏链接的列表

	参数：
		pageUrl 指定页面的链接

	返回：
		游戏条目列表
		list
	"""
	gameItemList = []

	ret = requests.get(url=pageUrl, headers=headers)
	ret.encoding = ret.apparent_encoding

	soup = BeautifulSoup(ret.text, 'html.parser')
	gameDivs = soup.find('body').find(name='div', class_='content').find(name='div', class_='Ranking').find(name='div', class_='warp').find_all(name='div', class_='item')

	for div in gameDivs:
		tempList = []

		# 添加游戏链接
		url_a = div.find(name='div', class_='bt').find('a').get('href')
		tempList.append(url_a)

		# 添加游戏大小
		gameSize = div.find(name='div', class_='p').find('span').text
		tempList.append(gameSize[3:])

		gameItemList.append(tempList)

	return gameItemList







def getGameData(rating, gameItem):
	"""
	功能：
		根据游戏链接获取游戏信息

	参数：
		rating   游戏排名
		gameItem 游戏条目

	返回:
		游戏信息字典
		dict
	"""
	gameDataDict = {}

	# 解析游戏条目
	gameUrl = gameItem[0]
	gameSize = gameItem[1]

	ret = requests.get(url=gameUrl, headers=headers)
	ret.encoding = ret.apparent_encoding

	soup = BeautifulSoup(ret.text, 'html.parser')
	gameInfoDiv = soup.find('body').find(name='div', class_='content').find(name='div', class_='detail-top')

	# 游戏ID
	gameDataDict['id'] = rating
	# 游戏名
	gameDataDict['name'] = gameInfoDiv.find('h1').text
	# 游戏口号
	gameDataDict['slogan'] = gameInfoDiv.find(name='div', class_='bt').find('span').text
	# 游戏大小
	gameDataDict['size'] = gameSize
	# 游戏版本
	gameDataLis = gameInfoDiv.find(name='ul', class_='lis').find_all('li')
	gameDataDict['version'] = gameDataLis[0].text[3:]
	# 游戏平台
	gameDataDict['platform'] = gameDataLis[1].find('a').text
	# 游戏类型
	gameDataDict['type'] = gameDataLis[2].text[3:]
	# 游戏发售日期
	gameDataDict['releaseDate'] = transformDate(gameDataLis[3].text[3:])
	# 游戏发行
	gameDataDict['release'] = gameDataLis[4].text[3:]
	# 游戏语言
	gameDataDict['language'] = gameDataLis[5].text[3:]
	# 游戏评分
	scoreDiv = gameInfoDiv.find(name='div', class_='scorewrap score_c')
	gameDataDict['score'] = scoreDiv.find(name='div', class_='processingbar').find('font').text
	# 游戏评分人数
	gameDataDict['raterNum'] = scoreDiv.find(name='div', class_='txt').find('span').text
	# 游戏图像
	gameDataDict['img'] = gameInfoDiv.find(name='div', class_='img').find('img').get('src')

	# 游戏简介
	gameIntroductionDiv = soup.find('body').find(name='div', class_='content').find(name='div', class_='detail_cont').find(name='div', class_='cont_L').find(name='div', class_='detail-txt')
	gameIntroduction = gameIntroductionDiv.find('p').text

	print(gameIntroduction)
	
	getGameIntroduction.insertIntroduction('a'+str(gameDataDict['id']), 'ar_'+gameDataDict['name'], gameIntroduction)

	return gameDataDict


def decodeImgUrl(gameImgUrl):
	"""
	功能：
		解析游戏图像链接

	参数：
		游戏图像链接

	返回：
		解析后的图像链接
	"""
	global imgUrl

	imgPath = gameImgUrl[gameImgUrl.rindex('/', 0, gameImgUrl.rindex('/', 0, gameImgUrl.rindex('/'))) + 1:]
	return imgUrl + imgPath


def getConn():
	"""
	功能：
		获取 mysql 的连接

	返回：
		连接
	"""
	conn = mysql.connector.connect(user='root', passwd='1214', database='design_pattern')

	return conn



def innsertData(conn, gameDatas):
	"""
	功能:
		将数据插入到数据库表

	参数：
		conn 数据库连接
		gameDatas 多条记录组成的列表

	返回：
		插入的记录数
	"""
	try: 
		cursor = conn.cursor()
		sql = 'insert into android_game_rating (game_id, game_name, game_slogan, game_size, game_version, game_platform, game_type, game_release_date, game_release, game_language, game_score, game_rater_num, game_img) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.executemany(sql, gameDatas)
		conn.commit()
	except mysql.connector.Error as err:
		print('失败原因：', err)

	return cursor.rowcount





def transformDate(dateStr):
	"""
	功能：
		判断字符串是日期格式，并且返回正确格式

	参数：
		dateStr 爬取的日期字符串

	返回：
		正确日期格式的字符串
	"""
	try:
		time.strptime(dateStr, '%Y-%m-%d')
		return dateStr
	except:
		if dateStr == '':
			return None
		else:
			return dateStr[0:4] + '-01-01'		# 测试





def downloadImg(imgUrl):
	"""
	功能:
		根据图片链接下载图片到本地

	参数：
		imgUrl 图片链接

	"""

	# 解析imgUrl
	imgPath = imgUrl[imgUrl.rindex('/', 0, imgUrl.rindex('/', 0, imgUrl.rindex('/'))) + 1:]
	imgPath = rootDir + imgPath.replace('/', '\\')

	# 分离目录与文件名
	folderPath = os.path.split(imgPath)[0]
	filePath = os.path.split(imgPath)[1]

	# 检测文件目录是否存在
	if not os.path.exists(folderPath):
		os.makedirs(folderPath)

	# 检测文件是否存在
	if os.path.exists(folderPath + filePath):
		return

	ret = requests.get(url=imgUrl, headers=headers)
	ret.encoding = ret.apparent_encoding

	# 下载图片
	with open(imgPath, 'wb') as fp:
		fp.write(ret.content)




def getJson(filePath):
	"""
	功能：
		读取json配置文件

	参数: 
		filePath  配置文件地址

	"""
	global rootDir
	global imgUrl

	with open(filePath, 'r') as fp:
		# 异步读取
		properties = json.load(fp)
		rootDir = properties['rootDir'] + 'androidGameRating\\'
		imgUrl = properties['imgUrl'] + 'androidGameRating/'




if __name__ == '__main__':
	getJson('properties.json')
	conn = getConn()
	pageUrlList = getPageUrl()
	for pageUrl in pageUrlList:
		gameItemList = getGameItem(pageUrl)
		
		gameDatas = []
		rating = 0
		for gameItem in gameItemList:
			rating += 1
			# 获取游戏数据
			tempDict = getGameData(rating, gameItem)
			# 根据真实图像链接，下载图像
			downloadImg(tempDict['img'])
			# 修改图像链接，为本网站地址
			tempDict['img'] = decodeImgUrl(tempDict['img'])
			# 字典转为元组，方便插入数据
			tempTuple = tuple(tempDict.values())
			gameDatas.append(tempTuple)
			print(tempTuple)

		rowcount = innsertData(conn=conn, gameDatas=gameDatas)
		print(str(rowcount) + '条记录插入成功' if rowcount != -1 else '插入失败')

	conn.close()
	print('安卓游戏爬取完成')