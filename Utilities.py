def binary_to_char(binary_str):
    return chr(int(binary_str, 2))

def char_to_binary(char_str):
    return format( ord(char_str), '08b' )

def binary_to_int(binary_str):
    return int(binary_str, 2)

def int_to_binary(num):
    return format(int(num),  '08b')

def Message_to_BinaryList(message):
    b_list=[]
    for char in message:
        b_list.append(char_to_binary(char))
    return b_list

def BinaryList_to_Message(b_list):
    message=""
    for binary_str in b_list:
        message+=binary_to_char(binary_str)
    return message
