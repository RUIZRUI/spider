# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import json
import mysql.connector
import uuid
import time
import getGameIntroduction



# 配置
# 添加防盗链
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/51.0.2704.63 Safari/537.36', 'Referer': 'https://www.3dmgame.com/'}
# 数据保存根目录
rootDir = ''
# 图像 url
imgUrl = ''
# 网页游戏主链接
onlineGameUrl = 'https://ol.3dmgame.com/'





def getPageUrl(start, end):
	"""
	功能：
		爬取[start, end) 区间内页面的链接列表

	参数：
		start 满足 start >= 1
		第一页：https://ol.3dmgame.com/ku/
		第二页：https://ol.3dmgame.com/ku_all_2/
		最后一页：https://ol.3dmgame.com/ku_all_6/

	返回：
		指定区间的页面链接组成的列表
		list
		元素形式
			第一页：ku/
			第二页：ku_all_2/
			最后一页：ku_all_6/
	"""
	pageUrlList = []
	if start >= end:
		print('Error: 获取页面链接失败，区间为空')

	for i in range(end - start):
		if start == 1 and i == 0:
			pageUrlList.append('ku/')
		else:
			pageUrlList.append('ku_all_' + str(start+i) + '/')

	return pageUrlList





def getGameUrl(pageUrl):
	"""
	功能：
		获取指定页面中游戏链接的列表

	参数：
		pageUrl 指定页面的链接

	返回：
		游戏链接列表
		list
	"""
	gameUrlList = []

	ret = requests.get(url=onlineGameUrl+pageUrl, headers=headers)
	ret.encoding = ret.apparent_encoding

	soup = BeautifulSoup(ret.text, 'html.parser')
	# gameLis = soup.find('body').find(name='div', class_='content').find(name='div', class_='listwrap').find(name='ul', class_='downllis').find_all('li')
	gameLis = soup.find('body').find(name='div', class_='content').find(name='div', class_='cent').find(name='div', class_='wy_arearlist').find('ul').find_all('li')

	for li in gameLis:
		url_a = li.find('a').get('href')
		gameUrlList.append(url_a)

	return gameUrlList





def getGameData(gameUrl):
	"""
	功能：
		根据游戏链接获取游戏信息

	参数：

		gameUrl 游戏链接

	返回:
		游戏信息字典
		dict
	"""
	gameDataDict = {}

	ret = requests.get(url=gameUrl, headers=headers)
	ret.encoding = ret.apparent_encoding

	soup = BeautifulSoup(ret.text, 'html.parser')
	gameInfoDiv = soup.find('body').find(name='div', class_='content').find(name='div', class_='item1')

	# 游戏ID
	gameDataDict['id'] = str(uuid.uuid1())
	# 游戏名
	gameDataLis = gameInfoDiv.find('ul').find_all('li')
	gameDataDict['name'] = gameDataLis[0].text
	# 游戏期待人数
	gameDataDict['hope_num'] = gameDataLis[1].find('span').text
	# 游戏类型
	gameDataDict['type'] = gameDataLis[2].find('a').text
	# 游戏画面
	gameDataDict['frame'] = gameDataLis[3].find('span').text
	# 游戏开发商
	gameDataDict['develop'] = gameDataLis[4].find('span').text
	# 游戏运营商
	gameDataDict['operator'] = gameDataLis[5].find('a').text
	# 游戏官网
	gameDataDict['website'] = gameDataLis[6].find('a').get('href')
	# 游戏状态
	gameDataDict['status'] = gameDataLis[7].find('span').text
	# 游戏标签
	labelList = []
	aList = gameDataLis[8].find_all('a')
	for a in aList:
		labelList.append(a.text)
	gameDataDict['label'] = json.dumps(labelList, ensure_ascii=False)		# 数组转为json字符串
	# 游戏评分
	scoreDiv = gameInfoDiv.find(name='div', class_='scorewrap')
	gameDataDict['score'] = scoreDiv.find(name='div', class_='processingbar').find('font').text
	# 游戏评分人数
	gameDataDict['raterNum'] = scoreDiv.find(name='div', class_='txt').find('span').text
	# 游戏图像
	gameDataDict['img'] = gameInfoDiv.find('img').get('data-original')
	# print(gameInfoDiv.find('img').get('data-original'))

	# 游戏简介
	gameIntroductionDiv = soup.find(name='div', class_='content').find(name='div', class_='item2')
	if gameIntroductionDiv == None:
		gameIntroduction = None
	else:
		gameIntroduction = gameIntroductionDiv.find('p').text
	print(gameIntroduction)
	getGameIntroduction.insertIntroduction(gameDataDict['id'], 'o_'+gameDataDict['name'], gameIntroduction)

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

	imgPath = gameImgUrl[gameImgUrl.rindex('/', 0, gameImgUrl.rindex('/')) + 1:]
	return imgUrl + imgPath




def getConn():
	"""
	功能：
		获取 mysql 的连接

	返回：
		连接
	"""
	conn = mysql.connector.connect(user='root', passwd='0508', database='game_forum')

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
		sql = 'insert into online_game (game_id, game_name, game_hope_num, game_type, game_frame, game_develop, game_operator, game_website, game_status, game_label, game_score, game_rater_num, game_img) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.executemany(sql, gameDatas)
		conn.commit()
	except mysql.connector.Error as err:
		print('失败原因：', err)

	return cursor.rowcount




def downloadImg(imgUrl):
	"""
	功能:
		根据图片链接下载图片到本地

	参数：
		imgUrl 图片链接

	"""

	# 解析imgUrl
	imgPath = imgUrl[imgUrl.rindex('/', 0, imgUrl.rindex('/')) + 1:]
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
		rootDir = properties['rootDir'] + 'onlineGame\\'
		imgUrl = properties['imgUrl'] + 'onlineGame/'




if __name__ == '__main__':
	getJson('properties.json')
	conn = getConn()
	pageUrlList = getPageUrl(1, 2)
	for pageUrl in pageUrlList:
		gameUrlList = getGameUrl(pageUrl)

		gameDatas = []
		for gameUrl in gameUrlList:
			# 获取游戏数据
			tempDict = getGameData(gameUrl)
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
	print('网页游戏爬取成功')