import hashlib

# Initialize all Linear Feedback Shift Registers 

LFSR1 = []
LFSR2 = []
LFSR3 = []

# Places within the LFSR's to xor to create the next bit

LFSR1_TAPS = [79,70]
LFSR2_TAPS = [58,39]
LFSR3_TAPS = [23,18]

# Constants from the size of each LFSR

LFSR1_SIZE = 79
LFSR2_SIZE = 58
LFSR3_SIZE = 23
DEBUG = 0

# Clear all LFSR's before re-initializing the generator

def clear_lfsr():
    global LFSR1,LFSR2,LFSR3
    LFSR1 = []
    LFSR2 = []
    LFSR3 = []

# XOR 2 binary numbers

def xor_binary(a,b):
    return a ^ b

# XOR 2 lists number by number, returns a lit with the length of the first

def xor_list(a,b):
    return [a[i] ^ b[i] for i in range(len(a))]

# Shift a list by one, usefull for retreiving one item from the end of the LFSR and inputing n

def shift(l,n):
    l[:] = [n] + l[:-1]

"""
    Next function: Returns one bit

    Walkthrough:
        - The return values will be the xor function between all the last bits of the 3 LFSR's
        - Calculate the next bit to input in all of the LFSR's
        - If the number created by each LFSR is equal to the majority then the LFSR shifts, if not, it stays the same
"""
        
def next():
    ret = xor_binary(LFSR1[-1],xor_binary(LFSR2[-1],LFSR3[-1]))

    xord1 = xor_binary(LFSR1[LFSR1_TAPS[0]-1],LFSR1[LFSR1_TAPS[1]-1])

    xord2 = xor_binary(LFSR2[LFSR2_TAPS[0]-1],LFSR2[LFSR2_TAPS[1]-1])

    xord3 = xor_binary(LFSR3[LFSR3_TAPS[0]-1],LFSR3[LFSR3_TAPS[1]-1])

    majority = 0 if sum([xord1,xord2,xord3]) < 2 else 1

    if xord1 == majority:
        shift(LFSR1,xord1)
    if xord2 == majority:
        shift(LFSR2,xord2)
    if xord3 == majority:
        shift(LFSR3,xord3)

    return ret

# Simple function using next() to create an int from 0-255

def nextByte():
    return next() * 2**7 + next() * 2**6 + next() * 2**5 + next() * 2**4 + next() * 2**3 + next() * 2**2 \
        + next() * 2**1 + next()

"""
    hmac_sha1 function: Implemnetation following the specifications of hmac_sha1

    Walkthrough:
        - Creation of the ipad and opad
        - Hashing the confusion string passed by the user 
        - Padding of the password to make 64 characters
        - Xor the password with both ipad and opad
        - Hash the ikeypad plus the confusion string(hashed)
        - Hash the opad with the hash done in the previous step to finalize the hmac_sha1
"""

def hmac_sha1(password,salt):
    ipad = [0x36] * 64
    opad = [0x5C] * 64
    password = [ord(a) for a in password]
    salt = list(hashlib.sha1(salt.encode()).digest())
    while len(password) < 64:
        password += [0]

    ikeypad = xor_list(ipad,password)
    okeypad = xor_list(opad,password)

    first_pass = ikeypad + salt
    first_pass = hashlib.sha1(bytes(first_pass))
    dig_first_pass = list(first_pass.digest())
    second_pass = okeypad + dig_first_pass
    second_pass = hashlib.sha1(bytes(second_pass))
    dig_second_pass = list(second_pass.digest())
    return dig_second_pass

"""
    Seed function: Creation of a seed from the password, confusion string and the iteration count, based on the PBKDF2
    key derivation function

    Walkthrough:
        - hmac_sha1 the password and the confusion string
        - Xor the seed with the hmac_sha1 between the password and the last seed created
        - Repeat for the number on iterations
"""

def seed(password,salt,c):
    seed = hmac_sha1(password,salt)
    for i in range(c):
        seed = xor_list(seed,hmac_sha1(password,''.join([chr(s) for s in seed])))
    return seed

"""
    Initiation function: Responsible for updating the values of the LFSR's given by a 20 byte key (160 bits)

    Walkthrough:
        - Transformation of the key in a string with 0's and 1's from the bytes passed (Padding done to ensure 
            160 bits at the end)
        - For each LFSR add bits by order with the respective length adn sequencial order (LFSR1 -> LFSR2 -> LFSR3)
"""

def initiate(key):
    clear_lfsr()
    key_str = ''
    for i in key:
        key_str += bin(i)[2:].zfill(8)

    for bit in key_str[:LFSR1_SIZE]:
        LFSR1.append(int(bit))

    for bit in key_str[LFSR1_SIZE:LFSR1_SIZE+LFSR2_SIZE]:
        LFSR2.append(int(bit))

    for bit in key_str[LFSR1_SIZE+LFSR2_SIZE:]:
        LFSR3.append(int(bit))

    if(DEBUG):
        print("LFSR1 with length {len} -> {lfsr}".format(len=len(LFSR1),lfsr=LFSR1))
        print("LFSR2 with length {len} -> {lfsr}".format(len=len(LFSR2),lfsr=LFSR2))
        print("LFSR3 with length {len} -> {lfsr}".format(len=len(LFSR3),lfsr=LFSR3))

"""
    Start function: Initialize the generator using a password, a confusions string and a ietration number

    Walkthrough:
        - Initiate the generator with a seed from the 3 parameters
        - Hash the confusion string and take as many bytes form the begining as it's length (This will be the confusion
            pattern)
        - For the number of iterations look for that pattern and when it is reached re-seed the generator using the 
            next 160 bits produced after the pattern
        - The generator is now read to output random bits/bytes
"""

def start(password,cs,iter):
    initiate(seed(password,cs,iter))
    cp = list(hashlib.sha1(cs.encode()).digest())[:len(cs)]
    count = 0
    temp = [nextByte() for i in range(len(cs))]
    for i in range(iter):
        count = 0
        new_seed = []
        while(1):
            count += 1
            if cp == temp:
                count = 0
                break
            b = nextByte()
            shift(temp,b)
        for i in range(20):
            new_seed.append(nextByte())
        initiate(new_seed)
        temp = [nextByte() for i in range(len(cs))]
    return True