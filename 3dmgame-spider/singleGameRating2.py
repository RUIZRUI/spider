# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import json
import time
import mysql.connector
import getGameIntroduction



"""
1. 每页前两个没获取数据
2. 当前用户评分还需要获取吗？
3. 下载图片时，还需要指定 ret.encoding 吗？
4. 多条插入由于重复失败时，应该进一步细化，单挑插入
5. gameInfoDiv.find(name='div', class_='score-box clear') 空
   gameInfoDiv.find(name='div', class_='score-box ') 空 
   gameInfoDiv.find(name='div', class_='score-box') 正确，不为空
"""


# 配置
# 添加防盗链
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/51.0.2704.63 Safari/537.36', 'Referer': 'https://www.3dmgame.com/'}
# 数据保存根目录
rootDir = ''
# 图像 url
imgUrl = ''
# 单机游戏主链接
singleGameUrl = 'https://www.3dmgame.com/phb.html'




def getPageUrl():
	"""
	功能：
		爬取[start, end) 区间内页面的链接列表

	参数：
		start 满足 start >= 1
		第一页：https://dl.3dmgame.com/all_all_1_hot/
		第二页：https://dl.3dmgame.com/all_all_2_hot/
		最后一页：https://dl.3dmgame.com/all_all_2009_hot/

	返回：
		指定区间的页面链接组成的列表
		list
		元素形式
			第一页：all_all_1_hot/
			第二页：all_all_2_hot/
			最后一页：all_all_2009_hot/
	"""
	pageUrlList = []
	pageUrlList.append('https://www.3dmgame.com/phb.html')

	return pageUrlList




def getGameItem(pageUrl):
	"""
	功能：
		获取指定页面中游戏链接的列表

	参数：
		pageUrl 指定页面的链接

	返回：
		游戏链接列表
		list
	"""
	gameItemList = []

	ret = requests.get(url=pageUrl, headers=headers)
	ret.encoding = ret.apparent_encoding

	soup = BeautifulSoup(ret.text, 'html.parser')
	gameDivs = soup.find('body').find(name='div', class_='content').find(name='div', class_='Phbright').find_all(name='div', class_='phlist')

	for div in gameDivs:
		itemList = []

		# 添加 gameUrl
		url_a = div.find('a').get('href')
		itemList.append(url_a)

		# 添加 gameLabel
		labelList = []
		labelAs = div.find(name='ul', class_='infolis').find_all('li')[-1].find_all('a')
		for a in labelAs:
			labelList.append(a.text)
		itemList.append(labelList)

		gameItemList.append(itemList)

	return gameItemList





def getGameData(rating, gameItem):
	"""
	功能：
		根据游戏链接获取游戏信息

	参数：
		rating 游戏排名
		gameItem 游戏条目

	返回:
		游戏信息字典
		dict
	"""
	gameDataDict = {}

	# 解析游戏条目
	gameUrl = gameItem[0]
	labelList = gameItem[1]

	ret = requests.get(url=gameUrl, headers=headers)
	ret.encoding = ret.apparent_encoding

	soup = BeautifulSoup(ret.text, 'html.parser')

	try:
		gameInfoDiv = soup.find('body').find(name='div', class_='content zqwrap').find(name='div', class_='ZQ_Left')
		print('此条目支持爬取')
		return None
	except:
		print('此条目不支持爬取')
		gameInfoDiv = soup.find('body').find(name='div', class_='content zqcomment2').find(name='div', class_='inforbox')
		# 游戏ID
		gameDataDict['id'] = rating
		# 游戏名
		gameInfo = gameInfoDiv.find(name='div', class_='left_')
		gameDataDict['name'] = gameInfo.find(name='div', class_='h3').contents[0].text
		# 游戏英文名
		gameDataDict['EnglishName'] = gameInfo.find(name='div', class_='h3').find('span').text
		# 游戏类型
		gameDataLis = gameInfoDiv.find('ul', class_='lis').find_all('li')
		gameDataDict['type'] = gameDataLis[0].text
		# 游戏开发制作
		gameDataDict['develop'] = gameDataLis[1].text
		# 游戏平台
		platformList = []
		aList = gameDataLis[3].find_all('a')
		for a in aList:
			platformList.append(a.text)
		gameDataDict['platform'] = json.dumps(platformList, ensure_ascii=False)
		# 游戏发行
		gameDataDict['release'] = gameDataLis[2].text
		# 发售日期
		gameDataDict['releaseDate'] = transformDate(gameDataLis[4].find('a').text)
		# 游戏语言
		gameDataDict['language'] = '语言：简中 | 繁中 | 英文 | 多国'
		# 官方网站
		gameDataDict['website'] = '暂无' if gameDataLis[5].find('a') is None else gameDataLis[5].find('a').get('href')
		# 标签
		gameDataDict['label'] = json.dumps(labelList, ensure_ascii=False)  # 数组转为json字符串
		# 游戏评分
		scoreDiv = gameInfoDiv.find(name='div', class_='rit_').find(name='div', class_='pcli pcli2')
		gameDataDict['score'] = scoreDiv.find(name='div', class_='circle-wrapper').find(name='span', class_='percent number2').text
		# 游戏评分人数
		gameDataDict['raterNum'] = scoreDiv.find(name='div', class_='text_ text_p').find('i').text
		# 游戏图像
		gameDataDict['img'] = gameInfoDiv.find(name='div', class_='img').find('img').get('data-original')
		# 游戏简介
		gameIntroductionDiv = gameInfoDiv.find(name='div', class_='rit_').find(name='div', class_='ptext')
		gameIntroduction = gameIntroductionDiv.find('p').text
		print(gameIntroduction)
		getGameIntroduction.insertIntroduction('s' + str(gameDataDict['id']), 'sr_' + gameDataDict['name'], gameIntroduction)

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
		sql = 'insert into single_game_rating (game_id, game_name, game_english_name, game_type, game_develop, game_platform, game_release, game_release_date, game_language, game_website, game_label, game_score, game_rater_num, game_img) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
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
	dateStr = dateStr.strip()[0:10]
	try:
		dateStr = dateStr[0:10]
		time.strptime(dateStr, '%Y-%m-%d')
		return dateStr
	except:
		if dateStr == '':
			return None
		elif dateStr.strip() == '未知':
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
		rootDir = properties['rootDir'] + 'singleGameRating\\'
		imgUrl = properties['imgUrl'] + 'singleGameRating/'







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
			if tempDict is None:
				continue
			# 根据真实图像链接，下载图像
			downloadImg(tempDict['img'])
			# 修改图像链接，为本网站地址
			tempDict['img'] = decodeImgUrl(tempDict['img'])
			# 字典转为元组，方便插入数据
			tempTuple = tuple(tempDict.values())
			gameDatas.append(tempTuple)
			print(tempTuple)
			# break
		
		rowcount = innsertData(conn=conn, gameDatas=gameDatas)
		print(str(rowcount) + '条记录插入成功' if rowcount != -1 else '插入失败')

	conn.close()
	print('单机游戏爬取完成')