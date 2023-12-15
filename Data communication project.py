divisor = '1011'
empty_7bits = '0000000'
def sender(message): # Haytham Work
    pass

def sender_CRC(message, cipher): # Zeyad Hemeda Work
    toBeSent = [message,  cipher]
    for m in range(len(toBeSent))
        # initializing string 
        test_str = str(toBeSent[m].encode('utf-8'))
    
        print("The original string is : " + str(test_str))

        bit_arr1 = [format(ord(i), '08b') for i in test_str]

        bit_arr = [i + empty_7bits for i in bit_arr1]

        crc_bits = [format(int(i, 2) % int(divisor, 2), '08b') for i in bit_arr]

        bit_arr = [int(bit_arr1[i] + crc_bits[i], 2) for i in range(len(bit_arr1))]

        toBeSent[m] = bit_arr
        # send to reciever CRC
        receiver_CRC(toBeSent[0], toBeSent[1])


def receiver_CRC(message, cipher): # Zeyad Hemeda Work
    pass

def receiver(message): # not determined
    pass

def welcome_page(): # not determined
    pass

