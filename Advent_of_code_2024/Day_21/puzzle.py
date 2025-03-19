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

keyPairMap = {}

class Pad:

    global keyPairMap

    def __init__(self, layout, name):
        print(f"Keypad sequence for {name}")
        self.name = name
        self.layout = layout[:]
        simpleMap = getSimpleMap(layout)
        self.localPairMap = getMap(simpleMap, keyPairMap)
        # compute relative cost of a string
        self.cCost= {'A':0, '^':1, 'v':2, '>':1, '<':3}
        self.simpleMap = {}


    # use just the keyPairMap to get List of first mappings.
    # return list of shortest.
    def getFirstListOfSeqs(self,str):
        # get all combinations
        Astr = 'A' + str
        seq = []
        for i in range(len(Astr)-1):
            oneKeySeqs = self.localPairMap[Astr[i:i+2]][0]
            #print(f"{Astr[i:i+2]} => {oneKeySeqs}")
            seq.append(oneKeySeqs)
        
        res = ''.join(seq)
        print(f"getFirstListOfSeqs of {str} => {res}")
        return res
    

# get list of shortest paths from key at (fx,fy) to key at (tx,ty) (1 or 2 paths possible)
def getPathsAtoB(fx,fy,tx,ty,layout):
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
        s1 = getPathsAtoB(fx,fy,fx,ty, layout)
        s2 = getPathsAtoB(fx,ty,tx,ty, layout)
        if len(s1) and len(s2): seqA = [s1[0][0:-1]+s2[0]]
        else: seqA = []
        s1 = getPathsAtoB(fx,fy,tx,fy, layout)
        s2 = getPathsAtoB(tx,fy,tx,ty, layout)
        if len(s1) and len(s2): seqB = [s1[0][0:-1]+s2[0]]
        else: seqB = []
        assert len(seqA) or len(seqB)
        if not len(seqA): return seqB
        if not len(seqB): return seqA
        # print(f"     SeqA: {seqA[0]}    SeqB: {seqB[0]}")
        #if len(seqA) < len(seqB) : return seqA
        #return seqB
        return [seqA[0], seqB[0] ]




def getSimpleMap(layout):
    Simplemap = {}
    for fy,fl in enumerate(layout):
        for fx,fc in enumerate(fl):
            if fc  == 'X': continue
            for ty,tl in enumerate(layout):
                for tx,tc in enumerate(tl):
                    if tc=='X' : continue
                    k = fc + tc
                    Simplemap[k] = getPathsAtoB(fx,fy,tx,ty,layout)
    for k in Simplemap: print(f"Simplemap {k} -> {Simplemap[k]}")
    return Simplemap

# Map string str to a list of maps
def getListOfMaps(str, smallMap):
    r = ['']
    for i in range(len(str)-1):
        opts = smallMap[str[i:i+2]]
        newr = []
        for o in opts:
            for rs in r:
                newr.append(rs + o)
        r = newr
    return r
    

def getMap( Simplemap, smallMap):
    map = {}
    for kp in Simplemap:
        firstOptionsL = Simplemap[kp]
        if len(firstOptionsL)==1: # only one option
            map[kp] = firstOptionsL
            continue
        so = [] # list of pairs: (kp, currentMap)
        for fo in firstOptionsL:
            # map fo to new string and get length
            str = 'A' + fo
            soL = getListOfMaps(str, smallMap)
            for soLi in soL: so.append((fo, soLi))
        for fo,soLi in so:
            print(f"getMap: {kp}  option {fo} => {soLi}")

        newSo = []
        for fo,soLi in so:
            str = 'A' + soLi
            toL = getListOfMaps(str, smallMap)
            for toLi in toL: newSo.append((fo, toLi))
        
        shortest=BIGNUM
        for fo,toLi in newSo:
            print(f"getMap: {kp}  2nd option {fo} => {toLi}")
            if len(toLi) < shortest:
                shortest = len(toLi)
                map[kp] = [fo]
        print(f"getMap: {kp} CHOSE {map[kp]}")
    for kp in map:
        print(f"{kp} => {map[kp]}")
    return map


# map the string (contining no As) to list of shortest sequence of new commands
@functools.cache
def getSubSeq(str:string):
    # print(f"getShortest of {str}")
    # get all combinations
    res = []
    for i in range(len(str)-1):
        r = keyPairMap[str[i:i+2]][0]
        res.append(r)
        # print(f"\t\tgetSubSeq {str[i:i+2]} => {r}")
    return ''.join(res)

  

# find the shortest sequence of new commands that does 'str'(string)
# returns list of new sequences
#@functools.cache
def getNewSeq(listOfSeqs:list):
    r = []
    for str in listOfSeqs:
        subs = str.split('A')
        for s in subs[0:-1]:
            seq = getSubSeq('A' + s + 'A')
            # print(f"     getNewSeq substr {s+'A'} => {seq}")
            r.append(seq)
    return r

@functools.cache
def getSeqLen(seq, numMaps):
    str = [seq]
    for loop in range(numMaps):
        newStr = getNewSeq(str)
        str = newStr
    l = sum([len(s) for s in str])
    print(f"Orig str of len {len(seq)} maps to final string of length {l}.")
    return l

def getStage2(l1, numMaps):
    print(f"Getting stage2 of list of {len(l1)} subseqs. Applying {numMaps}.")
    #print(f"{l1[0:6]}")
    tot_len = 0
    for seq in l1:
        tot_len += getSeqLen(seq, numMaps)
    return tot_len
  
def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]


def process(l, numericPad, keyPad1, numK=2):

    seq1 = numericPad.getFirstListOfSeqs(l)  # 1st map
    print(f"f1 is {seq1}")
    l1 = getNewSeq([seq1])                   # 2nd map
    lastTime = round(time.time())

    reps = numK-1
    if reps >15: reps=15

    for rep in range(reps):                  # 3rd - 17th
        l1_len = sum([len(sub) for sub in l1])
        if l1_len < 80: print(f"K{rep+1}: l1={l1}  (len={l1_len})")
        #else: 
        print(f"K{rep+1}: l1 len is {l1_len}     {round(time.time() - lastTime)}s")
        lastTime = round(time.time())
        l2 = getNewSeq(l1)
        numAs = sum([s.count('A') for s in l2])
        if numAs != l1_len :
            print(f"ERROR: saw {numAs} 'A's in result string but source string has len {l1_len}")
            sys.exit(1)
        l1 = l2

    sm = sum([len(sub) for sub in l1])

    if (numK > 16): 
        sm = getStage2(l1, numK-17)

    print(f"Result: l1 has len {sm} ")
    num = int(l[0:-1])
    prod = num * sm
    print(f"So value is {num} * {sm} = {prod}")
    return prod


def doPart1(db):
    global keyPairMap
    comp = 0
    numericPad = Pad([ ['7','8','9'],['4','5','6'],['1','2','3'],['X','0','A']], 'Numeric')
    keyPad1 = Pad([['X','^','A'],['<','v','>']],'Keypad1')
    for l in db:
        comp = comp + process(l, numericPad, keyPad1,2)
    return comp



def doPart2(db):
    global keyPairMap
    comp = 0
    numericPad = Pad([ ['7','8','9'],['4','5','6'],['1','2','3'],['X','0','A']], 'Numeric')
    keyPad1 = Pad([['X','^','A'],['<','v','>']],'Keypad1')
    for l in db:
        comp = comp + process(l, numericPad, keyPad1, 26)
    return comp


    
#---------------------------------------------------------------------------------------
# Load input
db = load_db()
s = getSimpleMap([['X','^','A'],['<','v','>']])
keyPairMap = getMap(s, s)
#sys.setrecursionlimit(10000)
#p1 = doPart1(db)
#print(f"Part 1 is {p1}\n\n")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
