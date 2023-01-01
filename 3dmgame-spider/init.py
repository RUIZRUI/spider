# -*- coding: utf-8 -*-
import mysql.connector
import os
import json

"""
1. 执行 conn.reconnect() 后，是否应该重新获取游标
"""

# mysql 连接信息
mysqlInfo = {}
# 数据保存根目录
rootDir = ''



def getJson(filePath):
	"""
	功能：
		读取json配置文件

	参数: 
		filePath  配置文件地址

	"""
	global rootDir
	global mysqlInfo

	with open(filePath, 'r') as fp:
		properties = json.load(fp)
		rootDir = properties['rootDir']
		mysqlInfo = properties['mysqlInfo']



def databaseInit():
	"""
	功能：
		初始化数据库
		创建数据库 game_forum
		创建表 single_game
		创建表 android_game
		创建表 ios_game
		创建表 online_game
	"""
	# 连接数据库
	conn = mysql.connector.connect(user=mysqlInfo['user'], passwd=mysqlInfo['passwd'])

	# 获取操作游标
	cursor = conn.cursor()

	# 创建数据库 game_forum
	sql = 'create database if not exists ' + mysqlInfo['database']
	cursor.execute(sql)

	# 连接到数据库 design_pattern
	conn.config(database=mysqlInfo['database'])
	conn.reconnect()

	# 创建表 base_game
	sql = '''
	create table if not exists base_game(
		`game_id` varchar(255) primary key,
		`game_name` varchar(255) not null,		-- 不设为 unqiue
		`game_belong` varchar(255) not null 	-- 单机游戏 | 安卓游戏 | 苹果游戏 | 网页游戏
	)
	'''
	cursor.execute(sql)

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


	# 创建 single_game_rating
	sql = '''
	create table if not exists single_game_rating(
		`game_id` int(11) primary key,
		`game_name` varchar(255) not null unique,
		`game_english_name` varchar(255) not null unique,
		`game_type` varchar(255),
		`game_develop` varchar(255),
		`game_platform` varchar(255),
		`game_release` varchar(255),
		`game_release_date` date,
		`game_language` varchar(255),
		`game_website` varchar(255),
		`game_label` varchar(255),
		`game_score` double(2, 1),
		`game_rater_num` int(11),
		`game_img` varchar(255) 
	)
	'''
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


	# 创建表 android_game_rating
	sql = '''
	create table if not exists android_game_rating(
		`game_id` int(11) primary key,
		`game_name` varchar(255) not null unique,
		`game_slogan` varchar(255),
		`game_size` varchar(255),
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


	# 创建表 ios_game_rating
	sql = '''
	create table if not exists ios_game_rating(
		`game_id` int(11) primary key,
		`game_name` varchar(255) not null unique,
		`game_slogan` varchar(255),
		`game_size` varchar(255),
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


	# 创建表 online_game_rating
	sql = '''
		create table if not exists online_game_rating(
		`game_id` int(11) primary key,
		`game_name` varchar(255) not null unique,
		`game_hope_num` int(11),
		`game_type` varchar(255),
		`game_frame` varchar(255),
		`game_test_date` date,
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


	# 创建表 user
	sql = '''
		create table if not exists user(
			user_id int(11) auto_increment primary key,
			password varchar(18) not null,
			priority varchar(10) not null,
			fans_number int(11) default 0,
			logintime timestamp default current_timestamp(),
			user_name varchar(255) unique not null,
			phone varchar(11) unique,
			mail varchar(255) unique,
			status boolean not null,
			img varchar(255) default "http://localhost:8080/forum/images/avatar/default.jpg",
			follow_number int(11) default 0,
			sex varchar(20) default "未设置",
			birthdate date default '1970-01-01',		-- 1970-01-01 08:00:00
			index index_id(user_id)
		)engine=InnoDB;
	'''
	cursor.execute(sql)


	# 创建表 comments
	sql = '''
		create table if not exists comments(
			comment_id int(11) auto_increment,
			user_id_from int(11) not null,		-- 发送评论的用户
			user_id_to int(11),					-- 接收评论的用户，如果是游戏，则为null
			game_id varchar(255) not null,
			parent_id int(11),
			content text not null,
			comment_time timestamp default current_timestamp(),
			likes int(11) default 0,
			dislike int(11) default 0,
			primary key(comment_id),
			foreign key(user_id_from) references user(user_id)
			ON DELETE CASCADE ON UPDATE CASCADE,		-- 外键约束
			foreign key(parent_id) references comments(comment_id)
			ON DELETE CASCADE ON UPDATE CASCADE,		-- 外键约束
			foreign key(user_id_to) references user(user_id)
			ON DELETE CASCADE ON UPDATE CASCADE,		-- 外键约束
			index index_id(comment_id)
		)engine=InnoDB;
	'''
	cursor.execute(sql)


	# 创建表 user_relationship
	sql = '''
		create table if not exists user_relationship(
			main_userid int(11) not null,			-- 爱豆的 user_id
			fans_userid int(11) not null,			-- 粉丝的 user_id
			primary key(main_userid, fans_userid),
			foreign key(main_userid) references user(user_id)
			ON DELETE CASCADE ON UPDATE CASCADE,
			foreign key(fans_userid) references user(user_id)
			ON DELETE CASCADE ON UPDATE CASCADE
		)
	'''
	cursor.execute(sql)


	# 创建表 collection
	sql = '''
		create table if not exists collection(
			user_id int(11) not null,
			game_id varchar(255) not null,
			game_name varchar(255) not null,
			game_type varchar(255) not null,
			game_platform varchar(255) not null,
			game_belong varchar(255) not null,
			game_img varchar(255) not null,
			primary key(user_id,game_id),
			foreign key(user_id) references user(user_id)
			ON DELETE CASCADE ON UPDATE CASCADE,
			index index_id(user_id)
		)engine=InnoDB;
	''' 
	cursor.execute(sql)


	# 创建表 login_log
	sql = '''
		create table if not exists login_log(
			user_id int(11) primary key,
			login_time date not null,
			foreign key(user_id) references user(user_id)
			ON DELETE CASCADE ON UPDATE CASCADE,
			index index_id(user_id)
		)engine=InnoDB;
	''' 
	cursor.execute(sql)


	# 创建表 game_introduction
	sql = '''
	create table if not exists game_introduction(
		`game_id` varchar(255) primary key,
		`game_name` varchar(255) not null unique,
		`content` Text,
		index index_id(`game_id`)		-- 建立索引，优化
	) engine=InnoDB;
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
	singleGameDict = rootDir + 'singleGame\\'
	if not os.path.exists(singleGameDict):
		os.makedirs(singleGameDict)

	# 创建单机游戏排行榜根文件夹 singleGameRating
	singleGameRatingDict = rootDir + 'singleGameRating\\'
	if not os.path.exists(singleGameRatingDict):
		os.makedirs(singleGameRatingDict)

	# 创建安卓游戏根文件夹 androidGame
	androidGameDict = rootDir + 'androidGame\\'
	if not os.path.exists(androidGameDict):
		os.makedirs(androidGameDict)

	# 创建安卓游戏排行榜根文件夹 androidGameRating
	androidGameRatingDict = rootDir + 'androidGameRating\\'
	if not os.path.exists(androidGameRatingDict):
		os.makedirs(androidGameRatingDict)

	# 创建苹果游戏根文件夹 iosGame
	iosGameDict = rootDir + 'iosGame\\'
	if not os.path.exists(iosGameDict):
		os.makedirs(iosGameDict)


	# 创建苹果游戏排行榜根文件夹 iosGameRating
	iosGameRatingDict = rootDir + 'iosGameRating\\'
	if not os.path.exists(iosGameRatingDict):
		os.makedirs(iosGameRatingDict)


	# 创建网页游戏根文件夹 onlineGame
	onlineGameDict = rootDir + 'onlineGame\\'
	if not os.path.exists(onlineGameDict):
		os.makedirs(onlineGameDict)


	# 创建网页游戏排行榜根文件夹 onlineGameRating
	onlineGameRatingDict = rootDir + 'onlineGameRating\\'
	if not os.path.exists(onlineGameRatingDict):
		os.makedirs(onlineGameRatingDict)

	print('文件系统初始化成功')







if __name__ == '__main__':
	# 读取配置文件
	getJson('properties.json')
	# 初始化数据库
	databaseInit()
	# 初始化文件系统
	dictInit()