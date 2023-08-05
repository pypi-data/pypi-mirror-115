def mxmul(mx1,mx2,row1,col1,col2):
    rst = [[0 for y in range(col2)] for x in range(row1)]
    for i in range(row1):
        for j in range(col2):
            for k in range(col1):
                rst[i][j] += mx1[i][k] * mx2[k][j]
    return rst

def mxsum(mx,row,col):
    s = 0
    for i in range(row):
        for j in range(col):
            s += j
    return s

if __name__ == "__main__":
    import time
    row1,col1,col2 = 3, 4, 3
    mx1 = [[x for x in range(col1)] for y in range(row1)]
    mx2 = [[x for x in range(col2)] for y in range(col1)]
    start = time.perf_counter()
    rst = mxmul(mx1,mx2,row1,col1,col2)
    end = time.perf_counter()
    print(rst)
    print("运算时间为{:.4f}s".format(end-start))
    print(mxsum(mx1,3,4))