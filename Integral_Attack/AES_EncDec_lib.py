#-------------------------
# 암호분석 2020
#-------------------------

import copy      # 딥 카피 (깊은 복사) 

# Rijndael S-box
Sbox =  [ 0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67,
        0x2b, 0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59,
        0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7,
        0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1,
        0x71, 0xd8, 0x31, 0x15, 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05,
        0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83,
        0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29,
        0xe3, 0x2f, 0x84, 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
        0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 0xd0, 0xef, 0xaa,
        0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c,
        0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc,
        0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c, 0x13, 0xec,
        0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19,
        0x73, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee,
        0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 0xe0, 0x32, 0x3a, 0x0a, 0x49,
        0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4,
        0xea, 0x65, 0x7a, 0xae, 0x08, 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6,
        0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 0x70,
        0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9,
        0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e,
        0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 0x8c, 0xa1,
        0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0,
        0x54, 0xbb, 0x16]

# Rijndael Inverted S-box
ISbox = [ 0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3,
        0x9e, 0x81, 0xf3, 0xd7, 0xfb , 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f,
        0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb , 0x54,
        0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b,
        0x42, 0xfa, 0xc3, 0x4e , 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24,
        0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25 , 0x72, 0xf8,
        0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d,
        0x65, 0xb6, 0x92 , 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda,
        0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84 , 0x90, 0xd8, 0xab,
        0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3,
        0x45, 0x06 , 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1,
        0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b , 0x3a, 0x91, 0x11, 0x41,
        0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6,
        0x73 , 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9,
        0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e , 0x47, 0xf1, 0x1a, 0x71, 0x1d,
        0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b ,
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0,
        0xfe, 0x78, 0xcd, 0x5a, 0xf4 , 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07,
        0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f , 0x60,
        0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f,
        0x93, 0xc9, 0x9c, 0xef , 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5,
        0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61 , 0x17, 0x2b,
        0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55,
        0x21, 0x0c, 0x7d]

# Round constant for Key schedule
RC = [ 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]


#-- xtime 유한체 GF(2^8)에서의 곱셈 (다항식에 x를 곱하기)
def xtime(x):
    y = (x << 1) & 0xff
    if x >= 128:
        y ^= 0x1b
    return y

#-- MixColumn 용 '0x02' 곱하기
def m02(x):
    return xtime(x)

#-- MixColumn 용 '0x03' 곱하기
def m03(x):
    return m02(x)^x

#-- 4바이트 회전 (key schedule 함수용)
def Rotl(col):
    new_col = [ col[1], col[2], col[3], col[0] ]
    return new_col

#-- 한 Column에 대한 MixColumns 연산
    # [ [2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2] ]
def MC_Col(col):
    new_col = [0]*4
    new_col[0] = m02(col[0]) ^ m03(col[1]) ^ col[2] ^ col[3]
    new_col[1] = col[0] ^ m02(col[1]) ^ m03(col[2]) ^ col[3]
    new_col[2] = col[0] ^ col[1] ^ m02(col[2]) ^ m03(col[3])
    new_col[3] = m03(col[0]) ^ col[1] ^ col[2] ^ m02(col[3])
    return new_col

#---- InvMC 용 곱하기
def m04(x):
    return m02(m02(x))

def m08(x):
    return m04(m02(x))

def m09(x):
    return m08(x)^x

def m0b(x):
    return m08(x)^m03(x)

def m0d(x):
    return m08(x)^m04(x)^x

def m0e(x):
    return m08(x)^m04(x)^m02(x)

#-- 한 Column에 대한 InvMixColumns 연산
    # [ [e, b, d, 9], [9, e, b, d], [d, 9, e, b], [b, d, 9, e] ]
def InvMC_Col(col):
    new_col = [0]*4
    new_col[0] = m0e(col[0]) ^ m0b(col[1]) ^ m0d(col[2]) ^ m09(col[3])
    new_col[1] = m09(col[0]) ^ m0e(col[1]) ^ m0b(col[2]) ^ m0d(col[3])
    new_col[2] = m0d(col[0]) ^ m09(col[1]) ^ m0e(col[2]) ^ m0b(col[3])
    new_col[3] = m0b(col[0]) ^ m0d(col[1]) ^ m09(col[2]) ^ m0e(col[3])
    return new_col

#===================================

#-- 한 column에 대한 Sbox
def SubByte_Col(col):
    new_col = [ Sbox[col[i]] for i in range(4) ]
    return new_col

#-- 한 Column의 XOR
def Xor_Col(c1, c2):
    new_col = [ c1[i]^c2[i] for i in range(4) ]
    return new_col

#-- AddRoundkey
def AddRoundKey(state, rkey):
    new_state = []
    for col in range(4):
        new_col = [ state[col][i] ^ rkey[col][i] for i in range(4) ]
        new_state.append(new_col)
    return new_state

#-- SubBytes
def SubBytes(state):
    new_state = []
    for col in range(4):
        new_col = [ Sbox[ state[col][i] ] for i in range(4) ]
        new_state.append(new_col)
    return new_state

#-- ShiftRows
def ShiftRows(state):
    new_state = []
    for col in range(4):
        new_col = [ state[(col+i)%4][i] for i in range(4) ]
        new_state.append(new_col)
    return new_state

#-- MixColumns
def MixColumns(state):
    new_state = []
    for col in range(4):
        new_col = MC_Col(state[col])
        new_state.append(new_col)
    return new_state

#===================================

#-- 한 column에 대한 InvSbox
def InvSubByte_Col(col):
    new_col = [ ISbox[col[i]] for i in range(4) ]
    return new_col

#-- InvSubBytes
def InvSubBytes(state):
    new_state = []
    for col in range(4):
        new_col = [ ISbox[ state[col][i] ] for i in range(4) ]
        new_state.append(new_col)
    return new_state

#-- InvShiftRows
def InvShiftRows(state):
    new_state = []
    for col in range(4):
        new_col = [ state[(col-i)%4][i] for i in range(4) ]
        new_state.append(new_col)
    return new_state

#-- InvMixColumns
def InvMixColumns(state):
    new_state = []
    for col in range(4):
        new_col = InvMC_Col(state[col])
        new_state.append(new_col)
    return new_state

#===================================
#-- 16바이트를 4x4 행렬(state)로 변환 
def block2state(in_block):
    new_state = []
    for col in range(4):
        new_col = [ in_block[col*4+i] for i in range(4) ]
        new_state.append(new_col)
    return new_state

#-- (4x4 state) 출력
def hex_print(state):
    print('[', end='')
    for i in range(4):
        print('[%02x, %02x, %02x, %02x]' \
              %(state[i][0], state[i][1], state[i][2], state[i][3]), end='')
        if i<3:
            print(', ', end='')
    print(']')

#-- 암호화 라운드 함수
def AES_Round(state, rkey):
    new_state = copy.deepcopy(state)
    new_state2 = SubBytes(new_state)
    #hex_print(new_state2)
    new_state3 = ShiftRows(new_state2)
    #hex_print(new_state3)
    new_state4 = MixColumns(new_state3)
    new_state5 = AddRoundKey(new_state4, rkey)
    return new_state5

#-- 복호화 라운드 함수
def AES_InvRound(state, rkey):
    new_state5 = copy.deepcopy(state)
    new_state4 = AddRoundKey(new_state5, rkey)
    new_state3 = InvMixColumns(new_state4)
    new_state2 = InvShiftRows(new_state3)
    new_state1 = InvSubBytes(new_state2)
    
    return new_state1

#-----
# AES key schedule에서만 사용되는 4바이트 변환함
# 바이트 rotation -> Sbox 적용 ->  RoundConstant 적
def KeySR(col, round):
    new_col = Rotl(col)
    round_constant = [ RC[round-1], 0, 0, 0]
    new_col2 = SubByte_Col(new_col)
    new_col3 = Xor_Col(new_col2, round_constant)
    return new_col3

#-----
# AES Encrytion용 Key schedule
# 입력: 암호키 (4x4 state)
# 출력: 11개의 라운드키(4x4 state) 
# 출력 rkey = [ rkey[0], rkey[1], ... , rkey[10] ]
# rkey[r] = [ [rk00, rk10, rk20, rk30], ... , [rk03, rk13, rk23, rk33] ]
def key_schedule_Enc(key_state):
    rkey = [ copy.deepcopy(key_state) ]
    for round in range(1,11):
        new_state = []
        new_w0 = Xor_Col(rkey[round-1][0], KeySR(rkey[round-1][3], round))
        new_state.append(new_w0)
        new_w1 = Xor_Col(rkey[round-1][1], new_w0)
        new_state.append(new_w1)
        new_w2 = Xor_Col(rkey[round-1][2], new_w1)
        new_state.append(new_w2)
        new_w3 = Xor_Col(rkey[round-1][3], new_w2)
        new_state.append(new_w3)
        rkey.append(new_state)
    return rkey

#-- AES-128 암호화
def AES_Enc(pt, key):
    rkey = key_schedule_Enc(key)
    state = copy.deepcopy(pt)
    new_state = AddRoundKey(state, rkey[0])
    for i in range(1,10):  # 1,2,...,9
        out_state = AES_Round(new_state, rkey[i])
        new_state = copy.deepcopy(out_state)
        print(i, ': ', end ='')
        hex_print(new_state)
    #-- final round
    new_state2 = SubBytes(new_state)
    new_state3 = ShiftRows(new_state2)
    new_state4 = AddRoundKey(new_state3, rkey[10])
    return new_state4

#-- AES-128 복호화
def AES_Dec(ct, key):
    rkey = key_schedule_Enc(key)
    state = copy.deepcopy(ct)
    new_state1 = AddRoundKey(state, rkey[10])
    new_state2 = InvShiftRows(new_state1)
    new_state = InvSubBytes(new_state2)
    for i in range(9,0,-1):  # 9,8,..., 1
        out_state = AES_InvRound(new_state, rkey[i])
        new_state = copy.deepcopy(out_state)
        print(i, ': ', end ='')
        hex_print(new_state)
    
    new_state3 = AddRoundKey(new_state, rkey[0])
    return new_state3


#-- AES-128 암호화(부분 라운드)
def AES_EncR(pt, key, round):
    rkey = key_schedule_Enc(key)
    state = copy.deepcopy(pt)
    new_state = AddRoundKey(state, rkey[0])
    for i in range(1,round): 
        out_state = AES_Round(new_state, rkey[i])
        new_state = copy.deepcopy(out_state)
        #print(i, ': ', end ='')
        #hex_print(new_state)
    #-- final round
    new_state2 = SubBytes(new_state)
    new_state3 = ShiftRows(new_state2)
    new_state4 = AddRoundKey(new_state3, rkey[round])
    return new_state4

#-- AES-128 복호화(부분 라운드)
def AES_DecR(ct, key, round):
    rkey = key_schedule_Enc(key)
    state = copy.deepcopy(ct)
    #-- final round
    
    new_state1 = AddRoundKey(state, rkey[round])
    new_state2 = InvShiftRows(new_state1)
    new_state = InvSubBytes(new_state2)     
        
    for i in range(round-1,0,-1):  
        out_state = AES_InvRound(new_state, rkey[i])
        new_state = copy.deepcopy(out_state)
        #print(i, ': ', end ='')
        #hex_print(new_state)
    new_state4 = AddRoundKey(new_state, rkey[0])
    return new_state4
#=========================
    
def main():
    
    #---
    # 테스트 벡터: FIPS 197 - AES (page 33)
    block = [ 0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, \
            0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34 ]
    key = [ 0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, \
            0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c ]
    
    in_state = block2state(block)
    key_state = block2state(key)
    
    print('plaintext =')
    hex_print(in_state)
    print('key=')
    hex_print(key_state)
    
    new_state = AES_Enc(in_state, key_state)
    print('ciphertext=')
    hex_print(new_state)
    
    dec_state = AES_Dec(new_state, key_state)  
    print('Decrypted = ')
    hex_print(dec_state)
    
        
if __name__ == '__main__':
    main()        
        
        
        
        
        
        