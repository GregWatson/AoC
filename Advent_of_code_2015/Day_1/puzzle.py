#import argparse
import sys
import re
import functools
import array
import copy

input_file_name = 'input.txt'
print_on = True

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]


def do_part1(db):
    d = 0
    for c in db[0]:
        if c == '(': d += 1
        elif c == ')': d -= 1
    return d

def do_part2(db):
    d = 0
    i = 0
    for c in db[0]:
        i += 1
        if c == '(': d += 1
        elif c == ')': d -= 1
        if d == -1: return i
    return 0

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
x_max = len(db[0])
y_max = len(db)

p1 = do_part1(db)
print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Total for part 1 is {p1}.    Total for part 2 is {p2}.")

