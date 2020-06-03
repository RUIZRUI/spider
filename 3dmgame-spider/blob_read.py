# -*- coding: utf-8 -*-
from mysql.connector import MySQLConnection, Error
import mysql.connector
# from python_mysql_dbconfig import read_db_config


# 数据保存根目录
# rootDir = 'D:\\spider\\3dmgame\\singleGame\\'

# conn = mysql.connector.connect(user='root', passwd='1214', database='design_pattern')
# cursor = conn.cursor()

# sql = 'select img from test where id = %s'
# val = (1,)
# cursor.execute(sql, val)

# imgData = cursor.fetchone()[0]
# with open(rootDir + 'test.jpg', 'wb') as fp:
# 	fp.write(imgData)

# print('blob数据读取成功')
# conn.close()


def read_blob(id, filename):
    # select photo column of a specific author
    query = "SELECT img FROM test WHERE id = %s"
 
    # read database configuration
    # db_config = read_db_config()
 
    try:
        # query blob data form the authors table
        # conn = MySQLConnection(**db_config)
        conn = mysql.connector.connect(user='root', passwd='1214', database='design_pattern')
        cursor = conn.cursor()
        cursor.execute(query, (id,))
        imgData = cursor.fetchone()[0]
 
        # write blob data into a file
        write_file(imgData, filename)
 
    except Error as e:
        print(e)
 
    finally:
        cursor.close()
        conn.close()



def write_file(imgData, filename):
    # with open(filename, 'wb') as f:
    #     f.write(imgData)
    print(imgData)


def main():
    read_blob(4,"D:\\spider\\3dmgame\\singleGame\\garth_stein.jpg")
 
if __name__ == '__main__':
    main()