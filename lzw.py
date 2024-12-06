# lzw.py
def lzw_compress(input_text):
    """LZW compression algorithm."""
    dictionary = {chr(i): i for i in range(256)}
    current_string = ""
    compressed_data = []
    next_code = 256
    
    for symbol in input_text:
        current_string_plus_symbol = current_string + symbol
        if current_string_plus_symbol in dictionary:
            current_string = current_string_plus_symbol
        else:
            compressed_data.append(dictionary[current_string])
            dictionary[current_string_plus_symbol] = next_code
            next_code += 1
            current_string = symbol
    
    if current_string:
        compressed_data.append(dictionary[current_string])
    print(compressed_data)
    return compressed_data

def lzw_decompress(compressed_data):
    """LZW decompression algorithm."""
    dictionary = {i: chr(i) for i in range(256)}
    next_code = 256
    current_string = chr(compressed_data.pop(0))
    decompressed_data = current_string
    
    for code in compressed_data:
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = current_string + current_string[0]
        else:
            raise ValueError("Bad compressed code")
        
        decompressed_data += entry
        dictionary[next_code] = current_string + entry[0]
        next_code += 1
        current_string = entry
    
    return decompressed_data


