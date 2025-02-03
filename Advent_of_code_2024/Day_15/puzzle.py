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

def getWarehouse2(db):
    rx=-1
    ry=-1
    warehouse = [ ['.' for x in range(2*MAX)] for y in range(MAX) ]
    for y,l in enumerate(db):
        if len(l) >0 and l[0] == '#':
            for x,c in enumerate(l):
                warehouse[y][2*x] = c
                warehouse[y][2*x+1] = c
                if c == 'O':
                    warehouse[y][2*x] = '['
                    warehouse[y][2*x+1] = ']'
                if c == '@':
                    warehouse[y][2*x+1] = '.'
                    rx=2*x; ry=y

    return warehouse, rx, ry

def printWarehouse(warehouse):
    for y in range(MAX):
        print(f"{y} ",end='')
        if y < 10: print(' ',end='')
        for x in range(len(warehouse[0])):
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


def moveBox2(warehouse, x, by, xs, ys):
    bc = warehouse[by][x]
    print(f"    moveBox2 called x={x} by={by}  xs,ys={xs},{ys}  box char is {bc}")
    if not bc in '[]':
        print(f"Expected to see box at {x},{by} but found char {bc}")
        sys.exit(1)
    # always use left side of box as reference.
    if bc == '[':
        bx=x
    elif bc == ']':
        bx=x-1
    nbx = bx + xs; nby = by + ys

    cl = warehouse[nby][nbx]; cr = warehouse[nby][nbx+1]

    if ys == 0: # only move left or right.
        if xs == -1: # move left
            if cl == '#' : return False, warehouse
            if cl == '.' : 
                warehouse[by][bx]='.'; warehouse[by][bx+1]='.'
                warehouse[by][bx-1]='['; warehouse[by][bx]=']'
                return True, warehouse
            if cl == ']':
                ok, warehouse = moveBox2(warehouse, nbx, nby ,xs,ys)
                if not ok:
                    return False, warehouse
                warehouse[by][bx]='.'; warehouse[by][bx+1]='.'
                warehouse[by][bx-1]='['; warehouse[by][bx]=']'
                return True, warehouse
            else:
                print(f"Error move left - expected to see ] but saw {cl}")
                sys.exit(1)

        # Move box right (xs=1)
        
        if cr == '#' : return False, warehouse
        if cr == '.' : 
            warehouse[by][bx]='.'; warehouse[by][bx+1]='.'
            warehouse[by][bx+1]='['; warehouse[by][bx+2]=']'
            return True, warehouse
        if cr == '[':
            ok, warehouse = moveBox2(warehouse, bx+2, nby ,xs,ys)
            if not ok:
                return False, warehouse
            warehouse[by][bx]='.'; warehouse[by][bx+1]='.'
            warehouse[by][bx+1]='['; warehouse[by][bx+2]=']'
            return True, warehouse
        else:
            print(f"Error move left - expected to see [ but saw {cr}")
            sys.exit(1)
    # Move up or Down - might move 2 boxes
    assert xs==0
    print(f"    Moving {ys}.  cl,cr = {cl}{cr}")
    if cl=='#' or cr=='#' : return False,warehouse
    if cl=='.' and cr=='.' :
        warehouse[by][bx]='.'; warehouse[by][bx+1]='.'
        warehouse[nby][bx]='['; warehouse[nby][bx+1]=']'
        return True,warehouse
    if cl == '[': # just move one box
        ok, warehouse = moveBox2(warehouse, nbx, nby, xs, ys)
        if not ok:
            return False, warehouse
        warehouse[by][bx]='.'; warehouse[by][bx+1]='.'
        warehouse[nby][bx]='['; warehouse[nby][bx+1]=']'
        return True,warehouse
    # Move two boxes
    origWarehouse = copy.deepcopy(warehouse)
    if cl == '.': okl = True
    else:
        okl, warehouse = moveBox2(warehouse, nbx, nby, xs, ys)
    if cr == '.': okr = True
    else:
        okr, warehouse = moveBox2(warehouse, nbx+1, nby, xs, ys)
    if okl and okr:
        warehouse[by][bx]='.'; warehouse[by][bx+1]='.'
        warehouse[nby][nbx]='['; warehouse[nby][bx+1]=']' 
        return True, warehouse

    return False, origWarehouse


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
    

def applyCommand2(cmd, warehouse,rx,ry):
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

    print(f"Cmd is {cmd} robot= {rx},{ry}  xs={xs}  ys={ys}  nrx={nrx}  nry={nry}   char at nrx,nry is {c}")

    if c == '#': return warehouse,rx,ry
    if c == '.': 
        warehouse[nry][nrx]='@'
        warehouse[ry][rx]='.'
        return warehouse, nrx, nry
    # its a box - either [ or ]
    ok, warehouse = moveBox2(warehouse, nrx, nry,xs,ys)
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

def runCommands2(cmds, warehouse, rx, ry):
    print("\033[2J")
    for i,cmd in enumerate(cmds):
        w,rx,ry = applyCommand2(cmd, warehouse, rx, ry)
        warehouse = w
        print("\033[H")  # Move cursor to top-left corner
        printWarehouse(warehouse)

        print(f"\nCmd {i} of {len(cmds)} was {cmd}.                                            ")
        #tmp = input("Press return")

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
    warehouse,rx,ry = getWarehouse2(db)
    cmds = getCommands(db)

    #printWarehouse(warehouse)
    print(f"Robot at {rx},{ry}")
    print(f"Have {len(cmds)} commands.")

    warehouse = runCommands2(cmds, warehouse, rx, ry)

    # printWarehouse(warehouse)

    for y in range(MAX):
        for x in range(2*MAX):
            c = warehouse[y][x]
            if c  == '[' : s = s + 100*y + x
    return s

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#p1 = doPart1(db)
#print(f"Part 1 is {p1}")

db = load_db()
p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
