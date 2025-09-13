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
aSize = 1000

# Load input data to db if file_path exists and is readable
if os.path.exists(file_path) and os.path.isfile(file_path) and os.access(file_path, os.R_OK):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            db = [ l.strip() for l in lines ]
    except IOError as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

def getGrid(db, aSize):
    a = [ [0 for i in range(aSize) ] for j in range (aSize)] 
    for y,l in enumerate(db):
        for x,c in enumerate(l):
            a[y+aSize//2][x+aSize//2] = 1 if c=='#' else 0
    return a

def getRanges(a):
    xmin = ymin = BIGNUM
    xmax = ymax = -BIGNUM
    for j in range(len(a)):
        for i in range(len(a[j])):
            if a[j][i]:
                if i<xmin: xmin=i
                if i>xmax: xmax=i
                if j<ymin: ymin=j
                if j>ymax: ymax=j
    return xmin,xmax,ymin,ymax

def printGrid(a, x=None, y=None):
    xmin,xmax,ymin,ymax = getRanges(a)
    print(f"x: {xmin} to {xmax}, y: {ymin} to {ymax}   x={x}, y={y}")
    for j in range(ymin,ymax+1):
        for i in range(xmin,xmax+1):
            if x==i and y==j:
                print('[' + ('#' if a[j][i] else '.') + ']', end='')
            else:
                print(' ' + ('#' if a[j][i] else '.') + ' ', end='')
        print()
    print()

def runIterations(a, iterations, x, y):
    dir = 0 # up
    newinfections = 0
    for i in range(iterations):
        if a[y][x]==0: # clean
            dir = (dir-1)%4 # turn left
            a[y][x] = 1 # infected
            newinfections += 1
        else: # infected
            dir = (dir+1)%4 # turn right
            a[y][x] = 0 # clean
        if dir==0: y-=1
        elif dir==1: x+=1
        elif dir==2: y+=1
        elif dir==3: x-=1
    return newinfections, x, y

# 0 = clean, 1 = infected , 2 = weakened, 3 = flagged
def runIterations2(a, iterations, x, y):
    dir = 0 # up
    newinfections = 0
    for _ in range(iterations):
        state = a[y][x]
        if state==0: # clean
            dir = (dir-1)%4 # turn left
            a[y][x] = 2 # weakened
        elif state==1: # infected
            dir = (dir+1)%4 # turn right
            a[y][x] = 3 # clean
        elif state==2: # weakened
            a[y][x] = 1 # infected
            newinfections += 1
        elif state==3: # flagged
            dir = (dir+2)%4 # reverse
            a[y][x] = 0 # clean
        if dir==0: y-=1
        elif dir==1: x+=1
        elif dir==2: y+=1
        elif dir==3: x-=1
    return newinfections, x, y

def doPart1(db):
    grid = getGrid(db, aSize)
    x = aSize//2+len(db[0])//2
    y = aSize//2+len(db[0])//2
    printGrid(grid, x, y)
    newinfections,x ,y = runIterations(grid, 10000,x, y)
    #printGrid(grid, x, y)
    return newinfections
   
    
def doPart2(db):
    grid = getGrid(db, aSize)
    x = aSize//2+len(db[0])//2
    y = aSize//2+len(db[0])//2
    printGrid(grid, x, y)
    newinfections,x ,y = runIterations2(grid, 10000000,x, y)
    #printGrid(grid, x, y)
    return newinfections
    
#---------------------------------------------------------------------------------------
# Input is in db if neede.

#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"\nPart 2 is {p2}")
