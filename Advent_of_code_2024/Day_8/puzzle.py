#import argparse
import sys
import re
import functools
import array
import copy
import hashlib
import string
import itertools

# --- Blender ---
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
    # for y in range(MAX):
    #     for x in range(MAX):
    #         c = a[y][x]
    #         if c != '.':
    #             col = charToCol(c)
    #             addCuboid(POS=(x,MAX-1-y,0), COL=col)
    addVertCylinder(POS=(0,0,0), SCALE=(0.2,0.2,5),COL=RED80)     

def doPart1(db):
    s = 0
    a = getArray(db)
    drawArray(a)
    return s
   

# Only try obstructions at locations that have been visited
def doPart2(db):
    s = 0
    return s

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

p1 = doPart1(db)
print(f"Part 1 is {p1}")

#p2 = doPart2(db)
#print(f"Part 2 is {p2}")



