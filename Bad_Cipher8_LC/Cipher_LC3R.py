# =======================
# 암호분석 2021
# =======================

import CipherBC8_lib as CB8
import my_lib2 as Common
import random
import copy

'''
# =======================
# 평문 암호문 쌍 만들기

num_ptct_pairs = 1 << 8
cipher_round = 3
#라운드 수

ptct_list = []
key = [i for i in range(cipher_round+1)]
# key = [0, 1, 2, 3]
# print(key)
for i in range(num_ptct_pairs):
    pt = i
    ct = CB8.CipherBC8R_Enc(pt, key, cipher_round)
    ptct_pairs = copy.deepcopy([pt, ct])
    ptct_list.append(ptct_pairs)

ptct_file = '3R_ptct_CipherBC8_256.var'
Common.save_var_to_file(ptct_list, ptct_file)
print('-- CipherBC8R ', cipher_round, 'round version')
print(' The num. of pt-ct pairs: ', num_ptct_pairs)
print(' Saved to file: ', ptct_file)

'''
# =============================
# 선형 공격
# -- 3라운드 암호화: m --> m xor k0 --> S --> xor k1 --> S --> xor k2 -(y)-> S --> xor k3(guessing key) --> c
# Max bias = 128 (128 --> 4) => Max count = 256
# Max linear probability = 1
# Max bias = -20 (4 --> 45) => Max count = 108
# Max linear probability =  0.578125
# (in_mask 내적 m) xor (out_mask 내적 IS(c xor key_guess)) = (128 내적 k0) xor (4 내적 k1) xor (4 내적 k2)
# 올바른 키 추정의 경우

ptct_file = '3R_ptct_CipherBC8_256.var'
ptct_list = Common.load_var_from_file(ptct_file)
in_mask = 128
out_mask = 45

score_list = [0] * 256 # 공격 대상 암호키 guessing --> 선형식을 만족하는 개수
for key_guess in range(256):
    for i in range(len(ptct_list)):
        pt, ct = ptct_list[i][0], ptct_list[i][1]
        y = CB8.IS[ct ^ key_guess]
        if Common.hw_mod2(in_mask & pt) == Common.hw_mod2(out_mask & y):
            score_list[key_guess] += 1
print(score_list)

def MyOrder(x):
    return x[1]

key_candid_list = [[i, abs(score_list[i] - 128)] for i in range(256)]
# 가운데에서 가장 멀리 떨어진 값이 키 후보
key_candid_list.sort(key=MyOrder, reverse=True)

print(key_candid_list[:10])

