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



def doPart1(db):
    x = db[0].find('S')
    l = [0 for i in range(len(db[0]))]
    l[x]=1  # tachyon
    c = 0
    # print(f"Initial: {l} x={x}")
    for y in range(len(db)):
        if y==0 or y % 2: continue
        row = db[y]
        newl = [0 for i in range(len(db[0]))]
        for x in range(len(l)):
            if l[x]==0: continue
            if row[x]=='.':
                newl[x]=1
            elif row[x]=='^':
                newl[x-1]=1
                newl[x+1]=1
                c += 1
            else:
                print(f"Unknown char {row[x]} at {x},{y}")
        l=newl
    return c
    
def doPart2(db):
    x = db[0].find('S')
    l = [0 for i in range(len(db[0]))]
    l[x]=1  # tachyon
    c = 0
    # print(f"Initial: {l} x={x}")
    for y in range(len(db)):
        if y==0 or y % 2: continue
        row = db[y]
        newl = [0 for i in range(len(db[0]))]
        for x in range(len(l)):
            if l[x]==0: continue
            if row[x]=='.':
                newl[x] += l[x]
            elif row[x]=='^':
                newl[x-1] += l[x]
                newl[x+1] += l[x]
            else:
                print(f"Unknown char {row[x]} at {x},{y}")
        l=newl
    return sum(l)

#---------------------------------------------------------------------------------------
#sys.setrecursionlimit(10000)

p1 = doPart1(db)
print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"\nPart 2 is {p2}")
