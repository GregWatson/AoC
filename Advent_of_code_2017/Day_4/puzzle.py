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
    count = 0
    for line in db:
        words = line.split()
        if len(words) == 1:
            count += 1
            continue
        foundDup = False
        for i,w in enumerate(words):
            if foundDup:
                break
            if i < len(words)-1:
                for ww in words[i+1:]:
                    if w == ww:
                        foundDup = True
                        break
        if not foundDup:
            count += 1
            print(f"OK : {words}")
    return count

def isAna(w1,w2):
    if len(w1) != len(w2):
        return False
    w1 = sorted(w1)
    w2 = sorted(w2)
    return w1 == w2


def doPart2(n):
    count = 0
    for line in db:
        words = line.split()
        if len(words) == 1:
            count += 1
            continue
        foundDup = False
        for i,w in enumerate(words):
            if foundDup:
                break
            if i < len(words)-1:
                for ww in words[i+1:]:
                    if isAna(w,ww):
                        foundDup = True
                        break
        if not foundDup:
            count += 1
            print(f"OK : {words}")
    return count


#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#sys.setrecursionlimit(10000)
p1 = doPart1(db)
#p1 = doPart1(10)
print(f"Part 1 is {p1}\n\n")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
