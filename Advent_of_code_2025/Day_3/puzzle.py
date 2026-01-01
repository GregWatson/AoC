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

def getMax(l):
    m1 = max(l[0:-1])
    i1 = l.index(m1)
    m2 = max(l[i1+1:])
    print(f"'{l}' Max1 {m1}{m2}")
    return int(m1+m2)

def getMax2(l):
    s = ''
    for i in range(11):
        j = i-11
        print(f"l is {l} and j is {j}")
        mx = max(l[0:j])
        s += mx
        ix = l.index(mx)
        print(f"i={i} j={j} l is '{l}' search range is '{l[0:j]}'  mx is '{mx}'")
        l = l[ix+1:]
    mx = max(l)
    s += mx
    print(f"'{l}' Max is {s}")
    return int(s)

def doPart1(db):
    c = 0
    for l in db:
        c += getMax(l)
    return c
    
def doPart2(db):
    c = 0
    for l in db:
        c += getMax2(l)
    return c


#---------------------------------------------------------------------------------------
#sys.setrecursionlimit(10000)

p1 = doPart1(db)
print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"\nPart 2 is {p2}")
