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
NUMONES = {'0':0, '1':1, '2':1, '3':2, '4':1, '5':2, '6':2, '7':3, '8':1, '9':2, 'a':2, 'b':3, 'c':2, 'd':3, 'e':3, 'f':4}
USEDBLOCKS = {'0':'....', '1':'...#', '2':'..#.', '3':'..##', '4':'.#..', '5':'.#.#', '6':'.##.', 
              '7':'.###', '8':'#...', '9':'#..#', 'a':'#.#.', 'b':'#.##', 'c':'##..', 'd':'##.#', 'e':'###.', 'f':'####'}
MAX=141; MINSAVED=100; NUMCHEATS=20
LIST = [97,167,54,178,2,11,209,174,119,248,254,0,255,1,64,190]
LISTSTRING = '97,167,54,178,2,11,209,174,119,248,254,0,255,1,64,190'

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

# given string, compute knot hash of the string
def computeHash(s):
    l = [ i for i in range(256) ]
    pos = 0
    skip = 0
    lens = [ord(c) for c in s] + [17, 31, 73, 47, 23]
    for i in range(64):
        for length in lens:
            #print(f"length = {length} pos = {pos} skip = {skip}")
            #print(f"l = {l}")
            l = l[pos:] + l[:pos]
            l = l[:length][::-1] + l[length:]
            l = l[-pos:] + l[:-pos]
            pos += length + skip
            pos %= len(l)
            skip += 1
    #print(f"l = {l}")
    dense = []
    for i in range(16):
        block = l[i*16:(i+1)*16]
        xor = 0
        for b in block:
            xor ^= b
        dense.append(xor)
    #print(f"dense = {dense}")
    hexstring = ''.join([f"{x:02x}" for x in dense])
    #print(f"hexstring = {hexstring}")
    return hexstring  

def getNumOnes(s):
    count = 0
    for c in s:
        count += NUMONES[c]
    return count

def getCol(hash):
    s = ''
    for c in hash: s += USEDBLOCKS[c]
    return list(s)

def updateDisk(x,y,disk):
    # moving only up, down, left or right, delete used sectors.
    disk[y][x] = '.'
    for xx,yy in ( (x,y+1), (x,y-1), (x-1,y), (x+1,y)):
        if xx>=0 and xx <128 and yy>=0 and yy < 128:
            if disk[yy][xx]=='#': updateDisk(xx,yy,disk)


def doPart1():
    count = 0
    for row in range(128):
        s = 'nbysizxe-'+str(row)
        hash = computeHash(s)
        numOnes = getNumOnes(hash)
        count += numOnes
        print(f"{row} : {s} -> {hash}   {numOnes}  {count}")
    return count

def doPart2():
    count = 0
    disk = []
    for row in range(128):
        s = 'nbysizxe-'+str(row)
        hash = computeHash(s)
        r = getCol(hash)
        disk.append(r)
    done = False
    for y in range(128):
        for x in range(128):
            if disk[y][x] == '#':
                updateDisk(x,y,disk)
                count += 1

    return count



#---------------------------------------------------------------------------------------
# Load input
#db = load_db()

#sys.setrecursionlimit(10000)
p1 = doPart1()
print(f"Part 1 is {p1}\n\n")

#ls = ''
p2 = doPart2()
print(f"\n\n\n\nPart 2 is {p2}")
