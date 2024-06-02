
def convert_byte_to_byte_string(byte):
    binary_string = bin(byte)[2:].zfill(16)
    formatted_string = ' '.join([binary_string[i:i+4] for i in range(0, len(binary_string), 4)])
    return formatted_string

def convert_byte_to_list_int(byte):
    result = []
    for i in range(3, -1, -1):
        number = byte & (0b1111 << 4*i)
        number = number >> 4*i
        result.append(number)
    return result

def convert_list_int_to_byte(numbers):
    result = 0
    for i in range(len(numbers)):
        result = result | (numbers[i] << 4*(len(numbers)-1-i))
    return result
    
number = 0b0010000100000000
print(convert_byte_to_byte_string(number))
res = convert_byte_to_list_int(number)
print(res)
res = convert_list_int_to_byte(res)
print(res)
print(convert_byte_to_byte_string(res))

