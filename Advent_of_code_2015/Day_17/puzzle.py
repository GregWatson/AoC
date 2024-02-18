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

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def load_info(db):
    odds= []
    evens= []
    for l in db:
        m = re.match(r'(\d+)',l)
        if m:
            n = int(m.group(1))
            if n % 2 == 0: evens.append(n)
            else: odds.append(n)
    return odds,evens

def powerset(s):
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))

def do_part1(db):
    tot = 0
    odds,evens = load_info(db)
    print(f"Odds is {odds}  evens is {evens}")
    #print(f"Odds sum is {sum(odds)}  evens sum is {sum(evens)}")
    
    # Sum of all odds is 150, so only 1 combo that uses just odds.
    # So go through all evens combos and see if we can get to 150 with pairs of odds.

    # get all odd combos (sum must be even number)
    o = list(powerset(odds))
    o2 = []
    for l in o:
        if len(l) and (len(l) % 2) == 0: 
            o2.append(l)
            # print(f"{l}")
    print(f"Saw {len(o2)} even length odd combos")
    o_counts  = {}
    for l in o2:
        s = sum(l)
        if s:
            if s in o_counts: o_counts[s] += 1
            else: o_counts[s] = 1
    
    keys = o_counts.keys()
    sorted(keys)
    for n in keys: print(f"{n} -> {o_counts[n]}")

    e = list(powerset(evens))
    for l in e:
        s = sum(l)
        need = 150 - s
        if need and (need in o_counts): 
            tot += o_counts[need]
        else:
            if s == 150: tot += 1

    return tot



def do_part2(db):
    tot = 0
    odds,evens = load_info(db)
    print(f"Odds is {odds}  evens is {evens}")
    #print(f"Odds sum is {sum(odds)}  evens sum is {sum(evens)}")
    
    # Sum of all odds is 150, so only 1 combo that uses just odds.
    # So go through all evens combos and see if we can get to 150 with pairs of odds.

    # get all odd combos (sum must be even number)
    o = list(powerset(odds))
    o2 = []
    for l in o:
        if len(l) and (len(l) % 2) == 0: 
            o2.append(l)
            # print(f"{l}")
    print(f"Saw {len(o2)} even length odd combos")
    o_counts  = {}
    o_count_min = {}
    for l in o2:
        s = sum(l)
        if s:
            ll = len(l)
            if s in o_counts: 
                o_counts[s] += 1
                if o_count_min[s] > ll: o_count_min[s] = ll
            else: 
                o_counts[s] = 1
                o_count_min[s] = ll
    
    keys = o_counts.keys()
    sorted(keys)
    for n in keys: print(f"{n} -> {o_counts[n]}   min={o_count_min[n]}")

    min_len = 1000
    min_count = 0
    e = list(powerset(evens))
    for l in e:
        s = sum(l)
        ll = len(l)
        need = 150 - s
        if need and (need in o_counts): 
            tot += o_counts[need]
            tot_len = ll + o_count_min[need]
            if tot_len == min_len: min_count += 1
            elif tot_len < min_len:
                min_len = tot_len
                min_count = 1
        else:
            if s == 150: 
                tot += 1
            if ll == min_len: 
                min_count += 1
            elif ll < min_len:
                min_len = ll
                min_count = 1
    tot = min_count
    print(f"Min len is {min_len} and min_count is {min_count}")
    return tot

    

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
print(f"Loaded {len(db)} lines from input")

p1 = do_part1(db)
print(f"Part 1 is {p1}")

p2 = do_part2(db)
print(f"Total for part 1 is {p1}.    Total for part 2 is {p2}.")

