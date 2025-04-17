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
    for l in db:
        n = list(map(lambda x: int(x), l.split()))
        count += max(n) - min(n)
    return count

def doPart2(db):
    count = 0
    for l in db:
        n = list(map(lambda x: int(x), l.split()))
        for i in range(len(n)-1):
            for j in range(i+1, len(n)):
                if n[i] % n[j] == 0:
                    count += n[i] // n[j]
                elif n[j] % n[i] == 0:
                    count += n[j] // n[i]
    return count

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}\n\n")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
