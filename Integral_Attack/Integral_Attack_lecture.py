#-------------------------
# 암호분석 2021
#
#  4라운드 AES의 Integral Cryptanalysis
#
#-------------------------

import AES_EncDec_lib as AES
import my_lib2 as Common
import random 
import copy

#==== integral cryptanalysis 용 선택평문 만들기
def pt_256(col, row):
    s256 = []   # 256개의 평문 저장
    state = []  # 한개의 평문
    for i in range(4):
        new_col = [ random.randint(0,255) for j in range(4) ]
        state.append(new_col)
        
    for n in range(256):
        state[col][row] = n  # 0,1,2,...,255
        s256.append(copy.deepcopy(state))
    
    return s256

#---- Balanced check (256개의 XOR = 0)
def xor_256(byte_list):
    # byte_list = [b0, b1, ... , b255]
    xor_ed = 0
    for n in range(256):
        xor_ed ^= byte_list[n]
    return xor_ed
    
#--- Print round key
def print_rkey(key_state, round):
    rkey = AES.key_schedule_Enc(key_state)
    for r in range(0, round+1): # 0,1,2,...,round
        print('rk[%1d]=' %(r), end='')
        print(rkey[r])
   
'''    
#======================================
# 선택평문-암호문쌍 만들기       

key = [ 2*i for i in range(16)]    # 공격자가 찾아야 할 키
key_state = AES.block2state(key)

active_col, active_row = 0, 0
pt256 = pt_256(active_col, active_row) # 선택평문 만들기
num_ptct_pairs = 256
round = 4 # 4라운드 AES
ptct_list = []
for i in range(num_ptct_pairs):
    pt = pt256[i]
    ct = AES.AES_EncR(pt, key_state, round)
    ptct_pair = copy.deepcopy([pt, ct])
    ptct_list.append(ptct_pair)
    
ptct_file = 'AES4R_ptct.var'
Common.save_var_to_file(ptct_list, ptct_file)
print('--- Cipher: AES')
print('The number of pt-ct pairs:', num_ptct_pairs)
print('File name:', ptct_file)
'''
             
#======================================
# Integral cryptanalysis

ptct_file = 'AES4R_ptct.var'
ptct_list = Common.load_var_from_file(ptct_file)        

target_col, target_row = 2,2
key_candidate_list = []

for key_guess in range(256): # 한바이트 키 예측
    byte_r3_list = []    
    for n in range(256):  # 256개 평문-암호문
        ct = ptct_list[n][1] 
        byte1 = ct[target_col][target_row] ^ key_guess
        byte2 = AES.ISbox[byte1]
        byte_r3_list.append(byte2)
    
    if xor_256(byte_r3_list)==0:
        key_candidate_list.append(key_guess)

print('target = [%d][%d]' %(target_col, target_row))
print('Key Candidate(s):', key_candidate_list)    




'''
#=== 정답
key = [ 2*i for i in range(16)]    # 공격자가 찾아야 할 키
key_state = AES.block2state(key)
print_rkey(key_state,4)

target = [0][0]
Key Candidate(s): [65, 251]

rk[0]=[[0, 2, 4, 6], [8, 10, 12, 14], [16, 18, 20, 22], [24, 26, 28, 30]]
rk[1]=[[163, 158, 118, 171], [171, 148, 122, 165], [187, 134, 110, 179], [163, 156, 114, 173]]
rk[2]=[[127, 222, 227, 161], [212, 74, 153, 4], [111, 204, 247, 183], [204, 80, 133, 26]]
rk[3]=[[40, 73, 65, 234], [252, 3, 216, 238], [147, 207, 47, 89], [95, 159, 170, 67]]
rk[4]=[[251, 229, 91, 37], [7, 230, 131, 203], [148, 41, 172, 146], [203, 182, 6, 209]]
target = [1][2]
Key Candidate(s): [16, 104, 131, 135]

target = [2][2]
Key Candidate(s): [172]
'''

'''
#-----------------
chosen_pt = pt_256(1,0)    
print(chosen_pt[0])
print(chosen_pt[1])
print(chosen_pt[2])
print(chosen_pt[255])

xor_list = xor_256([ chosen_pt[n][1][1] for n in range(256) ])
print('XOR = ', xor_list)

key = [ i for i in range(16)]
key_state = AES.block2state(key)
round_key = AES.key_schedule_Enc(key_state)
print_rkey(key_state,10)
'''
