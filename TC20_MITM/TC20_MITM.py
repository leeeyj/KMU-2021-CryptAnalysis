# ----------------------------
# 2021 암호분석
# Meet in the middle attack
# ----------------------------

import TC20_lib as TC20
import pickle

# =======================
# 평문, 암호문 2쌍 준비
#
# PT -> E(key1) -> M -> E(key2) -> CT
# =======================
'''
PT1 = list(ord(ch) for ch in "SEED")
PT2 = list(ord(ch) for ch in "ARIA")
print("PT1 = ", PT1)
print("PT2 = ", PT2)

key1 = [0, 1, 2, 3]
key2 = [0, 10, 20, 30]

M1 = TC20.TC20_Enc(PT1, key1)
CT1 = TC20.TC20_Enc(M1, key2)
M2 = TC20.TC20_Enc(PT2, key1)
CT2 = TC20.TC20_Enc(M2, key2)

print("CT1 = ", CT1)
print("CT2 = ", CT2)
'''


# ====================================
# Meet in the middle attack
# 주어진 (PT1, CT1), (PT2, CT2)로부터
# 키 key1, key2 찾기
# ====================================

# 정수를 16진수 리스트로
def int2list(n):
    out_list = []
    out_list.append((n >> 24) & 0xff)
    out_list.append((n >> 16) & 0xff)
    out_list.append((n >> 8) & 0xff)
    out_list.append(n & 0xff)

    return out_list


# 16진수 리스트를 16진수 하나로
def list2int(l):
    n = 0
    num_bytes = len(l)
    for idx in range(len(l)):
        n += l[idx] << 8 * (num_bytes - idx - 1)

    return n


# --- 변수를 파일에 저장하기
def save_var_to_file(var, filename):
    f = open(filename, 'w+b')
    pickle.dump(var, f)
    f.close()


# --- 파일에서 변수를 가져오기
def load_var_from_file(filename):
    f = open(filename, 'rb')
    var = pickle.load(f)
    f.close()
    return var


# --------------------------------
# (1) 사전 만들기 M1 = E(PT1, k1)
# dic = { M: [k1_1, k1_2, ......]
# --------------------------------

def make_enc_dic(pt):
    dic = {}
    print('Making Encrpytion Drictionary', end='')
    N = 1 << 24  # 24비트 키
    for idx in range(0, N):
        key1_guess = int2list(idx)
        mid = TC20.TC20_Enc(pt, key1_guess)
        int_mid = list2int(mid)
        # int_key_guess = list2int(key1_guess) = idx

        if int_mid in dic:
            # idx = key 정수 value
            # 전에 나온적이 있는 mid 값 인가?
            dic[int_mid].append(idx)
        else:
            dic[int_mid] = [idx]

        if idx % (1 << 18) == 0:
            print('.', end='')

    print('Done!!')
    return dic


# -------------------------------------------------------------------
# 주어진 키 key1 후보 리스트 중에서 올바른 키가 있는지 찾는다.
# key1 후보들 중에서 PT2를 암호화하여 주어진 key2에 대한 CT2를 만든 것을 찾는다.
# CT2 <- E(M, key2) <- M <- E(PT2, key1) <- PT2
def verify_key1_candidate(key1_list, key2, PT2, CT2):
    flag = False
    for key1_guess in key1_list:
        key1_state = int2list(key1_guess)
        mid2 = TC20.TC20_Enc(PT2, key1_state)
        CT2_guess = TC20.TC20_Enc(mid2, key2)
        if CT2_guess == CT2:
            print("\nkey1 = ", key1_state, " key2 = ", key2)
            flag = True
    # return flag


PT1 = [83, 69, 69, 68]
PT2 = [65, 82, 73, 65]
CT1 = [98, 127, 56, 252]
CT2 = [151, 9, 130, 177]
# -------------------------------------------------------------------
# 사전 만들기
# mid_dic = make_enc_dic(PT1)

# 사전을 파일로 저장하기
# save_var_to_file(mid_dic, 'TC20MidDic.p')
# print('Dic Saved!')
# 파일에서 사전을 불러오기
mid_dic = load_var_from_file('TC20MidDic.p')
print("Dic Loaded")

# -------------------------------------------------------------------
# CT -> Dec(key2) -> M == M'
N = 1 << 24
for idx in range(0, N):
    key2_guess = int2list(idx)
    mid1 = TC20.TC20_Dec(CT1, key2_guess)
    int_mid1 = list2int(mid1)
    if int_mid1 in mid_dic:
        list_key1_candidate = mid_dic[int_mid1]
        if len(list_key1_candidate) > 0:
            # PT2, CT2 를 만족하는 key 후보 찾기
            verify_key1_candidate(list_key1_candidate, key2_guess, PT2, CT2)
    if idx % (1 << 18) == 0:
        print('.', end='')

print("\nKey Search completed !!!")
