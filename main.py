import os
import time

from lzw import lzw_compress, lzw_decompress
from huffman import build_frequency_table, build_huffman_tree, generate_huffman_codes, huffman_encode

def compress_with_huffman(input_text):
    # Step 1: LZW Compression
    lzw_compressed = lzw_compress(input_text)
    
    # Step 2: Build frequency table from LZW output
    frequency_table = build_frequency_table(lzw_compressed)
    
    # Step 3: Build Huffman Tree and generate codes
    huffman_tree = build_huffman_tree(frequency_table)
    huffman_codes = generate_huffman_codes(huffman_tree)
    
    # Step 4: Huffman encoding of LZW compressed data
    huffman_encoded_data = huffman_encode(lzw_compressed, huffman_codes)
    
    return huffman_encoded_data

def write_lzw_compressed_file(file_name, compressed_data):
    """Writes the LZW compressed data to a binary file."""
    with open(file_name, "wb") as file:
        # Write the LZW compressed data as binary integers (using 2 bytes per integer)
        for data in compressed_data:
            file.write(data.to_bytes(2, byteorder='big'))
            

def write_binary_file(file_name, binary_data):
    """Writes the binary data to a file."""
    with open(file_name, "wb") as file:
        file.write(binary_data)


def calculate_compression_rate(original_file, compressed_file):
    original_size = os.path.getsize(original_file)
    compressed_size = os.path.getsize(compressed_file)
    return compressed_size / original_size

def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def print_nice_output(lzw_compression_rate, huffman_compression_rate, compression_ratio, compression_time, decompression_time):
    print("\n" + "=" * 40)
    print("      Compression Results Summary")
    print("=" * 40)
    
    print(f"LZW Compression Rate:         {lzw_compression_rate:.4f}")
    print(f"LZW + Huffman Compression:    {huffman_compression_rate:.4f}")
    print(f"Compression Ratio:            {compression_ratio:.2f}:1")
    print(f"Compression Time:             {compression_time:.4f} seconds")
    print(f"Decompression Time:           {decompression_time:.4f} seconds")

    print("=" * 40 + "\n")


# Use this function after calculating all metrics:
if __name__ == "__main__":
    original_file = "folktale.txt"
    output_directory = "compressed_files"
    
    # Ensure the directory exists
    ensure_directory(output_directory)

    # Read the folktale text
    with open(original_file, "r", encoding="utf-8") as file:
        input_text = file.read()

    # Measure Compression Time
    start_time = time.time()
    lzw_compressed = lzw_compress(input_text)
    compression_time = time.time() - start_time

    # Write LZW compressed data
    lzw_compressed_file = os.path.join(output_directory, "lzw_compressed.bin")
    write_lzw_compressed_file(lzw_compressed_file, lzw_compressed)

    # Measure Decompression Time
    start_time = time.time()
    decompressed_text = lzw_decompress(lzw_compressed)
    decompression_time = time.time() - start_time

    # LZW + Huffman Compression
    huffman_compressed = compress_with_huffman(input_text)
    huffman_compressed_file = os.path.join(output_directory, "huffman_compressed.bin")
    write_binary_file(huffman_compressed_file, huffman_compressed)

    # Calculate compression metrics
    lzw_compression_rate = calculate_compression_rate(original_file, lzw_compressed_file)
    huffman_compression_rate = calculate_compression_rate(original_file, huffman_compressed_file)
    compression_ratio = 1 / lzw_compression_rate

    # Print a nice output summary
    print_nice_output(lzw_compression_rate, huffman_compression_rate, compression_ratio, compression_time, decompression_time)
