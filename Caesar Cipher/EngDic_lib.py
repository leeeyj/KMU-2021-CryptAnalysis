'''
===========================
English Dictionary Library
===========================
'''

UpAlphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

letters_and_space = UpAlphabet + UpAlphabet.lower() + " " + "\t\n"
# 대문자 소문자 화이트 스페이스 포함 = letters_and_space

#------------------------------------------------------------------------

def LoadDictionary():
    dicFileObj = open('dictionary.txt')
    EnglishDic = {}

    # 사전 읽고 split => dictionary 타입으로 저장
    for word in dicFileObj.read().upper().split("\n"):
        EnglishDic[word] = None
    dicFileObj.close()
    print("English Dictionary Loaded... (%d word)" %(len(EnglishDic)))
    return EnglishDic

#------------------------------------------------------------------------

English_Dictionary = LoadDictionary() # 전역변수

#------------------------------------------------------------------------

# 문자가 아닌 것들을 지우는 함수
def RemoveNonLetters(message):
    letters_only = []
    for ch in message:
        # 문자 하나씩 판단
        if ch in letters_and_space:
            letters_only.append(ch)
    return ''.join(letters_only)

#------------------------------------------------------------------------

# 영어단어가 올바른 것이 몇 퍼센트인지 구하는 함수(바른 단어 수 / 전체 단어 수)
def percentEnglishWords(message):
    message = message.upper()
    message = RemoveNonLetters(message)
    word_list = message.split()

    if not word_list:
        return 0.0

    count_words = 0

    for word in word_list:
        if word in English_Dictionary:
            count_words += 1

    return float(count_words) / len(word_list)

#------------------------------------------------------------------------

# 문자열이 영어인지 판단하기
# 사전에 들어 있는 단어 20% 정도, 전체 문자의 80% 영문자이다를 의미
def IsEnglish(message, wordPercent = 20, letterPercent = 80):

    wordMatch = percentEnglishWords(message) * 100 >= wordPercent
    # 단어가 20% 보다 크면 단어 매칭 성공

    numLetters = len(RemoveNonLetters(message))
    MsgLetterPercent = float(numLetters) / len(message)
    # message 중 문자의 비율 구하기
    letterMatch = MsgLetterPercent * 100 >= letterPercent

    return wordMatch and letterMatch


#------------------------------------------------------------------------
def main():
    message = "This is a plain message!!!"
    print(percentEnglishWords(message))
    print(IsEnglish(message))

if __name__ == '__main__':
    main()