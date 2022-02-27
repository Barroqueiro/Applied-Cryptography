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
        - Make the shuffledsbox
        - Create the keys using AES Expansion schedule
        - Stdin to read data to encrypt
        - Split the data in blocks, encrypt each one
        - For the last block add padding to make it 16 characters for encryption 

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
    else:
        make_keys(0,sys.argv[2],0)
    plainText = input()
    block = []
    counter = 0
    start_time = time.time()
    for l in plainText:
        block.append(l)
        counter += 1
        if counter % 16 == 0:
            saes_encrypt(to_matrix(pad_block(block)))
            block = []
    saes_encrypt(to_matrix(pad_block(block)))
    final_time = (time.time() - start_time)
    if args['time']:
        with open(args['time'],"a") as f:
            f.write(str(final_time)+"\n")

# Call for main
main()