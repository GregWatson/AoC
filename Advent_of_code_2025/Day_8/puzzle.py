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
import os.path

BLENDER=False

# --- Blender ---
if BLENDER:
    import bpy
    sys.path.append(r'C:\cygwin64\home\gwatson\AOC')
    from blenderLib import *
# ---------------

file_path = 'input.txt'
print_on = False
BIGNUM=10000000
MAX=141; MINSAVED=100; NUMCHEATS=20

# Load input data to db if file_path exists and is readable
if os.path.exists(file_path) and os.path.isfile(file_path) and os.access(file_path, os.R_OK):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            db = [ l.strip() for l in lines ]
    except IOError as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
else: db = []

origdb = copy.deepcopy(db)

db = []
for line in origdb:
    x,y,z= line.split(',')
    db.append([int(x),int(y),int(z),0])  # last entry is cct number

def addShortest(shortest, entry, num): # entry is (distance, index1, index2)
    # insert entry into shortest in sorted order
    if len(shortest)==0:
        shortest.append(entry)
        return
    if entry[0] > shortest[-1][0] and len(shortest) > num: # longer than num longest
        return
    for i in range(0,len(shortest)):
        if entry[0]<shortest[i][0]:
            shortest.insert(i,entry)
            del shortest[-1]
            return
    # add at end
    if len(shortest) < num:
        shortest.append(entry)

# return list of shortest distances between all pairs
# entry is (distance, index1, index2) where index is index in db
def getShortestDistances(db,num=10):
    shortest = []
    for i1 in range(0,len(db)-1):
        print(f"Getting distances for point {i1} of {len(db)}")
        p1 = db[i1]
        for i2 in range(i1+1,len(db)):
            p2 = db[i2]
            dist = math.sqrt( (float(p1[0])-float(p2[0]))**2 + (float(p1[1])-float(p2[1]))**2 + (float(p1[2])-float(p2[2]))**2 )
            addShortest(shortest, (dist,i1,i2), num)
    return shortest

def getCircuits(db, shortest,num):
    print(f"Getting circuits for num={num}")
    ccts = [] # list of list of points in each cct
    numAssigned = 0
    numBoxesAdded = 0
    for entry in shortest:
        printNumAdded = False
        # print(f"Distance {entry[0]} between points {db[entry[1]]} and {db[entry[2]]}")
        p1,p2 = db[entry[1]], db[entry[2]]
        if p1[3]==0 and p2[3]==0:
            # new circuit
            p1[3] = len(ccts)+1
            p2[3] = len(ccts)+1
            ccts.append( [p1, p2] )
            numBoxesAdded += 2; printNumAdded = True
        elif p1[3]>0 and p2[3]==0:
            # add p2 to p1 cct
            cctnum = p1[3]
            p2[3] = cctnum
            ccts[cctnum-1].append(p2)
            numBoxesAdded += 1; printNumAdded = True
        elif p1[3]==0 and p2[3]>0:
            # add p1 to p2 cct
            cctnum = p2[3]
            p1[3] = cctnum
            ccts[cctnum-1].append(p1)
            numBoxesAdded += 1; printNumAdded = True
        elif p1[3]>0 and p2[3]>0 and p1[3]!=p2[3]:
            # merge circuits
            cctnum1 = p1[3]
            cctnum2 = p2[3]
            for p in ccts[cctnum2-1]:
                p[3] = cctnum1
                ccts[cctnum1-1].append(p)
            ccts[cctnum2-1] = []
        # check if done
        numAssigned += 1
        if printNumAdded: 
            print(f"Number of boxes assigned to circuits: {numBoxesAdded} of {len(db)}")
            print(f"x1 * x2 is {p1[0]*p2[0]}")
        if numAssigned>=num:
            break
    return ccts

def doPart1(db):
    n = 10; 
    if len(db)>20: n=1000
    sP = getShortestDistances(db, n)
    circuits = getCircuits(db,sP,n)
    nonzero = [ len(c) for c in circuits if len(c)>0 ]
    nonzero.sort()
    nonzero.reverse()
    print(f"Circuits lengths: {nonzero[0:10]}")
    return nonzero[0] * nonzero[1] * nonzero[2]

def doPart2(db):
    n = 10; 
    if len(db)>20: n=8000  # Found 8000 by trial and error 
    sP = getShortestDistances(db, n)
    circuits = getCircuits(db,sP,n)
    nonzero = [ len(c) for c in circuits if len(c)>0 ]
    nonzero.sort()
    nonzero.reverse()
    print(f"Circuits lengths: {nonzero[0:10]}")
    return nonzero[0] * nonzero[1] * nonzero[2]

#---------------------------------------------------------------------------------------
#sys.setrecursionlimit(10000)

#p1 = doPart1(db)
#print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"\nPart 2 is {p2}")
