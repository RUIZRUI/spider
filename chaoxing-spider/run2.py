# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import openpyxl

# 配置
# 添加防盗链
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    'Cookie': 'k8s=0baa706986b839aba84715acec2e0a4645e084f8; jrose=3CEE2D36C5CA465D8F808546FCC84F32.mooc-1523198214-zz7qv; route=440ceb57420433374ff0504da9778fc7; lv=1; fid=67889; _uid=69768608; uf=fbe48ba271b0dbbdb5427138866c41c2891819d1110d1b2aef06b79cb59fb462852dbd3f4b696450e768b4aebacb023e913b662843f1f4ad6d92e371d7fdf6441f4d46e6e633da49efcee624f188c883c992d031135b2ab786e12ac4b4c2400bee1ac9eb75c67126aa2ebad65cd196bb; _d=1652527990855; UID=69768608; vc=BD3B5D85E3F1CC14E3EB14AAD86C4029; vc2=E27FBEE05EC864744AD2E352B7A688A6; vc3=EXVAKMjVUwPV%2FrNMBsD6lBJpV1wPUSbJV36jH1r81%2FN%2Fh60yMZ53Sm3%2FoonKLXgwwaEjQhzVKMacO9Hq5%2BDi4vhZWZsk3ZN2ZKYAolRGTf%2BS0uNDZHWiBJzR53KMjqQlr46i3bOJ7dFRpurQdbZjhKB94P%2BgThKq8BAZFhuTWLE%3Df5c96c9432fae0adc0ab5f2002e3d5ad; xxtenc=d504f7001b98cd9c1466feb27f4a8871; DSSTASH_LOG=C_38-UN_62371-US_69768608-T_1652527990857; thirdRegist=0',
    'Referer': 'https://mooc1-1.chaoxing.com/',
    'Connection': 'keep-alive'
}


# 目标 url
url = 'https://mooc1-1.chaoxing.com/exam/test?classId=51876029&courseId=223137437&ut=t&enc=0a42d14fca324163cc1467660dd276e2&cpi=93844352&openc=31aea7eb6e55d090fdd12012590e10d4'
tableUrlPre = 'https://mooc1-1.chaoxing.com/exam/test/searchMarkList?sw=&courseId=223137437&size=&classId=51876029&tempClassId=51876029&schoolId=-1&schoolName=&sort=&sortType=&examsystem=0&openc=31aea7eb6e55d090fdd12012590e10d4&qbanksystem=0&qbankbackurl='
pageNumPre = 'start='
scoreList = []

# Excel文件
excelName = '2022年C++平时成绩.xlsx'


def getScore(workId):
    '''
    获取一次作业的分数
    '''
    tableUrl = tableUrlPre + '&' + workId
    for pageNum in range(4):
        getScoreByPage(tableUrl, pageNum)


def getScoreByPage(tableUrl, pageNum):
    '''
    获取一次作业其中一页的分数
    '''
    tableUrl = tableUrl + '&' + pageNumPre + str(pageNum*15)
    print('tableUrl=' + tableUrl)

    ret = requests.get(tableUrl, headers=headers)
    ret.encoding = ret.apparent_encoding
    # print(ret.text)

    # 解析
    soup = BeautifulSoup(ret.text, 'html.parser')
    table = soup.find(name='tbody', attrs={'id': 'tableId'})
    # print(table.text)
    tr_list = table.findAll(name='tr')
    print(len(tr_list))
    for tr in tr_list:
        td_list = tr.findAll(name='td')
        score = {}
        # 学号
        # print(td_list[1].text.strip(), end=' ')
        score['sid'] = td_list[1].text.strip()
        # 分数
        # print(td_list[8].text.strip())
        score['score'] = td_list[8].text.strip()
        print(score)
        scoreList.append(score)
        # for td in td_list:
        #     print(td.text.strip(), end=' ')
        # print()
    # print(scoreList)
    print(len(scoreList))


def writeExcel(columnIndex):
    '''
    将学生的分数写入 Excel
    columnIndex: 分数要插入的列
    '''
    wb = openpyxl.load_workbook(excelName)
    sheet1 = wb.worksheets[0]


    # 遍历
    for row in sheet1.iter_rows():
        counter = 0
        sid = None
        for cell in row:
            if counter == 0 and (cell.value == None or cell.value == '学号'):
                # 无效数据，跳出循环
                break
            if counter == 0:
                sid = str(cell.value)
            elif counter == columnIndex:
                score = getScoreBySid(sid)
                cell.value = score
                print('sid=', sid, ', score=', score)
            counter += 1

    # 保存
    wb.save(excelName)

def getScoreBySid(sid):
    '''
    根据学号（sid）查找分数
    '''
    for score in scoreList:
        if sid == score['sid']:
            return score['score']
    return '0'









if __name__ == '__main__':
    ret = requests.get(url, headers=headers)
    ret.encoding = ret.apparent_encoding
    # print(ret.text)

    # 解析
    soup = BeautifulSoup(ret.text, 'html.parser')
    div = soup.find(name='div', attrs={'class': 'ulDiv'})
    a_workId = div.findAll(name='a', attrs={'class': 'Btn_blue_1'})
    print(len(a_workId))
    workIdList = []
    for a in a_workId:
        # print(a.get('onclick'))
        a_href = a.get('onclick')
        # print(a_href.split('&'))
        workId = a_href.split('&')[2]
        # print(workId)
        workIdList.append(workId)
    print(workIdList)
    workLen = len(workIdList)
    workId = workIdList[workLen-1]
    print(workId)
    getScore(workId)

    print('-------------------------', end='')
    print(len(scoreList), end='')
    print('-------------------------')
    # 将学生的分数写入 Excel
    writeExcel(18)



