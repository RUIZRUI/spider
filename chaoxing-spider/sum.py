import openpyxl

excelName = '2022年C++平时成绩.xlsx'
wb = openpyxl.load_workbook(excelName)
sheet = wb.worksheets[0]


## 定义变量
# 作业总分
totalScoreList1 = [100, 50, 100, 100, 100, 100, 100, 20, 60]
# 测试总分
totalScoreList2 = [100, 100, 100, 150, 60, 50]

def sumScore():
    '''
    计算作业总分和测试总分以及最终分
    '''
    # 遍历
    for row in sheet.iter_rows():
        counter = 0
        sum = 0
        sum2 = 0
        sum3 = 0
        for cell in row:
            if counter == 0 and (cell.value == None or cell.value == '学号'):
                # 无效数据，跳出循环
                # print('无效数据，跳出循环', end=' ')
                break
            # 作业总分
            if counter == 9:
                score = (float(cell.value)/totalScoreList1[counter-3])*10
                sum += score
                print(score, end=' ')
            elif counter >= 3 and counter <= 11:
                score = (float(cell.value)/totalScoreList1[counter-3])*5
                sum += score
                print(score, end=' ')
            elif counter == 12:
                cell.value = str(sum)
                print(', sum =', sum)
            # 测试总分
            elif counter >= 13 and counter <= 18:
                score = (float(cell.value)/totalScoreList2[counter-13])*5
                sum2 += score
                print(score, end=' ')
            elif counter == 19:
                cell.value = str(sum2)
                print(', sum2 =', sum2)
            # 最终分
            elif counter == 25:
                print(sum, end=' ')
                sum3 += sum
                sum3 += sum2
                print(sum2, end=' ')
                score = float(cell.value)
                print(score, end=' ')
                sum3 += score
            elif counter == 26:
                score = float(cell.value)
                print(score, end=' ')
                sum3 += score
            elif counter == 27:
                cell.value = str(sum3)
                print(', sum3 =', sum3)
            counter += 1

    # 保存
    wb.save(excelName)



if __name__ == '__main__':
    sumScore()


