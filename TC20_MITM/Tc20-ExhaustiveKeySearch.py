# -------------------------
# 암호분석 2021 Week6
# TC20 키 전수조사 알고리즘
# -------------------------

import TC20_lib as TC20

# 정답: Key =  [0, 1, 2, 3]

PT = [65, 82, 73, 65]
CT = [202, 134, 119, 230]

# 정수를 16진수 리스트로
def int2list(n):
    out_list = []
    out_list.append( (n >> 24) & 0xff )
    out_list.append( (n >> 16) & 0xff )
    out_list.append( (n >>  8) & 0xff )
    out_list.append( (n      ) & 0xff )

    return out_list


# 16진수 리스트를 16진수 하나로
def list2int(l):
    n = 0
    num_bytes = len(l)
    for idx in range(len(l)):
        n += l[idx] << 8 * (num_bytes - idx - 1)

    return n


Flag = False

KeyRange = 1 << 24
# 24-bit key size

key_guess = None
key_guess_list = []
print('Key searching', end='')
for idx in range(0, KeyRange):
    key_guess = int2list(idx)
    ct_guess = TC20.TC20_Enc(PT, key_guess)
    if ct_guess == CT:
        key_guess_list.append(key_guess)

print(key_guess_list)
PT2 = []
CT2 = []

for key_list in key_guess_list:
    ct2_guess = TC20.TC20_Enc(PT2, key_list)
    if ct2_guess == CT2:
        print("key = ", key_list)
        break


'''
print('\n')
if Flag:
    print('Key Found! Key =', key_guess)
else:
    print('Key not Found')
'''