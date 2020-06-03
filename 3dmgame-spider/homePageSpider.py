# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


# 配置
# 添加防盗链
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/51.0.2704.63 Safari/537.36', 'Referer': 'https://www.3dmgame.com/'}
# 数据保存根目录
rootDir = 'D:\\spider\\3dmgame\\'
# 根url
rootUrl = 'https://www.3dmgame.com/'









def getGategories():
	"""
	功能：
		获取集合：比如单机、手游、网游、自运营

	返回：
		集合列表

	"""
	gategoryList = []

	ret = requests.get(url=rootUrl, headers=headers)
	ret.encoding = ret.apparent_encoding

	soup = BeautifulSoup(ret.text, 'html.parser')
	# 获取<li>列表
	gategoryLis = soup.find('body').find(name='div', attrs={'class': 'nav'}).find('ol').find_all('li')
	
	# 解析 gategoryLis
	for gategory in gategoryLis:
		temp = {}
		temp_a = gategory.find('a')
		temp['name'] = temp_a.text
		temp['url'] = temp_a.get('href')
		gategoryList.append(temp)

	return gategoryList



def getSingleGameItems(gategoryUrl):
	"""
	功能：获取一个单机游戏集合中的游戏条目

	参数：单机游戏集合的链接

	返回：单机游戏条目的链接列表
	"""
	itemList = []




















# 主函数
if __name__ == '__main__':
	"""
	功能：
		该文件获取3dmgame主页的热门游戏、近期新作、即将上市等
	"""

	# gategoryList = getGategories()
	
	itemList = getSingleGameItems(gategoryUrl = 'https://www.3dmgame.com/games/')
	print(itemList)

	print('程序运行结束...')