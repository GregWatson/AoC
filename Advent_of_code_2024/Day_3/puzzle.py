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

def doPart1(db):
    s = 0
    for l in db:
        m = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)',l)
        if m:
            for a,b in m:
                s = s+ int(a) * int(b)
    return s
   

def doPart2(db):
    s = 0
    l = ''.join(db)
    code = re.split(r'do\(\)', l)
    for c in code:
        do_code = re.split(r'don\'t\(\)',c)[0]
        #print(f"{do_code}")
        m = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)',do_code)
        if m:
            for a,b in m:
                s = s + int(a) * int(b)
    return s

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

p1 = doPart1(db)
print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"Part 2 is {p2}.")



