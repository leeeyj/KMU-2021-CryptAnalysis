# ===================
# 암호분석2021
# ===================

# CipherOne
#   from the block cipher companion

import random

# Sbox 생성
S = [6, 4, 12, 5, 0, 7, 2, 14, 1, 15, 3, 13, 8, 10, 9, 11]
IS = [0] * len(S)
for i in range(0, len(S)):
    IS[S[i]] = i

# Sbox 확인
print("S = [", end='')
for x in range(0, len(S)):
    print("% 02x" %(S[x]), end='')
print(']')
print("IS = [", end='')
for x in range(0, len(S)):
    print("% 02x" %(IS[x]), end='')
print(']')

# CipherOne()
def CipherOne(m, k0, k1):
    u = m ^ k0
    v = S[u]
    c = v ^ k1
    return c
'''
# = 차분 특성표 만들기

DTable = []
for i in range(len(S)):
    # DTable.append([0 for j in range(len(S))])
    DTable.append(([0]*len(S)))

# - 입출력 차분 카운트하기
# - 입력 차분 X1 ^ X2 = 0,1,2,.....,7

for X1 in range(len(S)):
    y1 = S[X1]
    for dx in range(len(S)):
        # dx는 입력 차분: X1 ^ X2 = dx <==> X2 = X1 ^ dx
        X2 = X1 ^ dx
        y2 = S[X2]
        # dy는 출력 차분
        dy = y1 ^ y2
        DTable[dx][dy] += 1

# - 출력
print('\n')
print('입/출', end='')
for i in range(len(S)):
    print('%3d ' %(i), end='')
print('\n')
for dx in range(len(S)):
    print('%3d ' % (dx), end='')
    for dy in range(len(S)):
        print('%3d ' %(DTable[dx][dy]), end='')
    print('\n')

# - 최대 차분 확률 max probability of (dx ---> dy)
max_count = 0
max_dx, max_dy = 0, 0
for dx in range(1, len(S)):
    for dy in range(len(S)):
        if DTable[dx][dy] > max_count:
            max_count = DTable[dx][dy]
            max_dx, max_dy = dx, dy

print('Max count = %d(%d-->%d)' %(max_count, max_dx, max_dy))
print('Max count = %d(%02x-->%02x)' %(max_count, max_dx, max_dy))
print('Max Differential Probability = ', max_count/len(S)) 
'''

# 공격 목표
k0 = random.randint(0, len(S)-1) # 끝점 포함
k1 = random.randint(0, len(S)-1)
print("== 공격자가 찾아야할 암호키 == ")
print("key0 = %02x,  key1 = %02x" %(k0, k1))

# =========================
# 평문-암호문 쌍
m0 = random.randint(0, len(S)-1)
dx = random.randint(1, len(S))
m1 = m0 ^ dx

c0 = CipherOne(m0, k0, k1)
c1 = CipherOne(m1, k0, k1)

# ===========================
# 공격자는 (m0, c0) (m1, c1) 평문 암호문 쌍을 가진다.
# m ---> u = m ^ key1 ---> [S] ---> v ---> v ^ key1= c
k1_candidate = []
for key1_guess in range(0, len(S)):
    v0 = c0 ^ key1_guess
    v1 = c1 ^ key1_guess
    u0 = IS[v0]
    u1 = IS[v1]
    du = u0 ^ u1
    if du == dx:
        k1_candidate.append(key1_guess)

print('\n')
print('m0 = %02x, m1 = %02x, dx = %02x' %(m0, m1, dx))
print('c0 = %02x, c1 = %02x' %(c0, c1))
print('key1 candidate = ', k1_candidate)

# 2번째 평문 암호문 쌍 생성
m0 = random.randint(0, len(S)-1)
dx = random.randint(1, len(S))
m1 = m0 ^ dx

c0 = CipherOne(m0, k0, k1)
c1 = CipherOne(m1, k0, k1)

# 2차 key1 추측
k1_candidate = []
for key1_guess in range(0, len(S)):
    v0 = c0 ^ key1_guess
    v1 = c1 ^ key1_guess
    u0 = IS[v0]
    u1 = IS[v1]
    du = u0 ^ u1
    if du == dx:
        k1_candidate.append(key1_guess)

print('\n')
print('m0 = %02x, m1 = %02x, dx = %02x' %(m0, m1, dx))
print('c0 = %02x, c1 = %02x' %(c0, c1))
print('key1 candidate = ', k1_candidate)
