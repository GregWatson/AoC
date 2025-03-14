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
#MAX=15; MINSAVED=50; NUMCHEATS=20

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def getMaze(db):
    maze =  [ ['.' for x in range(MAX)] for y in range(MAX) ]
    for y,l in enumerate(db):
        if len(l):
            for x,c in enumerate(l):
                maze[y][x] = c
                if c == 'S': sx,sy = x,y
                if c == 'E': ex,ey = x,y
    return maze, sx,sy, ex, ey

def printMaze(maze):
    for y in range(MAX): 
        for x in range(MAX): 
            print(f"{maze[y][x]}",end='')
        print('')
    print('')




def walkPath(maze, sx, sy, eX, eY):
    print(f"walkPath from {sx},{sy} to {eX},{eY}")
    cost = 0
    pathCostTo = {}
    path = []
    x = sx; y = sy
    m = copy.deepcopy(maze)
    pathCostTo[1000*sx+sy] = 0
    path.append((x,y))
    while (x!=eX) or (y!=eY):
        m[y][x]='O'
        numOptions = 0
        for xs,ys in ((1,0),(-1,0),(0,1),(0,-1)):
            newx=x+xs; newy=y+ys
            if m[newy][newx] in '.E':
                nx=newx; ny=newy
                numOptions = numOptions+1
        if numOptions != 1:
            printMaze(m)
            print(f"At {x},{y} options = {numOptions}")
            sys.exit(1)
        x = nx; y = ny; cost = cost + 1
        pathCostTo[1000*x+y] = cost
        path.append((x,y))
    # printMaze(m)
    return pathCostTo, path

def walkWithCheats(maze, sx, sy, eX, eY, pathCostTo, path):
    print(f"walkPath with cheats from {sx},{sy} to {eX},{eY}")
    atLeast100 = 0
    m = copy.deepcopy(maze)
    for x,y in path:
        pcost = pathCostTo[1000*x+y]
        m[y][x] = 'O'
        # Try the 4 directions
        for xs,ys in ((1,0),(-1,0),(0,1),(0,-1)):
            wx=x+xs; wy=y+ys
            if m[wy][wx] != '#': continue  
            # try cheat
            tx=wx+xs; ty=wy+ys  # NEXT TILE
            if (tx<0)or (tx>=MAX)or(ty<0)or(ty>=MAX): continue
            if m[ty][tx] in '.E': # Yes, going through 1 wall gets us to a later path
                loc=1000*tx+ty
                if not loc in pathCostTo:
                    print(f"ERROR: Found path {tx},{ty} but it has no cost info")
                    sys.exit(1)
                costSaving = pathCostTo[loc] - pcost - 2
                print(f"{x},{y}: cheat wall at {wx},{wy}. Start cost is {pcost} cost at {tx},{ty} is {pathCostTo[loc]} So saving is {costSaving}")
                if costSaving >= 100: 
                    atLeast100 = atLeast100 + 1
    return atLeast100

def getToExitDirectly(x,y,eX,eY):
    dist = abs(x-eX) + abs(y-eY)
    return dist <= NUMCHEATS

def cheats2(path):
    print(F"len path is {len(path)}")
    count  = 0
    for i,(x,y) in enumerate(path[0:-100]):
        # print(f"{i} is {x},{y}")
        for i2, (x2,y2) in enumerate(path[i+100:]):
            dist = abs(x-x2) + abs(y-y2)
            if dist <= NUMCHEATS and (i2 - dist) >= 0:
                count = count + 1
    print(f"Count is {count}")
    return count



def doPart1(db):
    maze, sx,sy, ex, ey = getMaze(db)
    pathCostTo, path = walkPath(maze, sx,sy,ex,ey)
    print(f"Original Track len is {len(pathCostTo)}")
    # printMaze(maze)
    s = walkWithCheats(maze, sx,sy,ex,ey,pathCostTo,path)
    return s


def doPart2(db):
    maze, sx,sy, ex, ey = getMaze(db)
    pathCostTo, path = walkPath(maze, sx,sy,ex,ey)
    print(f"Original Track len is {len(pathCostTo)}")
    # printMaze(maze)
    cheats = cheats2(path)
    return cheats
    
#---------------------------------------------------------------------------------------
# Load input
db = load_db()
#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
