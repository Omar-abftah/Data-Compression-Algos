import struct

def get_frequency(data):
    frequency_dict = {}
    for char in data:
        frequency_dict[char] = frequency_dict.get(char, 0) + 1
    for key in frequency_dict.keys():
        frequency_dict[key] /= len(data)
    return frequency_dict

def generate_ranges(data):
    freq = get_frequency(data)
    start = 0
    dictionary = {}
    sorted_chars = sorted(freq.keys())
    for key in sorted_chars:
        value = freq[key]
        dictionary[key] = (start, start + value)
        start += value
    return dictionary

def compress(data, file_name):
    ranges = generate_ranges(data)
    low = 0.0
    high = 1.0
    for char in data:
        range_width = high - low
        high = low + range_width * ranges[char][1]
        low = low + range_width * ranges[char][0]
    write_into_binary_file((low+high)/2, file_name)
    print(f"The string is Compressed in the Binary File {file_name}")
    return ranges

def decompress(float_number, ranges, length):
    answer = ''
    cnt = length
    while cnt > 0:
        for key in ranges.keys():
            if ranges[key][0] <= float_number <= ranges[key][1]:
                answer += key
                float_number = (float_number - ranges[key][0])/(ranges[key][1] - ranges[key][0])
                break
        cnt-=1
    return answer

def write_into_binary_file(data, filename):
    with open(filename, 'wb') as file:
        float_number = struct.pack('f', data)
        file.write(float_number)


def read_from_file(filename):
    with open(filename, 'rb') as file:
        float_number = struct.unpack('f', file.read(4))[0]
        return float_number

string_to_compress = str(input("Enter the string to be compressed: "))
file_name = input("Enter the file name: ")
ranges = compress(string_to_compress, file_name)
compressed_float = read_from_file(file_name)
print(compressed_float)
decompressed_string = decompress(compressed_float, ranges, len(string_to_compress))
print(decompressed_string)
