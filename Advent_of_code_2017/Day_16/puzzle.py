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


def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def dance(p, moves):
    pos = p[:]
    for move in moves:
        if move[0] == 's':
            num = int(move[1:])
            pos = pos[-num:] + pos[:-num]
        elif move[0] == 'x':
            a, b = map(int, move[1:].split('/'))
            pos[a], pos[b] = pos[b], pos[a]
        elif move[0] == 'p':
            a, b = map(pos.index, move[1:].split('/'))
            pos[a], pos[b] = pos[b], pos[a] 
    return pos

def doPart1(db):
    count = 0
    moves = db[0].split(',')
    pos = list('abcdefghijklmnop')
    pos = dance(pos, moves)
    return ''.join(pos)

def doPart2(db):
    count = 0
    moves = db[0].split(',')
    pos = list('abcdefghijklmnop')
    for loop in range(1000000000 % 36):
        pos = dance(pos, moves)
        count += 1
        print(f"{count} pos: {pos}")
    print(f"After {count} iterations pos= {pos}")

    return ''.join(pos)

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#sys.setrecursionlimit(10000)
p1 = doPart1(db)
print(f"Part 1 is {p1}\n\n")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
