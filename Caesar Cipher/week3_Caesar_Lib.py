'''
20192243 이용진
Cryptanalysis Week3-Caesar Cipher Library
'''

# --시저 암호화 함수
def encrypt(msg, key):
    upAlphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lowerAlphabet = "abcdefghijklmnopqrstuvwxyz"
    ciphertext_msg = ''

    for ch in msg:
        if ch in upAlphabet:
            idx = upAlphabet.find(ch)
            new_idx = (idx + key) % 26
            cipher_ch = upAlphabet[new_idx]
            ciphertext_msg += cipher_ch

        elif ch in lowerAlphabet:
            idx = lowerAlphabet.find(ch)
            new_idx = (idx + key) % 26
            cipher_ch = lowerAlphabet[new_idx]
            ciphertext_msg += cipher_ch

        else:
            ciphertext_msg += ch

    return ciphertext_msg


# --시저 복호화 함수
def decrypt(msg, key):
    upAlphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lowerAlphabet = "abcdefghijklmnopqrstuvwxyz"
    recovered_msg = ''

    for ch in msg:
        if ch in upAlphabet:
            idx = upAlphabet.find(ch)
            new_idx = (idx - key) % 26
            recover_ch = upAlphabet[new_idx]
            recovered_msg += recover_ch

        elif ch in lowerAlphabet:
            idx = lowerAlphabet.find(ch)
            new_idx = (idx - key) % 26
            recover_ch = lowerAlphabet[new_idx]
            recovered_msg += recover_ch

        else:
            recovered_msg += ch

    return recovered_msg

#==================================
def main():
    msg = "This is a mesaage"
    key = 3
    cipher_msg = encrypt(msg, key)

    print("Plaintext = ", msg)
    print("Ciphertext = ", cipher_msg)

    recovered = decrypt(cipher_msg, key)
    print("Recovered text = ", recovered)

#==================================

if __name__ == '__main__':
    main()

#==================================
# 이 라이브러리가 실행 파일이 되면 main 함수를 실행해라 라는 뜻