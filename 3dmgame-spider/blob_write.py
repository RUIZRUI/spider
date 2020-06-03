# -*- coding: utf-8 -*-
import mysql.connector

conn = mysql.connector.connect(user='root', passwd='1214', database='design_pattern')
cursor = conn.cursor()


with open('D:\\spider\\3dmgame\\singleGame\\1589509586_590108.jpg', 'rb') as fp:
	imgData = fp.read()



sql = 'insert into test (id, img) values (%s, %s)'
val = (4, imgData)
cursor.execute(sql, val)
conn.commit()

# mediumblob




conn.close()