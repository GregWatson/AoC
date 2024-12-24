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
MAX=43
#MAX=8

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def getArray(db):
    a = [ array.array('i',[0 for x in range(MAX)]) for y in range(MAX) ]
    for y,l in enumerate(db):
        for x,c in enumerate(l):
            a[y][x] = int(c)
    return a

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

def getTrailEndsFrom(a,x,y,expLev, unique):
    trailEnds = []
    for (dx,dy) in [(-1,0),(1,0),(0,1),(0,-1)]:
        nx=x+dx; ny=y+dy
        if nx<0 or nx>=MAX or ny<0 or ny>=MAX: continue
        if a[ny][nx] == expLev+1:
            if expLev==8:
                end = f"{nx}_{ny}"
                if not unique:trailEnds.append(end)
                else:
                    if not end in trailEnds: 
                        trailEnds.append(end)
            else:
                newTrailEnds = getTrailEndsFrom(a,nx,ny,expLev+1,unique)
                for end in newTrailEnds:
                    if not unique:
                        trailEnds.append(end)
                    else:
                        if not end in trailEnds: 
                            trailEnds.append(end)
    return trailEnds            

def getTrailScore(a,x,y,unique):
    trailEnds=[]
    for (dx,dy) in [(-1,0),(1,0),(0,1),(0,-1)]:
        nx=x+dx; ny=y+dy
        if nx<0 or nx>=MAX or ny<0 or ny>=MAX: continue
        if a[ny][nx] == 1 :
            newTrailEnds = getTrailEndsFrom(a,nx,ny,expLev=1,unique=unique)
            if unique:
                for end in newTrailEnds:
                    if not end in trailEnds: 
                        trailEnds.append(end)
                        print(f"     Added end '{end}'")
            else:
                trailEnds.extend(newTrailEnds)
    return len(trailEnds)


def countTrailheadScores(a, unique):
    s = 0
    for y in range(MAX):
        for x in range(MAX):
            if a[y][x]==0: 
                print(f"Start from {x},{y}")
                s = s + getTrailScore(a,x,y,unique)
    return s

def doPart1(db):
    s = 0
    a = getArray(db)
    if BLENDER: run_ops_without_view_layer_update(drawArray, a)
    s = countTrailheadScores(a, unique=True)
    return s
   

# Only try obstructions at locations that have been visited
def doPart2(db):
    s = 0
    a = getArray(db)
    s = countTrailheadScores(a, unique=False)
    return s

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

p1 = doPart1(db)
print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"Part 2 is {p2}")



