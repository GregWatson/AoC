#import argparse
import sys
import re
import functools
import array
import copy
import hashlib
import string
import itertools

input_file_name = 'input.txt'
print_on = False

# grid=array.array('l',[1 for i in range(NUMX*NUMY)])

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def parsedb(db):
    a=[]
    b=[]
    for l in db:
        m = re.match(r'(\d+)\s+(\d+)',l)
        if m:
            a.append(int(m.group(1)))
            b.append(int(m.group(2)))
    return a,b

def doPart1(a,b):
    a.sort()
    b.sort()
    z = zip(a,b)
    diff = 0
    for (a1,b1) in z:
        diff = diff + abs(a1-b1)
    return diff

def doPart2():
    c={}
    for n in b:
        if n in c: c[n] = c[n]+1
        else: c[n] = 1
    s= 0
    for n in a:
        if n in c:
            s = s + n * c[n]
    return s
        



#---------------------------------------------------------------------------------------
# Load input
db = load_db()
(a,b) = parsedb(db)

p1 = doPart1(a,b)
print(f"Part 1 is {p1}")

p2 = doPart2(a,b)
print(f"Part 2 is {p2}.")



