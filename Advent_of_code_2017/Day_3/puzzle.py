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

# map circular pattern to x and y coordinates
def getXY(n):
    #print(f"getXY({n})")
    if n == 1: return (0, 0)
    largestSqrt = int(math.sqrt(n))
    if largestSqrt % 2 == 0:
        largestSqrt -= 1
    if largestSqrt*largestSqrt == n:
        return (largestSqrt//2, largestSqrt//2)
    newSideLen=largestSqrt+2
    largestSquare = largestSqrt*largestSqrt
    x=(largestSqrt-1)//2; y=x
    tmp = largestSquare+1
    x = x+1
    #print(f"largestSqrt={largestSqrt}, largestSquare={largestSquare}, newSideLen={newSideLen}")
    while tmp < largestSquare+newSideLen:
        #print(f"{tmp} < {largestSquare+newSideLen}   ({x}, {y})")
        if tmp == n:
            return (x, y)
        tmp += 1
        y -= 1
    y=y+1;x=x-1
    while tmp < largestSquare+newSideLen*2-1:
        #print(f"{tmp} < {largestSquare+newSideLen*2-1}   ({x}, {y})")
        if tmp == n:
            return (x, y)
        tmp += 1
        x -= 1
    x=x+1;y=y+1
    while tmp < largestSquare+newSideLen*3-2:
        #print(f"{tmp} < {largestSquare+newSideLen*3-2}   ({x}, {y})")
        if tmp == n:
            return (x, y)
        tmp += 1
        y += 1
    y=y-1;x=x+1
    while tmp < largestSquare+newSideLen*4-3:
        #print(f"{tmp} < {largestSquare+newSideLen*4-3}   ({x}, {y})")
        if tmp == n:
            return (x, y)
        tmp += 1
        x += 1
    return (x, y)

def getManhattanDistance(x, y):
    return abs(x) + abs(y)

def getDistance(n):
    x, y = getXY(n)
    return getManhattanDistance(x, y)


def doPart1(n):
    #for i in range(12):
    #    print(f"{i+1} => {getXY(i+1)}")
    return getDistance(n)


def doPart2(n):
    d = {"0,0": 1, "1,0": 1}
    x=1; y=0;xd=1;yd=0
    while True:
        #can I turn left?
        if xd==1: nxd=0;nyd=-1
        elif xd==-1: nxd=0;nyd=1
        elif yd==-1: nxd=-1;nyd=0
        else: nxd=1;nyd=0
        px = x + nxd
        py = y + nyd
        if f"{px},{py}" in d: #must continue
            px= x + xd
            py= y + yd
        else: 
            xd=nxd;yd=nyd
        n1= 0
        for (xx,yy) in [(px-1, py-1), (px, py-1), (px+1, py-1), (px-1, py), (px+1, py), (px-1, py+1), (px, py+1), (px+1, py+1)]:
            if f"{xx},{yy}" in d:
                n1+= d[f"{xx},{yy}"]
        if n1 > n:
            return n1
        d[f"{px},{py}"] = n1
        x=px
        y=py
        print(f"{px},{py} => {n1}")

#---------------------------------------------------------------------------------------
# Load input
#db = load_db()

#sys.setrecursionlimit(10000)
p1 = doPart1(277678)
#p1 = doPart1(10)
print(f"Part 1 is {p1}\n\n")

p2 = doPart2(277678)
print(f"\n\n\n\nPart 2 is {p2}")
