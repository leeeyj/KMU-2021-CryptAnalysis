#-------------------------
# 암호분석 2021
#
#  BC20R - BadCipher with Whitening - Reduced round version
#
#-------------------------


#== Bad Sbox
BSbox = [ 0x13,0x31,0xba,0x03,0xa9,0xb8,0x32,0x88,0x23,0xa8,0x33,0x9b,0xb9,0x28,0x91,0x98,
          0x29,0x3b,0x3a,0x38,0x09,0x89,0x01,0x80,0x83,0x10,0xb0,0x19,0xab,0x12,0x02,0x90,
          0xb3,0x30,0x08,0x11,0xbb,0x81,0x9a,0xa3,0xb2,0xa2,0x22,0x8b,0x20,0x1b,0x2a,0x82,
          0x8a,0x2b,0x0a,0x1a,0xaa,0x93,0x00,0x21,0x99,0xb1,0x18,0xa0,0x0b,0xa1,0x39,0x92,
          0x53,0x71,0xfa,0x43,0xe9,0xf8,0x72,0xc8,0x63,0xe8,0x73,0xdb,0xf9,0x68,0xd1,0xd8,
          0x69,0x7b,0x7a,0x78,0x49,0xc9,0x41,0xc0,0xc3,0x50,0xf0,0x59,0xeb,0x52,0x42,0xd0,
          0xf3,0x70,0x48,0x51,0xfb,0xc1,0xda,0xe3,0xf2,0xe2,0x62,0xcb,0x60,0x5b,0x6a,0xc2,
          0xca,0x6b,0x4a,0x5a,0xea,0xd3,0x40,0x61,0xd9,0xf1,0x58,0xe0,0x4b,0xe1,0x79,0xd2,
          0x44,0x37,0x0e,0x6c,0x3f,0x1f,0x8e,0x76,0x7d,0x26,0x2f,0x94,0x5c,0x0c,0x66,0x17,
          0x1d,0x97,0x14,0xb6,0xac,0xcf,0x87,0x06,0x6f,0xae,0xc7,0x5f,0x24,0xc6,0x96,0xe4,
          0xc4,0xe5,0xec,0x34,0x4e,0x0f,0x74,0xbe,0xff,0x0d,0x9d,0xf5,0xa6,0x84,0x2e,0x4d,
          0xdf,0x05,0x6d,0x45,0x54,0xde,0x5e,0x95,0xbc,0x3e,0xad,0x46,0x47,0x7e,0x7f,0x36,
          0xd4,0xf7,0x9f,0xbd,0x7c,0x56,0x1c,0x3d,0x27,0xa7,0x25,0x67,0xaf,0xed,0xa4,0x57,
          0x8d,0x4f,0xf6,0xfd,0x85,0x1e,0xb5,0x65,0xa5,0x6e,0x77,0xe6,0xee,0x8f,0xd6,0x3c,
          0x55,0xcd,0x07,0xb7,0xe7,0x64,0xcc,0x2d,0x75,0xb4,0x5d,0x2c,0x35,0x8c,0x9e,0x16,
          0x9c,0xc5,0x86,0x15,0xfc,0x04,0xd7,0x4c,0xdd,0xce,0xd5,0xfe,0xdc,0xbf,0xf4,0xef ]

#== Inverse Bad Sbox
IBSbox = [ 0x36,0x16,0x1e,0x03,0xf5,0xb1,0x97,0xe2,0x22,0x14,0x32,0x3c,0x8d,0xa9,0x82,0xa5,
           0x19,0x23,0x1d,0x00,0x92,0xf3,0xef,0x8f,0x3a,0x1b,0x33,0x2d,0xc6,0x90,0xd5,0x85,
           0x2c,0x37,0x2a,0x08,0x9c,0xca,0x89,0xc8,0x0d,0x10,0x2e,0x31,0xeb,0xe7,0xae,0x8a,
           0x21,0x01,0x06,0x0a,0xa3,0xec,0xbf,0x81,0x13,0x3e,0x12,0x11,0xdf,0xc7,0xb9,0x84,
           0x76,0x56,0x5e,0x43,0x80,0xb3,0xbb,0xbc,0x62,0x54,0x72,0x7c,0xf7,0xaf,0xa4,0xd1,
           0x59,0x63,0x5d,0x40,0xb4,0xe0,0xc5,0xcf,0x7a,0x5b,0x73,0x6d,0x8c,0xea,0xb6,0x9b,
           0x6c,0x77,0x6a,0x48,0xe5,0xd7,0x8e,0xcb,0x4d,0x50,0x6e,0x71,0x83,0xb2,0xd9,0x98,
           0x61,0x41,0x46,0x4a,0xa6,0xe8,0x87,0xda,0x53,0x7e,0x52,0x51,0xc4,0x88,0xbd,0xbe,
           0x17,0x25,0x2f,0x18,0xad,0xd4,0xf2,0x96,0x07,0x15,0x30,0x2b,0xed,0xd0,0x86,0xdd,
           0x1f,0x0e,0x3f,0x35,0x8b,0xb7,0x9e,0x91,0x0f,0x38,0x26,0x0b,0xf0,0xaa,0xee,0xc2,
           0x3b,0x3d,0x29,0x27,0xce,0xd8,0xac,0xc9,0x09,0x04,0x34,0x1c,0x94,0xba,0x99,0xcc,
           0x1a,0x39,0x28,0x20,0xe9,0xd6,0x93,0xe3,0x05,0x0c,0x02,0x24,0xb8,0xc3,0xa7,0xfd,
           0x57,0x65,0x6f,0x58,0xa0,0xf1,0x9d,0x9a,0x47,0x55,0x70,0x6b,0xe6,0xe1,0xf9,0x95,
           0x5f,0x4e,0x7f,0x75,0xc0,0xfa,0xde,0xf6,0x4f,0x78,0x66,0x4b,0xfc,0xf8,0xb5,0xb0,
           0x7b,0x7d,0x69,0x67,0x9f,0xa1,0xdb,0xe4,0x49,0x44,0x74,0x5c,0xa2,0xcd,0xdc,0xff,
           0x5a,0x79,0x68,0x60,0xfe,0xab,0xd2,0xc1,0x45,0x4c,0x42,0x64,0xf4,0xd3,0xfb,0xa8 ]

#-- AR: Add Roundkey
def AR(in_state, rkey):
    out_state = [0, 0, 0, 0]
    for i in range(len(in_state)):
        out_state[i] = in_state[i] ^ rkey[i]
    return out_state


#-- BS layer
def BS_Layer(in_state):
    out_state = [0, 0, 0, 0]
    for i in range(len(in_state)):
        out_state[i] = BSbox[in_state[i]]
    return out_state

#-- LM: Linear Map (LM = LM^(-1) involution)
def LM_Layer(in_state):
    out_state = [0, 0, 0, 0]
    all_xor = in_state[0] ^ in_state[1] ^ in_state[2] ^ in_state[3]
    for i in range(len(in_state)):
        out_state[i] = in_state[i] ^ all_xor
    return out_state    

#-- Encrypt Round
def Enc_Round(in_state, rkey):
    out_state1 = [0, 0, 0, 0]
    out_state2 = [0, 0, 0, 0]
    out_state3 = [0, 0, 0, 0]
    out_state1 = AR(in_state, rkey)
    out_state2 = BS_Layer(out_state1)
    out_state3 = LM_Layer(out_state2)
    
    return out_state3

#-- BC20 Encryption
def BC20_Enc(input_state, key):
    state = input_state
    numRound = 10 # 라운드 수
    for i in range(0, numRound):
        state = Enc_Round(state, key)

    #== Whitening Key (추가)
    state = AR(state, key)
    
    return state

#--- BC20R Encryption (Reduced Round BC20)
def BC20R_Enc(input_state, key, num_round):
    state = input_state
    for i in range(0, num_round):
        state = Enc_Round(state, key)

    #== Whitening Key (추가)
    state = AR(state, key)
    
    return state
    


#-- Inverse BS layer
def IBS_Layer(in_state):
    out_state = [0, 0, 0, 0]
    for i in range(len(in_state)):
        out_state[i] = IBSbox[in_state[i]]
    return out_state

#-- Decrypt Round
def Dec_Round(in_state, rkey):
    out_state1 = [0, 0, 0, 0]
    out_state2 = [0, 0, 0, 0]
    out_state3 = [0, 0, 0, 0]
    out_state1 = LM_Layer(in_state)
    out_state2 = IBS_Layer(out_state1)
    out_state3 = AR(out_state2, rkey)
    
    return out_state3

#-- BC20 Decryption
def BC20_Dec(input_state, key):
    numRound = 10 # 라운드 수
    
    #== Whitening Key (추가)
    state = AR(input_state, key)
    
    for i in range(0, numRound):
        state = Dec_Round(state, key)
    
    return state

#--- BC20R Decryption (Reduced Round BC20)
def BC20R_Dec(input_state, key, num_round):
    #== Whitening Key (추가)
    state = AR(input_state, key)
    
    for i in range(0, num_round):
        state = Dec_Round(state, key)
    
    return state

#------------------------------------------------
def main():
    message = 'ABCD'
    key = [0, 1, 2, 3]
    input_state = [ ord(ch) for ch in message ]
    output_state = BC20R_Enc(input_state, key, 5)
    
    print('message =', message)
    print('input plaintext =', input_state)
    print('output ciphertext =', output_state)

    dec_state = BC20R_Dec(output_state, key,5)
    
    print('decrypted state =', dec_state)
    byte1 = bytes(dec_state)
    str1 = byte1.decode('utf8')
    print('decrypted message =', str1)

'''
(출력)    
message = ABCD
input plaintext = [65, 66, 67, 68]
output ciphertext = [31, 90, 23, 227]
decrypted state = [65, 66, 67, 68]
decrypted message = ABCD
'''

##-- Run main()

if __name__ == '__main__':
    main()