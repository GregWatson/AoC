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

def printStr(s):
    a = s.split('/')
    for row in a:
        print(row)
    print()

def printGridRow(row):
    grids = [ r.split('/') for r in row ]
    for l in range(len(grids[0])):
        print(f"|", end='')
        for g in grids:
            print(g[l], end='|')
        print()

def printGrid(grid):
    n = int(math.sqrt(len(grid)))
    if len(grid[0]) == 5: w = 3
    else: w = 4
    print(f"{'-' * (n * w + 1)}")
    for i in range(n):
        printGridRow(grid[i*n:(i+1)*n])
        print(f"{'-' * (n * w + 1)}")
    print() 


# def getRotatesAndFlips(s):
#     variations = set()
#     a = s.split('/')
#     for _ in range(4):
#         a = [''.join(row) for row in zip(*a[::-1])]
#         variations.add('/'.join(a))
#         variations.add('/'.join(a[::-1]))
#     # print(f"Variations for {s}:")
#     # for v in variations: printStr(v)
#     return variations

def flip(s):
    a = s.split('/')
    a = a[::-1]
    return '/'.join(a)

def getRotations(s):
    if len(s)==5: # 2x2
        a = s.split('/')
        r1 = a[1][0] + a[0][0] + '/' + a[1][1] + a[0][1]
        r2 = a[1][1] + a[1][0] + '/' + a[0][1] + a[0][0]
        r3 = a[0][1] + a[1][1] + '/' + a[0][0] + a[1][0]
        return [ s, r1, r2, r3 ]
    elif len(s)==11: # 3x3
        a = s.split('/')
        c0 = a[0][0]
        c1 = a[0][1]
        c2 = a[0][2]
        c3 = a[1][0]
        c4 = a[1][1]
        c5 = a[1][2]
        c6 = a[2][0]
        c7 = a[2][1]
        c8 = a[2][2]
        r1 = c6+c3+c0+'/'+c7+c4+c1+'/'+c8+c5+c2
        r2 = c8+c7+c6+'/'+c5+c4+c3+'/'+c2+c1+c0
        r3 = c2+c5+c8+'/'+c1+c4+c7+'/'+c0+c3+c6
        return [ s, r1, r2, r3 ]
    else:
        print(f"Unexpected string length {len(s)} for {s}")
        sys.exit(1)

src = {} # map any variation to the variation in the db

def getRotatesAndFlips(s):
    global src
    variations = set()
    for r in getRotations(s):
        variations.add(r)
        src[r] = s
    for r in getRotations(flip(s)):
        variations.add(r)
        src[r] = s
    return variations


def getEnhancements(db):
    enh = {}
    for line in db:
        parts = line.split(' => ')
        variations = getRotatesAndFlips(parts[0])
        for v in variations: enh[v] = parts[1]
    return enh

def fracture(s): # break 4x4 into 4 2x2
    a = s.split('/')
    assert len(a) == 4
    assert len(a[0]) == 4
    l = [ a[0][0:2] + '/' + a[1][0:2],
          a[0][2:4] + '/' + a[1][2:4],
          a[2][0:2] + '/' + a[3][0:2],
          a[2][2:4] + '/' + a[3][2:4] ]
    # print(f"Fracturing {s} into {l}")
    return l

# grid is a string like .#./..#/###
# if input is length 2 then return [ strLen3 ]
# if input is length 3 then return [ [ strLen4, strLen4, strLen4, strLen4 ] ]
def processString(grid, enh):
    if len(grid) == 5: # 2x2
        print(f"{grid} -> {enh[grid]}  (src={src[grid]})")
        return [ enh[grid] ]
    elif len(grid) == 11: # 3x3
        if grid in enh:
            s4 = enh[grid]
            print(f"{grid} -> {s4}     (src={src[grid]})")
            return fracture(s4)
        else:   
            print(f"Did not find {grid} in enhancements")
    else:
        print(f"Unexpected grid length {len(grid)} for {grid}")
        sys.exit(1)

# Reordering is only needed because I store grids as a flat list
# e.g. for 16 2x2 grids:
# [ g0, g1, g2, g3, g4, g5, ... g15 ]
# but they are really:
# [ g0, g1, g4, g5 ]
# [ g2, g3, g6, g7 ]
# [ g8, g9, g12,g13]
# [ g10,g11,g14,g15]
# This is just for display purposes; the processing should work fine without it
# as each grid is independent.
def reorderGrid(grids): 
    newGrid = []
    n = int(math.sqrt(len(grids)))
    if n==2: return grids
    assert n%2==0
    arr = [grids[i*n:(i+1)*n] for i in range(n)]
    # print(f"Reorder arr is {arr} ")
    for y in range(0, n, 2):
        r1 = arr[y]
        r2 = arr[y+1]
        # print(f"Reordering rows {y} and {y+1}: {r1} and {r2}")
        for x4 in range(len(r1)//4):
            # print(f"  Taking cols {x4*4} to {x4*4+1} from each: {r1[x4*4:x4*4+2]} and {r2[x4*4:x4*4+2]}")
            newGrid.extend(r1[x4*4:x4*4+2])
            newGrid.extend(r2[x4*4:x4*4+2])
            # print(f"--- So newgrid is {newGrid}")
        for x4 in range(len(r1)//4):
            newGrid.extend(r1[x4*4+2:x4*4+4])
            newGrid.extend(r2[x4*4+2:x4*4+4])
    # print(f"Reordered grid is:")
    # printGrid(newGrid)
    return newGrid

# grids is a list of strings
def processGrids(grids, enh):
    newGrid = []
    for g in grids:
        newGrid.extend(processString(g, enh))
    if len(newGrid[0]) == 5: # 2x2
        return reorderGrid(newGrid)
    return newGrid

def countOn(grids):
    mycount = 0
    for g in grids:
        c = g.count('#')
        mycount += c
        # print(f"Counting on in {g} is {c} Tot is {mycount}")
    return mycount

def doPart1(db):
    enh = getEnhancements(db)
    grids = ['.#./..#/###']
    for it in range(3):
        print(f"Iteration {it+1} is starting with {len(grids)} grids.")
        newgrids = processGrids(grids, enh)
        grids = newgrids
        on = countOn(grids)
        print(f"After {it+1} iterations there are {len(grids)} grids. {on} pixels are on")
        printGrid(grids)
    return on
   
    
def doPart2(db):
    return 0
#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"\nPart 2 is {p2}")
