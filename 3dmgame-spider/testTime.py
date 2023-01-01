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
	dateStr = dateStr.strip()[0:10]
	try:
		time.strptime(dateStr, '%Y-%m-%d')
		return dateStr
	except:
		if dateStr == '':
			return None
		elif dateStr.strip() == '未知':
			return None
		else:
			return dateStr[0:4] + '-01-01'		# 测试

if __name__ == '__main__':
	timeStr = '未知'
	print(transformDate(timeStr))