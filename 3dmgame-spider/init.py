# -*- coding: utf-8 -*-
import mysql.connector
import os

"""
1. 执行 conn.reconnect() 后，是否应该重新获取游标
"""


def databaseInit():
	"""
	功能：
		初始化数据库
		创建数据库 design_pattern
		创建表 single_game
		创建表 android_game
		创建表 ios_game
		创建表 online_game
	"""
	# 连接数据库
	conn = mysql.connector.connect(user='root', passwd='1214')

	# 获取操作游标
	cursor = conn.cursor()

	# 创建数据库 design_pattern
	sql = 'create database if not exists design_pattern'
	cursor.execute(sql)

	# 连接到数据库 design_pattern
	conn.config(database='design_pattern')
	conn.reconnect()

	# 创建表 single_game
	sql = '''
	create table if not exists single_game(
		`game_id` varchar(255) primary key,
		`game_name` varchar(255) not null unique,
		`game_type` varchar(255),
		`game_release` varchar(255),
		`game_release_date` date,
		`game_arrange_date` date,
		`game_platform` varchar(255),
		`game_website` varchar(255),
		`game_label` varchar(255),
		`game_language` varchar(255),
		`game_score` double(2, 1),			-- 精度，评分10可以吗？
		`game_rater_num` int(11),
		`game_img` varchar(255)
	)
	'''
	# cursor = conn.cursor()		
	cursor.execute(sql)


	# 创建表 android_game
	sql = '''
	create table if not exists android_game(
		`game_id` varchar(255) primary key,
		`game_name` varchar(255) not null unique,
		`game_slogan` varchar(255),
		`game_version` varchar(255),
		`game_platform` varchar(255),
		`game_type` varchar(255),
		`game_release_date` date,
		`game_release` varchar(255),
		`game_language` varchar(255),
		`game_score` double(2, 1),
		`game_rater_num` int(11),
		`game_img` varchar(255)
	)
	'''
	cursor.execute(sql)


	# 创建表 ios_game
	sql = '''
	create table if not exists ios_game(
		`game_id` varchar(255) primary key,
		`game_name` varchar(255) not null unique,
		`game_slogan` varchar(255),
		`game_version` varchar(255),
		`game_platform` varchar(255),
		`game_type` varchar(255),
		`game_release_date` date,
		`game_release` varchar(255),
		`game_language` varchar(255),
		`game_score` double(2, 1),
		`game_rater_num` int(11),
		`game_img` varchar(255)
	)
	'''
	cursor.execute(sql)


	# 创建表 online_game
	sql = '''
	create table if not exists online_game(
		`game_id` varchar(255) primary key,
		`game_name` varchar(255) not null unique,
		`game_hope_num` int(11),
		`game_type` varchar(255),
		`game_frame` varchar(255),
		`game_develop` varchar(255),
		`game_operator` varchar(255),
		`game_website` varchar(255),
		`game_status` varchar(255),
		`game_label` varchar(255),
		`game_score` double(2, 1),
		`game_rater_num` int(11),
		`game_img` varchar(255)
	)
	'''
	cursor.execute(sql)




	# 关闭连接
	conn.close()

	print('数据库初始化成功')





def dictInit():
	"""
	功能：
		初始化文件系统

	"""
	# 创建单机游戏根文件夹 singleGame
	singleGameDict = 'D:\\spider\\3dmgame\\singleGame\\'
	if not os.path.exists(singleGameDict):
		os.makedirs(singleGameDict)

	# 创建安卓游戏根文件夹 androidGame
	androidGameDict = 'D:\\spider\\3dmgame\\androidGame\\'
	if not os.path.exists(androidGameDict):
		os.makedirs(androidGameDict)

	# 创建苹果游戏根文件夹 iosGame
	iosGameDict = 'D:\\spider\\3dmgame\\iosGame\\'
	if not os.path.exists(iosGameDict):
		os.makedirs(iosGameDict)


	# 创建网页游戏根文件夹 onlineGame
	onlineGameDict = 'D:\\spider\\3dmgame\\onlineGame\\'
	if not os.path.exists(onlineGameDict):
		os.makedirs(onlineGameDict)

	print('文件系统初始化成功')







if __name__ == '__main__':
	# 初始化数据库
	databaseInit()
	# 初始化文件系统
	dictInit()