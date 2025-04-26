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

# is x connected to y (directly or indirectly)
# breadth first search (finds shortest)
def getConnectedTo(x,y,directTo, visited=None):
    if x == y:
        return True
    if x not in directTo:
        return False
    if visited is None:
        visited = [x]
    remaining = directTo[x]
    while len(remaining) > 0:
        newRemaining = []
        for n in remaining:
            if n in visited:
                continue
            visited.append(n)
            if n == y:
                return True
            if n in directTo:
                for nn in directTo[n]:
                    if nn not in visited:
                        newRemaining.append(nn)
        remaining = newRemaining
    return False

def doPart1(db):
    count = 1
    directTo = {}
    for l in db:
        m = re.match(r'(\d+) <-> (.*)', l)
        if m:
            num = int(m.group(1))
            nums = [int(x) for x in m.group(2).split(',')]
            directTo[num] = nums
            print(f"{num} => {directTo[num]}")
    for n in directTo:
        if n == 0:
            continue
        if getConnectedTo(0,n,directTo):
            count += 1
    return count

def doPart2(db):
    count = 0
    directTo = {}
    for l in db:
        m = re.match(r'(\d+) <-> (.*)', l)
        if m:
            num = int(m.group(1))
            nums = [int(x) for x in m.group(2).split(',')]
            directTo[num] = nums
    groups = []
    for n in directTo:
        for g in groups:
            if getConnectedTo(n,g[0],directTo):
                g.append(n)
                break
        else:
            groups.append([n])
    return len(groups)

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}\n\n")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
