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

def getConnectedTo(db):
    connectsTo = {}
    for l in db:
        m = re.match(r'([a-z])([a-z])-([a-z])([a-z])',l)
        if m:
            #print(f"{m.group(1)}{m.group(2)}-{m.group(3)}{m.group(4)}")
            c1 = m.group(1)+m.group(2)
            c2 = m.group(3)+m.group(4)
            if c2 < c1: c1,c2 = c2,c1
            if c1 in connectsTo: connectsTo[c1].append(c2)
            else: connectsTo[c1] = [c2]
            if not c2 in connectsTo: connectsTo[c2] = []
    for k in connectsTo: connectsTo[k].sort()
    return connectsTo
    
def getTrios(connectsTo, computers):
    listOfTrios = []
    for c in computers:
        l = connectsTo[c]
        if len(l)<2: continue
        for i1,c1 in enumerate(l[0:-1]):
            for i2,c2 in enumerate(l[i1+1:]):
                if c2 in connectsTo[c1]:
                    trio = (c,c1,c2)
                    listOfTrios.append(trio)
                    print(f"Trio:{trio}")
    return listOfTrios

def doPart1(db):
    count = 0
    connectsTo = getConnectedTo(db)
    computers = [k for k in connectsTo]
    computers.sort()
    for c in computers: print(f"{c} -> {connectsTo[c]}")
    trios = getTrios(connectsTo, computers)
    for trio in trios:
        for c in trio: 
            if c.startswith('t'):
                count=count+1
                break
    return count



def doPart2(db):
    count = 0
    connectsTo = getConnectedTo(db)
    computers = [k for k in connectsTo]
    computers.sort()
    isInSets = {c:[] for c in computers} # map comp name to a list of all sets that the comp is in
    allSets = []
    for c in computers:
        for c1 in connectsTo[c]:
            #print(f"{c}->{c1}   sets with {c} are {isInSets[c]}")
            for aset in isInSets[c]:
                ok = True
                for c2 in aset:
                    if not((c2 in connectsTo[c1]) or (c1 in connectsTo[c2])):
                        ok = False
                if ok:
                    print(f"Add {c1} to set {aset}")
                    aset.add(c1)
            newSet = set([c,c1])
            isInSets[c].append(newSet)
            isInSets[c1].append(newSet)
            allSets.append(newSet)
            #print(f"Sets are now {allSets}")
    maxLen = 0
    for aset in allSets:
        if len(aset) > maxLen:
            print(f"Longer Set is: {aset}")
            maxLen = len(aset)
            res = list(aset)
            res.sort()
            count = print(','.join(res))
    return count


    
#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#sys.setrecursionlimit(10000)
#p1 = doPart1(db)
#print(f"Part 1 is {p1}\n\n")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
