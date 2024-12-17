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
MAX=130

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]


def getFloor(db):
    (gx,gy)=(0,0)
    f = [ array.array('i',[0 for i in range(MAX)]) for y in range(MAX) ]
    for y,l in enumerate(db):
        for x,c in enumerate(l):
            if c == '#': 
                f[y][x]=-1
                # print(f"Obstacle at {x},{y}")
            elif c=='^':
                gx=x; gy=y
    if gx == 0 and gy ==0:
        print("Error: no guard")
        sys.exit(1)
    return (f, gx, gy)

def moveGuard(f,gX,gY):
    F = copy.deepcopy(f)
    (gx,gy) = (gX, gY)
    dx=0; dy=-1
    while True:
        F[gy][gx] = 1
        # print(f"g({gx},{gy})   dir=[{dx},{dy}]")
        ngx=gx+dx; ngy=gy+dy
        if ngx < 0 or ngx >= MAX or ngy <0 or ngy >= MAX: return F
        if F[ngy][ngx] == -1: # obstruction
            if dy != 0:
                dx = -dy; dy = 0
            else:
                dy = dx; dx = 0
        else:
            (gx, gy)= (ngx,ngy)

def isLoop(f,gX,gY):
    F = copy.deepcopy(f)
    (gx,gy) = (gX, gY)
    dirChanges=[]
    dx=0; dy=-1
    while True:
        F[gy][gx] = 1
        # print(f"g({gx},{gy})   dir=[{dx},{dy}]")
        ngx=gx+dx; ngy=gy+dy
        if ngx < 0 or ngx >= MAX or ngy <0 or ngy >= MAX: 
            # print(f"Exited at {ngx},{ngy}")
            return (False,F)
        if F[ngy][ngx] == -1: # obstruction
            dirChange=f"{gx},{gy},{dx},{dy}"
            #print(f"{dirChange}")
            if dirChange in dirChanges: return (True, F)
            dirChanges.append(dirChange)
            # print(f"changes = {len(dirChanges)}")
            if dy != 0:
                dx = -dy; dy = 0
            else:
                dy = dx; dx = 0
        else:
            (gx, gy)= (ngx,ngy)

def countOnes(f):
    c = 0
    for y in range(MAX):
        for x in range(MAX):
            if f[y][x] == 1: c = c + 1
    return c

def printF(f):
    for y in range(MAX):
        for x in range(MAX):
            c = f[y][x]
            if c==0: print(f".",end='')
            if c==1: print(f"X",end='')
            if c==-1: print(f"#",end='')
        print(f"")
    print(f"")

def doPart1(db):
    s = 0
    (f, gx, gy) = getFloor(db)
    #printF(f)
    print(f"G:({gx},{gy})")
    f = moveGuard(f, gx,gy)
    s = countOnes(f)
    return s
   

# Only try obstructions at locations that have been visited
def doPart2(db):
    s = 0
    (f, gx, gy) = getFloor(db)
    f1 = moveGuard(f, gx,gy)    # update so 1 = visited 
    #sys.exit(1)
    for y in range(MAX):
        for x in range(MAX):
            if (y==gy) and (x==gx): continue
            if f1[y][x] != 1: continue # was visited
            f[y][x] = -1
            (isloop, F) = isLoop(f,gx,gy)
            if isloop:
                print(f"It's a loop: {x},{y}")
                s = s+1
            #print(f"{x},{y}")
            #printF(F)
            #print("")
            f[y][x]=0
        print(f"y is {y}")
    return s

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#p1 = doPart1(db)
#print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"Part 2 is {p2}")



