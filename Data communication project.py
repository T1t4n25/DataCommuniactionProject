import base64
from random import choice, randint
from cryptography.fernet import Fernet
import pyfiglet
from termcolor import colored
from itertools import cycle
from termcolor import colored

divisor = '1011'

correct_cipher = []
correct_bytes = []

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

# use this to convert the messege from binary to bytes
def bin_to_string(to_convert):# Zeyad Hemeda
    string = "".join(chr(byte) for byte in to_convert)
    print('bin to string out: ',string)
    return string

def sender(message): # Haytham Work

    # Generate a random encryption key
    key = 'secretkey'
    key_byte = key.encode('utf-8')
    print("cipher1", key_byte)
    key_base = base64.urlsafe_b64encode(key_byte.ljust(32)[:32])
    # Create a Fernet cipher with the key
    cipher = Fernet(key_base)
    print("Original Text: ", message)
    # Convert the text to bytes
    text_bytes = message.encode('utf-8')
    print("Encoded Text: ", cipher)
    # Encrypt the text
    encrypted_text = cipher.encrypt(text_bytes)
    print("Encrypted Text: ", encrypted_text)

    sender_crc(encrypted_text, key_byte)

###################################################################

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
                print(f"\033[91m [*] Packet error at index : {m} {i}\033[0m")
                print(f"\033[92m [*] Resending correct bits\033[0m")


###############################################################
def error_sim(bits_arr):
    if choice([True, False]):
        random_bit = randint(0, len(bits_arr) - 1)
        packet_to_flip = list(bits_arr)
        if packet_to_flip[random_bit] == '0':
            packet_to_flip[random_bit] = '1'
            bits_arr = ''.join(i for i in packet_to_flip)
        else:
            packet_to_flip[random_bit] = '0'
            bits_arr = ''.join(i for i in packet_to_flip)
    return bits_arr


def receiver_crc(receivedMessage, flag):  # Zeyad Hemeda Work
    global correct_cipher
    global correct_bytes
    global correct_bytes
    receivedMessage = error_sim(receivedMessage)
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

def receiver(encrypted_text, cipher): # Zeyad Mohsen Work
    cipher_bytes = cipher.encode('utf-8')
    cipher_bytes = base64.urlsafe_b64encode(cipher_bytes.ljust(32)[:32])
    cipher_suite = Fernet(cipher_bytes)
    # Decrypt the encrypted text
    decrypted_text = cipher_suite.decrypt(encrypted_text)

    # Convert the decrypted bytes back to a string
    decrypted_text_str = decrypted_text.decode('utf-8')

    print("Decrypted Text: ", decrypted_text_str)

def welcome_page(): # Zeyad ElHarty and Saed Ragheb work
    member_names = [
        'Z i a d  H e m e d a',
        'S a m i  E m a d',
        'H a i t h a m  M o h a m e d',
        'S a e e d  R a g h e b ',
        'Z i a d  H e i k a l',
        'Z i a d  A l - H a r t e y'
    ]
    colors = cycle(['red', 'green', 'blue'])
    font = pyfiglet.Figlet(font='small', width= 100)
    welcome_message = ["W e l c o m e  t o", "C R C  \nS i m u l a t i o n", "T e a m M e m b e r s"]
    banner = []
    banner = [font.renderText(i) for i in welcome_message]

    for i in banner:
        print(colored(i, next(colors), attrs=['bold'])) 

    print(" \n".join(member_names))

    user_message = input("Enter your message: ")
    print("User Message:", user_message)
    sender(user_message)



if __name__ == "__main__":
    welcome_page()
    #print('cipher', correct_cipher)
    receiver(bin_to_string(correct_bytes), bin_to_string(correct_cipher))
    