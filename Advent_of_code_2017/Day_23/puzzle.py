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

def isPrime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def runCode(db,mode=0):
    regs = { 'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0, 'g':0, 'h':0 }
    if mode==1:
        regs['a'] = 1
    pc = 0
    muls = 0
    while pc>=0 and pc<len(db):
        if print_on:
            print(f"pc={pc} {db[pc]} {regs}")
        inst = db[pc].split()
        if inst[0]=='set':
            if inst[2] in regs:
                regs[inst[1]] = regs[inst[2]]
            else:
                regs[inst[1]] = int(inst[2])
        elif inst[0]=='sub':
            if inst[2] in regs:
                regs[inst[1]] -= regs[inst[2]]
            else:
                regs[inst[1]] -= int(inst[2])
        elif inst[0]=='mul':
            muls += 1
            if inst[2] in regs:
                regs[inst[1]] *= regs[inst[2]]
            else:
                regs[inst[1]] *= int(inst[2])
        elif inst[0]=='jnz':
            if inst[1] in regs:
                v = regs[inst[1]]
            else:
                v = int(inst[1])
            if v!=0:
                if inst[2] in regs:
                    pc += regs[inst[2]]
                else:
                    pc += int(inst[2])
                continue
        elif inst[0]=='prime':
            if isPrime(regs['b']): f = 1 
            else: f = 0
            regs['f'] = f
        else:
            print(f"Unknown instruction {db[pc]}")
            break
        pc += 1
    print(f"Finished with regs {regs}")
    return muls, regs['h']

def doPart1(db):
    muls, h = runCode(db)
    return muls
   
    
def doPart2(db):
    muls, h = runCode(db,mode=1)
    return h

#---------------------------------------------------------------------------------------
#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"\nPart 2 is {p2}")
