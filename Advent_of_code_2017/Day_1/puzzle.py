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
    L = list(db[0])
    L.append(db[0][0])
    for i,n in enumerate(L[0:-1]):
        if n == L[i+1]:
            count += int(n)
    return count

def doPart2(db):
    count = 0
    L = list(db[0])
    for i,n in enumerate(L):
        halfway = int(len(L)/2)
        if i < halfway:
            n1 = L[i+halfway]
        else:
            n1 = L[i-halfway]
        if n == n1:
            count += int(n)
    return count

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}\n\n")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
