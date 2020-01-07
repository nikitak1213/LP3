FIXED_IP = [2, 6, 3, 1, 4, 8, 5, 7]
FIXED_EP = [4, 1, 2, 3, 2, 3, 4, 1]
FIXED_IP_INVERSE = [4, 1, 3, 5, 7, 2, 8, 6]
FIXED_P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
FIXED_P8 = [6, 3, 7, 4, 8, 5, 10, 9]
FIXED_P4 = [2, 4, 3, 1]

S0 = [[1, 0, 3, 2],
      [3, 2, 1, 0],
      [0, 2, 1, 3],
      [3, 1, 3, 2]]

S1 = [[0, 1, 2, 3],
      [2, 0, 1, 3],
      [3, 0, 1, 0],
      [2, 1, 0, 3]]


def permute(bits, pertable):
    string_new = ""
    for i in range(len(pertable)):
        string_new = string_new + bits[pertable[i] - 1]
    return string_new


def shift(bits):
    string_new = ""
    for i in range(1, len(bits)):
        string_new = string_new + bits[i]
    string_new = string_new + bits[0]
    return string_new


def get_keys(key):
    keys = []
    key = permute(key, FIXED_P10)
    ls_1 = shift(key[:5]) + shift(key[5:])
    keys.append(permute(ls_1, FIXED_P8))
    ls_2 = shift(ls_1[:5]) + shift(ls_1[5:])
    ls_2 = shift(ls_2[:5]) + shift(ls_2[5:])
    keys.append(permute(ls_2, FIXED_P8))
    return keys


def xor(bits1, bits2):
    new_string = ""
    for i in range(len(bits1)):
        new_string = new_string + str((int(bits1[i]) + int(bits2[i])) % 2)
    return new_string


def substitute(bits,table):
    row = bits[0]+bits[3]
    col = bits[1]+bits[2]
    row_num = int(row, base=2)
    col_num = int(col, base=2)

    output = table[row_num][col_num]
    output = format(output, 'b').zfill(2)

    return output


def fk(right, key):
    ep = permute(right, FIXED_EP)
    output = xor(ep, key)
    s0 = substitute(output[:4], S0)
    s1 = substitute(output[4:], S1)
    output = permute(s0+s1,FIXED_P4)
    return output


def function_k(bits, key):
    right = fk(bits[4:],key)
    left = bits[:4]
    output = xor(left, right)
    return output


def swap(left,right):
    return right + left


def encryption(bits, key):
    keys = get_keys(key)
    bits = permute(bits, FIXED_IP)
    left = function_k(bits, keys[0])
    right = bits[4:]
    bits = swap(left, right)
    left = function_k(bits, keys[1])
    right = bits[4:]
    output = left+right
    output = permute(output,FIXED_IP_INVERSE)
    return output


def decryption(bits, key):
    keys = get_keys(key)
    bits = permute(bits, FIXED_IP)
    left = function_k(bits, keys[1])
    right = bits[4:]
    bits = swap(left, right)
    left = function_k(bits, keys[0])
    right = bits[4:]
    output = left+right
    output = permute(output,FIXED_IP_INVERSE)
    return output

if __name__ == '__main__':
    key = "1010000010"
    plaintext = "10101110"
    print("Enter 10 bit Key: ")
    key = input()
    print("Enter 8 bit PlainText: ")
    plaintext = input()
    #print(int("100", base=2))
    ciper = encryption(plaintext, key)
    print("ciper text afer sdes: "+ciper)
    print("After decrypting ciper text: "+decryption(ciper,key))
    
