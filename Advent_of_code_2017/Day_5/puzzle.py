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
    jumps = list(map(lambda x: int(x), db))
    count = 0
    ptr = 0
    while ptr >=0 and ptr < len(db):
        #print(f"@{ptr} ")
        nextptr = ptr + jumps[ptr]
        jumps[ptr] += 1
        count += 1
        ptr = nextptr
    print(f"ptr is {ptr}")
    return count


def doPart2(db):
    jumps = list(map(lambda x: int(x), db))
    count = 0
    ptr = 0
    while ptr >=0 and ptr < len(db):
        #print(f"@{ptr} ")
        nextptr = ptr + jumps[ptr]
        if jumps[ptr] >= 3:
            jumps[ptr] -= 1
        else:
            jumps[ptr] += 1
        count += 1
        ptr = nextptr
    print(f"ptr is {ptr}")
    return count
    

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}\n\n")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
