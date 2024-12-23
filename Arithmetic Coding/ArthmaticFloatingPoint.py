from decimal import Decimal, getcontext

getcontext().prec = 200


def get_frequency(data):
    frequency_dict = {}
    for char in data:
        frequency_dict[char] = frequency_dict.get(char, 0) + 1
    for key in frequency_dict.keys():
        frequency_dict[key] = Decimal(frequency_dict[key]) / Decimal(len(data))
    return frequency_dict


def generate_ranges(data):
    freq = get_frequency(data)
    start = Decimal(0)
    dictionary = {}
    sorted_chars = sorted(freq.keys())
    for key in sorted_chars:
        value = freq[key]
        dictionary[key] = (start, start + value)
        start += value
    return dictionary


def compress(data, file_name):
    ranges = generate_ranges(data)
    low = Decimal(0)
    high = Decimal(1)

    for char in data:
        range_width = high - low
        high = low + range_width * ranges[char][1]
        low = low + range_width * ranges[char][0]

    compressed_value = (low + high) / 2
    write_decimal_to_binary(compressed_value, file_name)
    print(f"The string is compressed in the file {file_name}")
    return ranges


def decompress(float_number, ranges, length):
    answer = ''
    cnt = length
    while cnt > 0:
        for key in ranges.keys():
            if ranges[key][0] <= float_number <= ranges[key][1]:
                answer += key
                float_number = (float_number - ranges[key][0]) / (ranges[key][1] - ranges[key][0])
                break
        cnt -= 1
    return answer


def write_decimal_to_binary(data, filename):
    with open(filename, 'wb') as file:
        encoded_data = str(data).encode('utf-8')
        file.write(encoded_data)


def read_decimal_from_binary(filename):
    with open(filename, 'rb') as file:
        encoded_data = file.read()
        return Decimal(encoded_data.decode('utf-8'))


string_to_compress = str(input("Enter the string to be compressed: "))
file_name = input("Enter the file name: ")

ranges = compress(string_to_compress, file_name)

compressed_float = read_decimal_from_binary(file_name)
print("Compressed value:", compressed_float)

decompressed_string = decompress(compressed_float, ranges, len(string_to_compress))
print("Decompressed string:", decompressed_string)
