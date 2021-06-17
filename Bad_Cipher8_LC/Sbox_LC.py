# ===================
# 암호분석 2021
# ===================

# Sbox의 선형 특성
import my_lib2 as Common

S = [ 0x13,0x31,0xba,0x03,0xa9,0xb8,0x32,0x88,0x23,0xa8,0x33,0x9b,0xb9,0x28,0x91,0x98,
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

# Max bias = 128 (128 --> 4) => Max count = 256
# Max linear probability = 1
# Max bias = -20 (4 --> 45) => Max count = 108
# Max linear probability =  0.578125
# 최대 선형 확률은 1/2에서 벗어날 수록 선형특성을 가진다.
# 어쨋든 0 또는 1로 한 쪽으로 치우쳐지는 현상이 발생
'''
# --선형 특성표 LTable[in_mask_a][out_mask_b] = #{ x | ax=bS(x) } - 2 ^ (n-1)
LTable = []
# size LTable = 256 ^ 256
for i in range(len(S)):
    LTable.append([0]*len(S))
    # [0,0,........,0]

print('In-Out Masking', end='')
for in_mask in range(len(S)): # in mask a
    for out_mask in range(len(S)): # in mask b
        local_count = 0
        for x in range(len(S)):
            y = S[x]
            if Common.hw_mod2(in_mask & x) == Common.hw_mod2(out_mask & y):
                local_count += 1
        LTable[in_mask][out_mask] = local_count - 128
    print('.', end='')
print('\n')

print('LTable = ', LTable)
'''

'''
#- 최대 선형 확률 계산
# max_count 는 최대 bias
max_count = 0
max_in, max_out = 0, 0
for in_mask in range (1, len(S)):
    for out_mask in range(len(S)):
        if abs(LTable[in_mask][out_mask]) > max_count:
            max_in = in_mask
            max_out = out_mask
            max_count = abs(LTable[in_mask][out_mask])

print('Max count = %d (%d --> %d)' %(LTable[max_in][max_out], max_in, max_out))
print('Max linear probability = ', max_count/256 + 0.5)
# Max count = 128 (128 --> 4)
# Max linear probability = 1
'''

'''
# Max count = ??? (4 --> ???)
print('In_mask = 4')
in_mask = 4
LTable_out = [0] * len(S)
for out_mask in range(len(S)):
    local_count = 0
    for x in range(len(S)):
        y = S[x]
        if Common.hw_mod2(in_mask & x) == Common.hw_mod2(out_mask & y):
            local_count += 1
    LTable_out[out_mask] = local_count - 128
    # LTable_out[out_mask] = local_count
    # NS(a, b)
max_count = 0
max_in, max_out = 4, 0
for out_mask in range(len(S)):
    if abs(LTable_out[out_mask]) > max_count:
        max_out = out_mask
        max_count = abs(LTable_out[out_mask])
        # 최대 편차 값

print('Max count = %d (%d --> %d)' %(LTable_out[max_out], max_in, max_out))
print('Max linear probability = ', max_count/256 + 0.5 )
'''
