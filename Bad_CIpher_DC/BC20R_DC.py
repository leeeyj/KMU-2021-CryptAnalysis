# ====================
# 암호분석 2021
# ====================

import random
import BC20R_lib as BC20R
import copy
import my_lib as Common

# =======================
# BSbox의 차분 특성 확인
# 64(입력차분) --> BS --> 64(출력 차분) p = 0.52
'''
dx = 64
num_iteration = 100
count = 0
for i in range(num_iteration):
    P1 = random.randint(0, 255)
    P2 = P1 ^ dx
    C1 = BC20R.BSbox[P1]
    C2 = BC20R.BSbox[P2]
    dy = C1 ^ C2
    if dy == 64:
        count += 1

print("%d ---> %d (probability = %5.2f)" %(dx, dy, count/num_iteration))
'''

'''
# ========================
# BS의 1라운드 차분 특성 확인
# [64, 0, 0, 0] -----> BS -----> [0, 64, 64, 64]

key = [1, 2, 3, 4]
# 공격자가 찾아야 하는 키
diff_dic = {}

dx = 64
num_iteration = 100
count = 0
for i in range(num_iteration):
    P1 = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    P2 = [P1[0] ^ dx, P1[1], P1[2], P1[3]]
    C1 = BC20R.BC20R_Enc(P1, key, 1)
    C2 = BC20R.BC20R_Enc(P2, key, 1)
    dy = [C1[0] ^ C2[0], C1[1] ^ C2[1], C1[1] ^ C2[1], C1[1] ^ C2[1]]
    dy_int = Common.list2int(dy) # 출력 차분 정수로 변환
    if dy_int in diff_dic:
        diff_dic[dy_int].append(P1)
    else:
        diff_dic[dy_int] = [P1]
    expected_dy = [0, 64, 64, 64]
    expected_int = Common.list2int(expected_dy)
    if expected_int == dy_int:
        count += 1

print('probability = ', count/num_iteration)
print(len(diff_dic[expected_int]))
'''

'''
# ========================
# BS의 3라운드 차분 특성 확인
# [64, 0, 0, 0] -----> 1R -----> [0, 64, 64, 64] 확률 p = 0.52
# [0, 64, 64, 64] -----> 2R -----> [64, 0, 0, 0] 확률 p = (0.52) ^ 3
# [64, 0, 0, 0] -----> 3R -----> [0, 64, 64, 64] 확률 p = 0.52
# [64, 0, 0, 0] -----> 1R-3R -----> [0, 64, 64, 64] 확률 p = (0.52) ^ 5

key = [1, 2, 3, 4]
# 공격자가 찾아야 하는 키
diff_dic = {}

dx = 64
num_iteration = 100
count = 0
for i in range(num_iteration):
    P1 = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    P2 = [P1[0] ^ dx, P1[1], P1[2], P1[3]]
    C1 = BC20R.BC20R_Enc(P1, key, 3)
    C2 = BC20R.BC20R_Enc(P2, key, 3)
    dy = [C1[0] ^ C2[0], C1[1] ^ C2[1], C1[1] ^ C2[1], C1[1] ^ C2[1]]
    dy_int = Common.list2int(dy) # 출력 차분 정수로 변환
    if dy_int in diff_dic:
        diff_dic[dy_int].append(P1)
    else:
        diff_dic[dy_int] = [P1]
    expected_dy = [0, 64, 64, 64]
    expected_int = Common.list2int(expected_dy)
    if expected_int == dy_int:
        count += 1

print('probability = ', count/num_iteration)
print(len(diff_dic[expected_int]))
'''


# ========================
# 평문 암호문 쌍 만들기
dx = 64
num_ptct_pairs = 1 << 16
num_round = 4
ptct_list = []

key = [1, 2, 3, 4]

for i in range(num_ptct_pairs):
    P1 = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    P2 = [P1[0] ^ dx, P1[1], P1[2], P1[3]]
    C1 = BC20R.BC20R_Enc(P1, key, num_round)
    C2 = BC20R.BC20R_Enc(P2, key, num_round)

    ptct_pairs = copy.deepcopy([P1, P2, C1, C2])
    ptct_list.append(ptct_pairs)
    # ptct_list = [[P1, P2, C1, C2], [P1, P2, C1, C2] ....]

ptct_file = '4R_ptct.var'
Common.save_var_to_file(ptct_list, ptct_file)

# ========================
# 4R 차분 공격: 3R 차분 특성을 이용한 4R 공격법
# 공격자는 수집된 평문 암호문 쌍으로 공격을 진행한다.
# 4 번째 라운드(마지막 라운드) -> AR -> BS -> LM -> AR(Whitening key) -> C
# 마지막 라운드 동치 변환      -> AR -> BS -> AR(LM(Whitening key)) -> LM -> C
ptct_file = '4R_ptct.var'
ptct_list = Common.load_var_from_file(ptct_file)

dx = 64
num_round = 4
rkey_dic = {}
byte_pos = 2
for i in range(len(ptct_list)):
    C1 = copy.deepcopy(ptct_list[i][2])
    C2 = copy.deepcopy(ptct_list[i][3])
    state1 = BC20R.LM_Layer(C1)
    state2 = BC20R.LM_Layer(C2)
    for rk in range(0, 256):
        # 4R 라운드 키 한 바이트 예측
        byte1 = BC20R.IBSbox[state1[byte_pos] ^ rk]
        byte2 = BC20R.IBSbox[state2[byte_pos] ^ rk]
        delta = byte1 ^ byte2
        if delta == dx:
            if rk in rkey_dic:
                rkey_dic[rk] += 1
            else:
                rkey_dic[rk] = 1

max_count = 0
max_rk = 0
for rk in rkey_dic:
    if rkey_dic[rk] > max_count:
        max_count = rkey_dic[rk]
        max_rk = rk

print('max count = ', max_count)
print('max rk = ', max_rk)
# max rk(1-byte) = LM(Whitening key)[byte_pos]
# => LM[1, 2, 3, 4] = [?, 6, 7, 0]
# 1 ^ 3 ^ 4 = 6
# 1 ^ 2 ^ 4 = 7
# 1 ^ 2 ^ 3 = 0
