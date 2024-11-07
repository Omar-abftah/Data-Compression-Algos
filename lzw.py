def LZW(str):
    iterate = 0
    compressed = []
    ascii_dict = {chr(i): i for i in range(0, 128)}
    characters = ''
    while iterate < len(str):
        if(characters + str[iterate] in ascii_dict):
            characters += str[iterate]
            iterate += 1
        else:
            ascii_dict[characters + str[iterate]] = len(ascii_dict)
            compressed.append(ascii_dict[characters])
            characters = ''

    if characters:
        compressed.append(ascii_dict[characters])
    return compressed

def LZWDecompress(arr):
    dict = {i: chr(i) for i in range(0, 128)}
    start = 128
    st = dict[arr[0]]
    decompressed = st

    for num in arr[1:]:
        if num in dict:
            temp = dict[num]
        elif num == start:
            temp = st + st[0]
        decompressed += temp
        dict[start] = st + temp[0]
        start += 1
        st = temp
    return decompressed


st = input("Enter the string u want to compress: ")
comp = LZW(st)
print(comp)

print("The decompressed string is: ", LZWDecompress(comp))


