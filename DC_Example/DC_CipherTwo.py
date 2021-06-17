import random

# Sbox 생성
S = [6, 4, 12, 5, 0, 7, 2, 14, 1, 15, 3, 13, 8, 10, 9, 11]
IS = [0] * len(S)
for i in range(0, len(S)):
    IS[S[i]] = i

# CipherTwo()
# m --> m^k0 = u --> S[u] --> v --> v ^ k1 = w --> S[w] --> x --> x ^ k2 = c
# dx = 15(0x0f) --> [S] --> dy = 13(0x0d) (10/16)
# <==> 차분특성: f --> [S] --> d (10/16)
def CipherTwo(m, k0, k1, k2):
    u = m ^ k0
    v = S[u]
    w = v ^ k1
    x = S[w]
    c = x ^ k2
    return c

# 공격 목표
k0 = random.randint(0, len(S)-1) # 끝점 포함
k1 = random.randint(0, len(S)-1)
k2 = random.randint(0, len(S)-1)

print("== 공격자가 찾아야할 암호키 == ")
print("key0 = %02x,  key1 = %02x, key2 = %02x" %(k0, k1, k2))

# =========================
# 평문-암호문 쌍
N = 1 << 8 # 평문 암호문 쌍의 개수

Tcount = [0] * len(S)

for i in range(0, N):
    m0 = random.randint(0, len(S)-1)
    dx = 0x0f
    m1 = m0 ^ dx
    # <==> 차분특성: f --> [S] --> d (10/16)
    c0 = CipherTwo(m0, k0, k1, k2)
    c1 = CipherTwo(m1, k0, k1, k2)
    # m --> m^k0 = u --> S[u] --> v --> v ^ k1 = w --> S[w] --> x --> x ^ k2 = c
    for key2_guess in range(0, len(S)):
        w0 = IS[c0 ^ key2_guess]
        w1 = IS[c1 ^ key2_guess]
        dw = w0 ^ w1
        if dw == 0x0d:
            # 0x0d가 나올 확률이 10/16
            Tcount[key2_guess] += 1

print('\nTcount = ', Tcount)
