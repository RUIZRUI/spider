import mysql.connector
import requests
import json

# 配置
# 添加防盗链
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/51.0.2704.63 Safari/537.36', 'Referer': 'http://dh.520.fi'}
apiUrl = 'http://api.520.fi/acgurl.php?return=json'


def conn():
    conn = mysql.connector.connect(host='localhost', user='root', password='1214', database='spider')
    return conn

def close(conn):
    conn.close()


def getAcgUrl():
    ret = requests.get(url=apiUrl, headers=headers, cookies=None, timeout=10)
    ret.encoding = ret.apparent_encoding
    response = json.loads(ret.text)
    print(response['acgurl'])
    return response['acgurl']

def insertData(conn):
    try:
        cursor = conn.cursor()
        sql = 'insert into 520_fi_acg (acg_url) values (%s)'
        cursor.execute(sql, (getAcgUrl(),))
        conn.commit()
    except mysql.connector.Error as err:
        print('失败原因：', err)



if __name__ == '__main__':
    conn = conn()
    insertData(conn)
    close(conn)