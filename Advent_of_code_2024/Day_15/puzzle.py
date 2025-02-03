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
MAX=50


def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def getWarehouse(db):
    rx=-1
    ry=-1
    warehouse = [ ['.' for x in range(MAX)] for y in range(MAX) ]
    for y,l in enumerate(db):
        if len(l) >0 and l[0] == '#':
            for x,c in enumerate(l):
                warehouse[y][x] = c
                if c == '@':
                    rx=x; ry=y

    return warehouse, rx, ry

def printWarehouse(warehouse):
    for y in range(MAX):
        print(f"{y} ",end='')
        for x in range(MAX):
            print(f"{warehouse[y][x]}",end='')
        print("")
    print("")

def getCommands(db):
    cmds=[]
    for l in db:
        if len(l)>0 and l[0] in '<>^v':
            cmds.extend(list(l))
    return cmds

# use memoization memo cacheing
#@functools.cache


def moveBox(warehouse, bx, by, xs, ys):
    nbx = bx + xs; nby = by + ys
    c = warehouse[nby][nbx]
    if c == '#': return False, warehouse
    if c == '.': 
        warehouse[nby ][nbx]='O'
        warehouse[by][bx]='.'
        return True, warehouse
    # its a box
    ok, warehouse = moveBox(warehouse, nbx, nby ,xs,ys)
    if not ok:
        return False, warehouse
    warehouse[nby ][nbx]='O'
    warehouse[by][bx]='.'
    return True, warehouse



def applyCommand(cmd, warehouse,rx,ry):
    xs=0; ys=0
    if cmd == '<': xs=-1
    elif cmd == '>': xs = 1
    elif cmd == '^':ys = -1
    elif cmd == 'v': ys = 1
    else:
        print(f"Unknown cmd {cmd}")
        sys.exit(1)
    nrx = rx + xs; nry = ry + ys
    # check wall
    c = warehouse[nry][nrx]
    if c == '#': return warehouse,rx,ry
    if c == '.': 
        warehouse[nry][nrx]='@'
        warehouse[ry][rx]='.'
        return warehouse, nrx, nry
    # its a box
    ok, warehouse = moveBox(warehouse, nrx, nry,xs,ys)
    if not ok:
        return warehouse,rx,ry
    warehouse[nry][nrx]='@'
    warehouse[ry][rx]='.'
    return warehouse, nrx, nry
    

def runCommands(cmds, warehouse, rx, ry):
    #print("\033[2J")
    for cmd in cmds:
        w,rx,ry = applyCommand(cmd, warehouse, rx, ry)
        warehouse = w
        #print("\033[H")  # Move cursor to top-left corner
        #printWarehouse(warehouse)

    return w

def doPart1(db):
    s = 0
    warehouse,rx,ry = getWarehouse(db)
    cmds = getCommands(db)

    #printWarehouse(warehouse)
    #print(f"Robot at {rx},{ry}")
    print(f"Have {len(cmds)} commands.")

    warehouse = runCommands(cmds, warehouse, rx, ry)

    printWarehouse(warehouse)

    for y in range(MAX):
        for x in range(MAX):
            c = warehouse[y][x]
            if c  == 'O' : s = s + 100*y + x

    return s

def doPart2(db):
    s = 0
    
    return s

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

p1 = doPart1(db)
print(f"Part 1 is {p1}")

db = load_db()
#p2 = doPart2(db)
#print(f"Part 2 is {p2}")
