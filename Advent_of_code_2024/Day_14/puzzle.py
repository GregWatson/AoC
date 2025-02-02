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
WIDTH=101
HEIGHT=103


def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

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

class Robot:
    def __init__(self, x:int, y:int, xs:int, ys:int ):
        self.x=x
        self.y=y
        self.xs=xs
        self.ys=ys

    def print(self):
        print(f"Robot at ({self.x},{self.y})  speed: ({self.xs},{self.ys})")
    
    def move(self):
        newx=(self.x + self.xs) % WIDTH
        newy=(self.y + self.ys) % HEIGHT
        self.x = newx
        self.y = newy
    
    def getQuad(self):
        if (self.x < 50):
            if (self.y < 51): return 0
            if (self.y > 51): return 1
            return 4
        if (self.x > 50):
            if (self.y < 51): return 2
            if (self.y > 51): return 3
        return 4
        
    # def addUsed(self,add:int):
    #     self.used = self.used + add
    #     if self.used > self.size:
    #         print(f"Error: node {x}:{y} exceeded its storage (add {add} but that makes size {self.size})")
    #         sys.exit(1)

def parseDB(db):
    robots=[]
    for l in db:
        m = re.match(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)',l)
        if m:
            r = Robot(x=int(m.group(1)), y=int(m.group(2)), xs=int(m.group(3)), ys=int(m.group(4)))
            r.print()
            robots.append(r)
    return robots

def makeBathroom(robots):
    bathroom = [ ['_' for x in range(WIDTH)] for y in range(HEIGHT) ]
    for r in robots:
        bathroom[r.y][r.x]="#"
    return bathroom

def showBathroom(bathroom):
    # print("\033[2J")
    for l in bathroom:
        for c in l:
            print(f"{c}",end='')
        print(f"\n")
    print(f"\n")

def looksLikeTree(bathroom):
    for l in bathroom:
        s = ''.join(l)
        if '########' in s: return True
    return False

def doPart1(db):
    s = 0
    robots = parseDB(db)
    for i in range(100):
        for r in robots: r.move()

    quadCounts = [0,0,0,0,0]
    for r in robots:
        quadCounts[r.getQuad()] = quadCounts[r.getQuad()]+1
            
    print(f"{quadCounts}")
    s = quadCounts[0] * quadCounts[1] * quadCounts[2] * quadCounts[3]
    return s
   

def doPart2(db):
    s = 0
    robots = parseDB(db)
    while True:
        for r in robots: r.move()
        s = s+1
        bathroom = makeBathroom(robots)
        if looksLikeTree(bathroom):
            showBathroom(bathroom)
            print(f"Count={s}")
    return s

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

p1 = doPart1(db)
print(f"Part 1 is {p1}")

db = load_db()
p2 = doPart2(db)
#print(f"Part 2 is {p2}")
