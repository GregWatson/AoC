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
        print(f"Keypad sequence for {name}")
        self.name = name
        self.layout = layout[:]
        self.map = self.getMap(layout)


    # get shortest path from key at (fx,fy) to key at (tx,ty)
    def getPath(self, fx,fy,tx,ty,layout):
        if fx==tx and fy==ty: return 'A'
        if fx==tx:
            seq = ''
            dir = -1 ; 
            if fy<ty: dir = 1
            y=fy
            while y != ty:
                y = y + dir
                if dir == 1: seq = seq + 'v'
                else: seq = seq + '^'
                if layout[y][fx] == 'X': return ''
            return seq + 'A'
        elif fy==ty:
            seq = ''
            dir = -1 ; 
            if fx<tx: dir = 1
            x=fx
            while x != tx:
                x = x + dir
                if dir == 1: seq = seq + '>'
                else: seq = seq + '<'
                if layout[fy][x] == 'X': return ''
            return seq + 'A'
        else: # try both ways (y first, then x first)
            s1 = self.getPath(fx,fy,fx,ty, layout)
            s2 = self.getPath(fx,ty,tx,ty, layout)
            if len(s1) and len(s2): seqA = s1[0:-1]+s2
            else: seqA = ''
            s1 = self.getPath(fx,fy,tx,fy, layout)
            s2 = self.getPath(tx,fy,tx,ty, layout)
            if len(s1) and len(s2): seqB = s1[0:-1]+s2
            else: seqB = ''
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
                        k = fc + tc
                        map[k] = self.getPath(fx,fy,tx,ty,layout)
                        if (self.name == 'Kad1'): 
                            s = map[k]
                            print(f"   {fc} -> {tc} is {s}")
        return map

    # map the string l to a sequence of new commands
    @functools.cache
    def getNewSeq(self, l:string):
        seq = []
        for i in range(len(l)-1):
            oneKeySeqs = self.map[l[i:i+2]]
            seq.append(oneKeySeqs)
        r = ''.join(seq)
        self.map[l] = r
        if len(r)<50:
            print(f"Mapped {l} to {r}")
        else:
            print(f"mapped len {len(l)} to new len {len(r)}")
        return r

    def getSeqs(self, l:list):
        r = []
        for seq in l:
            subs = seq.split('A')[0:-1]
            #print(f"\tMapping {subs}")
            for ss in subs:
                ss1 = 'A' + ss + 'A'
                if ss1 in self.map: 
                    res = self.map[ss1]
                else:
                    res = self.getNewSeq(ss1)
                r.append(res)
                #print(f"\t\tSUB {ss1} -> {res}  ")
            #print(f"\t\tFINAL: {joined}")
        return r


def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]


def process(l, numK=2):
    numericPad = Pad([ ['7','8','9'],['4','5','6'],['1','2','3'],['X','0','A']], 'Numeric')
    keyPad1 = Pad([['X','^','A'],['<','v','>']],'Keypad1')

    l1 = numericPad.getSeqs([l])
    print(f"K1: {l} is {l1}\nlen= {len(l1)}")

    for rep in range(numK):
        print(f"==== Rep = {rep+1} of {numK} ===== str len= {len(l1)}",flush=True)
        l2 = keyPad1.getSeqs(l1)
        l1 = l2

    sm = len(''.join(l1))
    num = int(l[0:-1])
    prod = num * sm
    print(f"So value is {num} * {sm} = {prod}")
    return prod


def doPart1(db):
    comp = 0
    for l in db:
        comp = comp + process(l, 2)
    return comp



def doPart2(db):
    comp = 0
    for l in db:
        comp = comp + process(l, 26)
    return comp


    
#---------------------------------------------------------------------------------------
# Load input
db = load_db()
#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}\n\n")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
