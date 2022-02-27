import os
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
key = os.urandom(32)
cipher = Cipher(algorithms.AES(key), modes.ECB())
encryptor = cipher.encryptor()
l = input()
ct = bytes()
start_time = time.time()
for i in range(0,len(l),16):
    ct += encryptor.update(bytes(l[i:i+16],"ascii"))
ct += encryptor.finalize()
final_time = (time.time() - start_time)
with open("times_enc_cryptography_aes.txt","a") as f:
    f.write(str(final_time)+"\n")
pt = bytes()
decryptor = cipher.decryptor()
start_time = time.time()
for i in range(0,len(ct),16):
    pt += decryptor.update(ct[i:i+16])
pt += decryptor.finalize()
final_time = (time.time() - start_time)
with open("times_dec_cryptography_aes.txt","a") as f:
    f.write(str(final_time)+"\n")