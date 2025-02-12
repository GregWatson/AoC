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
MAX=71


def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

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
                    nx=x+xs; ny=y+ys
                    if nx<0 or nx>=MAX or ny<0 or ny>=MAX: continue
                    if maze[ny][nx] == '.': c = c + 1
                if c == 1: # deadend
                    removedSome = True
                    maze[y][x] = '#'
                    dcount = dcount + 1
    print(f"Deleted {dcount} tiles as deadends.")
    return maze

def getJunctions(maze):
    isJunction = [ array.array('i',[0 for x in range(MAX)]) for y in range(MAX) ]
    for y in range(MAX):
        for x in range(MAX):
            if not maze[y][x] == '.': continue
            numxdots = 0
            for xs in [1,-1]:
                if (x+xs)<0 or (x+xs)>=MAX: continue
                if maze[y][x+xs] in '.SE': numxdots=numxdots+1
            numydots = 0
            for ys in [1,-1]:
                if (y+ys)<0 or (y+ys)>=MAX: continue
                if maze[y+ys][x] in '.SE': numydots=numydots+1
            numdots = numxdots + numydots
            if numdots > 2: isJunction[y][x] = 1
            elif numdots==1: isJunction[y][x] = 1
            else: 
                if numxdots == 1 and numydots == 1:
                    isJunction[y][x] = 1
    return isJunction

def getMaze(db, numLines):
    maze =  [ ['.' for x in range(MAX)] for y in range(MAX) ]
    for i,l in enumerate(db):
        m = re.match(r'(\d+),(\d+)',l)
        if i<numLines and m:
            x = int(m.group(1)); y = int(m.group(2))
            maze[y][x] = '#'

    # maze = removeDeadEnds(maze)

    isJunction = getJunctions(maze)
    return maze, isJunction


def printMaze(maze):
    for y in range(MAX): 
        for x in range(MAX): 
            print(f"{maze[y][x]}",end='')
        print('')
    print('')

def getCheapestCostTo(maze, isJunction, costTo, x, y, exitX, exitY, costSoFar=0, depth=0, path=[]):
    indent=' '*(depth>>2)
    #print(f"{indent}getCCost ({x},{y}) {path}")
    # If we have already been here with a lower cost then quit
    if costSoFar >= costTo[y][x]:
        # print(f"{indent}-- CostTo {x},{y} is {costSoFar} which is more than {costTo[y][x]} so abandoning.")
        return []
    costTo[y][x] = costSoFar

    if x==exitX and y==exitY: # at exit
        # print(f"{indent}-- At EXIT! path is {path}")
        return path

    cheapest = BIGNUM
    cheapestPath = []

    for newxs,newys in ((1,0),(-1,0),(0,1),(0,-1)):
        tx = x+newxs; ty = y+newys; 
        if tx<0 or tx>=MAX or ty<0 or ty>=MAX: continue
        if maze[ty][tx] == '#': 
            continue   # dont walk into a wall
        if (tx,ty) in path: continue
        newCostSoFar = costSoFar + 1
        newPath = path[:]
        newPath.append((tx,ty))
        #print(f"{indent}--({x},{y}) Trying loc {tx},{ty}  Depth {depth}")
        # keep moving until we are at a junction
        abort = False
        while isJunction[ty][tx] == 0: # not a junction
            assert maze[ty][tx] is '.'
            tx = tx+newxs; ty = ty+newys; 
            if (tx,ty) in path: 
                abort = True
            else:
                newCostSoFar = newCostSoFar + 1
                newPath.append((tx,ty))
        if abort: continue
        p = getCheapestCostTo(maze, isJunction, costTo, tx, ty, exitX, exitY, newCostSoFar, depth=depth+1, path=newPath)
        if len(p):
            if len(p) < cheapest: 
                cheapest = len(p)
                cheapestPath = p
                # print(f"{indent}--New Cheapest path is len {len(p)} {p}")
    return cheapestPath



def doPart1(db):
    maze, isJunction = getMaze(db, numLines=1024)
    printMaze(maze)
    costTo = [ array.array('L',[BIGNUM for x in range(MAX)]) for y in range(MAX) ]
    getCheapestCostTo(maze, isJunction, costTo, 0, 0, MAX-1, MAX-1, costSoFar=0, depth=0, path=[])    
    return costTo[MAX-1][MAX-1]

def doPart2(db, shortest):
    maze, isJunction = getMaze(db, numLines=1024)
    costTo = [ array.array('L',[BIGNUM for x in range(MAX)]) for y in range(MAX) ]
    path = getCheapestCostTo(maze, isJunction, costTo, 0, 0, MAX-1, MAX-1, costSoFar=0, depth=0, path=[])    
    for i,l in enumerate(db):
        m = re.match(r'(\d+),(\d+)',l)
        if i>=1024 and m:
            x = int(m.group(1)); y = int(m.group(2))
            maze[y][x] = '#'
            if ((x,y)) in path:
                isJunction = getJunctions(maze)
                costTo = [ array.array('L',[BIGNUM for x in range(MAX)]) for y in range(MAX) ]
                path = getCheapestCostTo(maze, isJunction, costTo, 0, 0, MAX-1, MAX-1, costSoFar=0, depth=0, path=[])
                if (costTo[MAX-1][MAX-1] != BIGNUM): 
                    print(f"{x},{y} has solution: {costTo[MAX-1][MAX-1]} ")
                else: return f"{x},{y}"
            else:
                print(f"{x},{y} not in path.")
    return "No Solution found."
    
#---------------------------------------------------------------------------------------
# Load input
db = load_db()
sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}")

p2 = doPart2(db, p1)
print(f"\n\n\n\nPart 2 is {p2}")
