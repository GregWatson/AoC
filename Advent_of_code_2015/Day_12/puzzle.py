#import argparse
import sys
import re
import functools
import array
import copy
import json

input_file_name = 'input.txt'
print_on = False


def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]



def do_part1(db):
    tot = 0
    for l in db:
        m = re.findall('(-?[1-9][0-9]*)', l)
        if m:
            for n in m:
                print(f"{n}, ",end='')
                tot += int(n)
    print("")
    return tot

def process_dict(d):
    for k in d:
        if d[k] == 'red': return [0]
    newd = {}
    for k in d:
        t = type(d[k])
        if t is list:
            newd[k] = process_list(d[k])
        elif t is dict:
            newd[k] = process_dict(d[k])
        else:
            newd[k] = d[k]
    return newd

def process_list(l):
    newl = []
    for i in l:
        t = type(i)
        if t is list:
            newl.append(process_list(i))
        elif t is dict:
            newl.append(process_dict(i))
        else:
            newl.append(i)
    return newl

def print_json(data):
    for k in data:
        print(f"{k} ==> {data[k]}")

def do_part2(db):
    tot = 0
    with open(input_file_name, 'r') as f:
        data = json.load(f)
    print_json(data)

    d = process_dict(data)

    s = str(d)
    print(f"\n\nNew string is {s}")

    tot = do_part1([s])
    return tot

    

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
print(f"Loaded {len(db)} lines from input")

p1 = 0
#p1 = do_part1(db)
#print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Total for part 1 is {p1}.    Total for part 2 is {p2}.")

