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

class Gate():
    def __init__(self,i1,i2,o1,op,wires,gateDrivingWire):
        if i1.startswith('y') and i2.startswith('x'):
            i1,i2 = i2,i1
        self.i1 = i1 # wire
        self.i2 = i2 # wire
        self.o1 = o1 # wire
        self.op = op # OR , AND, XOR
        self.wires = wires
        self.gateDrivingWire = gateDrivingWire
        self.name = ''

    def display(self):
        return f"{self.name} : {self.op}({self.i1},{self.i2}) -> {self.o1}"

    def eval(self, tab=0):
        indent = ' '*(tab*2)
        if self.wires[self.i1] == -1: 
            self.gateDrivingWire[self.i1].eval(tab+1)
        if self.wires[self.i2] == -1: 
            self.gateDrivingWire[self.i2].eval(tab+1)
        op = self.op

        if op == 'AND': res = self.wires[self.i1] & self.wires[self.i2]
        elif op == 'OR' : res = self.wires[self.i1] | self.wires[self.i2]
        elif op == 'XOR': res = self.wires[self.i1] ^ self.wires[self.i2]
        else: 
            print(f"ERROR: unknown opcode {op}")
            sys.exit(1)
        self.wires[self.o1] = res
        print(f"{indent}{self.op}({self.i1},{self.i2}) -> {self.o1} ({self.wires[self.o1]})")

    def set_name(self):
        self.name = f"{self.op}_{self.i1}_{self.i2}__{self.o1}"


def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def getInit(db):
    wires= {}
    gateDrivingWire = {}
    for l in db:
        m = re.match(r'(...): (0|1)',l)
        if m:
            wires[m.group(1)] = int(m.group(2))
            continue
        else:
            m = re.match(r'(...) (...?) (...) -> (...)',l)
            if m:
                i1 = m.group(1)
                op = m.group(2)
                i2 = m.group(3)
                o1 = m.group(4)
                g = Gate(i1, i2, o1, op, wires, gateDrivingWire)
                g.set_name()
                gateDrivingWire[o1] = g
                if i1 not in wires: wires[i1] = -1
                if i2 not in wires: wires[i2] = -1
                if o1 not in wires: wires[o1] = -1

    return wires, gateDrivingWire



def  getValue(wires, gateDrivingWire):
    zL = [ w for w in wires if w.startswith('z') ]
    zL.sort()
    zL.reverse()
    outs = {}
    for z in zL: 
        gateDrivingWire[z].eval()
        outs[z] = wires[z]
    n = 0
    for z in zL: n= (n << 1) + outs[z]
    return n

def replace(wires, gateDrivingWire, orig_o1:string, new_o1:string):
    print(f"REPL: {orig_o1} -> {new_o1}")
    wires[new_o1] = wires[orig_o1]
    del wires[orig_o1]
    for z, g in gateDrivingWire.items():
        if g.i1 == orig_o1: 
            g.i1 = new_o1
            #print(f"repl i1: {g.name} ==> ",end='')
            g.set_name()
            #print(f"{g.name}   op is {g.op}")
        if g.i2 == orig_o1: 
            #print(f"repl i2: {g.name} ==> ",end='')
            g.i2 = new_o1
            g.set_name()
            #print(f"{g.name}   op is {g.op}")


def step1(wires, gateDrivingWire):
    newGates={}
    repl = []
    for z,gate in gateDrivingWire.items():
        if ((gate.i1.startswith('x') and gate.i2.startswith('y')) or (gate.i1.startswith('y') and gate.i2.startswith('x')) )and gate.i1[1:]==gate.i2[1:] and gate.op in ['XOR','AND'] and not gate.o1.endswith(gate.i1[1:]):
            #print(f"Candidate {gate.display()}", end='')
            new_o1 = gate.op[0] + gate.i1[1:]
            if new_o1 in wires:
                print(f"EEEEK new wire output {new_o1} is already in wire list!")
                sys.exit(1)
            orig_o1 = gate.o1
            gate.o1 = new_o1
            gate.set_name()
            #print(f"  ==> {gate.display()}")
            newGates[new_o1] = gate
            repl.append((orig_o1, new_o1))
        else:
            newGates[z] = gate
    for orig_o1, new_o1 in repl:
        replace(wires, newGates, orig_o1, new_o1)
    return newGates

def step2(wires, gateDrivingWire):
    newGates={}
    repl = []
    for z,gate in gateDrivingWire.items():
        if (gate.i1.startswith('A') or gate.i2.startswith('A')) and gate.op == 'OR' and not gate.o1.startswith('z'):
            print(f"Candidate 2 {gate.display()}",end='')
            index = gate.i1[1:]
            if gate.i2.startswith('A'): index = gate.i2[1:]
            new_o1 = 'C' + index
            if new_o1 in wires:
                print(f"EEEEK new wire output {new_o1} is already in wire list!")
                sys.exit(1)
            orig_o1 = gate.o1
            gate.o1 = new_o1
            gate.set_name()
            print(f"  ==> {gate.display()}")
            newGates[new_o1] = gate
            repl.append((orig_o1, new_o1))
        else:
            newGates[z] = gate
    for orig_o1, new_o1 in repl:
        replace(wires, newGates, orig_o1, new_o1)
    return newGates


def step3(wires, gateDrivingWire):
    newGates={}
    repl = []
    for z,gate in gateDrivingWire.items():
        if (gate.i1.startswith('X') or gate.i2.startswith('X')) and gate.op == 'AND' and not gate.o1.startswith('Y'):
            #print(f"Candidate {gate.display()}",end='')
            index = gate.i1[1:]
            if gate.i2.startswith('X'): index = gate.i2[1:]
            new_o1 = 'Y' + index
            if new_o1 in wires:
                print(f"EEEEK new wire output {new_o1} is already in wire list!")
                sys.exit(1)
            orig_o1 = gate.o1
            gate.o1 = new_o1
            gate.set_name()
            #print(f"  ==> {gate.display()}")
            newGates[new_o1] = gate
            repl.append((orig_o1, new_o1))
        else:
            newGates[z] = gate
    for orig_o1, new_o1 in repl:
        replace(wires, newGates, orig_o1, new_o1)
    return newGates



def doPart1(db):
    count = 0
    wires, gateDrivingWire = getInit(db)
    count = getValue(wires, gateDrivingWire)
    return count

def doPart2(db):
    count = 0
    wires, gateDrivingWire = getInit(db)

    gateDrivingWire = step1(wires, gateDrivingWire)
    print("AFTER STEP1:")
    # gnames = [gateDrivingWire[z].name for z in gateDrivingWire]
    # gnames.sort()
    # for gname in gnames: print(f"{gname}")

    gateDrivingWire = step2(wires, gateDrivingWire)
    print("AFTER STEP2:")

    # gnames = [gateDrivingWire[z].name for z in gateDrivingWire]
    # gnames.sort()
    # for gname in gnames: print(f"{gname} ")

    gateDrivingWire = step3(wires, gateDrivingWire)
    print("AFTER STEP3:")

    gnames = [gateDrivingWire[z].name for z in gateDrivingWire]
    gnames.sort()
    for gname in gnames: print(f"{gname} ")

    return count

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#sys.setrecursionlimit(10000)
#p1 = doPart1(db)
#print(f"Part 1 is {p1}\n\n")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
