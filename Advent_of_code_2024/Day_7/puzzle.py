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
MAX=130

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def tryThis(ans, soFar, L):
    if soFar > ans: return False
    add = soFar+L[0]
    mul = soFar*L[0]
    # print(f"{ans}: {soFar}   +={add}  *={mul}   rest:{L[1:]}")
    if len(L) == 1:
        return (add == ans) or (mul == ans)
    else:
        if tryThis(ans, add, L[1:]) : return True
        else: return tryThis(ans, mul, L[1:])

def hasSolution(l):
    m = re.match(r'(\d+): (.*)',l)
    if m:
        ans=int(m.group(1))
        nums=list(map(int, m.group(2).split()))
        #print(f"{ans} from {nums}")
    else:
        print("Unknown format")
        sys.exit(1)
    biggest = functools.reduce(lambda x, y: x * y, nums)
    #if biggest < ans: return 0
    if biggest == ans: 
        print(f"MULTIPLY: {l}")
        return ans
    if tryThis(ans, nums[0], nums[1:]) : return ans
    else: return 0


def tryThis2(ans, soFar, L):
    if soFar > ans: return False
    cat = int(f"{soFar}{L[0]}")
    # print(f"{soFar}{L[0]} -> {cat}")
    add = soFar+L[0]
    mul = soFar*L[0]
    # print(f"{ans}: {soFar}   +={add}  *={mul}   rest:{L[1:]}")
    if len(L) == 1:
        return (add == ans) or (mul == ans) or (cat == ans)
    else:
        if tryThis2(ans, add, L[1:]) : return True
        elif tryThis2(ans, mul, L[1:]) : return True
        else: return tryThis2(ans, cat, L[1:])

def hasSolution2(l):
    m = re.match(r'(\d+): (.*)',l)
    if m:
        ans=int(m.group(1))
        nums=list(map(int, m.group(2).split()))
        #print(f"{ans} from {nums}")
    else:
        print("Unknown format")
        sys.exit(1)
    if tryThis2(ans, nums[0], nums[1:]) : return ans
    else: return 0


def doPart1(db):
    s = 0
    for l in db:
        ans = hasSolution(l)
        if ans: print(f"{l}")
        s = s + ans
        # sys.exit(1)
    return s
   

# Only try obstructions at locations that have been visited
def doPart2(db):
    s = 0
    for l in db:
        ans = hasSolution2(l)
        if ans: print(f"{l}")
        s = s + ans
        # sys.exit(1)
    return s

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#p1 = doPart1(db)
#print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"Part 2 is {p2}")



