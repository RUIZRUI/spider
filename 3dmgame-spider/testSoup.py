from bs4 import BeautifulSoup

soup = BeautifulSoup('<div>荒野大嫖客2<span>（Red Dead: RedemptionⅡ）</span></div>', 'html.parser')
soupDiv = soup.find('div')
print(soup.text)
print(soup.contents)
print(soupDiv.text)
print(soupDiv.contents)
print(soupDiv.contents[0])
print(type(soupDiv.contents[0]))
print(soupDiv.contents[0].text)
print(type(soupDiv.contents[0].text))