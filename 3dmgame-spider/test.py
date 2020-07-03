# -*- coding: utf-8 -*-
import time
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

print(transformDate('2020-06-22'))