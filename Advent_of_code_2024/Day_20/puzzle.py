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
MAX=15; MINSAVED=50; NUMCHEATS=6

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

def cheats2(maze, sx, sy, eX, eY, pathCostTo, path):
    print(f"cheats2 from {sx},{sy} to {eX},{eY}")
    atLeast100 = 0
    cheats = {}
    m = copy.deepcopy(maze)
    for x,y in path:
        pcost = pathCostTo[1000*x+y]
        for xdelta in range(-NUMCHEATS, NUMCHEATS+1):
            yswing = abs(NUMCHEATS-xdelta)
            for ydelta in range(-yswing, yswing+1):
                px=x+xdelta; py=y+ydelta
                if px<1 or px>=MAX or py<1 or py>=MAX: continue
                if px!=x or py!=y:
                    if m[py][px] not in '.E':
                        continue
                    #m[py][px] = '*'
                    cheatID = f"{x}_{y}_{px}_{py}"
                    #if cheatID in cheats: 
                    #    continue
                    cheatCost = abs(xdelta) + abs(ydelta)
                    if cheatCost < 2: continue
                    saved = pathCostTo[1000*px+py] - pcost - cheatCost
                    if (x==1) and (y==3):print(f"Cheat {cheatID} goes from {pcost} to {pathCostTo[1000*px+py]} at a cost of {cheatCost} - SAVING IS {saved}")
                    if saved >= MINSAVED:
                        cheats[cheatID] = saved
                        atLeast100 = atLeast100 + 1
        #printMaze(m)
        #sys.exit(1)
    print(f"Found {atLeast100} cheats")
    return cheats

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
    printMaze(maze)
    cheats = cheats2(maze, sx,sy,ex,ey,pathCostTo,path)
    saved = []
    for c in cheats: 
        if cheats[c] not in saved: saved.append(cheats[c])
    saved.sort()
    for val in saved:
        num = 0
        for c in cheats: 
            if cheats[c] == val: num = num + 1
        print(f"{num} cheats save {val} ps")
    
#---------------------------------------------------------------------------------------
# Load input
db = load_db()
#sys.setrecursionlimit(10000)
#p1 = doPart1(db)
#print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
