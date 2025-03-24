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
        l = f.read()
        # print(f"len is {len(l)}")
    keys = l.split("\n\n")
    db = [ l.split("\n") for l in keys ]
    print(f"db is {db}")
    return db

def getData(db):
    keys=[]
    locks=[]
    for obj in db:
        lens=[ -1 for i in range(5)]
        for l in obj:
            for i,c in enumerate(l):
                if c=='#': lens[i]+=1
        if obj[0] == '#####': locks.append(lens)
        else: keys.append(lens)
    return keys,locks

def keyFitsLock(k,l):
    for i in range(5):
        if k[i] + l[i] > 5: return False
    return True

def doPart1(db):
    count = 0
    getData(db)
    keys,locks=getData(db)
    print(f"keys is {keys}")
    print(f"locks is {locks}")
    for k in keys:
        for l in locks:
            if keyFitsLock(k,l): count+=1
    return count

def doPart2(db):
    count = 0
    return count

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}\n\n")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
