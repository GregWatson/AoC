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

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]


def doPart1(db):
    max= 0
    for l in db:
        (lo,hi) = map(int, l.split("-"))
        print(f"{lo} -> {hi}")
        if lo>(max+1): return max+1
        if hi>max: max=hi
    return 0


def doPart2(db):
    num = 0
    max = 0
    for l in db:
        (lo,hi) = map(int, l.split("-"))
        print(f"{lo} -> {hi}")
        if lo>(max+1): num = num + (lo - max) - 1
        if hi>max: max=hi
    return num
        



#---------------------------------------------------------------------------------------
# Load input
db = load_db()

p1 = doPart1(db)
print(f"Part 1 is {p1}")

p2 = doPart2(db)
print(f"Part 2 is {p2}.")



