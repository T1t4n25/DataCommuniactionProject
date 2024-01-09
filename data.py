from helper import *
from cryptography.fernet import Fernet
from itertools import cycle
from random import randint, choice
from termcolor import colored
import pyfiglet
divisor = '1011'

correct_bytes = []


def sender_crc(message):
    str_conv = str(message)
    # convert from string to int
    bit_arr1 = [ord(i) for i in str_conv]
    # shift the bits to get the remainder
    bit_arr = [format(i << 3, '08b') for i in bit_arr1]
    # here we calculate the crc bits
    crc_bits = [mod2div(i, divisor) for i in bit_arr]
    # the final message bits embedded with crc bits
    bit_arr = [format(bit_arr1[i], '08b') + crc_bits[i] for i in range(len(bit_arr1))]
    message = bit_arr
    print('message as bits: ', bit_arr)
    
    # send to receiver CRC function
    i = 0
    while i < len(message):
        x = receiver_crc(message[i])
        if x == 0:
            print(f"\033[91m [*] Packet error at index : {i}\033[0m")
            print(f"\033[92m [*] Resending correct bits\033[0m")
        else:
            i += 1  # Increment i only if no error is detected

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


def receiver_crc(receivedMessage):
    global correct_bytes
    receivedMessage = error_sim(receivedMessage)
    remainder = int(mod2div(receivedMessage, divisor), 2)
    if (remainder == 0):
        correct_bytes.append(int(receivedMessage, 2) >> 3)
        return 1
    else:  # packet error not correct
        return 0


def welcome_page():
    
    colors = cycle(['red', 'green', 'blue'])
    font = pyfiglet.Figlet(font='small', width= 100)
    welcome_message = "C R C  \nS i m u l a t i o n"
    
    banner = font.renderText(welcome_message)

    print(colored(banner, next(colors)))  # type: ignore


if __name__ == "__main__":
    welcome_page()
    messege = input("Enter the messege you want to transmit:")
    #messege = 'zeyad hemeda'
    sender_crc(messege)
    print('delivered messege: ', bin_to_string(correct_bytes))
