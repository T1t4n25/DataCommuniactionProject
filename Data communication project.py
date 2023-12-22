from cryptography.fernet import Fernet
divisor = '1011'


def xor(a, b):# Zeyad Hemeda
    result = []

    # noinspection PyArgumentList
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

# use this to convert the messege from binary to string
def bin_to_string(to_convert):# Zeyad Hemeda
    print(to_convert)
    string = ''.join(chr(i) for i in to_convert)
    return string

def sender(message): # Haytham Work

    # Generate a random encryption key
    key = Fernet.generate_key()

    # Create a Fernet cipher with the generated key
    cipher = Fernet(key)
    print("Original Text: ", message)
    # Convert the text to bytes
    text_bytes = message.encode('utf-8')
    print("Encoded Text: ", text_bytes)
    # Encrypt the text
    encrypted_text = cipher.encrypt(text_bytes)
    print("Encrypted Text: ", encrypted_text)

    sender_crc(encrypted_text, cipher)

#################################################################################################################

def sender_crc(message, cipher):  # Zeyad Hemeda Work
    to_be_sent = [message, cipher]
    for m in range(len(to_be_sent)):
        str_conv = str(to_be_sent[m])
        # convert from string to int
        bit_arr1 = [ord(i) for i in str_conv]
        # shift the bits to get the remainder
        bit_arr = [format(i << 3, '08b') for i in bit_arr1]
        # here we calculate the crc bits
        crc_bits = [mod2div(i, divisor) for i in bit_arr]

        # the final message bits embedded with crc bits
        bit_arr = [format(bit_arr1[i], '08b') + crc_bits[i] for i in range(len(bit_arr1))]
        to_be_sent[m] = bit_arr
        # send to receiver CRC (still needs work not finished)
        for i in range(len(to_be_sent[m])):
            x = receiver_crc(to_be_sent[m][i], m)
            if x != 1:
                i = i - 1
                print(f"Packet error at {m}, {i}, {x}")


###############################################################
# these contain the transmitted messege as bytes
correct_bytes = []
correct_cipher = []


def receiver_crc(receivedMessage, flag):  # Zeyad Hemeda Work
    remainder = int(mod2div(receivedMessage, divisor), 2)
    if (remainder == 0) and flag == 0:
        correct_bytes.append(int(receivedMessage, 2) >> 3)
        return 1
    
    elif (remainder == 0) and flag == 1:
        correct_cipher.append(int(receivedMessage, 2) >> 3)
        return 1
    
    elif remainder != 0:  # packet error not correct
        print(mod2div(receivedMessage, divisor))
        return 0
    
#########################################################################################


def receiver(message, encrypted_text): # Zeyad Mohsen Work
    pass

def welcome_page(): # Zeyad ElHarty and Saed Ragheb work
    pass

if __name__ == "__main__":
    messege = 'mahmoud'
    sender(messege)
    print("messege", bin_to_string(correct_bytes))
    print("cipher", bin_to_string(correct_cipher))

