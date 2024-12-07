#import argparse
import sys
import re
import functools
import array
import copy
import hashlib
import string
import itertools

input_file_name = 'input.txt'
print_on = False
MAX=140

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def isXmas(db,x,y,xd,yd):
    if (xd ==0 and yd ==0): return 0
    X=x; Y=y
    X=X+xd;Y=Y+yd
    if ((X<0) or (X>=MAX) or (Y<0) or (Y>=MAX)): return 0
    if db[Y][X]!='M': return 0
    X=X+xd;Y=Y+yd
    if ((X<0) or (X>=MAX) or (Y<0) or (Y>=MAX)): return 0
    if db[Y][X]!='A': return 0
    X=X+xd;Y=Y+yd
    if ((X<0) or (X>=MAX) or (Y<0) or (Y>=MAX)): return 0
    if db[Y][X]!='S': return 0
    return 1        



def countXmas(db,x,y):
    s = 0
    for xd in (-1,0,1):
        for yd in (-1,0,1):
            s = s + isXmas(db,x,y,xd,yd)
    return s

def isMAS(db,x,y):
    s1=db[y-1][x-1] + db[y+1][x+1]
    if not s1 in ('MS','SM'):return 0
    s1=db[y+1][x-1] + db[y-1][x+1]
    if not s1 in ('MS','SM'):return 0
    return 1

def doPart1(db):
    s = 0
    for y,l in enumerate(db):
        for x,c in enumerate(l):
            # print(f"{c}",end='')
            if c=='X':
                s = s+countXmas(db, x,y)
        # print("")
    return s
   

def doPart2(db):
    s = 0
    for y,l in enumerate(db):
        if (y==0 or y==139): continue
        for x,c in enumerate(l): 
            if (x==0 or x==139): continue
            if c=='A':
                s = s + isMAS(db,x,y)
    return s

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

p1 = doPart1(db)
print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"Part 2 is {p2}.")



