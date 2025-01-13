
def bits_to_string(bits):
    # Chia chuỗi bit thành các phần có chiều dài 8
    chunks = [bits[i:i+8] for i in range(0, len(bits), 8)]
    
    # Chuyển đổi từng phần thành một số nguyên và sau đó thành ký tự
    characters = [chr(int(chunk, 2)) for chunk in chunks]
    
    # Kết hợp các ký tự để tạo thành chuỗi
    result_string = ''.join(characters)
    
    return result_string

# Sử dụng hàm với một ví dụ
bit_string = "0010000001010100011010000110010100100000011001100110110001100001011001110010000001101001011100110010000001000110010011000100000101000111011110110110100101110100001101010101111100110011011011100011000001110101001110010110100001011111011010100101010100110101010101000101111101110100010011110101111101110011010010000011000101100110011101000101111101001101001100110111110100100000"
string_result = bits_to_string(bit_string)
print(string_result)
