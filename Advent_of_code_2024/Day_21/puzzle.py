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

keyPairMap = {}

class Pad:

    global keyPairMap

    def __init__(self, layout, name):
        print(f"Keypad sequence for {name}")
        self.name = name
        self.layout = layout[:]
        self.localPairMap = self.getMap(layout)
        # compute relative cost of a string
        self.cCost= {'A':0, '^':1, 'v':2, '>':1, '<':3}

    # get list of shortest paths from key at (fx,fy) to key at (tx,ty) (1 or 2 paths possible)
    def getPathsAtoB(self, fx,fy,tx,ty,layout):
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
            s1 = self.getPathsAtoB(fx,fy,fx,ty, layout)
            s2 = self.getPathsAtoB(fx,ty,tx,ty, layout)
            if len(s1) and len(s2): seqA = [s1[0][0:-1]+s2[0]]
            else: seqA = []
            s1 = self.getPathsAtoB(fx,fy,tx,fy, layout)
            s2 = self.getPathsAtoB(tx,fy,tx,ty, layout)
            if len(s1) and len(s2): seqB = [s1[0][0:-1]+s2[0]]
            else: seqB = []
            assert len(seqA) or len(seqB)
            if not len(seqA): return seqB
            if not len(seqB): return seqA
            # print(f"     SeqA: {seqA[0]}    SeqB: {seqB[0]}")
            #if len(seqA) < len(seqB) : return seqA
            #return seqB
            return [seqA[0], seqB[0] ]


    def getMap(self,layout):
        map = {}
        for fy,fl in enumerate(layout):
            for fx,fc in enumerate(fl):
                if fc  == 'X': continue
                for ty,tl in enumerate(layout):
                    for tx,tc in enumerate(tl):
                        if tc=='X' : continue
                        k = fc + tc
                        map[k] = self.getPathsAtoB(fx,fy,tx,ty,layout)
                        if (self.name == 'Keypad1'): 
                            s = ", ".join(map[k])
                            print(f"   {fc} -> {tc} is {s}")
        return map


    # use just the keyPairMap to get List of first mappings.
    # return list of shortest.
    def getFirstListOfSeqs(self,str):
        # get all combinations
        Astr = 'A' + str
        seq = ['']
        for i in range(len(Astr)-1):
            oneKeySeqs = self.localPairMap[Astr[i:i+2]]
            newseq = []
            for orig in seq:
                for s in oneKeySeqs:
                    newseq.append(orig + s)
            seq = newseq
        # find shortest
        minLen = min([len(s) for s in seq])
        res = [s for s in seq if len(s) == minLen]
        print(f"getFirstListOfSeqs of {str} => {res}")
        return res
    


# map the string l to list of shortest sequence of new commands
@functools.cache
def getListOfShortest(str:string):
    # print(f"getListOfShortest of {str}")
    # get all combinations
    Astr = str
    if str[0] != 'A': Astr = 'A' + str
    seq = ['']
    for i in range(len(Astr)-1):
        oneKeySeqs = keyPairMap[Astr[i:i+2]]
        newseq = []
        for orig in seq:
            for s in oneKeySeqs:
                newseq.append(orig + s)
        seq = newseq
    # find shortest
    minLen = min([len(s) for s in seq])
    res = [s for s in seq if len(s) == minLen]
    return res

# return shortest soln from a list of solutions (options is list of strings)
# returns string
def getShortestFromList(options):
    nextup = [ getListOfShortest(opt)  for opt in options ] # each entry is a list of seqs of same (min) length
    nextupLens = [ len(n[0]) for n in nextup ]
    nextupMinLen = min(nextupLens)
    print(f"options: {options}")
    print(f"nextup:")
    for nL in nextup:
        for n in nL:
            print(f"{len(n)}:{n} ",end='')
        print('')
    count = nextupLens.count(nextupMinLen) # num times min occurs
    print(f"nextuplens: {nextupLens}   Min is {nextupMinLen} which occurs {count} times")
    if count == 1:
        for oi, opt in enumerate(options):
            if nextupLens[oi]==nextupMinLen: return opt
    
    # find shortest of the mapping of the first mapping
    shortest = BIGNUM
    for oi, opt in enumerate(options):
        nextnext = [ getListOfShortest(n) for n in nextup[oi] ]
        if len(nextnext[0])<shortest:
            shortest=len(nextnext[0]); res = opt
    print(f"For options {options} best is {res}")
    return res       

# find the shortest sequence of new commands that does 'str'(string)
# returns string
@functools.cache
def getNewSeq(str:string):
    options = getListOfShortest(str)
    assert len(options)>0
    if len(options) == 1:
        print(f"getNewSeq of {str} is {options[0]}")
        return options[0]
    # all entries in options have same len. So see if they map to different lengths
    s = getShortestFromList(options)
    print(f"getNewSeq of {str} is {s}")
    return s


  
def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]


def process(l, numericPad, keyPad1, numK=2):

    l1List = numericPad.getFirstListOfSeqs(l) # list of alts
    l1 = getShortestFromList(l1List)

    print(f"K1: {l} => {l1}\nK1: len= {len(''.join(l1))}")

    for rep in range(numK):
        print(f"K{rep+2}: rep {rep+2} of {numK} ===== str len= {len(l1)}",flush=True)
        l1_len = len(l1)
        if l1_len < 80: print(f"K{rep+2}: l1={l1} ")
        print(f"K{rep+2}: l1 len is {l1_len}")
        l2 = getNewSeq(l1)
        l1 = l2

    sm = len(l1)
    print(f"Result: l1 has len {sm} and is {l1}")
    num = int(l[0:-1])
    prod = num * sm
    print(f"So value is {num} * {sm} = {prod}")
    return prod


def doPart1(db):
    global keyPairMap
    comp = 0
    numericPad = Pad([ ['7','8','9'],['4','5','6'],['1','2','3'],['X','0','A']], 'Numeric')
    keyPad1 = Pad([['X','^','A'],['<','v','>']],'Keypad1')
    keyPairMap = keyPad1.localPairMap
    for l in db:
        comp = comp + process(l, numericPad, keyPad1,2)
    return comp



def doPart2(db):
    global keyPairMap
    comp = 0
    numericPad = Pad([ ['7','8','9'],['4','5','6'],['1','2','3'],['X','0','A']], 'Numeric')
    keyPad1 = Pad([['X','^','A'],['<','v','>']],'Keypad1')
    keyPairMap = keyPad1.localPairMap
    for l in db:
        comp = comp + process(l, numericPad, keyPad1, 26)
    return comp


    
#---------------------------------------------------------------------------------------
# Load input
db = load_db()
#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}\n\n")

#p2 = doPart2(db)
#print(f"\n\n\n\nPart 2 is {p2}")
