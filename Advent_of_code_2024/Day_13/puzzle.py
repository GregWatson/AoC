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


def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def getGames(db):
    games = []
    while(len(db)):
        l = db.pop(0)
        m = re.match(r'Button A: X\+(\d+), Y\+(\d+)', l)
        if m:
            g = {'A': (int(m.group(1)), int(m.group(2)))}
            l = db.pop(0)
            m = re.match(r'Button B: X\+(\d+), Y\+(\d+)', l)
            if m:
                g ['B'] = ((int(m.group(1))), int(m.group(2)))
                l = db.pop(0)
                m = re.match(r'Prize: X=(\d+), Y=(\d+)', l)
                if m:
                    g['P'] = ((int(m.group(1))), int(m.group(2)))
                    print(f"A:{g['A']} B:{g['B']},  Prize:{g['P']}")
                    games.append(g)
    return games

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


def doPart1(db):
    s = 0
    games = getGames(db)
    return s
   

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
