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
import string
import os.path

BLENDER=False

# --- Blender ---
if BLENDER:
    import bpy
    sys.path.append(r'C:\cygwin64\home\gwatson\AOC')
    from blenderLib import *
# ---------------

file_path = 'input.txt'
print_on = False
BIGNUM=10000000
MAX=141; MINSAVED=100; NUMCHEATS=20

# Load input data to db if file_path exists and is readable
if os.path.exists(file_path) and os.path.isfile(file_path) and os.access(file_path, os.R_OK):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            db = [ l.strip() for l in lines ]
    except IOError as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
else: db = []

def getInvalids(r):
    rlo,rhi = r.split('-')
    print(f"{rlo}-{rhi}")
    rhi_i = int(rhi)
    s = rlo
    c = 0
    while int(s) <= rhi_i:
        if len(s)%2 : # odd len, add a 0
            s = '1' + '0'*len(s)
            print(f"   Move to {s}")
            continue
        halflen = len(s)//2
        sl = s[0:halflen] ; sr = s[halflen:]
        if sl == sr: 
            c += int(s)
            print(f"   valid: {sl}{sr}")
        s = str(int(s)+1)
    return c

def getInvalids2(r):
    c = 0
    rlo,rhi = r.split('-')
    print(f"{rlo}-{rhi}")
    rhi_i = int(rhi)
    s = rlo
    while int(s) <= rhi_i:
        slen = len(s)
        sublen = 1
        while sublen <= slen//2:
            if slen % sublen != 0:
                sublen += 1
                continue
            sub = s[0:sublen]
            expCopies = slen // sublen
            if sub * expCopies == s:
                c += int(s)
                print(f"   valid: {s} = {sub} * {expCopies}")
                break
            sublen += 1
        s = str(int(s)+1)
    return c



def doPart1(db):
    c = 0
    for r in db: c += getInvalids(r)
    return c
    
def doPart2(db):
    c = 0
    for r in db: c += getInvalids2(r)
    return c


#---------------------------------------------------------------------------------------
#sys.setrecursionlimit(10000)
ndb1 = db[0].split(',')
ndb = [ s.strip() for s in ndb1]

p1 = doPart1(ndb)
print(f"Part 1 is {p1}")

p2 = doPart2(ndb)
print(f"\nPart 2 is {p2}")
