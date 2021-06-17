# ===========================
# 치환 암호 알파벳 빈도 분석 공격
# ===========================

import substcipher_lib as substcipher

ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ' # 빈도 순서 (이미 알려진 영문 특성)
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


# -----------------
# 알파벳 빈도를 카운트
def getLetterCount(message):
    # dictionary {key: value
    letterCount = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0,
                   'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0,
                   'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0,
                   'Y': 0, 'Z': 0}

    for ch in message.upper():
        if ch in LETTERS:
            letterCount[ch] += 1

    return letterCount


# --------------------------
# 정렬(sort)를 위한 함수 정의
def getItemZero(items):
    return items[0]
    # items[0] = (28, 'A') -> return 28
    # items[0] 를 기준으로 정렬
    # ex) (28, 'A'), (36, 'B") 라면
    # items[0] = 28 or 36 ....
    # items[0]를 기준으로 정렬


# --------------------------
# 알파벳 출현 빈도 순서대로 쓰기
def getFreqOrder(message):
    # msg의 빈도수 측정
    letter2freq = getLetterCount(message)

    # 알파벳: 빈도수 -> 빈도수: 알파벳
    freq2letter = {}
    for ch in LETTERS:
        if letter2freq[ch] not in freq2letter:
            freq2letter[letter2freq[ch]] = [ch]
            # { 빈도수: [알파벳] }
        else:
            freq2letter[letter2freq[ch]].append(ch)
            # 빈도수가 같은 경우
            # { 빈도수: [알파벳].append(ch) }

    # 빈도수가 많은 순서로 sort
    for freq in freq2letter:
        freq2letter[freq].sort(key=ETAOIN.find, reverse=False)
        # 작은 순서로
        # freq2letter의 key에 해당하는 값(list)를 sort(정렬) => 리스트 값을 정렬
        # sort는 ETAOIN.find 함수를 기준으로 함
        # ex) ETAOIN.find('A') = 2 (ETAOIN 에서의 A의 index 값)
        # 만약 freq2letter[freq] = ['B', 'A'] 를
        # ETAOIN.find, reverse = Flase(작은 순서로) 정렬하면
        # ETAOIN.find('A') = 2, ETAOIN.find('B') = 19 임으로
        # freq2letter[freq] = ['A', 'B'] 로 바뀜 (작은 순서로 정렬했기 때문)

        freq2letter[freq] = ''.join(freq2letter[freq])
        # ex) { 빈도수: 'AB' } -> 리스트를 문자열로 변경

    freqPairs = list(freq2letter.items())
    # print("FreqPairs = ", freqPairs)
    # [(28, 'A'), (78, 'B'), (15, 'CG'), ...]

    # 빈도수 값을 큰 순서로 정렬
    # 큰 순서로
    freqPairs.sort(key=getItemZero, reverse=True)

    # 가장 많이 나온 알파벳을 freqOrder 리스트에 append
    freqOrder = []
    for freq_pair in freqPairs:
        # freq_pair = (28, 'A') ...
        # freq_pair[1] = 'A'
        freqOrder.append(freq_pair[1])

    return ''.join(freqOrder)


# freq_order = BNRVSILHEXMYADFCGOTKUPWJQZ
# ETAOIN = ETAOINSHRDLCUMWFGYPBVKJXQZ 비교 => 빈도순서 (영문 특성)
# -----------------------------
# 빈도순서를 이용하여 암호키 예측하기
def Freq2Key(freq_order):
    temp_dict = {}
    i = 0
    for ch in freq_order:
        temp_dict[ETAOIN[i]] = ch
        # ex) { 'E': 'B', 'T': 'N', ....}

        i += 1
    temp_list = list(temp_dict.items())
    # ex) [ ('E', 'B'), ('T', 'N'), .....]

    temp_list.sort(key=getItemZero, reverse=False)
    # 알파벳 순서 == 작은 순서
    # [ ('A': 'R'), ('B': 'K') ......]

    temp_key_list = []
    for item in temp_list:
        temp_key_list.append(item[1])

    return ''.join(temp_key_list)

in_file = 'my_text_enc.txt'
msg = substcipher.ReadFile(in_file)
freq_order = getFreqOrder(msg)
key_guess = Freq2Key(freq_order)
print("Guess key = ", key_guess)

# freq_order = BNRVSILHEXMYADFCGOTKUPWJQZ
# ETAOIN =     ETAOINSHRDLCUMWFGYPBVKJXQZ
# key_guess =  RKYXBCGHSWPMDIVTQELNAUFJOZ
# LETTERS =    ABCDEFGHIJKLMNOPQRSTUVWXYZ
# my_key =     VWXABCDEIJKFGHLMQRSNOPTUYZ
out_file = 'freq_my_text_dec.txt'
freq_decrypt = substcipher.subst_decrypt(key_guess, msg)
substcipher.WriteFile(out_file, freq_decrypt)


'''
Dictionary
{'A': 57, 'B': 3, 'C': 39, 'D': 28, 'E': 78, 'F': 15, 'G': 25, 'H': 42, 
'I': 51, 'J': 1, 'K': 6, 'L': 24, 'M': 15, 'N': 45, 'O': 50, 'P': 34, 
'Q': 1, 'R': 61, 'S': 55, 'T': 73, 'U': 13, 'V': 4, 'W': 12, 'X': 4, 
'Y': 31, 'Z': 0}

{'A': 28, 'B': 78, 'C': 15, 'D': 25, 'E': 42, 'F': 24, 'G': 15, 'H': 45, 
'I': 51, 'J': 1, 'K': 6, 'L': 50, 'M': 34, 'N': 73, 'O': 13, 'P': 4, 
'Q': 1, 'R': 61, 'S': 55, 'T': 12, 'U': 4, 'V': 57, 'W': 3, 'X': 39, 
'Y': 31, 'Z': 0}
'''