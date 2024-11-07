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

ans = compress("ABAABABAAABA")
print(ans)