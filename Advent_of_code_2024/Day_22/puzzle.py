#import argparse
import sys
import re
import functools
import array
import copy
import hashlib
import string
import itertools
import math
import time

BLENDER=False

# --- Blender ---
if BLENDER:
    import bpy
    sys.path.append(r'C:\cygwin64\home\gwatson\AOC')
    from blenderLib import *
# ---------------

input_file_name = 'input.txt'
print_on = False
BIGNUM=10000000
MAX=141; MINSAVED=100; NUMCHEATS=20

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def getSecret(start,num):
    secret = start
    for rep in range(num):
        secret = ((secret << 6) ^ secret ) % 16777216
        secret = ((secret >> 5) ^ secret ) % 16777216
        secret = ((secret << 11) ^ secret ) % 16777216
    return secret

def doPart1(db):
    c = 0
    sL = [ getSecret(int(start),num=2000) for start in db]
    print(f"{sL}") 
    return sum(sL)

def get4PossibleDeltas():
    d4s = {}
    for a in range(10):
        for b in range(10):
            for c in range(10):
                for d in range(10):
                    for e in range(10):
                        d4 = [b-a+9, c-b+9, d-c+9, e-d+9]
                        n = 0
                        for d9 in d4: n = (n << 8) | d9 # make a hashable number
                        d4s[n] = 1
    seqs = []
    for n in d4s:
        l = [(n>>24)-9, ((n>>16) & 0xff)-9, ((n>>8)&0xff)-9, (n&0xff)-9]
        print(f"{l}")
        seqs.append(l)
    print(f"There are {len(d4s)} different sequences")
    return seqs

def getBananas(db):
    bananas=[]; deltas=[]
    for m,start in enumerate(db):
        secret = int(start)
        nb = [secret % 10]
        nd = [999]   # anything not in [-9, 9] 
        #if m==0 : print(f"{secret} {nb[-1]} {nd[-1]}")
        for i in range(2000):
            secret = ((secret << 6) ^ secret ) % 16777216
            secret = ((secret >> 5) ^ secret ) % 16777216
            secret = ((secret << 11) ^ secret ) % 16777216
            nb.append(secret % 10)
            nd.append((secret % 10) - nb[i])
            # if m==0 and i<6: print(f"{secret} {nb[-1]} {nd[-1]}")
        bananas.append(nb)
        deltas.append(nd)
    return bananas, deltas


def scoreDelta(d4, delta, banana):
    global print_on
    i=1
    while i <= len(delta)-4:
        if print_on and i<6: print(f"d4={d4}  delta={delta[i:i+4]}")
        if d4[0] == delta[i]:
            # print(f"poss match: index={i}   seq is {delta[i:i+4]}")
            if d4[1] == delta[i+1] and d4[2]==delta[i+2] and d4[3]==delta[i+3]:
                s = banana[i+3]
                if print_on: print(f"{d4} --- Hit at index {i}, num bananas = {s}")
                return s
        i=i+1
    if print_on: print(f"{d4} - not found.")
    return 0

def scoreBananas(d4, bananas, deltas):
    global print_on
    tot = 0
    for di, delta in enumerate(deltas):
        tot = tot + scoreDelta(d4,delta,bananas[di])
        if print_on:print(f"delta {di} tot is now {tot}")
    return tot


def getBest(d4, bananas, deltas):
    global print_on
    bestSoFar = 0
    for i, d in enumerate(d4):
        if (d[0]==-2 and d[1]==1 and d[2]==-1 and d[3]==3): print_on = True
        # if (d[0]==-1 and d[1]==0 and d[2]==-1 and d[3]==8): print_on = True
        if print_on: print(f"PRINT_ON for {d}")
        if (i%2 == 0): print(f"{i} {d} ",flush=True) 
        b = scoreBananas(d, bananas,deltas)
        if b > bestSoFar:
            bestSoFar = b
            print(f"Best so far is {bestSoFar}")
        print_on = False
    return bestSoFar


def doPart2(db):
    c = 0
    d4 = get4PossibleDeltas()
    bananas, deltas = getBananas(db)
    c = getBest(d4, bananas, deltas)
    #s = scoreDelta([-2,1,-1,3], deltas[0], bananas[0])
    #print(f"{deltas[0][0:20]}")
    return c


    
#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#sys.setrecursionlimit(10000)
#p1 = doPart1(db)
#print(f"Part 1 is {p1}\n\n")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
