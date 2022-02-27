import rsa
import argparse
from pseudogen import *

# Argument parser to retreive all parameters for random number generator, size of the key and prefix of file to 
# store the keys

parser = argparse.ArgumentParser()
parser.add_argument('-p', type=str, required=True)
parser.add_argument('-c', type=str, required=True)
parser.add_argument('-i', type=int, required=True)
parser.add_argument('-s', type=int, required=True)
parser.add_argument('-f', type=str, required=True)
args = parser.parse_args()

# Start pseudo-random number generator with password, confusion string and iteratio count

start(args.p,args.c,args.i)

"""
    Write to PEM function: Designed to write the key pair in 2 files.

    Walkthrough:
        - Create rsa Public and Private keys objects using the keys generated
        - Retreve bytes in PKCS#1 format and write them to both pem files
"""

def writeToPEM(key,file):
    pub_key = rsa.PublicKey(n=key["n"],e=key["e"])
    priv_key = rsa.PrivateKey(n=key["n"],e=key["e"],d=key["d"],p=key["p"],q=key["q"])
    with open(file+"_pub"+'.pem', 'w') as f:
        f.write(pub_key.save_pkcs1().decode("utf8"))
    with open(file+"_priv"+'.pem', 'w') as f:
        f.write(priv_key.save_pkcs1().decode("utf8"))

"""
    Rabin Miller and isPrime functions, taken from https://langui.sh/2009/03/07/generating-very-large-primes/ as a way
    to generate large prime numbers.

    Walkthrough:
        - Even numbers are thrown out, only even prime is 2
        - Check if low prime numbers devide the random integer created
        - RSA numbers p-1 and q-1 should not be factorized by low primes, so we also check for that
        - Reach the Rabin Miller core an algorithm that returns wether a number is prime or not
"""


def rabinMiller(p,l):
    s = p-1
    t = 0
    while s&1 == 0:
        s = s//2
        t+=1
    k = 0
    while k <128:
        a = int(''.join([str(next()) for i in range(l)]),2)
        while a < 2 or a > p - 1:
            a = int(''.join([str(next()) for i in range(l)]),2)
        v = pow(a,s,p)
        if v != 1:
            i = 0
            while v != (p-1):
                if i == t-1:
                    return False
                else:
                    i = i+1
                    v = (v**2)%p
        k+=2
    return True

def isPrime(n,l):
    lowPrimes = [3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97
                   ,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179
                   ,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269
                   ,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367
                   ,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461
                   ,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571
                   ,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661
                   ,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773
                   ,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883
                   ,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997]
    if (n > 3):
        if (n&1 != 0):
            for p in lowPrimes:
                if n == p:
                    for lp in lowPrimes:
                        if n-1 / lowPrimes == 0:
                            return False
                    return True
                if (n % p == 0):
                    return False
            return rabinMiller(n,l)
    return False

"""
    Get RSA Prime function: Designed to return large primes of size n (bits)

    Walkthrough:
        - Generate random n bits and transform the binary number to an integer
        - Check if the number is Prime
"""

def getRSAPrime(n):
    while True:
        st = ''.join([str(next()) for i in range(n)])
        pp = int(st,2)
        if isPrime(pp,n):
            return pp

"""
    Make RSA Key: Generate a RSA key pair using the above functions

    Walkthrough:
        - Generate 2 large primes to serve as p and q
        - Get the modulos n by multipling both
        - e if fixed to 65537, a prime so no conflits with p and q
        - d is the inverse of e to modulos n
        - Write both keys to file
"""

def makeRSAKey(n,f):
    p = getRSAPrime(n//2)
    q = getRSAPrime(n//2)

    n = p*q

    e = 65537
    d = pow(e, -1, (p-1)*(q-1))

    key_obj = {
        "n": n,
        "e": e,
        "d": d,
        "p": p,
        "q": q,
    }

    writeToPEM(key_obj,f)

    return e,d,n
    
e,d,n = makeRSAKey(args.s,args.f)
