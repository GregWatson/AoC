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
LIST = [97,167,54,178,2,11,209,174,119,248,254,0,255,1,64,190]
LISTSTRING = '97,167,54,178,2,11,209,174,119,248,254,0,255,1,64,190'

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]


def doPart1(LIST):
    l = [ i for i in range(256) ]
    pos = 0
    skip = 0
    for length in LIST:
        #print(f"length = {length} pos = {pos} skip = {skip}")
        #print(f"l = {l}")
        l = l[pos:] + l[:pos]
        l = l[:length][::-1] + l[length:]
        l = l[-pos:] + l[:-pos]
        pos += length + skip
        pos %= len(l)
        skip += 1
    return l[0] * l[1]   


def doPart2(lstring):
    l = [ i for i in range(256) ]
    pos = 0
    skip = 0
    lens = [ord(c) for c in lstring] + [17, 31, 73, 47, 23]
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
    print(f"l = {l}")
    dense = []
    for i in range(16):
        block = l[i*16:(i+1)*16]
        xor = 0
        for b in block:
            xor ^= b
        dense.append(xor)
    print(f"dense = {dense}")
    hexstring = ''.join([f"{x:02x}" for x in dense])
    print(f"hexstring = {hexstring}")
    return hexstring




#---------------------------------------------------------------------------------------
# Load input
#db = load_db()

#sys.setrecursionlimit(10000)
p1 = doPart1(LIST)
print(f"Part 1 is {p1}\n\n")

ls = LISTSTRING
#ls = ''
p2 = doPart2(ls)
print(f"\n\n\n\nPart 2 is {p2}")
