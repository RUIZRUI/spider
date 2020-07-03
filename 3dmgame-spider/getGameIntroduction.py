# -*- coding: utf-8 -*-
import mysql.connector
import json


# 数据库配置信息
user = ''
passwd = ''
database = ''



def getJson():
	"""
	功能：
		获取数据库连接配置
	"""
	global user 
	global passwd
	global database

	with open('properties.json', 'r') as fp:
		properties = json.load(fp)
		user = properties['mysqlInfo']['user']
		passwd = properties['mysqlInfo']['passwd']
		database = properties['mysqlInfo']['database']




def getConn():
	"""
	功能：
		获取 mysql 的连接

	返回：
		连接
	"""
	getJson()

	conn = mysql.connector.connect(user=user, passwd=passwd, database=database)

	return conn




def insertIntroduction(gameId, gameName, gameIntroduction):
	"""
	功能：
		将游戏简介插入数据库

	参数:
		conn: 数据库连接
		gameId: 游戏id
		gameName: 游戏名
		gameIntroduction: 游戏简介<string>
	"""
	try:
		conn = getConn()
		cursor = conn.cursor()
		sql = 'insert into game_introduction (game_id, game_name, content) values (%s, %s, %s)'
		cursor.execute(sql, (gameId, gameName, gameIntroduction))
		conn.commit()
		conn.close()
	except mysql.connector.Error as err:
		print('插入简介出错： ', err)



if __name__ == '__main__':
	pass



