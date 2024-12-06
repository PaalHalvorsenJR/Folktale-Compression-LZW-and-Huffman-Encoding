import heapq
from collections import defaultdict

class Node:
    """A node class for Huffman Tree."""
    def __init__(self, symbol, frequency):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency
    
def build_frequency_table(data):
    """Builds frequency table from data."""
    frequency = defaultdict(int)
    for symbol in data:
        frequency[symbol] += 1
    return frequency

def build_huffman_tree(frequency_table):
    """Builds Huffman Tree from the frequency table."""
    priority_queue = [Node(symbol, freq) for symbol, freq in frequency_table.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = Node(None, left.frequency + right.frequency)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)
    
    return heapq.heappop(priority_queue)

def generate_huffman_codes(node, current_code="", code_map={}):
    """Generates Huffman codes from the Huffman tree."""
    if node is None:
        return
    
    if node.symbol is not None:
        code_map[node.symbol] = current_code
    
    generate_huffman_codes(node.left, current_code + "0", code_map)
    generate_huffman_codes(node.right, current_code + "1", code_map)
    
    return code_map

def huffman_encode(data, huffman_codes):
    """Encodes data using the Huffman codes and stores it as binary."""
    encoded_data = ''.join(huffman_codes[symbol] for symbol in data)
    
    # Convert the binary string to a byte array
    byte_array = bytearray()
    for i in range(0, len(encoded_data), 8):
        byte = encoded_data[i:i+8]  # Get 8 bits at a time
        byte_array.append(int(byte, 2))  # Convert binary string to integer
    print(byte_array)

    return byte_array
    

def huffman_decode(encoded_data, huffman_tree):
    """Decodes Huffman encoded data using the Huffman tree."""
    current_node = huffman_tree
    decoded_data = ""

    for bit in encoded_data:
        current_node = current_node.left if bit == '0' else current_node.right
        if current_node.symbol is not None:
            decoded_data += current_node.symbol
            current_node = huffman_tree
    return decoded_data
