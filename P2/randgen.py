import time
import numpy as np
from PIL import Image
import argparse
from pseudogen import *
import matplotlib.pyplot as plt

# Parse all arguments from the user

parser = argparse.ArgumentParser()
parser.add_argument('-p', type=str, required=False)
parser.add_argument('-c', type=str, required=False)
parser.add_argument('-i', type=int, required=False)
parser.add_argument('-s', required=False,action="store_false")
parser.add_argument('-g', type=int, required=False)
args = parser.parse_args()

# Decision between outputting bytes nad doing statistical work

if not args.s:
    password = "password"
    cs = "a"
    i = 1

    # Start the geerator with preselected parameters

    start(password,cs,i)

    # Prepare an image to fill with random pixels to show 

    data = np.zeros((1024, 1024, 3), dtype=np.uint8)
    data[512, 512] = [254, 0, 0]

    # Fill each pixel with 3 random bytes

    for i in range(0, 1024):
        for j in range(0, 1024):
            data[i, j] = [nextByte(), nextByte(), nextByte()]

    # Created and saved image that shows true randomness, no patterns

    img = Image.fromarray(data, 'RGB')
    img.save("ShowOfRandomness.png")

    # Unifromity study to show that all numbers from 0-256 are being generated an equal amount of time

    res = {}
    for i in range(10000000):
        b = nextByte()
        if b in res:
            res[b] += 1
        else:
            res[b] = 1

    cs1 = plt.figure(1)
    plt.bar(res.keys(), res.values(), color='g')
    plt.savefig("Histogram.png")

    # Study on how changing the number of iterations on the same confusion string alters setup time

    password = "password"
    cs = ["a","bb"]
    iter = [1,5,20,50,100,200]
    results_iter = [[],[]]
    for c in cs:
        for i in iter:
            st = time.time()
            start(password,c,i)
            end = time.time() - st
            results_iter[len(c)-1].append(end)

    cs2 = plt.figure(2)
    plt.plot(iter,results_iter[0],color='green', linestyle='dashed', linewidth = 3, marker = 'X',markerfacecolor='blue',markersize=12)
    plt.savefig("CS1_ModifyingIterations.png")

    cs3 = plt.figure(3)
    plt.plot(iter,results_iter[1],color='green', linestyle='dashed', linewidth = 3, marker = 'X',markerfacecolor='blue',markersize=12)
    plt.savefig("CS2_ModifyingIterations.png")

    # Study on how changing the length of the confusion string on the same iteration count alters setup time
    
    password = "password"
    cs = ["b","bb","bbb","bbbb"]
    iter = [1]
    results_cs = [[]]
    for i in iter:
        for c in cs:
            st = time.time()
            start(password,c,i)
            end = time.time() - st
            results_cs[len(iter)-1].append(end)

    # Print results in list form

    print(results_iter[0])
    print(results_iter[1])

    print(results_cs[0])

    cs4 = plt.figure(4)
    plt.plot(cs,results_cs[0],color='green', linestyle='dashed', linewidth = 3, marker = 'X',markerfacecolor='blue',markersize=12)
    plt.savefig("Iteration1_ModifyingCS.png")

# Print random bytes to output, if the number is less than 0 it will go one forever, if not the amount of bytes asked
# is printed

if args.g:
    if not args.p and not args.c and not args.i :
        print("usage: rand.py -p PASSWORD -c CONFUSION_STRING -i ITERATIONS [-s] [-g] amount")
        exit()
    password = args.p
    cs = args.c
    iter = args.i
    start(password,cs,iter)
    if args.g < 0:
        while True: 
            print(chr(nextByte()),end="")
    else:
        for i in range(args.g):
            print(chr(nextByte()),end="")