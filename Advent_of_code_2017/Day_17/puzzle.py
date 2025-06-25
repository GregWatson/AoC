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

def doPart1(db):
    my_list=[0,1]
    ll = 2 # length
    pos = 1
    for i in range(2016):
        if print_on:
            print(f"pos: {pos} my_list: {my_list}")
        steps = 324
        num_left = ll - pos - 1
        if num_left >= steps:
            pos = pos + steps + 1
            my_list.insert(pos, i + 2)
        else:
            pos = (steps - num_left) % ll
            my_list.insert(pos, i + 2)
        ll += 1
    return my_list[pos+1]

def doPart2(db):
    ll = 2 # length
    ans = 0
    zeropos = 0
    pos = 1
    i= 0
    steps = 324
    while i < 50000000:
        if i%10000000 == 0:
            print(f"{i}")
        num_left = ll - pos - 1
        if num_left >= steps:
            pos = pos + steps + 1
        else:
            pos = (steps - num_left) % ll
        if pos == zeropos+1:  
            ans = i + 2
        if pos <= zeropos: 
            zeropos += 1
            # print(f"{i}: New zeropos is {zeropos} answer is {ans}")
        ll += 1
        if (i+2) == 50000000: return ans
        i += 1

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}\n\n")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
