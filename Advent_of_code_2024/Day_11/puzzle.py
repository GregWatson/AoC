#import argparse
import sys
import re
import functools
import array
import copy
import hashlib
import string
import itertools

BLENDER=False

# --- Blender ---
if BLENDER:
    import bpy
    sys.path.append(r'C:\cygwin64\home\gwatson\AOC')
    from blenderLib import *
# ---------------

input_file_name = 'input.txt'
print_on = False
MAX=43
#MAX=8

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def getArray(db):
    nums = [c for c in db[0].split()]
    return nums

def drawArray(a):
    # field
    #addCuboid(POS=(0,0,0), SCALE=(MAX,MAX,0.1), COL=GREEN80)

    for y in range(MAX):
        print(f"{y}")
        for x in range(MAX):
            c = a[y][x]
            if c == 0 :  col = WHITE
            elif c == 9: col = RED80
            else:        col = (0,c/10,0,1)
            addCuboid(POS=(x,MAX-1-y,0), SCALE=(1,1,(c+1)/5), COL=col)

# use memoization memo cacheing
@functools.cache
def computeLen(num,times):
    if times == 1:
        if num == '0': return 1
        else:
            nlen = len(num)
            if nlen%2 == 0: return 2
            else: return 1

    if num == '0': r = computeLen('1',times-1)
    else:
        nlen = len(num)
        if nlen%2 == 0:
            s1 = num[0:nlen>>1]
            s2 = num[nlen>>1:]
            r = computeLen(str(int(s1)),times-1) + computeLen(str(int(s2)),times-1)
        else:
            r = computeLen(str(int(num)*2024), times-1)
    return r


def updateNums(nums,times):
    global numToLen
    c = 0
    for n in nums:
        c = c + computeLen(n, times)
    return c

def doPart1(db):
    # nums = ['125', '17']
    # s = updateNums(nums,6)
    # return s

    s = 0
    nums = getArray(db)
    print(f"nums is {nums}")
    s = updateNums(nums,25)
    return s
   

def doPart2(db):
    s = 0
    nums = getArray(db)
    print(f"nums is {nums}")
    s = updateNums(nums,75)
    return s

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

p1 = doPart1(db)
print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"Part 2 is {p2}")
