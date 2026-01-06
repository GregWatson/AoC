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


deltas = [ (-1,-1), (0,-1), (1,-1),
            (-1, 0),         (1, 0),
            (-1, 1), (0, 1), (1, 1) ]

maxX=0
maxY=0

def numAround(db, x, y):
    count = 0
    for dx,dy in deltas:
        nx = x + dx
        ny = y + dy
        if nx < 0 or nx > maxX or ny < 0 or ny > maxY:
            continue
        if db[ny][nx] == '@':
            count += 1
    return count


def doPart1(db):

    count = 0
    for y,l in enumerate(db):
        if len(l) <2: continue
        for x,ch in enumerate(l):
            if ch != '@': continue
            if numAround(db, x, y) < 4:
                count += 1
    return count
    
def doPart2(db):
    global maxY, maxX
    maxX=len(db[0])-1
    maxY=len(db)-1
    tot = 0
    done = False
    newdb = [ list(l) for l in db ]
    while not done:
        count = 0
        changes = []
        for y,l in enumerate(newdb):
            if len(l) <2: continue
            for x,ch in enumerate(l):
                if ch != '@': continue
                if numAround(newdb, x, y) < 4:
                    count += 1
                    changes.append( (x,y) )
        print(f"Changed {count} ")
        for x,y in changes:
            newdb[y][x] = '.'
        if count == 0:
            done = True
        tot += count
    return tot


#---------------------------------------------------------------------------------------
#sys.setrecursionlimit(10000)

p1 = doPart1(db)
print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"\nPart 2 is {p2}")
