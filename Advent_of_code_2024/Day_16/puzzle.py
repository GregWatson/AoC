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
MAX=141 
#MAX=15
#MAX=17 # small2
#MAX=5  #tiny
BIGNUM=100000000
minPath = 1

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def printMaze(maze):
    print('    012345678901234')
    for y in range(MAX): 
        print(f"{y} ",end='')
        if y < 10: print('  ',end='')
        elif y < 100: print(' ',end='')
        for x in range(MAX): 
            print(f"{maze[y][x]}",end='')
        print('')
    print('    012345678901234')

def removeDeadEnds(maze):
    removedSome = True
    dcount = 0
    while removedSome:
        removedSome = False
        for y in range(MAX):
            for x in range(MAX):
                if maze[y][x] != '.': continue
                c = 0
                for xs, ys in ((0,-1),(0,1),(-1,0),(1,0)):
                    if maze[y+ys][x+xs] in 'SE.': c = c + 1
                if c == 1: # deadend
                    removedSome = True
                    maze[y][x] = '#'
                    dcount = dcount + 1
    print(f"Deleted {dcount} tiles as deadends.")
    return maze

def getDir(xs,ys):
    if xs == 1:return 'px'
    if xs == -1: return 'mx'
    if ys == 1: return 'py'
    return 'my'

def getMaze(db):
    maze = [ ['.' for x in range(MAX)] for y in range(MAX)]
    for y,l in enumerate(db):
        for x,c in enumerate(l):
            maze[y][x] = c
            if c == 'S': sx=x; sy=y
            if c == 'E': ex=x; ey=y

    maze = removeDeadEnds(maze)

    costTo = {  'px': [ array.array('L',[BIGNUM for x in range(MAX)]) for y in range(MAX) ],
                'mx': [ array.array('L',[BIGNUM for x in range(MAX)]) for y in range(MAX) ],
                'py': [ array.array('L',[BIGNUM for x in range(MAX)]) for y in range(MAX) ],
                'my': [ array.array('L',[BIGNUM for x in range(MAX)]) for y in range(MAX) ] }

    isJunction = [ array.array('i',[0 for x in range(MAX)]) for y in range(MAX) ]
    for y in range(MAX):
        for x in range(MAX):
            if not maze[y][x] in '.SE': continue
            numxdots = 0
            for xs in [1,-1]:
                if maze[y][x+xs] in '.SE': numxdots=numxdots+1
            numydots = 0
            for ys in [1,-1]:
                if maze[y+ys][x] in '.SE': numydots=numydots+1
            numdots = numxdots + numydots
            if numdots > 2: isJunction[y][x] = 1
            elif numdots==1: isJunction[y][x] = 1
            else: 
                if numxdots == 1 and numydots == 1:
                    isJunction[y][x] = 1
    return maze, isJunction, costTo,sx,sy,ex,ey

def getCheapestCostTo(maze, isJunction, costTo, x, y, xs, ys , costSoFar=0, depth=0):
    indent=' '*(depth>>2)
    if print_on: print(f"{indent}getCCost ({x},{y}) dir={xs},{ys}")
    dir = getDir(xs,ys)
    # If we have already been here with a lower cost then quit
    if costTo[dir][y][x] <= costSoFar:
        return 
    costTo[dir][y][x] = costSoFar
    #c = maze[y][x]
    #print(f"\033[{y-55};{x}H",end='') # go to x,y
    #print(f"X",end='')

    if maze[y][x] == 'E':
        return 
    loc=1000*y+x
    #if loc in been: return # stop -  already visited
    #been[loc] = 1
    for newxs,newys in ((1,0),(-1,0),(0,1),(0,-1)):
        if newxs+xs == 0 and newys+ys == 0: # dont try going back
            continue
        if maze[y+newys][x+newxs] == '#': 
            continue   # dont walk into a wall
        newCostSoFar = costSoFar
        if print_on: print(f"{indent}--({x},{y}) Trying dir {newxs},{newys}   Depth {depth}")
        if newxs != xs or newys != ys: # made a turn
            newCostSoFar = newCostSoFar + 1000 
        tx = x+newxs; ty = y+newys; newCostSoFar = newCostSoFar + 1
        # keep moving until we are at a junction
        while isJunction[ty][tx] == 0: # not a junction
            assert maze[ty][tx] is '.'
            tx = tx+newxs; ty = ty+newys; newCostSoFar = newCostSoFar + 1
        getCheapestCostTo(maze, isJunction, costTo, tx, ty, newxs, newys , newCostSoFar, depth=depth+1)


lowestCostFrom = {'px': [ array.array('L',[BIGNUM for x in range(MAX)]) for y in range(MAX) ],
                  'mx': [ array.array('L',[BIGNUM for x in range(MAX)]) for y in range(MAX) ],
                  'py': [ array.array('L',[BIGNUM for x in range(MAX)]) for y in range(MAX) ],
                  'my': [ array.array('L',[BIGNUM for x in range(MAX)]) for y in range(MAX) ] }

minSeen = 1000000
allTiles = set()

# get cheapest cost to E from x,y,
def getCheapestCostTo2(maze, isJunction, costTo, x, y, xs, ys, costSoFar=0, been=set(), depth=0):
    global minSeen, lowestCostFrom, minPath, allTiles
    indent=' '*(depth*2)
    if print_on: print(f"{indent}getCCostTo2 ({x},{y}) dir={xs},{ys} costSoFar={costSoFar}")
    dir = getDir(xs,ys) 

    if costSoFar > minSeen: return

    if maze[y][x] == 'E':
        been.add((x,y))
        # lowestCostFrom[dir][y][x] = 0
        if costSoFar < minSeen:
            if print_on: print(f"{indent}-- Best path so far is {len(been)} {costSoFar}  (Target is {minPath})")
            minSeen = costSoFar
        if costSoFar == minPath:
            if print_on: print(f"{indent}-- Found an optimal path. tile len is {len(been)} cost:{costSoFar}  (Target is {minPath})")
            if print_on: print(f"{indent}   Path: {been}")
            for t in been: allTiles.add(t)
            return
        return 

    # if we have already been here THIS PATH then quit
    if (x,y) in been:
        return 
    # If we have already been here on ANY PATH with a lower cost then quit
    if costTo[dir][y][x] < costSoFar:
        return 


    #if print_on: print(f"{indent}-- Updated lc TO ({x},{y}) dir {dir}: {costSoFar} (Was {costTo[dir][y][x]})")
    costTo[dir][y][x] = costSoFar

    been.add((x,y))

    # if we already have the lowest cost from here to END then use it
    # if lowestCostFrom[dir][y][x] < BIGNUM:
    #     finalCost = costSoFar + lowestCostFrom[dir][y][x]
    #     if print_on: print(f"{indent}-- Have already got lc from {x},{y} dir {dir} - it is {lowestCostFrom[dir][y][x]}. So TC is  {finalCost}")
    #     if finalCost == minPath:
    #         print(f"{indent}-- Found an optimal path. tile len is {len(been)} cost:{finalCost}  (Target is {minPath})")
    #         print(f"{indent}   Path: {been}")
    #         return been, lowestCostFrom[dir][y][x]
    #     return set(), lowestCostFrom[dir][y][x]

    # OK, so now we need to find the lowest path from x,y to E

    # c = maze[y][x]
    #if print_on: print(f"\033[{y-55};{x}H",end='') # go to x,y
    #if print_on: print(f"X",end='')

    b2 = set()
    dirlist= [(xs,ys,dir)]  # always keep going in same direction if we can
    for newxs,newys,newdir in ((0,-1,'my'),(0,1,'py'),(-1,0,'mx'),(1,0,'px')):
        if newdir != dir: dirlist.append((newxs,newys,newdir))
    for newxs,newys,newdir in dirlist:
        if newxs+xs == 0 and newys+ys == 0: # dont try going back
            continue
        if maze[y+newys][x+newxs] == '#': 
            continue   # dont walk into a wall
        lbeen = copy.copy(been)
        lc = 0 # track local cost as we move from x,y to next junction
        if print_on: print(f"{indent}----({x},{y}) Trying dir {newxs},{newys}   Depth {depth}  costSoFar={costSoFar}")
        if newxs != xs or newys != ys: # made a turn
            lc = lc + 1000
        tx = x+newxs; ty = y+newys; lc = lc + 1
        # keep moving until we are at a junction
        while isJunction[ty][tx] == 0: # not a junction
            lbeen.add((tx,ty))
            assert maze[ty][tx] is '.'
            tx = tx+newxs; ty = ty+newys; lc = lc + 1
        getCheapestCostTo2(maze, isJunction, costTo, tx, ty, newxs, newys , (costSoFar + lc), been=lbeen, depth=depth+1)

    #     if lcf < BIGNUM:
    #         b2 = b2 | b
    #         tc = lcf + lc
    #         if tc < lc_seen: lc_seen = tc
    #         if tc < lowestCostFrom[dir][y][x]:
    #             print(f"{indent}  -- New lc FROM ({x},{y}) dir {dir} is {tc} (was {lowestCostFrom[dir][y][x]})")
    #             lowestCostFrom[dir][y][x] = tc
    #         else:
    #             if print_on: print(f"{indent}  ... computed lowest cost from ({x},{y}) dir {dir} is {tc} but bigger than {lowestCostFrom[dir][y][x]} ")

    # if len(b2): 
    #     if print_on: print(f"{indent}({x},{y}) returning b2 len of {len(b2)}")



def doPart1(db):
    global minPath
    s = 0
    maze, isJunction, costTo, sx,sy,ex,ey = getMaze(db)
    print("\033[2J")
    printMaze(maze)
    getCheapestCostTo(maze, isJunction, costTo, sx,sy,1,0)
    p1 = min(costTo['px'][ey][ex], costTo['mx'][ey][ex],costTo['py'][ey][ex],costTo['my'][ey][ex])
    minPath = p1
    return p1

def doPart2(db):
    global minPath, lowestCostFrom
    s = 0
    maze, isJunction, costTo, sx,sy,ex,ey = getMaze(db)
    print("\033[2J")
    printMaze(maze)
    print(f"Seeking number of tiles for minpath {minPath}")
    getCheapestCostTo2(maze, isJunction, costTo, sx,sy,1,0, costSoFar=0, been=set(), depth=0)
    #if minPath < 100000:
    #    for dir in ('x','y'):
    #        for y in range(MAX):
    #            for x in range(MAX):
    #                if lowestCostFrom[dir][y][x] < BIGNUM: print(f"LC from {x},{y} dir {dir} is {lowestCostFrom[dir][y][x]}")
    return len(allTiles)

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}")

db = load_db()
p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
