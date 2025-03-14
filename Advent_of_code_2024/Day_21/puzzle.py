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
BIGNUM=10000000
MAX=141; MINSAVED=100; NUMCHEATS=20

class Pad:
    def __init__(self, layout, name):
        if (print_on): print(f"Keypad sequence for {name}")
        self.layout = layout[:]
        self.map = self.getMap(layout)
        self.key = 'A'
        self.name = name

    def getPaths(self, fx,fy,tx,ty,layout):
        paths = []
        if fx==tx and fy==ty: return ['A']
        if fx==tx:
            seq = ''
            dir = -1 ; 
            if fy<ty: dir = 1
            y=fy
            while y != ty:
                y = y + dir
                if dir == 1: seq = seq + 'v'
                else: seq = seq + '^'
                if layout[y][fx] == 'X': return []
            return [seq + 'A']
        elif fy==ty:
            seq = ''
            dir = -1 ; 
            if fx<tx: dir = 1
            x=fx
            while x != tx:
                x = x + dir
                if dir == 1: seq = seq + '>'
                else: seq = seq + '<'
                if layout[fy][x] == 'X': return []
            return [seq + 'A']
        else: # try both ways (y first, then x first)
            s1 = self.getPaths(fx,fy,fx,ty, layout)
            s2 = self.getPaths(fx,ty,tx,ty, layout)
            if len(s1) and len(s2): seqA = [s1[0][0:-1]+s2[0]]
            else: seqA = []
            s1 = self.getPaths(fx,fy,tx,fy, layout)
            s2 = self.getPaths(tx,fy,tx,ty, layout)
            if len(s1) and len(s2): seqB = [s1[0][0:-1]+s2[0]]
            else: seqB = []
            assert len(seqA) or len(seqB)
            if not len(seqA): return seqB
            if not len(seqB): return seqA
            # print(f"     SeqA: {seqA[0]}    SeqB: {seqB[0]}")
            if len(seqA) < len(seqB) : return seqA
            return seqB
            #return [seqA[0], seqB[0] ]


    def getMap(self,layout):
        map = {}
        for fy,fl in enumerate(layout):
            for fx,fc in enumerate(fl):
                if fc  == 'X': continue
                for ty,tl in enumerate(layout):
                    for tx,tc in enumerate(tl):
                        if tc=='X' : continue
                        map[(fc,tc)] = self.getPaths(fx,fy,tx,ty,layout)
                        if (print_on): 
                            s = ', '.join(map[(fc,tc)])
                            print(f"   {fc}->{tc} is [{s}]")
        return map

    def getSeqs(self, l:string):
        seqs = ['']
        for c in l:
            oneKeySeqs = self.map[(self.key, c)]
            nseqs = []
            for s in seqs:
                for s1 in oneKeySeqs:
                    nseqs.append(s+s1)
            self.key = c
            seqs = nseqs
        return seqs

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def getShortest(LoS):
    return LoS
    slen = min([len(s) for s in LoS])
    res = [ s for s in LoS if len(s)==slen]
    print(f"Shortest: {len(LoS)} => {len(res)}")
    return res

def doPart1(db):
    comp = 0
    numericPad = Pad([ ['7','8','9'],['4','5','6'],['1','2','3'],['X','0','A']], 'numeric')
    keyPad1 = Pad([['X','^','A'],['<','v','>']],'Keypad1')
    for l in db:
        s1 = getShortest(numericPad.getSeqs(l))
        print(f"K1: {l} is {s1}\nlen= {len(s1)}")
        
        for rep in range(2):
            s2 = []
            for s in s1: 
                newSeqs = getShortest(keyPad1.getSeqs(s))
                s2.extend(newSeqs)
            print(f"K{2+rep}: {len(newSeqs)}")
            s1 = s2
            keyPad1.key='A'

        sm = BIGNUM
        for s in s1: 
            if len(s) < sm: sm=len(s)

        num = int(l[0:-1])
        prod = num * sm
        print(f"So value is {num} * {sm} = {prod}")
        comp = comp + prod
    return comp


def doPart2(db):
    comp = 0
    for l in db:
        numericPad = Pad([ ['7','8','9'],['4','5','6'],['1','2','3'],['X','0','A']], 'numeric')
        keyPad1 = Pad([['X','^','A'],['<','v','>']],'Keypad1')

        s1 = getShortest(numericPad.getSeqs(l))
        print(f"K1: {l} is {s1}\nlen= {len(s1)}")
        
        for rep in range(26):
            print(f"==== Rep = {rep} ===== list len= {len(s1)}",flush=True)
            s2 = []
            for s in s1: 
                newSeqs = getShortest(keyPad1.getSeqs(s))
                s2.extend(newSeqs)
            print(f"K{2+rep}: {len(newSeqs)}")
            s1 = s2
            keyPad1.key='A'

        sm = BIGNUM
        for s in s1: 
            if len(s) < sm: sm=len(s)

        num = int(l[0:-1])
        prod = num * sm
        print(f"So value is {num} * {sm} = {prod}")
        comp = comp + prod
    return comp
    
#---------------------------------------------------------------------------------------
# Load input
db = load_db()
#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
