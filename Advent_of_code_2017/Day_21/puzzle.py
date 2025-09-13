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
import time
import string

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
MAX=141; MINSAVED=100; NUMCHEATS=20


def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def printSquare(s):
    a = s.split('/')
    for row in a:
        print(row)
    print()

def getSquareSize(s):
    l = len(s)
    assert l in (5,11,19)
    return 2 if l==5 else 3 if l==11 else 4 

def printGridRow(row):
    grids = [ r.split('/') for r in row ]
    for l in range(len(grids[0])):
        print(f"|", end='')
        for g in grids:
            print(g[l], end='|')
        print()

class Grid:
    # A grid is a list of rows, each row is a list of squares (strings)
    def __init__(self, square=None):
        self.rows = []
        if square: # initialize with a single row of a single square
            self.rows.append([square])
            self.setInfo()

    def setInfo(self):
        if len(self.rows):
            self.width = len(self.rows[0])
            self.numSquares = self.width * self.width
            self.squareWidth = getSquareSize(self.rows[0][0])
            self.printWidth = self.width * (self.squareWidth + 1) + 1

    def addRow(self, row):
        self.rows.append(row)
        if len(self.rows) == 1:
            self.setInfo()

    def printGrid(self):
        print(f"{'-' * self.printWidth}")
        for row in self.rows:
            printGridRow(row)
            print(f"{'-' * self.printWidth}")
        print()

    def processRow(self, row, enh):
        newRow = []
        for square in row:
            if square in enh:
                newSquare = enh[square]
                newRow.append(newSquare)
            else:
                print(f"Did not find {square} in enhancements")
                sys.exit(1)
        print(f"Processed row of {len(row)} squares into {len(newRow)} squares\n{newRow}")
        return newRow

    def resize4to2(self): # 4x4 => 4 2x2
        newRows = []
        for row in self.rows:
            r0 = []
            r1 = []
            for sq in row:
                l = fracture(sq)
                r0.extend(l[0:2])
                r1.extend(l[2:4])
            newRows.append(r0)
            newRows.append(r1)
        self.rows = newRows
        self.setInfo()

    # process 2 rows of 3x3 at a time to yield 3 rows of 2x2
    def resize3to2(self): # 4 3x3 => 9 2x2
        newRows = []
        for ri in range(0, len(self.rows), 2):
            r3a = self.rows[ri]; r3b = self.rows[ri+1]
            r0 = []; r1 = []; r2 = []
            for si in range(0, len(self.rows[0]), 2):
                l0 = r3a[si].split('/'); l1 = r3a[si+1].split('/'); l2 = r3b[si].split('/'); l3 = r3b[si+1].split('/')
                s2_0 = l0[0][0:2] + '/' + l0[1][0:2]
                s2_1 = l0[0][2] + l1[0][0] + '/' + l0[1][2] + l1[1][0]
                s2_2 = l1[0][1:3] + '/' + l1[1][1:3]
                s2_3 = l0[2][0:2] + '/' + l2[0][0:2]
                s2_4 = l0[2][2] + l1[2][0] + '/' + l2[0][2] + l3[0][0]
                s2_5 = l1[2][1:3] + '/' + l3[0][1:3]
                s2_6 = l2[1][0:2] + '/' + l2[2][0:2]
                s2_7 = l2[1][2] + l3[1][0] + '/' + l2[2][2] + l3[2][0]
                s2_8 = l3[1][1:3] + '/' + l3[2][1:3]
                r0.extend([s2_0, s2_1, s2_2])
                r1.extend([s2_3, s2_4, s2_5])
                r2.extend([s2_6, s2_7, s2_8])
            newRows.append(r0)
            newRows.append(r1)
            newRows.append(r2)
        self.rows = newRows
        self.setInfo()


    def resizeIfNeeded(self):
        assert self.squareWidth in (3,4)
        pixelWidth = self.squareWidth * self.width # total pixels width for grid
        if pixelWidth % 2 == 0:
            if self.squareWidth == 4:
                print(f"Resize: Break 4x4 into 4 2x2\nStarting grid: ")
                self.printGrid()
                self.resize4to2()
            else:
                print(f"Resize: Break 4 3x3 into 9 2x2. \nStarting grid: ")
                self.printGrid()
                self.resize3to2()
        elif pixelWidth % 3 == 0:
            print(f"No Resize- keep as 3x3")
        else:
            print(f"pixelwidth not divisible by 2 or 3 - error")
            sys.exit(1)
        
    # process grid - apply enhancements to all current squares and return new grid
    def processGrid(self, enh):
        newGrid = Grid()
        for row in self.rows:
            newGrid.addRow(self.processRow(row, enh))
        print(f"After enhancements grid has {newGrid.numSquares} squares of {newGrid.squareWidth}x{newGrid.squareWidth}.")
        newGrid.resizeIfNeeded()
        return newGrid

    def countOn(self):
        mycount = 0
        for row in self.rows:
            for sq in row:
                c = sq.count('#')
                mycount += c
                # print(f"Counting on in {sq} is {c} Tot is {mycount}")
        return mycount
    
# def getRotatesAndFlips(s):
#     variations = set()
#     a = s.split('/')
#     for _ in range(4):
#         a = [''.join(row) for row in zip(*a[::-1])]
#         variations.add('/'.join(a))
#         variations.add('/'.join(a[::-1]))
#     # print(f"Variations for {s}:")
#     # for v in variations: printSquare(v)
#     return variations

def flip(s):
    a = s.split('/')
    a = a[::-1]
    return '/'.join(a)

def getRotations(s):
    if len(s)==5: # 2x2
        a = s.split('/')
        r1 = a[1][0] + a[0][0] + '/' + a[1][1] + a[0][1]
        r2 = a[1][1] + a[1][0] + '/' + a[0][1] + a[0][0]
        r3 = a[0][1] + a[1][1] + '/' + a[0][0] + a[1][0]
        return [ s, r1, r2, r3 ]
    elif len(s)==11: # 3x3
        a = s.split('/')
        c0 = a[0][0]
        c1 = a[0][1]
        c2 = a[0][2]
        c3 = a[1][0]
        c4 = a[1][1]
        c5 = a[1][2]
        c6 = a[2][0]
        c7 = a[2][1]
        c8 = a[2][2]
        r1 = c6+c3+c0+'/'+c7+c4+c1+'/'+c8+c5+c2
        r2 = c8+c7+c6+'/'+c5+c4+c3+'/'+c2+c1+c0
        r3 = c2+c5+c8+'/'+c1+c4+c7+'/'+c0+c3+c6
        return [ s, r1, r2, r3 ]
    else:
        print(f"Unexpected string length {len(s)} for {s}")
        sys.exit(1)

src = {} # map any variation to the variation in the db

def getRotatesAndFlips(s):
    global src
    variations = set()
    for r in getRotations(s):
        variations.add(r)
        src[r] = s
    for r in getRotations(flip(s)):
        variations.add(r)
        src[r] = s
    return variations


def getEnhancements(db):
    enh = {}
    for line in db:
        parts = line.split(' => ')
        variations = getRotatesAndFlips(parts[0])
        for v in variations: enh[v] = parts[1]
    return enh

def fracture(s): # break 4x4 into 4 2x2
    a = s.split('/')
    assert len(a) == 4
    assert len(a[0]) == 4
    l = [ a[0][0:2] + '/' + a[1][0:2],
          a[0][2:4] + '/' + a[1][2:4],
          a[2][0:2] + '/' + a[3][0:2],
          a[2][2:4] + '/' + a[3][2:4] ]
    # print(f"Fracturing {s} into {l}")
    return l


def doPart1(db):
    enh = getEnhancements(db)
    grid = Grid('.#./..#/###')
    print("Initial grid:")
    grid.printGrid()
    for it in range(5):
        print(f"Iteration {it+1} is starting with {grid.numSquares} squares.")
        newgrid = grid.processGrid(enh)
        print(f"After processing, new grid has {newgrid.numSquares} squares.")
        newgrid.printGrid()
        grid = newgrid
        on = grid.countOn()
        print(f"After {it+1} iterations there are {grid.numSquares} squares. {on} pixels are on")
        # printGrid(grids)
    return on
   
    
def doPart2(db):
    enh = getEnhancements(db)
    grid = Grid('.#./..#/###')
    print("Initial grid:")
    grid.printGrid()
    for it in range(18):
        print(f"Iteration {it+1} is starting with {grid.numSquares} squares.")
        newgrid = grid.processGrid(enh)
        print(f"After processing, new grid has {newgrid.numSquares} squares.")
        newgrid.printGrid()
        grid = newgrid
        on = grid.countOn()
        print(f"After {it+1} iterations there are {grid.numSquares} squares. {on} pixels are on")
        # printGrid(grids)
    return on

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"\nPart 2 is {p2}")
