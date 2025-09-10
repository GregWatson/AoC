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
import string

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
    return [ l for l in lines ]

def follow(db, y, x):
    print(f"{db}")
    if db[0][x] != '|':
        print("Error, not starting on |")
        return None
    print(f"Starting at {x},{y}")
    direction = 'D'
    letters = []
    steps = 0
    while True:
        steps += 1
        if direction == 'D':
            y += 1
        elif direction == 'U':
            y -= 1
        elif direction == 'L':
            x -= 1
        elif direction == 'R':
            x += 1
        else:
            print("Error, bad direction")
            return None
        if y < 0 or y >= len(db) or x < 0 or x >= len(db[y]):
            print("Error, out of bounds")
            return None
        c = db[y][x]
        if c == ' ':
            break
        elif c in string.ascii_uppercase:
            letters.append(c)
        elif c == '+':
            if direction in ('D','U'):
                if x > 0 and db[y][x-1] in ('-','+') + tuple(string.ascii_uppercase):
                    direction = 'L'
                elif x < len(db[y])-1 and db[y][x+1] in ('-','+') + tuple(string.ascii_uppercase):
                    direction = 'R'
                else:
                    print("Error, no left or right at +")
                    return None
            else:
                if y > 0 and db[y-1][x] in ('|','+') + tuple(string.ascii_uppercase):
                    direction = 'U'
                elif y < len(db)-1 and db[y+1][x] in ('|','+') + tuple(string.ascii_uppercase):
                    direction = 'D'
                else:
                    print("Error, no up or down at +")
                    return None
        elif c in ('|','-'):
            pass
        else:
            print(f"Error, unexpected char {c}")
            return None
    return ''.join(letters), steps

def doPart1(db,y,x):
    path, numsteps = follow(db, y, x)
    print(f"Num steps = {numsteps}")
    return path

    
def doPart2(db):
    return 0

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#sys.setrecursionlimit(10000)
p1 = doPart1(db, 0, db[0].index('|'))
print(f"Part 1 is {p1}\n\n")

p2 = doPart2(db)
print(f"\n\n\n\nPart 2 is {p2}")
