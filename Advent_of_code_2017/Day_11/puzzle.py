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

dirs = ['s', 'n', 'ne', 'nw', 'se', 'sw']

def distance(x, y):
    # for every 2 x I get a free y
    xa = abs(x); ya = abs(y)
    print(f"distance: xa = {xa} ya = {ya}")
    if ya > xa//2: return int(xa + (ya - xa//2))
    return int(xa)
  
def doPart12(db):
    count = 0
    l = db[0].split(',')
    x = 0; y = 0
    mx = 0
    for d in l: 
        if d == 'n':
            y -= 1
        elif d == 's':
            y += 1
        elif d == 'ne':
            x += 1; y -= 0.5
        elif d == 'sw':
            x -= 1; y += 0.5
        elif d == 'nw':
            x -= 1; y -= 0.5
        elif d == 'se':
            x += 1; y += 0.5
        else:
            print(f"Unknown direction {d}")
        di = distance(x,y)
        if di > mx:
            mx = di
        #print(f"dir = {d} x = {x} y = {y} di = {di}")
    print(f"part 1: {di}")
    print(f"part 2: {mx}")

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#sys.setrecursionlimit(10000)
p1 = doPart12(db)
