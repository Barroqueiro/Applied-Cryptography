import hashlib
import random
import string

def hex_matcher(l):
    return {
        "0":0,
        "1":1,
        "2":2,
        "3":3,
        "4":4,
        "5":5,
        "6":6,
        "7":7,
        "8":8,
        "9":9,
        "a":10,
        "b":11,
        "c":12,
        "d":13,
        "e":14,
        "f":15
    }[l]

def get_offset_from_key(n,sk):
    if sk == []: return -1
    return (sum(sk) % n) +1

res = {}

for i in range(100000):
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))
    shuffle_key = str(ran)
    digest_shuffle_key = hashlib.md5(shuffle_key.encode()).hexdigest()
    shuffle_key_final = []
    for i in range(len(digest_shuffle_key)):
        shuffle_key_final.append(hex_matcher(digest_shuffle_key[i]))

    n = get_offset_from_key(14,shuffle_key_final)
    if n in res:
        res[n] += 1
    else:
        res[n] = 1

print(res)