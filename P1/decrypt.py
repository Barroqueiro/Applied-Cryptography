import sys
import time
import hashlib
from saes_module import *
import argparse


"""
    main()

    Params:
        None

    Walkthrough:
        - Get the encryption and shuffle keys from command line arguments
        - Digest both using MD5
        - Make the shuffledsbox and the shuffledrsbox
        - Create the keys using AES Expansion schedule
        - Stdin to read data to decrypt
        - Split the data in blocks, decrypt each one
        - For the last block remove padding to make it the original message

"""

def main():
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-n','--normal', help='Normal key for encryption', required=True)
    parser.add_argument('-s','--shuffle', help='Shuffle key for encryption', required=False)
    parser.add_argument('-t','--time', help='Time the encryption to a file', required=False)
    args = vars(parser.parse_args())
    if args['shuffle']:
        make_keys(1,sys.argv[2],sys.argv[4])
        make_shuffledsbox()
        make_shuffledrsbox()
    else:
        make_keys(0,sys.argv[2],0)
    plainText = sys.stdin.read()
    blocks = []
    block = []
    counter = 0
    start_time = time.time()
    for l in plainText:
        block.append(l)
        counter += 1
        if counter % 16 == 0:
            decrypted = saes_decrypt(to_matrix(block))
            blocks.append(decrypted)
            block = []

    for i in range(len(blocks)-1):
        print(blocks[i],end="")
    print(unpad(blocks[-1]))
    final_time = (time.time() - start_time)
    if args['time']:
        with open(args['time'],"a") as f:
            f.write(str(final_time)+"\n")

# Call for main
main()