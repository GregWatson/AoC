#import argparse
import sys
import re
import functools
import array
import copy
import hashlib
import string

input_file_name = 'input.txt'
print_on = False

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def do_part1(db):
    s = set(string.ascii_lowercase)
    d = {}
    for c in s: d[c] = 0
    counts = [ copy.copy(d) for i in range(8)]

    for l in db:
        for i,c in enumerate(l):
            counts[i][c] += 1

    os = ''
    for i in range(8):
        max_seen = 0
        for c in s:
            if counts[i][c] > max_seen:
                cc = c
                max_seen = counts[i][c]
        os += cc
        print(f"max was {max_seen}  char was {cc}")
    return os



def do_part2(db):
    s = set(string.ascii_lowercase)
    d = {}
    for c in s: d[c] = 0
    counts = [ copy.copy(d) for i in range(8)]

    for l in db:
        for i,c in enumerate(l):
            counts[i][c] += 1

    os = ''
    for i in range(8):
        min_seen = 1000
        for c in s:
            if counts[i][c] < min_seen:
                cc = c
                min_seen = counts[i][c]
        os += cc
        print(f"max was {min_seen}  char was {cc}")
    return os

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

p1 = do_part1(db)
print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Total for part 1 is {p1}.    Total for part 2 is {p2}.")



