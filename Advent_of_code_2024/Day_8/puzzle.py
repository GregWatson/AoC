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

def getArray(db):
    a = [ array.array('u',['.' for x in range(MAX)]) for y in range(MAX) ]
    for y,l in enumerate(db):
        for x,c in enumerate(l):
            a[y][x] = c
    return a

def drawArray(a):
    # field
    addCuboid(POS=(0,0,0), SCALE=(MAX,MAX,0.1), COL=GREEN80)
    for y in range(MAX):
        for x in range(MAX):
            c = a[y][x]
            if c != '.':
                col = charToCol(c)
                if c.isalnum():
                    addCuboid(POS=(x,MAX-1-y,0), COL=col)
                else:
                    addVertCylinder(POS=(x, MAX-1-y,0), SCALE=(0.2,0.2,5),COL=col)

def addAntinodes(a):
    antennaPos= {}
    num = 0
    antennaField = [ array.array('u',['.' for x in range(MAX)]) for y in range(MAX) ]
    for y in range(MAX):
        for x in range(MAX):
            c = a[y][x]
            if c == '.' or c == '!': continue
            if not c in antennaPos:
                antennaPos[c] = [(x,y)]
                continue
            for (x1,y1) in antennaPos[c]:
                L = [( x1 + x1 - x, y1 + y1 - y), (x + x - x1, y + y - y1)]
                for (nx,ny) in L:
                    if nx<0 or nx>=MAX or ny<0 or ny>=MAX: continue
                    if antennaField[ny][nx] == '!': continue
                    antennaField[ny][nx] = '!'
                    num = num + 1
                    if a[ny][nx] == '.': a[ny][nx] = '!'
            antennaPos[c].append((x,y))
    return (a, num)


def addAntinodes2(a):
    antennaPos= {}
    num = 0
    antennaField = [ array.array('u',['.' for x in range(MAX)]) for y in range(MAX) ]
    for y in range(MAX):
        for x in range(MAX):
            c = a[y][x]
            if c == '.': continue
            if not c in antennaPos:
                antennaPos[c] = [(x,y)]
                continue
            for (x1,y1) in antennaPos[c]:
                if antennaField[y][x] != '!':
                    antennaField[y][x] = '!'
                    num = num + 1
                if antennaField[y1][x1] != '!':
                    antennaField[y1][x1] = '!'
                    num = num + 1
                dxdy= [(x1-x, y1-y), (x-x1, y-y1)]
                for (dx,dy) in dxdy:
                    nx=x+dx; ny=y+dy
                    while nx>=0 and nx<MAX and ny>=0 and ny<MAX:
                        if antennaField[ny][nx] != '!':
                            antennaField[ny][nx] = '!'
                            num = num + 1
                        nx=nx+dx; ny=ny+dy
            antennaPos[c].append((x,y))
    return (a, num)


def doPart1(db):
    s = 0
    a = getArray(db)
    an, s = addAntinodes(a)
    drawArray(an)
    return s
   

# Only try obstructions at locations that have been visited
def doPart2(db):
    s = 0
    a = getArray(db)
    an, s = addAntinodes2(a)
    return s

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#p1 = doPart1(db)
#print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"Part 2 is {p2}")



