def compress(s):
    idx = 0
    dic = {'':0}
    arr = []
    start = 1
    st = ''
    while idx < len(s):
        st += s[idx]
        if st not in dic:
            dic[st] = start
            start += 1
            c = st[-1] if len(st)-1 < len(s) else ''
            temp = st[:len(st)-1]
            arr.append((dic[temp],c))
            st = ''
        idx += 1
    if st:
        arr.append((dic[st[:-1]], st[-1]))
    return arr

def decompression(arr):
    st = ''
    dic = {0:''}
    start = 1
    for data in arr:
        temp = dic[data[0]] + data[1]
        st += temp
        dic[start] = temp
        start += 1
    return st

io = input("Enter string u want to compress: ")

ans = compress(io)
print(ans)
dec = decompression(ans)
print(dec)
print (dec == io)