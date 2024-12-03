
import heapq
from collections import Counter
from bitarray import bitarray

class Node :
    def __init__(self, value, freq):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None
    def __lt__(self, other):
        if self.freq == other.freq:
            return (self.value or '') < (other.value or '')
        return self.freq < other.freq

def build_frequency(data):
   return Counter(data)

def build_huffman_tree(freq_table):
    priority_queue = [Node(char, freq) for char, freq in freq_table.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)

        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)
    heapq.heapify(priority_queue)
    return priority_queue[0]

def generate_huffman_code(root):
    codes = {}
    def traverse(node, current_code):
        if node is not None:
            if node.value is not None:
                codes[node.value] = current_code
            traverse(node.left, current_code +'0')
            traverse(node.right, current_code +'1')
    traverse(root,'')

    return codes

def compress(data):
    freq_table = build_frequency(data)
    tree = build_huffman_tree(freq_table)
    codes = generate_huffman_code(tree)
    return ''.join(codes[char] for char in data), freq_table;

def decompress(compressed_data, freq_table):
    tree = build_huffman_tree(freq_table)
    node = tree
    ans = ''
    for bit in compressed_data:
        if bit == '0':
            node = node.left
        else:
            node = node.right
        if node.left is None and node.right is None:
            ans += node.value
            node = tree
    return ans



def saveOutputInFile(compressed_string,file_name):
    dataInBits = bitarray(compressed_string)
    with open(file_name, "wb") as binary_file:
        binary_file.write(len(compressed_string).to_bytes(4, byteorder='big'))
        dataInBits.tofile(binary_file)

def readOutputFromFile(file_name):
    with open(file_name, "rb") as binary_file:
        bit_length = int.from_bytes(binary_file.read(4), byteorder='big')
        bit_data = bitarray()
        bit_data.fromfile(binary_file)
        # Truncate the bitarray to the actual length
        return bit_data[:bit_length]

data = str(input("Enter the data you want to compress: "))
compressedString, freq_tree = compress(data)

file_name = str(input("Enter the name of the output file: "))
saveOutputInFile(compressedString,file_name)
print(f"Output is saved in {file_name} File ")
compressedDataFromFile = str(readOutputFromFile(file_name).to01())

print(f"The Compressed String is: {compressedDataFromFile}")
decompressedData = decompress(compressedDataFromFile, freq_tree)
print(f"Decompressed String is: {decompressedData}")