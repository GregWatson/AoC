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

def isSafe(nums):
    dir = 1
    if nums[0] == nums[1]: return 0
    if nums[0] > nums[1]: dir = -1
    i = 0
    while i < (len(nums)-1):
        a=nums[i]
        b=nums[i+1]
        if (((a > b) and (dir==-1)) or ((a<b) and (dir==1))) and (abs(a-b) <= 3) : 
            i = i + 1
            continue
        return 0
    return 1


def doPart1(db):
    s = 0
    for l in db:
        snums = l.split(' ')
        nums = list(map(int, snums))
        s = s + isSafe(nums)
    return s
   

def doPart2(db):
    s = 0
    for l in db: 
        snums = l.split(' ')
        nums = list(map(int, snums))
        if isSafe(nums): 
            s = s + 1
            continue
        i= 0
        while i < len(nums):
            newl = nums[:]
            newl.pop(i)
            if isSafe(newl):
                s = s + 1
                i = len(nums)+1
            i=i+1
    return s

        



#---------------------------------------------------------------------------------------
# Load input
db = load_db()

p1 = doPart1(db)
print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"Part 2 is {p2}.")



