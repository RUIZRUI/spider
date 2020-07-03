## 爬取 3DMGAME
*爬取 3DMGAME 中的游戏数据*
*[3DMGAME](https://www.3dmgame.com/)*

1. [单机游戏](https://dl.3dmgame.com/all_all_1_hot/)：singleGameSpider
2. [安卓游戏](https://shouyou.3dmgame.com/android/1_1_1/)：androidGameSpider
3. [苹果游戏](https://shouyou.3dmgame.com/ios/1_1_1/)：iosGameSpider
4. [网页游戏](https://ol.3dmgame.com/ku/)：onlineGameSpider

5. init.py 初始化数据库与文件系统






## Problem
1. 爬取游戏简介时，遇到重大错误，使用BeautifulSoup解析时，部分网页如'https://dl.3dmgame.com/pc/127151.html', 出现</body></html>提前，使得游戏简介div不在<body></body>之间，造成爬取简介失败
	* 目前解决方案：利用游戏简介div的class属性的唯一性，绕开<body></body>，直接由soup定位到游戏简介div
	```python
	import requests
	from bs4 import BeautifulSoup
	
	# 添加防盗链
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/51.0.2704.63 Safari/537.36', 'Referer': 'https://www.3dmgame.com/'}


	url = 'https://dl.3dmgame.com/pc/127151.html'
	ret = requests.get(url=url, headers=headers)
	ret.encoding = ret.apparent_encoding

	soup = BeautifulSoup(ret.text, 'html.parser')
	gameIntroduction = soup.find(name='div', class_='GmL_1')

	print(gameIntroduction.find('p').text)
	```

