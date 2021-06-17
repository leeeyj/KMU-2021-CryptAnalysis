# =======================================
# 암호분석 2021
# BCF 4라운드 Feistel 암호에 대한 선형 공격
# =======================================

import BCF_lib as BCF
import my_lib2 as Common
import copy
import random

'''
# BCF Test
pt = [1, 2]
key = [5, 6, 7, 8]
ct = BCF.BCF_Enc(pt, key)
print(ct)
dec_pt = BCF.BCF_Dec(ct, key)
print(dec_pt)
'''

'''
# Known Plaintext attack===============
# 평문-암호문 쌍 만들기

num_ptct_pairs = 1 << 12
ptct_list = []
key = [1, 2, 3, 4]
# 공격자가 모르는 키

for i in range(num_ptct_pairs):
    pt = [random.randint(0, 255), random.randint(0, 255)]
    ct = BCF.BCF_Enc(pt, key)
    ptct_pair = copy.deepcopy([pt, ct])
    ptct_list.append(ptct_pair)

ptct_file = 'BCF_ptct_4096.var'
Common.save_var_to_file(ptct_list, ptct_file)
print('---- Cipher: BCF ----')
print('The number of pt-ct pairs: ', num_ptct_pairs)
print('File name: ', ptct_file)
'''

# ==================================================================
# 선형 공격
# pt = [PL, PR], ct = [CL, CR]
# 라운드 선형 특성: a x = b F(x) <===> a x = b S(X)
# 1 라운드 선형 특성: a (PL xor K1) = b (PR xor A)

# 3 라운드 출력: [L, R]
# 3 라운드 선형 특성: a (R xor K3) = b (L xor A)
# 1~3 라운드 선형 특성: a (PL xor R xor K1 xor K3) = b (PR xor L)
# L = CL, R = CR xor S(L xor K4)

# 선형 공격에 필요한 식:
#   a (PL xor CR xor S(CL xor K4)) xor b (PR xor CL) = a (K1 xor K2)
# K4 예측하기!!

# input_mask = 12 = a
# output_mask = 4 = b
# for all x, ax = bS(x) with prob = 1

ptct_file = 'BCF_ptct_4096.var'
ptct_list = Common.load_var_from_file(ptct_file)

# in_mask = 128
# out_mask = 4
in_mask = 64
out_mask = 68

score_list = [0] * 256

print("Run LC", end='')
for key4_guess in range(256):
    for j in range(len(ptct_list)):
        pt, ct = ptct_list[j][0], ptct_list[j][1]
        PL, PR, CL, CR = pt[0], pt[1], ct[0], ct[1]
        lhs = Common.hw_mod2(in_mask & (PL ^ CR ^ BCF.S[CL ^ key4_guess]))
        rhs = Common.hw_mod2(out_mask & (PR ^ CL))
        if lhs == rhs:
            score_list[key4_guess] += 1

    print('.', end='')

print("\n")
# print(score_list)

# ==== 정렬을 위한 기준
def MyOrder(x):
    return x[1]

mid_value = 2048
key_candid_list = [[i, abs(score_list[i] - mid_value)] for i in range(256)]
key_candid_list.sort(key=MyOrder, reverse=True)
print(key_candid_list[:10])

