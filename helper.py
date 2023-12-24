
def xor(a, b):
    result = []

    # noinspection PyArgumentList
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')

    return ''.join(result)


# Performs Modulo-2 division
def mod2div(dividend, divisor2):
    pick = len(divisor2)
    tmp = dividend[0: pick]

    while pick < len(dividend):

        if tmp[0] == '1':
            tmp = xor(divisor2, tmp) + dividend[pick]

        else:
            tmp = xor('0' * pick, tmp) + dividend[pick]

        pick += 1

    if tmp[0] == '1':
        tmp = xor(divisor2, tmp)
    else:
        tmp = xor('0' * pick, tmp)

    checkword = tmp
    return checkword

# use this to convert the messege from binary to bytes
def bin_to_string(to_convert):
    string = "".join(chr(byte) for byte in to_convert)
    print('bin to string out: ',string)
    return string