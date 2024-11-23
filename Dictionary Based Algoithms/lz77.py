def lz77_compress(data, window_size):
    idx = 0
    compressed_data = []
    while idx < len(data):
        p = 0
        l = 0
        starting_idx = max(0, idx - window_size)
        window = data[starting_idx:idx]
        for j in range(len(window),starting_idx-1,-1):
            length = 0
            while idx + length < len(data) and length < len(window) - j and window[j + length] == data[idx + length]:
                length += 1

            if length > l:
                l = length
                p = len(window) - j

        if l > 0:
            c = data[idx+l] if idx + l < len(data) else ''
            compressed_data.append((p,l,c))
            idx += l + 1
        else:
            compressed_data.append((0,0,data[idx]))
            idx+=1
    return compressed_data

def lz77_decompress(v):
    sol = ""
    for item in v:
        idx = len(sol) - item[0]
        sol += sol[idx:idx+item[1]] + item[2]
    return sol


data = input("Enter the data to be compressed: ")
windowSize = int(input("Enter the window size: "))

arr = lz77_compress(data,windowSize)

print("Compression tuples: ")
for i in arr:
    print(i)

ans = lz77_decompress(arr)

print("Decompressed text: "+ans)
