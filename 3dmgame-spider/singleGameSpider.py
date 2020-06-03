# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import json
import mysql.connector
import uuid



"""
1. 每页前两个没获取数据
2. 当前用户评分还需要获取吗？
3. 下载图片时，还需要指定 ret.encoding 吗？
4. 多条插入由于重复失败时，应该进一步细化，单挑插入
"""


# 配置
# 添加防盗链
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/51.0.2704.63 Safari/537.36', 'Referer': 'https://www.3dmgame.com/'}
# 数据保存根目录
rootDir = 'D:\\spider\\3dmgame\\singleGame\\'
# 单机游戏主链接
singleGameUrl = 'https://dl.3dmgame.com/'




def getPageUrl(start, end):
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
	if start >= end:
		print('Error: 获取页面链接失败，区间为空')

	for i in range(end - start):
		pageUrlList.append('all_all_' + str(start+i) + '_hot/')

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

	ret = requests.get(url=singleGameUrl+pageUrl, headers=headers)
	ret.encoding = ret.apparent_encoding

	soup = BeautifulSoup(ret.text, 'html.parser')
	# gameLis = soup.find('body').find(name='div', class_='content').find(name='div', class_='listwrap').find(name='ul', class_='downllis').find_all('li')
	gameImgs = soup.find('body').find(name='div', class_='content').find(name='div', class_='listwrap').find(name='ul', class_='downllis').find_all(name='div', class_='img')

	count = 0
	for img in gameImgs:
		count += 1
		if count == 1 or count == 2:
			continue
		url_a = img.find('a').get('href')
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
	gameInfoDiv = soup.find('body').find(name='div', class_='content clear game').find(name='div', class_='gameinfo')

	# 游戏ID
	gameDataDict['id'] = str(uuid.uuid1())
	# 游戏名
	gameDataDict['name'] = gameInfoDiv.find('h1').text
	# 游戏类型
	gameDataLis = gameInfoDiv.find('ul').find_all('li')
	gameDataDict['type'] = gameDataLis[0].find('span').text
	# 开发发行
	gameDataDict['release'] = gameDataLis[1].find('span').text
	# 发售日期
	gameDataDict['releaseDate'] = transformDate(gameDataLis[2].find('span').text)
	# 整理时间
	gameDataDict['arrangeDate'] = transformDate(gameDataLis[3].find('span').text)
	# 游戏平台
	gameDataDict['platform'] = gameDataLis[4].find('span').text
	# 官方网站
	gameDataDict['website'] = '暂无' if gameDataLis[5].find('a') is None else gameDataLis[5].find('a').get('href')
	# 标签
	labelList = []
	iList = gameDataLis[6].find_all('i')
	for i in iList:
		labelList.append(i.find('a').text)
	gameDataDict['label'] = json.dumps(labelList)		# 数组转为json字符串
	# 游戏语言
	gameDataDict['language'] = gameDataLis[7].find('span').text
	# 游戏评分
	scoreDiv = gameInfoDiv.find(name='div', class_='scorewrap')
	gameDataDict['score'] = scoreDiv.find(name='div', class_='processingbar').find('font').text
	# 游戏评分人数
	gameDataDict['raterNum'] = scoreDiv.find(name='div', class_='txt').find('span').text
	# 游戏图像
	gameDataDict['img'] = gameInfoDiv.find(name='div', class_='img').find('img').get('src')

	return gameDataDict


	

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
		sql = 'insert into single_game (game_id, game_name, game_type, game_release, game_release_date, game_arrange_date, game_platform, game_website, game_label, game_language, game_score, game_rater_num, game_img) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
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












if __name__ == '__main__':
	conn = getConn()
	pageUrlList = getPageUrl(1, 3)
	for pageUrl in pageUrlList:
		gameUrlList = getGameUrl(pageUrl)
		
		gameDatas = []
		for gameUrl in gameUrlList:
			tempDict = getGameData(gameUrl)
			tempTuple = tuple(tempDict.values())
			gameDatas.append(tempTuple)
			print(tempTuple)
			downloadImg(tempTuple[-1])
			# break
		
		rowcount = innsertData(conn=conn, gameDatas=gameDatas)
		print(str(rowcount) + '条记录插入成功' if rowcount != -1 else '插入失败')

	conn.close()
	print('单机游戏爬取完成')