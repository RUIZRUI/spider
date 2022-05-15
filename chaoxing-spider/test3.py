originalList = [10, 6, 8, 18, 5, 8, 8, 18, 2]
sList = [4.0, 2.4, 3.2, 3.6, 4.0, 3.2, 3.2, 3.6, 4.0]

def quickSort(originalList, sList, left, right):
    '''
    快排
    '''
    if left < right:
        position = partition(originalList, sList, left, right)
        quickSort(originalList, sList, left, position - 1)
        quickSort(originalList, sList, position + 1, right)


def partition(originalList, sList, left, right):
    '''
    快排 partition
    '''
    i = left
    j = left
    while j <= right:
        if sList[j] >= sList[left]:
            print(1, ', j=', sList[j], ', left=', sList[left])
            j += 1
        else:
            print(2)
            i += 1
            temp = sList[i]
            sList[i] = sList[j]
            sList[j] = temp
            temp = originalList[i]
            originalList[i] = originalList[j]
            originalList[j] = temp
            j += 1
    temp = sList[left]
    sList[left] = sList[i]
    sList[i] = temp
    temp = originalList[left]
    originalList[left] = originalList[i]
    originalList[i] = temp
    return i

print(originalList)
print(sList)
quickSort(originalList, sList, 0, len(sList)-1)
print(originalList)
print(sList)