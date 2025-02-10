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

BLENDER=False

# --- Blender ---
if BLENDER:
    import bpy
    sys.path.append(r'C:\cygwin64\home\gwatson\AOC')
    from blenderLib import *
# ---------------

input_file_name = 'input.txt'
print_on = False
MAX=141 

regA=41644071
regB=0
regC=0

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def getCombo(arg):
    global regA,regB,regC
    if arg < 4: return arg
    if arg == 4: return regA
    if arg == 5: return regB
    if arg == 6: return regC
    #print ("illegal combo arg value 7.")
    #sys.exit(1)
    return 1

def runProgram(program=[]):
    global regA,regB,regC
    ip=0
    out=[]
    while ip < len(program):
        instr=program[ip]
        arg=program[ip+1]
        #print(f"@{ip} i:{instr}  arg:{arg}   A:{regA} B:{regB} C:{regC}")
        ip = ip+2
        r = math.floor(regA/(2**getCombo(arg)))
        if instr == 0:
            regA=r; continue
        if instr == 1:
            regB = regB ^ arg; continue
        if instr == 2:
            regB = getCombo(arg) % 8; continue
        if instr == 3:
            if regA != 0: ip = arg
            continue
        if instr == 4:
            regB = regB ^ regC; continue
        if instr == 5:
            out.append(getCombo(arg) % 8); continue
        if instr == 6:
            regB=r; continue
        if instr == 7:
            regC=r; continue
    return out

def runProgram2(program):
    global regA
    regB = 0; regC = 0
    out = []
    while regA != 0:
        regB = regA % 8
        regB = regB ^ 2
        regC = math.floor(regA/(2**regB))
        regB = regB ^ 7 ^ regC
        regA = regA >> 3
        out.append(regB % 8)
    return out



def doPart1(db):
    global regA,regB,regC
    s=0
    regA=41644071 ;    regB=0 ;    regC=0
    s = runProgram(program=[2,4,1,2,7,5,1,7,4,4,0,3,5,5,3,0])
    return s

def doPart2(db):
    global regA,regB,regC
    s=0
    max= 2**(16*3)
    startregA = 190593310982144     # found using a binary search while looking at the output sequence.

    scale = 1.00000001

    regA=startregA;   regB=0 ;    regC=0
    program = [2,4,1,2,7,5,1,7,4,4,0,3,5,5,3,0]
    s = runProgram2(program=program)
    done = False
    while not done:
        regA = startregA
        s = runProgram2(program=program)
        if startregA % (4096) == 0: print(f"{startregA} (prev {math.floor(startregA/scale)})  l={len(s)}   {s}")
        #startregA = round(startregA * scale)
        startregA = startregA + 1
        if len(s) != 16: continue
        for i,n in enumerate(s):
            if program[i] != n: break
        else:
            done = True
        if startregA > max: done = True
        
    return startregA-1
    

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
# sys.setrecursionlimit(10000)
#p1 = doPart1(db)
#print(f"Part 1 is {p1}")

#db = load_db()
p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
