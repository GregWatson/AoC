#import argparse
import sys
import re
import functools
import array
import copy
import json
import itertools

input_file_name = 'input.txt'
print_on = False
ings = ['Sugar','Sprinkles', 'Candy', 'Chocolate']

sue = { 'children': 3,
        'cats': 7,
        'samoyeds': 2,
        'pomeranians': 3,
        'akitas': 0,
        'vizslas': 0,
        'goldfish': 5,
        'trees': 3,
        'cars': 2,
        'perfumes': 1 }

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def load_info(db):
    sues = [{} for i in range(501)]
    props = [1,2,3]
    counts = [0,0,0]
    for l in db:
        m = re.match(r'Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+).*',l)
        if m:
            sue_id,  props[0], counts[0],props[1], counts[1],props[2], counts[2] \
            = (int(m.group(1)), m.group(2),int(m.group(3)),m.group(4),int(m.group(5)),m.group(6),int(m.group(7)))
            for i,p in enumerate(props):
                print(f"i,p,count are {i,p,counts[i]}")
                sues[sue_id][p] = counts[i]
        else:
            print(f"FAILED MATCH {l}")
    return sues

def do_part1(db):
    tot = 0
    sues = load_info(db)
    for sue_id in range(len(sues)):
        props = sues[sue_id]
        ok = 0
        for p in props:
            if p in ['cats','trees']:
                if sue[p] < props[p]: ok += 1
            elif p in ['pomeranians', 'goldfish']:
                if sue[p] > props[p]: ok += 1
            elif props[p] == sue[p]: ok += 1
        if ok == 3:
            tot = sue_id
            print(f"Matched on {sue_id}")
    return tot


def do_part2(db):
    tot = 0
 
    return tot

    

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
print(f"Loaded {len(db)} lines from input")

p1 = do_part1(db)
print(f"Part 1 is {p1}")

#p2 = do_part2(db)
#print(f"Total for part 1 is {p1}.    Total for part 2 is {p2}.")

