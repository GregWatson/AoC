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

# get position of scanner located at depth at time ps
# ps is the time in picoseconds
# depth is the depth of the scanner
# fw is a dictionary of depth:range
# returns the position of the scanner at time ps
def getPosAtTime(ps, depth, fw):
    irange = fw.get(depth, 0)
    if irange == 0:
        return -1
    scantime = 2 * (irange - 1)
    pos = ps % scantime
    if pos < irange:
        return pos
    else:
        return scantime - pos

def doPart1(db):
    count = 0
    fw={}
    for l in db:
        m = re.match(r'(\d+): (\d+)', l)
        if m:
            depth = int(m.group(1))
            irange = int(m.group(2))
            fw[depth] = irange
    severity = 0
    for time in range(100):
        pos = getPosAtTime(time, time, fw)
        if pos == 0:
            severity += time * fw[time]
            print(f"caught at {time} severity {severity}")
    return severity

def doPart2(db):
    count = 0
    fw={}
    scanners = []
    for l in db:
        m = re.match(r'(\d+): (\d+)', l)
        if m:
            depth = int(m.group(1))
            irange = int(m.group(2))
            fw[depth] = irange
            scanners.append(depth)
    ps = 0
    while True:
        caught = False
        for depth in scanners:
            pos = getPosAtTime(ps+depth, depth, fw)
            #print(f"ps {ps} depth {depth} pos {pos}")
            if pos == 0:
                caught = True
                break
        if not caught:
            print(f"not caught at {ps}")
            break
        ps += 1
        if ps % 1000000 == 0:
            print(f"ps {ps}")
    

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}\n\n")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
