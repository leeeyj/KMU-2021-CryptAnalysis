# =============
# subst cipher
# =============

import os
import sys

Alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def subst_encrypt(key, msg):
    result = ''
    InSet = Alphabet
    OutSet = key

    # 알파벳을 key에 대응하게 만들기
    # msg의 문자를 하나씩 읽어서 key 값으로 치환
    # 1. msg의 문자 index 찾기
    # 2. key[index]로 값을 치환
    for ch in msg:
        if ch.upper() in InSet:
            idx = InSet.find(ch.upper())
            if ch.isupper():
                result += OutSet[idx].upper()
            else:
                result += OutSet[idx].lower()
        else:
            result += ch
    return result


def subst_decrypt(key, cipher):
    result = ''
    InSet = key
    OutSet = Alphabet

    # key를 알파벳에 대응하게 만들기
    # cipher의 문자를 하나씩 읽어서 알파벳 값으로 치환
    # 1. cipher의 문자 index 찾기
    # 2. Alphabet[index]로 값을 치환
    for ch in cipher:
        if ch.upper() in InSet:
            idx = InSet.find(ch.upper())
            if ch.isupper():
                result += OutSet[idx].upper()
            else:
                result += OutSet[idx].lower()
        else:
            result += ch
    return result


def ReadFile(in_file_name):
    if not os.path.exists(in_file_name):
        print("File %s does not exist." % (in_file_name))
        sys.exit()

    inFileObj = open(in_file_name)
    file_content = inFileObj.read()
    inFileObj.close()

    return file_content


def WriteFile(out_file_name, msg):
    if os.path.exists(out_file_name):
        print('Overwrite %s? (Y)es or (N)o' % (out_file_name))
        response = input('===>')
        if not response.lower().startswith('y'):
            sys.exit()

    outFileObj = open(out_file_name, 'w')
    outFileObj.write(msg)
    outFileObj.close()

    return 0


def main():
    # msg = 'This is a simple message.'
    msg = ReadFile('my_text.txt')
    mykey = 'VWXABCDEIJKFGHLMQRSNOPTUYZ'

    cipher = subst_encrypt(mykey, msg)
    WriteFile('my_text_enc.txt', cipher)

    dec_cipher = subst_decrypt(mykey, cipher)
    print("PT = ", msg[:30])
    print("CT = ", cipher[:30])
    print("Decrypted Text = ", dec_cipher[:30])
    print("Key = ", mykey)

if __name__ == '__main__':
        main()