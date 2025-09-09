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
runcode0_waiting = False
runcode1_waiting = False
fifo0 = []
fifo1 = []

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def codeDone():
    global runcode0_waiting, runcode1_waiting, fifo0, fifo1
    return (runcode0_waiting and len(fifo1) == 0) and (runcode1_waiting and len(fifo0) == 0)


def runCode(db):
    regs = dict(zip(string.ascii_lowercase, [0]*26))
    pc = 0
    lastsound = 0
    while pc < len(db):
        if print_on:
            print(f"pc: {pc} {db[pc]} regs: {regs}")
        parts = db[pc].split()
        if parts[0] == 'snd':
            lastsound = regs[parts[1]]
            fifo0.append(lastsound)
            pc += 1
        elif parts[0] == 'set':
            if parts[2] in string.ascii_lowercase:
                regs[parts[1]] = regs[parts[2]]
            else:
                regs[parts[1]] = int(parts[2])
            pc += 1
        elif parts[0] == 'add':
            if parts[2] in string.ascii_lowercase:
                regs[parts[1]] += regs[parts[2]]
            else:
                regs[parts[1]] += int(parts[2])
            pc += 1
        elif parts[0] == 'mul':
            if parts[2] in string.ascii_lowercase:
                regs[parts[1]] *= regs[parts[2]]
            else:
                regs[parts[1]] *= int(parts[2])
            pc += 1
        elif parts[0] == 'mod':
            if parts[2] in string.ascii_lowercase:
                regs[parts[1]] = regs[parts[1]] % regs[parts[2]]
            else:
                regs[parts[1]] = regs[parts[1]] % int(parts[2])
            pc += 1
        elif parts[0] == 'rcv':
            if regs[parts[1]] != 0:
                return lastsound
            pc += 1
        elif parts[0] == 'jgz':
            if parts[1] in string.ascii_lowercase:
                val = regs[parts[1]]
            else:
                val = int(parts[1])
            if val > 0:
                if parts[2] in string.ascii_lowercase:
                    pc += regs[parts[2]]
                else:
                    pc += int(parts[2])
            else:
                pc += 1
    return 0

def runCode0(db, pc, regs, sendcount):
    global runcode0_waiting,fifo0, fifo1
    added = 0
    if pc > 0 and len(fifo1)==0:
        print(f"Program 0 CANNOT RESTART")
    while pc < len(db):
        if print_on:
            print(f"pc: {pc} {db[pc]} regs: {regs}")
        parts = db[pc].split()
        if parts[0] == 'snd':
            lastsound = regs[parts[1]]
            fifo0.append(lastsound)
            print(f"fifo0 len is now {len(fifo0)} fifo1 len is now {len(fifo1)}")
            added += 1
            sendcount += 1
            pc += 1
        elif parts[0] == 'set':
            if parts[2] in string.ascii_lowercase:
                regs[parts[1]] = regs[parts[2]]
            else:
                regs[parts[1]] = int(parts[2])
            pc += 1
        elif parts[0] == 'add':
            if parts[2] in string.ascii_lowercase:
                regs[parts[1]] += regs[parts[2]]
            else:
                regs[parts[1]] += int(parts[2])
            pc += 1
        elif parts[0] == 'mul':
            if parts[2] in string.ascii_lowercase:
                regs[parts[1]] *= regs[parts[2]]
            else:
                regs[parts[1]] *= int(parts[2])
            pc += 1
        elif parts[0] == 'mod':
            if parts[2] in string.ascii_lowercase:
                regs[parts[1]] = regs[parts[1]] % regs[parts[2]]
            else:
                regs[parts[1]] = regs[parts[1]] % int(parts[2])
            pc += 1
        elif parts[0] == 'rcv':
            if len(fifo1) == 0:
                runcode0_waiting = True
                print(f"Program 0 waiting after sending {added} values")
                return sendcount, pc, regs
            else:
                runcode0_waiting = False
                regs[parts[1]] = fifo1.pop(0)
                pc += 1
        elif parts[0] == 'jgz':
            if parts[1] in string.ascii_lowercase:
                val = regs[parts[1]]
            else:
                val = int(parts[1])
            if val > 0:
                if parts[2] in string.ascii_lowercase:
                    pc += regs[parts[2]]
                else:
                    pc += int(parts[2])
            else:
                pc += 1
        else:
            print(f"Unknown instruction {parts[0]}")
            sys.exit(1)
    print(f"Program 0 terminating normally after sending {sendcount} values")
    runcode0_waiting = True
    return sendcount, pc, regs

def runCode1(db, pc, regs, sendcount):
    global runcode1_waiting,fifo0, fifo1
    if (pc > 0) and len(fifo0)==0:
        print(f"Program 1 CANNOT RESTART\n")
    while pc < len(db):
        if print_on:
            print(f"pc: {pc} {db[pc]} regs: {regs}")
        parts = db[pc].split()
        if parts[0] == 'snd':
            lastsound = regs[parts[1]]
            fifo1.append(lastsound)
            print(f"fifo0 len is now {len(fifo0)} fifo1 len is now {len(fifo1)}")
            sendcount += 1
            pc += 1
        elif parts[0] == 'set':
            if parts[2] in string.ascii_lowercase:
                regs[parts[1]] = regs[parts[2]]
            else:
                regs[parts[1]] = int(parts[2])
            pc += 1
        elif parts[0] == 'add':
            if parts[2] in string.ascii_lowercase:
                regs[parts[1]] += regs[parts[2]]
            else:
                regs[parts[1]] += int(parts[2])
            pc += 1
        elif parts[0] == 'mul':
            if parts[2] in string.ascii_lowercase:
                regs[parts[1]] *= regs[parts[2]]
            else:
                regs[parts[1]] *= int(parts[2])
            pc += 1
        elif parts[0] == 'mod':
            if parts[2] in string.ascii_lowercase:
                regs[parts[1]] = regs[parts[1]] % regs[parts[2]]
            else:
                regs[parts[1]] = regs[parts[1]] % int(parts[2])
            pc += 1
        elif parts[0] == 'rcv':
            if len(fifo0) == 0:
                runcode1_waiting = True
                return sendcount, pc, regs
            else:
                runcode1_waiting = False
                regs[parts[1]] = fifo0.pop(0)
                pc += 1
        elif parts[0] == 'jgz':
            if parts[1] in string.ascii_lowercase:
                val = regs[parts[1]]
            else:
                val = int(parts[1])
            if val > 0:
                if parts[2] in string.ascii_lowercase:
                    pc += regs[parts[2]]
                else:
                    pc += int(parts[2])
            else:
                pc += 1
        else:
            print(f"Unknown instruction {parts[0]}")
            sys.exit(1)
    print(f"Program 1 terminating normally after sending {sendcount} values")
    runcode1_waiting = True
    return sendcount, pc, regs

def doPart1(db):
    return runCode(db)

def doPart2(db):
    global fifo0, fifo1
    fifo0 = []; fifo1 = []
    regs0 = dict(zip(string.ascii_lowercase, [0]*26))
    regs1 = dict(zip(string.ascii_lowercase, [0]*26))
    regs1['p'] = 1 
    pc0 = 0 ; pc1 = 0
    s1 = 0; s2 = 0
    while not codeDone():
        (s1, pc0, regs0) = runCode0(db, pc0, regs0, s1)
        print(f"Program 0 sent {s1} values. pc0={pc0} pc1={pc1} len(fifo0)={len(fifo0)} len(fifo1)={len(fifo1)}")
        if codeDone(): return s2
        (s2, pc1, regs1) = runCode1(db, pc1, regs1,s2)
        print(f"Program 1 sent {s2} values. pc0={pc0} pc1={pc1} len(fifo0)={len(fifo0)} len(fifo1)={len(fifo1)}")
    return s2

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}\n\n")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
