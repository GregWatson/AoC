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

NORMAL = 0
GARBAGE = 1
SKIPNEXT = 2

def doPart1(db):
    count = 0
    group = 0
    state = [NORMAL]
    for i, c in enumerate(db[0]):
        print(f"{' '*group}{db[0][i:i+10]}     {state[-1]}  {group}   {count}")
        if state[-1] == SKIPNEXT:
            state.pop(); continue
        if state[-1] == GARBAGE:
            if c == '>':
                state.pop(); continue
            elif c == '!':
                state.append(SKIPNEXT)
            continue
        if state[-1] == NORMAL:
            if c == '{':
                group = group + 1
                count += group
                continue
            if c == '}':
                group = group - 1
                continue
            if c == '<':
                state.append(GARBAGE); continue
            if c == '!':
                state.append(SKIPNEXT); continue
            continue
    return count

def doPart2(db):
    count = 0
    group = 0
    state = [NORMAL]
    gbg = 0
    for i, c in enumerate(db[0]):
        print(f"{' '*group}{db[0][i:i+10]}     {state[-1]}  {group}   {count}")
        if state[-1] == SKIPNEXT:
            state.pop(); continue
        if state[-1] == GARBAGE:
            if c == '>':
                state.pop(); continue
            elif c == '!':
                state.append(SKIPNEXT)
                continue
            gbg += 1
            continue
        if state[-1] == NORMAL:
            if c == '{':
                group = group + 1
                count += group
                continue
            if c == '}':
                group = group - 1
                continue
            if c == '<':
                state.append(GARBAGE); continue
            if c == '!':
                state.append(SKIPNEXT); continue
            continue
    return gbg


#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}\n\n")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
