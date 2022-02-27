from Crypto.Cipher import AES
import os
import time
from string import ascii_letters

key, iv = os.urandom(32), os.urandom(16)
cipher = AES.new(key, AES.MODE_ECB, iv)
plaintext = input()
ciphertext = bytes()
start_time = time.time()
ciphertext += cipher.encrypt(plaintext)
final_time = (time.time() - start_time)
with open("times_enc_pycrypto_aes.txt","a") as f:
    f.write(str(final_time)+"\n")
start_time = time.time()
plaintext = cipher.decrypt(ciphertext)
final_time = (time.time() - start_time)
with open("times_dec_pycrypto_aes.txt","a") as f:
    f.write(str(final_time)+"\n")