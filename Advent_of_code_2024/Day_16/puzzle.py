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
print_on = True
MAX=141
MAX=15
BIGNUM=100000000

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def printMaze(maze):
    print('   012345678901234')
    for y in range(MAX): 
        print(f"{y} ",end='')
        if y < 10: print(' ',end='')
        for x in range(MAX): 
            print(f"{maze[y][x]}",end='')
        print('')
    print('   012345678901234')

def getMaze(db):
    maze = [ ['.' for x in range(MAX)] for y in range(MAX)]
    for y,l in enumerate(db):
        for x,c in enumerate(l):
            maze[y][x] = c
            if c == 'S': sx=x; sy=y
    costFrom = [ array.array('L',[BIGNUM for x in range(MAX)]) for y in range(MAX) ]
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
    return maze, isJunction, costFrom,sx,sy

def getCheapestCostFrom(maze, isJunction, costFrom, x, y, xs, ys , been={},depth=0):
    indent=' '*(depth*2)
    if print_on: print(f"{indent}getCCost ({x},{y}) dir={xs},{ys}")
    if maze[y][x] == 'E': 
        costFrom[y][x] = 0
        return 0
    loc=1000*y+x
    if loc in been: return -1 # stop -  already visited
    been[loc] = 1
    cheapest = BIGNUM
    foundPath = False
    for newxs,newys in ((1,0),(-1,0),(0,1),(0,-1)):
        if newxs+xs == 0 and newys+ys == 0: # dont try going back
            continue
        if maze[y+newys][x+newxs] == '#': 
            continue   # dont walk into a wall
        if print_on: print(f"{indent}--({x},{y}) Trying dir {newxs},{newys}   Depth {depth}")
        moveCost = 0
        if newxs != xs or newys != ys: moveCost = moveCost + 1000  # made a turn
        tx = x+newxs; ty = y+newys; moveCost = moveCost + 1
        # keep going until a junction
        while isJunction[ty][tx] == 0: # not a junction
            tx = tx+newxs; ty = ty+newys; moveCost = moveCost + 1
        if costFrom[ty][tx] == BIGNUM: # not known
            c = getCheapestCostFrom(maze, isJunction, costFrom, tx, ty, newxs, newys , been=copy.copy(been), depth=depth+1)
            if c >= 0 and c < costFrom[ty][tx]:
                costFrom[ty][tx] = c
                if print_on: print(f"{indent}--The cost from {tx},{ty} is {c}")
        else: 
            c = costFrom[ty][tx]
        if c>=0:
            total = moveCost + c
            if total < cheapest: cheapest = total
            foundPath = True
    if foundPath: 
        if cheapest < costFrom[y][x]: 
            costFrom[y][x] = cheapest
            if print_on: print(f"{indent}--After choices, the cost from {x},{y} is {costFrom[y][x]}")
        return cheapest
    else: return -1
    

def doPart1(db):
    s = 0
    maze, isJunction, costFrom, sx,sy = getMaze(db)
    printMaze(maze)
    s  = getCheapestCostFrom(maze, isJunction, costFrom, sx,sy,1,0)
    return s

def doPart2(db):
    s = 0

    return s

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
sys.setrecursionlimit(2000)
p1 = doPart1(db)
print(f"Part 1 is {p1}")

#db = load_db()
#p2 = doPart2(db)
#print(f"\n\n\n\nPart 2 is {p2}")
