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
NUMX=38
NUMY=24
MINSIZE=85
MAXSIZE=94

grid=array.array('l',[1 for i in range(NUMX*NUMY)])

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

class Node:
    def __init__(self, x:int, y:int, size:int, used:int ):
        self.x=x
        self.y=y
        self.size=size
        self.used=used
        self.avail=size-used

    
    def addUsed(self,add:int):
        self.used = self.used + add
        if self.used > self.size:
            print(f"Error: node {x}:{y} exceeded its storage (add {add} but that makes size {self.size})")
            sys.exit(1)



def parsedb(db):
    nodes=[]
    for l in db:
        m = re.match(r'.dev.grid.node-x(\d+)-y(\d+) \s*(\d+)T \s*(\d+)',l)
        if m:
            (x,y,size,used) = (int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))
            n = Node(x,y,size,used)
            nodes.append(n)
    print(f"Loaded {len(nodes)} nodes.")
    return nodes
 
def getsizes(db):
    nodes=db
    minSize=1000
    maxSize=0
    minUsed=1000
    for n in nodes:
        if n.size<400:
            if n.size <400 and n.size > maxSize: maxSize=n.size
            if n.size < minSize: minSize = n.size
            if n.used > MINSIZE: print(f"n {x}-{y} has used {n.used}T which is greater than {MINSIZE}")
            if n.used > 0 and (n.used < minUsed): minUsed=n.used
    print(f"Min Size is {minSize}T and max Size is {maxSize}T.   Min used is {minUsed}T")
    return 0

def createGrid(db):
    for x in range(NUMX):
        for y in range(NUMY):
            n=db[x*NUMY + y]
            if n.used == 0: setGrid(x,y,0)  # empty
            if n.used > 100: setGrid(x,y,-1)  # no-go
    setGrid(37,0,2) # target


def setGrid(x,y,n):
    global grid
    grid[y*NUMX+x] = n

def getGrid(x,y):
    return grid[y*NUMX+x]

def printGrid(grid, moves):
    print(f"{moves} MOVES.")
    for y in range(NUMY):
        for x in range(NUMX):
            n=grid[y*NUMX+x]
            if n==0: print("0",end="")
            elif n<0: print("#",end="")
            elif n==2: print("G",end="")
            else: print(".",end="")
        print("")
    print("")

def doPart1(db):
    nodes = db
    ok=len(nodes)
    for n in nodes:
        if (n.used ==0 ) or (n.used >400): ok=ok-1
        #if (n.used > 91) : print(f"{n.x}-{n.y} has used {n.used}T")
        #if (n.avail > 50) : print(f"{n.x}-{n.y} has avail: {n.avail}T")
    return ok

def doPart2( db):
    global grid
    nodes=db
    moves=0
    createGrid(nodes)
    printGrid(grid,moves)
    # move empty to (29,0)
    moves=34
    setGrid(35,21,1)
    setGrid(36,0,0)
    printGrid(grid, moves)
    return 0
        



#---------------------------------------------------------------------------------------
# Load input
db = load_db()
db1 = parsedb(db)

p1 = doPart1(db1)
print(f"Part 1 is {p1}")

p2 = doPart2(db1)
print(f"Part 2 is {p2}.")

s = (NUMX-2)*5 + 34 + 1
print(f"Solved by hand. Steps = {s}")


