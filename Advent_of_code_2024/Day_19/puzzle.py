#import argparse
import sys
import re
from functools import lru_cache
import array
import copy
import hashlib
import string
import itertools
import math

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
MAX=71


def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def getInfo(db):
    designs = []
    for l in db:
        if ',' in l:
            patterns = l.split(', ')
            print(f"{patterns}")
        elif len(l) > 1: 
            designs.append(l)
    return patterns, designs

patterns = []

# @cache   PY >3.9
@lru_cache(maxsize=4096)
def canMake(design, depth=0, p1=False):
    global patterns
    # get all poss starting patterns
    indent = ' '*depth
    patts = [ p for p in patterns if design.startswith(p) ]
    # print(f"{indent}Design {design} has starts {patts}")
    c = 0
    for p in patts:
        if len(p) == len(design):
            if p1: return 1
            c = c + 1
            continue
        d = design[len(p):]
        c = c + canMake(d, depth+2, p1=p1)
    return c

def doPart1(db):
    global patterns
    good = 0
    patterns, designs = getInfo(db)
    for d in designs:
        if canMake(d, p1=True) > 0:
            good = good + 1
    return good
   
def doPart2(db):
    global patterns
    good = 0
    patterns, designs = getInfo(db)
    for d in designs:
        c = canMake(d)
        print(f"--- {d} has count {c}") 
        good = good + c
    return good
    
#---------------------------------------------------------------------------------------
# Load input
db = load_db()
#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
