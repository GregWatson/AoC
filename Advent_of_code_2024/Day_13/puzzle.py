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

def getMinTokens(g):
    minSoFar = 100000000
    prizeX = g['P'][0]; prizeY = g['P'][1]
    (ax, ay) = g['A']
    (bx, by) = g['B']
    x=0;y=0
    aPushes = 0
    while x <= prizeX and y <= prizeY:
        # Can we use just B button to get to prize?
        if (prizeX - x) % bx == 0:  # yes
            bPushes = (prizeX - x) / bx
            if y + bPushes*by == prizeY:
                print(f"from ({x},{y}) it is {bPushes} B pushes to get to Prize ({prizeX},{prizeY})")
                cost = aPushes*3 + bPushes
                if cost < minSoFar: minSoFar = cost
        x = x + ax; y = y + ay
        aPushes = aPushes + 1
    if minSoFar < 100000000: return minSoFar
    else: return 0  # cant get to prize

def getMinTokens2(g,adder=0):
    cost = 0
    prizeX = g['P'][0] + adder; prizeY = g['P'][1] + adder
    (ax, ay) = g['A']
    (bx, by) = g['B']
    bPushes = ((prizeX * ay) - (ax * prizeY)) / (bx * ay - by * ax)
    aPushes = (prizeX - bPushes * bx)/ax
    # print(f"{aPushes} aPushes and {bPushes} B pushes to get to Prize ({prizeX},{prizeY})")
    if (int(bPushes) == bPushes) and (int(aPushes) == aPushes):
        cost = 3 * aPushes + bPushes
        print(f"---- {aPushes} aPushes and {bPushes} B pushes to get to Prize ({prizeX},{prizeY})")
    return cost

def doPart1(db):
    s = 0
    games = getGames(db)
    for game in games: 
        s =  s + getMinTokens2(game)
    return s
   

def doPart2(db):
    s = 0
    games = getGames(db)
    for g in games:
        s =  s + getMinTokens2(g,10000000000000)
    return int(s)

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

p1 = doPart1(db)
print(f"Part 1 is {p1}")

db = load_db()
p2 = doPart2(db)
print(f"Part 2 is {p2}")
