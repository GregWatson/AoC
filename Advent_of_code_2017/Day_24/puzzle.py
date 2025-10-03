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

def getComponents(db):
    components = []
    hasPort = {}
    for i,line in enumerate(db):
        a,b = map(int,line.split('/'))
        components.append( (a,b) )
        if a not in hasPort:
            hasPort[a] = []
        if b not in hasPort:
            hasPort[b] = []
        hasPort[a].append(i)
        hasPort[b].append(i)
    return components, hasPort

best = 0
bestLength = 0

def search(port, strength, used, components, hasPort):
    # print(f"searching port {port} strength {strength}")
    global best
    if strength > best:
        best = strength
    for ci in hasPort.get(port, []):
        if not used[ci]:
            used[ci] = True
            a,b = components[ci]
            search(b if a == port else a, strength + a + b, used, components, hasPort)
            used[ci] = False

def search2(port, strength, curLength, used, components, hasPort):
    # print(f"searching port {port} strength {strength}")
    global best, bestLength
    if curLength == bestLength and strength > best:
        best = strength
    elif curLength > bestLength:
        bestLength = curLength
        best = strength
    for ci in hasPort.get(port, []):
        if not used[ci]:
            used[ci] = True
            a,b = components[ci]
            search2(b if a == port else a, strength + a + b, curLength+1, used, components, hasPort)
            used[ci] = False

def doPart1(db):
    global best
    components, hasPort = getComponents(db)
    used = [False] * len(components)
    best = 0
    search(0, 0, used, components, hasPort)
    return best
   
    
def doPart2(db):
    global best, bestLen
    components, hasPort = getComponents(db)
    used = [False] * len(components)
    best = 0
    search2(0, 0, 0, used, components, hasPort)
    return best

#---------------------------------------------------------------------------------------
#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"\nPart 2 is {p2}")
