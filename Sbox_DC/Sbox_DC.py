# ======================
# 암호분석 2021
# ======================

# ======================
# Sbox 차분 분석
# ======================

import random


# S = [0, 1, 3, 2, 6, 7, 5, 4]  # Bad Table(Linear)
S = [0, 1, 7, 2, 3, 4, 5, 6]  # Good Table(nonlinear)
# S = [i for i in range(8)]
# random.shuffle(S)
# print(S)
# = 함수값 확인

# for X in range(len(S)):
#     print("S[%d] = %d" %(X, S[X]))

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
print('Max Differential Probability = ', max_count/len(S))

# Q: 과제
# 최대차분확률을 갖는 dx-->dy의 모든 경우를 다 얻으려면..?
# 힌트: 최대가 되는 경우를 list에 append 하기
