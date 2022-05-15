def swap2():
    a = [1, 2]
    b = [3, 4]
    print('a=', a, ', b=', b)
    swap(a, b)
    print('a=', a, ', b=', b)

def swap(a, b):
    temp = a[0]
    a[0] = a[1]
    a[1] = temp
    temp = b[0]
    b[0] = b[1]
    b[1] = temp

swap2()