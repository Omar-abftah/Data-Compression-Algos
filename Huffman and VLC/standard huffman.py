
import heapq
from collections import Counter

class Node :
    def __init__(self, value, freq):
        self.value = value
        self.freq = freq
        self.left = None
        self.right = None
    def __lt__(self, other):
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
    return ''.join(codes[char] for char in data)

data = str(input("Enter the data you want to compress: "))

print(compress(data))