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
            db = [ l for l in lines ]
    except IOError as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
else: db = []

def getArray(db):
    arr = []
    for line in db:
        l = line.split()
        arr.append(l)
    print(f"Array: {arr}")
    return arr

def doPart1(db):
    arr = getArray(db)
    c = 0
    for col in range(len(arr[0])):
        op = arr[-1][col]
        v = 0
        if op == '*': v = 1
        for row in range(len(arr)-2,-1,-1):
            print(f"row {row} col {col} op {op} val {arr[row][col]}")
            if op == '+': v += int(arr[row][col])
            elif op == '*': v *= int(arr[row][col])
        c += v
    return c
    
def doPart2(db):
    c = 0
    signs = re.findall(r'[\+\*]\s+', db[-1])
    print(f"Signs: {signs}")
    for col in range(len(signs)):
        nums = []
        colWidth = len(signs[col])
        for row in range(len(db)-1):
            num = db[row][0:colWidth-1]
            nums.append(num)
            db[row] = db[row][colWidth:]
            print(f"Col {col} num '{num}'")
        op = signs[col].strip()
        v = 0
        if op == '*': v = 1
        for cc in range(colWidth-1):
            vnum = ''
            for r in range(len(nums)):
                vnum += nums[r][cc]
            print(f"col {col} op {op} val {vnum}")
            if op == '+': v += int(vnum)
            elif op == '*': v *= int(vnum)
        c += v
    return c

#---------------------------------------------------------------------------------------
#sys.setrecursionlimit(10000)

p1 = doPart1(db)
print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"\nPart 2 is {p2}")
