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

def getReg(r, regs):
    if not r in regs:
        regs[r] = 0; 
    return regs[r]

def doPart1(db):
    count = 0
    regs = {}
    for l in db:
        m = re.match(r'([a-z]+) (inc|dec) (-?\d+) if ([a-z]+) (\S+) (-?\d+).*',l)
        if m:
            reg1, op, num1, ifreg, ifop, ifnum = (m.group(1), m.group(2), int(m.group(3)), m.group(4), m.group(5), int(m.group(6)))
            #print(f"{reg1} {op} {num1} {ifreg} {ifop} {ifnum}")
            ok = False
            r = getReg(ifreg, regs)
            if ifop=='<' and r < ifnum: ok = True
            elif ifop=='<=' and r <= ifnum: ok = True
            elif ifop=='>' and r > ifnum: ok = True
            elif ifop=='>=' and r >= ifnum: ok = True
            elif ifop=='==' and r == ifnum: ok = True
            elif ifop=='!=' and r != ifnum: ok = True

            if ok:
                if op=='inc': regs[reg1] = getReg(reg1, regs) + num1
                elif op=='dec': regs[reg1] = getReg(reg1, regs) - num1

    return max([regs[r] for r in regs])

def doPart2(db):
    regs = {}
    mx = 0
    for l in db:
        m = re.match(r'([a-z]+) (inc|dec) (-?\d+) if ([a-z]+) (\S+) (-?\d+).*',l)
        if m:
            reg1, op, num1, ifreg, ifop, ifnum = (m.group(1), m.group(2), int(m.group(3)), m.group(4), m.group(5), int(m.group(6)))
            #print(f"{reg1} {op} {num1} {ifreg} {ifop} {ifnum}")
            ok = False
            r = getReg(ifreg, regs)
            if ifop=='<' and r < ifnum: ok = True
            elif ifop=='<=' and r <= ifnum: ok = True
            elif ifop=='>' and r > ifnum: ok = True
            elif ifop=='>=' and r >= ifnum: ok = True
            elif ifop=='==' and r == ifnum: ok = True
            elif ifop=='!=' and r != ifnum: ok = True

            if ok:
                if op=='inc': regs[reg1] = getReg(reg1, regs) + num1
                elif op=='dec': regs[reg1] = getReg(reg1, regs) - num1

                nm = max([regs[r] for r in regs])
                if nm > mx: mx = nm
    return mx

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}\n\n")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
