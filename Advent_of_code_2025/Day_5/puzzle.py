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

def getRangesIds(db):
    ranges = []
    ids = []
    for l in db:
        r = re.findall(r'(\d+)-(\d+)', l)
        if len(r): 
            ranges.append( (int(r[0][0]), int(r[0][1])) )
            continue
        r = re.findall(r'(\d+)$', l)
        if len(r): ids.append( int(r[0]) )
    print(f"{len(ranges)} ranges and {len(ids)} ids")
    return ranges, ids

def doPart1(db):
    ranges, ids = getRangesIds(db)
    c = 0
    for n in ids:
        found = False
        for r in ranges:
            if n >= r[0] and n <= r[1]:
                c += 1
                break
    return c
    
def doPart2(db):
    ranges, ids = getRangesIds(db)
    newRanges = []
    for r in ranges:
        cur = [ (r) ]
        for nr in newRanges:
            nrl,nrr = nr
            for c in cur:
                crl,crr = c
                if crr < nrl or crl > nrr:
                    continue
                if crl >= nrl and crr <= nrr:
                    cur.remove(c)
                    break
                if crl < nrl and crr > nrr:
                    cur.remove(c)
                    cur.append( (crl, nrl-1) )
                    cur.append( (nrr+1, crr) )
                    break
                if crl < nrl and crr >= nrl:
                    cur.remove(c)
                    cur.append( (crl, nrl-1) )
                    break
                if crl <= nrr and crr > nrr:
                    cur.remove(c)
                    cur.append( (nrr+1, crr) )
                    break
        newRanges.extend(cur)
    c = 0
    for r in newRanges:
        c += (r[1]-r[0]+1)
    return c

#---------------------------------------------------------------------------------------
#sys.setrecursionlimit(10000)

p1 = doPart1(db)
print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"\nPart 2 is {p2}")
