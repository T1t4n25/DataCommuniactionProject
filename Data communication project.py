divisor = '1011'
empty_7bits = '0000000'
def sender(message): # Haytham Work
    pass

divisor = '1011'


def xor(a, b):# Zeyad Hemeda
    result = []

    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')

    return ''.join(result)


# Performs Modulo-2 division
def mod2div(dividend, divisor2):# zeyad Hemeda
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


def sender_crc(message, cipher):  # Zeyad Hemeda Work
    to_be_sent = [message, cipher]
    for m in range(len(to_be_sent)):
        # initializing string 
        test_str = str(to_be_sent[m].encode('utf-8'))

        print("The original string is : " + test_str)
        # convert from string to int
        bit_arr1 = [ord(i) for i in test_str]
        # shift the bits to clear room for crc bits
        bit_arr = [format(i << 3, '08b') for i in bit_arr1]
        print('appended',bit_arr)
        # here we calculate the crc bits and remove excess bits
        crc_bits = [mod2div(i, divisor) for i in bit_arr]

        # the final message bits embedded with crc bits
        bit_arr = [format(bit_arr1[i], '08b') + crc_bits[i] for i in range(len(bit_arr1))]
        to_be_sent[m] = bit_arr
        print('to be sent',to_be_sent[m])
        # send to receiver CRC
        for i in range(len(to_be_sent[m])):
            x = receiver_crc(to_be_sent[m][i], m)
            if x != 1:
                i = i - 1
                print(f"Packet error at {m}, {i}, {x}")


###############################################################
correct_bytes = []
correct_cipher = []


def receiver_crc(receivedMessage, flag):  # Zeyad Hemeda Work
    print(receivedMessage, flag)
    if (int(mod2div(receivedMessage, divisor), 2) == 0) and flag == 0:
        print(1)
        correct_bytes.append([receivedMessage])
        return 1
    elif (int(mod2div(receivedMessage, divisor), 2) == 0) and flag == 1:
        print(2)
        correct_cipher.append([receivedMessage])
        return 1
    elif int(mod2div(receivedMessage, divisor), 2) != 0:  # packet error not correct
        print(mod2div(receivedMessage, divisor))
        return 0


def receiver(message, cipher): # not determined
    pass

def welcome_page(): # not determined
    pass

