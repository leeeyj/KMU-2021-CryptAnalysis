# ================
# 암호분석 2021
# ================

# S-box의 선형특성

S = [0, 1, 7, 2, 3, 4, 5, 6]

# Hamming Weight
# 1의 개수


def hw(n):
    count = sum([n & (1 << i) > 0 for i in range(32)])
    return count


def hw_mod2(n):
    return hw(n) % 2
    # 1의 개수 % 2


# == 선형 특성표 만들기
# LTable[in_mask a][out_mask b]: a x = b S[x]
LTable = []
for i in range(0, len(S)):
    LTable.append([0]*len(S))


# 입출력 마스크 in_mask a, out_mask b
for a in range(0, len(S)):
    for b in range(0, len(S)):
        for x in range(0, len(S)):
            y = S[x]
            if hw_mod2(a&x) == hw_mod2(b&y):
                # a&x 는 a에서 1인 부분만 계산하겠다는 뜻, b&y 또한 마찬가지
                # a&x의 hw 계산(1의 개수 알 수 있음) -> hw 가 홀수면 1, 짝수면 0 (xor 연산시)
                LTable[a][b] += 1
        LTable[a][b] -= 4


# - 출력
print('\n')
print('a/b ', end='')
for i in range(len(S)):
    print('%3d ' %(i), end='')
print('\n')
for a in range(len(S)):
    print('%3d ' % (a), end='')
    for b in range(len(S)):
        print('%3d ' %(LTable[a][b]), end='')
    print('\n')

# 최대 선형 확률
max_bias = 0
max_in, max_out = 0, 0
for a in range(1, len(S)):
    for b in range(0, len(S)):
        if abs(LTable[a][b]) >= max_bias:
            max_bias = abs(LTable[a][b])
            max_in, max_out = a, b

print('Max bias = %d (%02x ----> %02x)' %(LTable[max_in][max_out], max_in, max_out))
print("Max Linear probability = ", abs(max_bias)/len(S))
