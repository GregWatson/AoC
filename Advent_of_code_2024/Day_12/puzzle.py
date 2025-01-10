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
MAX=140
#MAX=8
TOP=0
BOTTOM=1
LEFT=2
RIGHT=3
sideName=['TOP','BOTTOM','LEFT','RIGHT']

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def getArray(db):
    plots = [ array.array('u',['.' for x in range(MAX)]) for y in range(MAX) ]
    for y,l in enumerate(db):
        for x,c in enumerate(l):
            plots[y][x]=c
    return plots

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
#@functools.cache

def findRegion(plots,x,y):
    c = plots[y][x]
    plots[y][x] = '#' # set to already checked
    area = 1
    fences = 4
    for (dx,dy) in [(0,-1),(0,1),(1,0),(-1,0)]:
        newx = x + dx
        newy = y + dy
        if (newx>=0) and (newx<MAX) and (newy>=0) and (newy<MAX):
            if ((c == plots[newy][newx]) or (plots[newy][newx]=='#')): # same type
                fences = fences - 1
                if c == plots[newy][newx]: 
                    (a,f) = findRegion(plots,newx,newy)
                    area = area + a
                    fences = fences + f
    return (area, fences)

def getNextRegion(plots,regions):
    x=0;y=0
    while y<MAX:
        if plots[y][x]=='.':
            x=x+1
            if x==MAX: 
                x=0; y=y+1
        else:
            break
    if y==MAX: return False

    vegType = plots[y][x]
    (area,fences) = findRegion(plots,x,y)
    for y in range(MAX):
        for x in range(MAX):
            if plots[y][x] == '#' : plots[y][x] = '.'
    if vegType in regions:
        regions[vegType].append((area, fences))
    else:
        regions[vegType] = [(area, fences)]
    return True

def getRegions(plots):
    regions= {} # map char to (area, fences)
    while getNextRegion(plots,regions) : continue
    return regions

def findEdges(plots,x,y):
    #print(f"calling findEdges at {x},{y}")
    c = plots[y][x]
    plots[y][x] = '#' # set to already checked
    area = 1
    edges = []
    for (side, dx,dy) in [(TOP,0,-1),(BOTTOM,0,1),(RIGHT,1,0),(LEFT,-1,0)]:
        newx = x + dx
        newy = y + dy
        #print(f"--- findEdges at {x},{y} trying adjacent location {newx},{newy} side {side}")
        if (newx>=0) and (newx<MAX) and (newy>=0) and (newy<MAX):
            if (c == plots[newy][newx]): # same type
                (a,e) = findEdges(plots,newx,newy)
                #print(f"findEdges at {newx},{newy} returned area {a} and edges {e}")
                area = area + a
                #print(f" ==> Before adding new edges, edges are {edges}")
                edges.extend(e)
                #print(f" ==> After adding new edges, edges are {edges}")
                continue
            if plots[newy][newx] != '#': 
                #print(f"    --- loc {x},{y} adds edge ({side},{x},{y})")
                edges.append((side,x,y))
                #print(f"         Edges now {edges}")
        else:
            #print(f"    --- loc {x},{y} adds edge ({side},{x},{y})")
            edges.append((side,x,y))
            #print(f"         Edges now {edges}")
    #print(f"findEdges at {x},{y} returns area {area} and edges {edges}")
    return (area, edges)

def getSideCount(l):
    if len(l)==1: return 1
    ix = 1
    while(ix<len(l)):
        if abs(l[ix] - l[ix-1]) != 1: # broken edge
            return 1 + getSideCount(l[ix:])
        ix = ix+1
    return 1

def countSides(edges):
    sideCount = 0
    for side in range(4):
        print(f"--- Processing side {sideName[side]}")
        sideEdges = [(el[1],el[2]) for el in edges if el[0]==side]
        print(f"Edges on side {sideName[side]} are {sideEdges}")
        while (len(sideEdges)):
            constIndex = 0; varIndex = 1
            if side==TOP or side==BOTTOM:
                constIndex = 1; varIndex = 0
            const = sideEdges[0][constIndex]
            var = sideEdges[0][varIndex]
            del sideEdges[0]
            newSideEdges = []
            sameSide = [var]
            for e in sideEdges:
                if e[constIndex] == const: 
                    sameSide.append(e[varIndex])
                else:
                    newSideEdges.append(e)
            # print(f"Sameside is {sameSide} newSideEdges is {newSideEdges}")
            sideEdges = newSideEdges
            sameSide.sort()
            s = getSideCount(sameSide)
            print(f"Same {sameSide} has {s} distinct sides.")
            sideCount = sideCount + s
    return sideCount



def getNextRegion2(plots,regions):
    x=0;y=0
    while y<MAX:
        if plots[y][x]=='.':
            x=x+1
            if x==MAX: 
                x=0; y=y+1
        else:
            break
    if y==MAX: return False

    vegType = plots[y][x]
    (area,edges) = findEdges(plots,x,y)
    # update plots
    for y in range(MAX):
        for x in range(MAX):
            if plots[y][x] == '#' : plots[y][x] = '.'

    print(f"'{vegType}' has area {area} and {len(edges)} edges.")

    sides = countSides(edges)

    if vegType in regions:
        regions[vegType].append((area, sides))
    else:
        regions[vegType] = [(area, sides)]
    return True

def getRegions2(plots):
    regions= {} # map char to (area, fences)
    while getNextRegion2(plots,regions) : continue
    return regions

def doPart1(db):
    plots = getArray(db)
    s = 0
    regions=getRegions(plots)
    for r in regions:
        l = regions[r]
        for (a,f) in l:
            s = s + a*f
    return s
   

def doPart2(db):
    plots = getArray(db)
    s = 0
    regions=getRegions2(plots)
    for r in regions:
        l = regions[r]
        for (a,f) in l:
            print(f"Region {r} has cost {a}*{f} = {a*f}")
            s = s + a*f
    return s

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#p1 = doPart1(db)
#print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"Part 2 is {p2}")
