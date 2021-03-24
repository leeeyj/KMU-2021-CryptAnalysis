'''
20192243 이용진
Cryptanalysis week3
Caesar Cipher Usage
'''

import week3_Caesar_Lib as caesar
import os
import sys
import EngDic_lib as EngDic

# Read Caesar Cipher...
cipher_file_name = 'my_cipher.txt'
if not os.path.exists(cipher_file_name):
    print("File %s does not exist." %(cipher_file_name))
    sys.exit()

inFileObj = open(cipher_file_name)
cipher_msg = inFileObj.read()
inFileObj.close()

# Exhaustive key search (Brute force attack)
final_key = -1
for key in range (0, 26):
    current_txt = caesar.decrypt(cipher_msg, key)
    curr_word_percent = EngDic.percentEnglishWords(current_txt) * 100
    print('key = %2d: %s (English %5.2f %%)\n' %(key, current_txt[0:20], curr_word_percent))

    if EngDic.IsEnglish(current_txt):
        final_key = key

if final_key >= 0:
    print("key = ", final_key)

